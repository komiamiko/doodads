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
