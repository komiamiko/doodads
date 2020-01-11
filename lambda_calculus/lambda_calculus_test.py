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
