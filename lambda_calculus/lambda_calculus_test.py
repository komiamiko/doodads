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

    def test_parse_str(self):
        """
        Tests the parser against some test vectors,
        and tests the parser's ability to reconstruct
        objects that have been str'd.
        """
        import functools
        from lambda_calculus import lambda_var, lambda_call, lambda_func, parse_lambda

        # make the test vectors list as (object, [str ...])
        # all test vectors here are currently supported by the parser

        test_vectors = [
            # parse a single variable
            (lambda_var('x'), ['x']),
            # handle extra whitespace
            (lambda_var('A'), ['A', '  A', 'A  ', '  A  ']),
            # parse number variables
            (lambda_var(1), ['1']),
            # parse multiple digit number variables
            (lambda_var(1234), ['1234']),
            # parse a basic call
            (lambda_call(lambda_var('x'), lambda_var('x')), ['x x', 'xx']),
            # test variables styled like latex commands
            (lambda_var('\\epsilon'), ['\\epsilon']),
            # parse a command that looks like lambda
            (lambda_var('\\lambdaa'), ['\\lambdaa']),
            # parse a name variable that actually contains the word lambda
            (functools.reduce(lambda_call,map(lambda_var,'lambdaa')), [
                'lambdaa',
                'lambd aa'
                ]),
            # parse larger call trees
            (functools.reduce(lambda_call,map(lambda_var,'xxxyyy')), [
                'x  x x  y y y',
                'xxx  yyy',
                'x x xy y y',
                # can it handle brackets well?
                '(xxx)yyy',
                '((xx)xy)yy',
                '( ( ( x ) x x ) y y ) y',
                '(((x)))(x)x(y)y((y))',
                '{[(x)]}xx[y]{y}(y)'
                ]),
            # test a simple lambda function
            (lambda_func(None,lambda_var(1)), [
                'λ.1',
                '\\lambda.1',
                'lambda.1',
                '\\lambda . 1',
                'lambda .1',
                'lambda.((1))'
                ]),
            # test nested lambda definitions
            (lambda_func(None,lambda_func(None,lambda_var(2))), [
                'λ.λ.2',
                'λ .λ .2',
                '\\lambda .lambda. 2',
                '\\lambda.(lambda.2)'
                ]),
            # test parse order with lambda function
            (lambda_call(lambda_var(1),lambda_func(None,lambda_call(lambda_var(1),lambda_var(1)))), [
                '1 (λ. 1 1)',
                '1(λ.1 1)',
                '1λ.1 1',
                '(1lambda.1 1)',
                '(1\\lambda.(1 1))'
                ]),
            # test subscripts and superscripts in variable names
            (lambda_var('x_2^4'), ['x_2^4']),
            (lambda_call(lambda_var('x_1^1'),lambda_var('x_3^3')), [
                'x_1^1  x_3^3',
                '{x_1^1}{x_3^3}',
                'x_1^1x_3^3'
                ]),
            # a more complicated function definition
            (lambda_func(None,lambda_func(None,lambda_func(None,lambda_call(lambda_call(lambda_var(3),lambda_var(1)),lambda_call(lambda_var(2),lambda_var(1)))))), [
                'λ.λ.λ.3 1 (2 1)',
                'lambda . lambda . lambda . ((3)(1))((2)(1))'
                ]),
            (lambda_call(lambda_func('x_y^z',lambda_var('x_y^z')),(lambda_func('π',lambda_var('π')))), [
                '(λ x_y^z.x_y^z)λπ.π',
                '[\\lambda x_y^z.x_y^z]{\\lambda π.π}'
                ])
            ]

        # test all the test vectors we made
        for as_obj, as_str_list in test_vectors:

            for as_str in as_str_list:

                # test that the parser can parse a string

                parse_result = parse_lambda(as_str)

                # test that the parsed result is correct

                self.assertTrue(parse_result == as_obj)

                # test that str works

                str_result = str(as_obj)

                # test that parsing it back works

                parse_result = parse_lambda(str_result)

                # see that it matches

                self.assertTrue(parse_result == as_obj)

class TestLambdaCompute(unittest.TestCase):
    """
    Test cases focused on performing computations with
    the lambda calculus. Somewhat low level, so
    like TestInternalState, a test case fail does not
    necessarily indicate the program has an error,
    but it is something to take note of.
    """
    def test_church_numerals(self):
        """
        Church numeral for an integer n is a function
        which causes its input to be repeated n times:
        n f x = f ( f ( ... ( x ) ... ) )
        with n copies of f.
        We can define some functions representing Church
        numerals, and then do some math with them.

        Assumes parser is already working.

        Not a comprehensive arithmetic test.
        At time of writing, remotely large Church numerals
        will result in exceeding the recursion depth limit,
        which is probably due to a bug rather than because
        the function evaluation is particularly complex.
        """
        from lambda_calculus import parse_lambda

        x = parse_lambda('x')
        y = parse_lambda('y')

        def verify_number(func, n):
            """
            Check that the function provided does actually
            represent the Church numeral for n.
            """
            # make the reference expression
            ref = y
            for _ in range(n):
                ref = x.call(ref)
            # make the actual test evaluation
            cmp = func.call(x).call(y).evaluate_now()
            # are they the same?
            self.assertTrue(ref == cmp)

        # check some of the basic ones

        n0 = parse_lambda('\\lambda.\\lambda.1')

        verify_number(n0, 0)

        n1 = parse_lambda('\\lambda.\\lambda.2 1')

        verify_number(n1, 1)

        I = parse_lambda('\\lambda.1')

        verify_number(I, 1)

        # the first non trivial counting numbers

        n2 = parse_lambda('\\lambda.\\lambda.2(2 1)')

        verify_number(n2, 2)

        n3 = parse_lambda('\\lambda.\\lambda.2(2(2 1))')

        verify_number(n3, 3)

        # make and test successor function

        succ = parse_lambda('\\lambda.\\lambda.\\lambda.2(3 2 1)')

        verify_number(succ.call(n0), 1)
        verify_number(succ.call(n1), 2)
        verify_number(succ.call(n2), 3)
        verify_number(succ.call(n3), 4)

        verify_number(succ.call(succ.call(n0)), 2)
        verify_number(succ.call(succ.call(n1)), 3)
        verify_number(succ.call(succ.call(n2)), 4)
        verify_number(succ.call(succ.call(n3)), 5)

        # no add, multiply, or exponent, since right now they
        # break the recursion limit

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
