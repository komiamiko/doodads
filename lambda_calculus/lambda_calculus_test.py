"""
Unit tests for the lambda calculus library.
"""

import unittest

class TestInternalState(unittest.TestCase):
    """
    Test cases focused on the internals of the library.
    Does basic logic and consistency checks.
    When implementations change, some of these tests may
    no longer pass. It is not necessarily an error.
    Take note of which test failed, and look at what
    change caused the test to fail. Sometimes these
    changes are completely intentional! And sometimes
    there is actually a bug.
    When the internal workings change intentionally,
    adjust the test cases accordingly.
    """
    def test_bind_ops(self):
        """
        Test the lambda_bind class.
        Adds some entries, removes some entries,
        checks equality and hash.
        """
        from lambda_calculus import lambda_bind

        # start with just one bindings object

        A = lambda_bind()

        # check self equality
        
        self.assertTrue(A == A)
        self.assertTrue(hash(A) == hash(A))

        # introduce another bindings object
        
        B = lambda_bind()

        # see that they are equal

        self.assertTrue(A == B)
        self.assertTrue(hash(A) == hash(B))

        # now we start modifying them
        # we will use str -> str mappings, which are
        # allowed in the current implementation

        A.append('xyz', 'abc')

        # A: [xyz := abc]
        # B: []

        # see that they are not equal anymore

        self.assertTrue(A != B)
        self.assertTrue(hash(A) != hash(B))

        # remove the most recent addition to A,
        # and ensure that it is the correct value

        self.assertTrue(A.pop() == 'abc')

        # A: []
        # B: []

        # they should be equal again now

        self.assertTrue(A == B)
        self.assertTrue(hash(A) == hash(B))

        # add some more things...

        A.append('ab', 'cd')
        A.append(None, 'xyz')
        B.append(None, 'xyz')
        B.append('ab', 'cd')

        # A: [ab := cd, xyz]
        # B: [xyz, ab := cd]
        # note that the order is important so these are different

        self.assertTrue(A != B)
        self.assertTrue(hash(A) != hash(B))

        # play with different ops

        # A: a
        # B: b

        B += A

        # A: a
        # B: ba

        self.assertTrue(A != B)
        self.assertTrue(hash(A) != hash(B))

        C = lambda_bind(A.flatten())

        # A: a
        # B: ba
        # C: a

        self.assertTrue(A == C)

        A.keep_first(1)

        # A: a'
        # B: ba
        # C: a

        self.assertTrue(A != C)

        A.keep_first(0)

        # A: []
        # B: ba
        # C: a

        self.assertTrue(A != C)
        self.assertTrue(A == lambda_bind())

        A = lambda_bind(B.flatten()[0:2])

        # A: b
        # B: ba
        # C: a

        self.assertTrue(A != B)
        self.assertTrue(A != C)
        self.assertTrue(B == A + C)

        A += C

        # A: ba
        # B: ba
        # C: a

        self.assertTrue(A == B)

    def test_expr_ops_no_func(self):
        """
        Tests operations on lambda expressions
        WITHOUT involving the lambda_func class.
        Tests include:
        - sanity checks
            ex. x = x
            ex. x x x =/= x (x x)
        - see that call with substitution
          is actually lazy
            ex. (x x)[x := y] =/= y y
        - see that substitution is correct
            ex. (x x)[x := y y] = y y (y y)
        """
        from lambda_calculus import lambda_var, lambda_bind
        
        # variables are distinguished by name

        # check self equality

        x = lambda_var('x')
        x_ = lambda_var('x')

        self.assertTrue(x == x)
        self.assertTrue(hash(x) == hash(x))
        self.assertTrue(x == x_)
        self.assertTrue(hash(x) == hash(x_))

        # check non-equality

        y = lambda_var('y')

        self.assertTrue(x != y)

        # check distinctness

        self.assertTrue(len(set(map(lambda_var, ['x', 'y', 'z']))) == 3)
        self.assertTrue(len(set(map(lambda_var, [1, 2, 3]))) == 3)
        self.assertTrue(len(set(map(lambda_var, ['x', 'y', 'z', 1, 2, 3]))) == 6)
        
        # okay so the equality is probably working just fine
        # let's build some expressions
        # we will name them using A for apply ex. AxAxx means x (x x)

        Axx = x.call(x)

        self.assertTrue(x != Axx)
        self.assertTrue(x.call(x) == Axx)

        Axy = x.call(y)

        self.assertTrue(x.call(y) == Axy)
        
        Ayx = y.call(x)
        Ayy = y.call(y)

        self.assertTrue(len({Axx,Axy,Ayx,Ayy}) == 4)

        AAxxx = Axx.call(x)
        AxAxx = x.call(Axx)

        self.assertTrue(AAxxx != AxAxx)

        # the expression building is probably fine by now
        # before we move on we will also check
        # immediate evaluation with an empty substitution

        for expr in (x, y, Axx, Axy, AAxxx, AxAxx):
            self.assertTrue(expr == expr.evaluate_now())

        # now we can test lazy substitution
        # we will write Lx for an expression which ultimately
        # evaluates to x but is using a lazy wrapper

        x_to_y = lambda_bind([('x', y)])
        
        Lyy = x.call(x, binds=x_to_y)

        self.assertTrue(len({Axx, Axy, Ayy, Lyy}) == 4)

        # and verify that the substitution is correct when evaluated

        self.assertTrue(Ayy == Lyy.evaluate_now())
        self.assertTrue(Ayy == Axx.evaluate_now(binds=x_to_y))

    def test_func_ops(self):
        """
        Test some basic functions and the ability to call functions.
        Will not use bindings directly.
        """
        import itertools
        from lambda_calculus import lambda_var, lambda_func

        # make the identity function

        I = lambda_func(None, lambda_var(1))

        # test that it works as expected

        for var_name in 'xyz':
            v = lambda_var(var_name)
            AIv = I.call(v)

            # lazy evaluation causes Iv to not
            # reduce to v yet
            # thus it should report not equal

            self.assertTrue(v != AIv)

            # but then when we force evaluation...

            self.assertTrue(v == AIv.evaluate_now())

        # make another identity function

        In = lambda_func('x', lambda_var('x'))

        # they aren't intensionally equal yet...

        self.assertTrue(I != In)

        # but actually it's just a
        # named indexed form of the other

        self.assertTrue(I == In.to_indexed())

        # test that .to_named() looks deterministic

        self.assertTrue(I.to_named() == I.to_named())

        # okay, let's try something else
        # let's make the K combinator,
        # defined by
        # Kxy = x

        K = lambda_func(None, lambda_func(None, lambda_var(2)))

        # try some examples with it

        for x, y in itertools.product(*[[
            lambda_var('w'),
            lambda_var('x'),
            lambda_var('y'),
            lambda_var('z'),
            I
            ]]*2):
            
            AAKxy = K.call(x).call(y)

            # again, lazy evaluation prevents
            # it from reducing to x early

            self.assertTrue(x != AAKxy)

            # but if we evaluate it, it should work just fine

            self.assertTrue(x == AAKxy.evaluate_now())

        # also check the named form

        Kn = lambda_func('x', lambda_func('y', lambda_var('x')))

        self.assertTrue(K != Kn)
        self.assertTrue(K == Kn.to_indexed())

    def test_string_ops(self):
        """
        Check that str and repr work as intended.
        str is meant to be LaTeX comaptible, but we can't check
        this cheaply. It is also meant to be able to reconstruct
        the objects through parse_lambda, though parsing
        will happen in a separate test.
        repr should be able to reconstruct the objects exactly.
        """
        from lambda_calculus import lambda_var, lambda_func

        # construct the namespace for repr tests

        import lambda_calculus
        namespace = {name:getattr(lambda_calculus, name) for name in dir(lambda_calculus)}

        # start with an easy test
        
        x = lambda_var('x')

        # does it str nicely?
        str(x)

        # reconstruction test
        self.assertTrue(eval(repr(x),namespace) == x)

        # use Kxx as an example
        # this should involve every one of the other types
        # thus, it's somewhat of a harder test
        # Kxy = x

        K = lambda_func(None, lambda_func(None, lambda_var(2)))

        AAKxx = K.call(x).call(x)

        # don't throw errors please
        str(AAKxx)

        # test reconstruction
        self.assertTrue(eval(repr(AAKxx),namespace) == AAKxx)

class TestLambdaCompute(unittest.TestCase):
    """
    Test cases focused on performing computations with
    the lambda calculus. Somewhat low level, so
    like TestInternalState, a test case fail does not
    necessarily indicate the program has an error,
    but it is something to take note of.
    """
    pass

class TestUserAPI(unittest.TestCase):
    """
    Highest level tests focused on the user API.
    Run something that a typical user might try,
    see if it does what we expect.
    A fail here is definitely an error,
    since these tests are based only on the
    public API.
    """
    pass

if __name__ == '__main__':
    unittest.main()
