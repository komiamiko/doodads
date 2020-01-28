"""
Unit tests for the ordinal library.
"""

import ordinal as _
import itertools
import warnings
import unittest

class TestBisectedFunctions(unittest.TestCase):
    """
    Test battery for the 'bisected' versions of utility functions.
    They are expected to do the same thing with better performance
    for certain kinds of inputs.
    """
    
    def test_reduce(self):
        """
        Tests the bisected version of 'reduce'
        against the original from functools
        """
        from ordinal import reduce_bisected
        from functools import reduce
        from random import randint
        from operator import add, mul

        int_seq = []
        for _ in range(1000):
            value = randint(-3, 3)
            int_seq.append(value)

        for n in range(0, 1001):
            subseq = int_seq[0:n]
            self.assertEqual(
                reduce(add, subseq, 0),
                reduce_bisected(add, subseq, 0)
                )

        int_seq = []
        for _ in range(1000):
            value = randint(-2, 3)
            if value <= 0:
                value -= 1
            int_seq.append(value)

        for n in range(0, 1001):
            subseq = int_seq[0:n]
            self.assertEqual(
                reduce(mul, subseq, 1),
                reduce_bisected(mul, subseq, 1)
                )

        lin_seq = []
        ident = (1, 0)
        for _ in range(1000):
            u = randint(-2, 3)
            if u <= 0:
                u -= 1
            v = randint(-5, 5)
            lin_seq.append((u, v))

        def lin_concat(a, b):
            au, av = a
            bu, bv = b
            return (au * bu, au * bv + av)

        for n in range(0, 1001):
            subseq = lin_seq[0:n]
            self.assertEqual(
                reduce(lin_concat, subseq, ident),
                reduce_bisected(lin_concat, subseq, ident)
                )
            
    def test_sum(self):
        """
        Tests the bisected version of 'sum'
        against the original in the builtins
        """
        from ordinal import sum_bisected
        from random import randint

        int_seq = []
        for _ in range(1000):
            value = randint(-1000, 1000)
            int_seq.append(value)

        for n in range(0, 1001):
            subseq = int_seq[0:n]
            self.assertEqual(
                sum(subseq),
                sum_bisected(subseq)
                )

class TestOrdinalClass(unittest.TestCase):
    """
    Test battery focused on the ordinal number class
    and its basic functionality.
    """

    def test_integers(self):
        """
        Sanity tests involving ordinals that are mathematically
        integers and the builtin int objects.
        Since integers are very straightforward and cheap to
        test with, we do a lot of the low level sanity checks here.
        """
        from ordinal import ordinal, ordinal_type

        for i in range(100):
            
            self.assertTrue(isinstance(i, ordinal_type))
            self.assertTrue(isinstance(ordinal(i), ordinal_type))
            
            self.assertEqual(i == i, ordinal(i) == i)
            self.assertEqual(i == i, ordinal(i) == ordinal(i))
            self.assertEqual(i != i, ordinal(i) != i)
            self.assertEqual(i != i, ordinal(i) != ordinal(i))
            self.assertEqual(i > i, ordinal(i) > i)
            self.assertEqual(i > i, ordinal(i) > ordinal(i))
            self.assertEqual(i >= i, ordinal(i) >= i)
            self.assertEqual(i >= i, ordinal(i) >= ordinal(i))
            self.assertEqual(i < i, ordinal(i) < i)
            self.assertEqual(i < i, ordinal(i) < ordinal(i))
            self.assertEqual(i <= i, ordinal(i) <= i)
            self.assertEqual(i <= i, ordinal(i) <= ordinal(i))

        for j in range(1, 100):
            for i in range(j):

                self.assertEqual(i == j, ordinal(i) == j)
                self.assertEqual(i == j, ordinal(i) == ordinal(j))
                self.assertEqual(i != j, ordinal(i) != j)
                self.assertEqual(i != j, ordinal(i) != ordinal(j))
                self.assertEqual(i > j, ordinal(i) > j)
                self.assertEqual(i > j, ordinal(i) > ordinal(j))
                self.assertEqual(i >= j, ordinal(i) >= j)
                self.assertEqual(i >= j, ordinal(i) >= ordinal(j))
                self.assertEqual(i < j, ordinal(i) < j)
                self.assertEqual(i < j, ordinal(i) < ordinal(j))
                self.assertEqual(i <= j, ordinal(i) <= j)
                self.assertEqual(i <= j, ordinal(i) <= ordinal(j))

                self.assertEqual(j == i, ordinal(j) == i)
                self.assertEqual(j == i, ordinal(j) == ordinal(i))
                self.assertEqual(j != i, ordinal(j) != i)
                self.assertEqual(j != i, ordinal(j) != ordinal(i))
                self.assertEqual(j > i, ordinal(j) > i)
                self.assertEqual(j > i, ordinal(j) > ordinal(i))
                self.assertEqual(j >= i, ordinal(j) >= i)
                self.assertEqual(j >= i, ordinal(j) >= ordinal(i))
                self.assertEqual(j < i, ordinal(j) < i)
                self.assertEqual(j < i, ordinal(j) < ordinal(i))
                self.assertEqual(j <= i, ordinal(j) <= i)
                self.assertEqual(j <= i, ordinal(j) <= ordinal(i))

        with self.assertRaises(ValueError):
            ordinal(-1)

        with self.assertRaises(TypeError):
            ordinal(0.5)

    def test_constants(self):
        """
        Small test case to ensure all the provided constants,
        such as omega, are actually the ordinals they're supposed to be.
        """
        from ordinal import ordinal, omega, epsilon_0, zeta_0

        self.assertEqual(omega, ordinal('omega'))
        self.assertEqual(epsilon_0, ordinal('epsilon_0'))
        self.assertEqual(zeta_0, ordinal('zeta_0'))
        
        self.assertTrue(1 < omega)
        self.assertTrue(omega < epsilon_0)
        self.assertTrue(epsilon_0 < zeta_0)

class TestOrdinalArithmetic(unittest.TestCase):
    """
    Test battery focused around ordinal operations.
    """

    def test_addition(self):
        """
        Tests ordinal addition, both directly
        against test vectors and with mathematical expectations.
        Can't reach omega^2 without multiplication, so stays
        below omega^2.
        """
        from ordinal import omega

        self.assertTrue(omega + 1 > omega)
        self.assertTrue(1 + omega == omega)
        self.assertTrue(omega + omega > omega + 1)
        self.assertTrue(omega + 1 + omega == omega + omega)

        big = 1<<1000
        self.assertTrue(omega + big < omega + omega)
        self.assertTrue(big + omega == omega)
        
        self.assertTrue(omega + omega < omega + omega + omega)
        self.assertTrue(omega + omega + omega == omega + (omega + omega))
        self.assertTrue(omega + omega + omega + omega == (omega + omega) + (omega + omega))

    def test_addition_veblen(self):
        """
        Extra tests on ordinal addition,
        now including ordinals in the Veblen hierarchy.
        These are 'harder' than the more basic test case.
        """
        from ordinal import omega, epsilon_0, veblen

        # more tests at the veblen hierarchy

        A = veblen(0, omega)
        self.assertTrue(omega + A == A)
        self.assertTrue(A + omega > A)
        self.assertTrue(A + omega < A + A)
        self.assertTrue(A < epsilon_0)
        self.assertTrue(A + epsilon_0 == epsilon_0)
        self.assertTrue(epsilon_0 + omega + A == epsilon_0 + A)
        self.assertTrue(epsilon_0 + A < epsilon_0 + epsilon_0)

    def test_multiplication(self):
        """
        Tests ordinal multiplication, both directly
        against test vectors and with mathematical expectations.
        Can't reach omega^omega without exponentiation,
        so all values are below omega^omega.
        """
        from ordinal import omega

        self.assertTrue(omega * 2 > omega)
        self.assertTrue(omega * 2 == omega + omega)
        self.assertTrue(2 * omega == omega)
        self.assertTrue(omega * omega > omega)
        self.assertTrue(omega + omega * omega == omega * omega)
        self.assertTrue(omega * 2 * omega == omega * omega)
        self.assertTrue((omega + 1) * 3 == omega * 3 + 1)
        self.assertTrue(3 * (omega + 1) == omega + 3)
        self.assertTrue((omega + 1) * omega == omega * omega)
        self.assertTrue(omega * (omega + 1) == omega * omega + omega)
        self.assertTrue((omega + 2) * (omega + 2) == omega * omega + omega * 2 + 2)

        # harder tests

        A = omega * 2 + 3
        self.assertTrue(omega * A == omega * omega * 2 + omega * 3)
        self.assertTrue(A * omega == omega * omega)
        self.assertTrue(A * A == omega * omega * 2 + omega * 6 + 3)
        self.assertTrue(A * A * A == A * (A * A))

    def test_multiplication_veblen(self):
        """
        Harder test case for ordinal multiplication, which involves
        ordinals drawn from within the Veblen hierarchy.
        """
        from ordinal import omega, epsilon_0, veblen
        # go harder! use veblen

        self.assertTrue(epsilon_0 * 2 > epsilon_0)
        self.assertTrue(epsilon_0 * 2 < epsilon_0 * omega)
        self.assertTrue(2 * epsilon_0 == epsilon_0)
        self.assertTrue(omega * epsilon_0 == epsilon_0)
        self.assertTrue(omega * 2 * epsilon_0 == epsilon_0)
        self.assertTrue(omega * (epsilon_0 * 2) == epsilon_0 * 2)
        self.assertTrue(epsilon_0 * 2 * epsilon_0 == epsilon_0 * epsilon_0)
        self.assertTrue(epsilon_0 * 2 * (epsilon_0 * 2) == epsilon_0 * epsilon_0 * 2)
        self.assertTrue(epsilon_0 * omega == veblen(0, epsilon_0 + 1))
        self.assertTrue(epsilon_0 * 2 * omega == veblen(0, epsilon_0 + 1))
        self.assertTrue(epsilon_0 * 2 * omega * 2 == veblen(0, epsilon_0 + 1) * 2)

    def test_power(self):
        """
        Test ordinal powers/exponentiation against test vectors
        and mathematical expectations.
        Already includes ordinals from the Veblen hierarchy,
        so this way we can test the fixed points and such.
        """
        from ordinal import ordinal, omega, epsilon_0, veblen

        # test integer cases work as expected

        for ni, nj in itertools.product(*[range(5)]*2):
            for i in (ni, ordinal(ni)):
                for j in (nj, ordinal(nj)):
                    self.assertTrue(i ** j == ni ** nj)

        # test some special cases that reduce easily
        As = (
            1,
            2,
            3,
            8,
            omega,
            omega + 1,
            omega * 2,
            omega * 3 + 4,
            epsilon_0,
            epsilon_0 + 1,
            epsilon_0 * 2 + 3,
            veblen(7, 7) + veblen(5, 5) * 3
            )
        for A in As:
            self.assertTrue(A ** 0 == 1)
            self.assertTrue(A ** 1 == A)
            self.assertTrue(2 ** (omega * A) == veblen(0, A))
            self.assertTrue(5 ** (omega * A) == veblen(0, A))

        # test some easy known cases
        self.assertTrue(omega ** 2 == omega * omega)
        self.assertTrue(omega ** epsilon_0 == epsilon_0)
        self.assertTrue(omega ** (epsilon_0 + 1) == epsilon_0 * omega)
        self.assertTrue(omega ** omega, veblen(0, omega))
        self.assertTrue(omega ** (omega * 2 + 3), veblen(0, omega * 2 + 3))

        # test small powers behave as expected
        for A in As:
            self.assertTrue(A ** 2 == A * A)
            self.assertTrue(A ** 3 == A * A * A)

        # test larger powers match results of exponentiation by squaring
        for A in As:
            A2 = A * A
            A4 = A2 * A2
            A8 = A4 * A4
            A16 = A8 * A8
            self.assertTrue(A ** 4 == A4)
            self.assertTrue(A ** 5 == A4 * A)
            self.assertTrue(A ** 11 == A8 * A2 * A)
            self.assertTrue(A ** 49 == A16 * A16 * A16 * A)

        # test power laws
        for A,B,C in itertools.product(*[As]*3):
            self.assertTrue(A ** (B * C) == (A ** B) ** C)
            self.assertTrue(A ** (B + C) == A ** B * A ** C)

        # test veblen function at 0 is identical to omega exponential
        for A in As:
            self.assertTrue(omega ** A == veblen(0, A))

        # test exponential is non-decreasing in both arguments
        for A,B in itertools.product(*[As]*2):
            if A <= 1:continue
            self.assertTrue(A ** B >= B)
            self.assertTrue(A ** B >= A)

        # test specific examples
        self.assertTrue((omega * 2 + 3) ** omega == omega ** omega)
        self.assertTrue(omega ** epsilon_0 == epsilon_0)
        self.assertTrue((omega * 2 + 3) ** epsilon_0 == epsilon_0)
        self.assertTrue(omega ** epsilon_0 * omega == omega ** (epsilon_0 + 1))
        self.assertTrue(epsilon_0 ** epsilon_0 == omega ** omega ** (epsilon_0 * 2))
        self.assertTrue(epsilon_0 ** omega == omega ** omega ** (epsilon_0 + 1))

    def test_veblen(self):
        """
        Test case specifically for the Veblen function
        and its behaviour.
        """
        from ordinal import veblen, omega, epsilon_0, zeta_0

        self.assertTrue(omega == veblen(0, 1))
        self.assertTrue(epsilon_0 == veblen(1, 0))
        self.assertTrue(zeta_0 == veblen(2, 0))
        self.assertTrue(omega * omega == veblen(0, 2))
        
        self.assertTrue(veblen(0, omega + 1) == veblen(0, omega) * omega)
        self.assertTrue(veblen(0, epsilon_0) == epsilon_0)
        self.assertTrue(veblen(0, epsilon_0 + 1) > epsilon_0)
        self.assertTrue(veblen(0, epsilon_0 + 1) == epsilon_0 * omega)
        self.assertTrue(veblen(0, epsilon_0 + 1) * 2 > epsilon_0 * 3)
        self.assertTrue(veblen(0, epsilon_0 + 1) * 2 > epsilon_0 * omega)
        self.assertTrue(veblen(0, epsilon_0 + 1) * 2 == epsilon_0 * omega * 2)
        self.assertTrue(veblen(0, veblen(0, omega)) > veblen(0, omega * omega))
        self.assertTrue(veblen(0, veblen(0, omega)) < epsilon_0)
        self.assertTrue(veblen(1, zeta_0) == zeta_0)
        self.assertTrue(veblen(1, zeta_0 + 1) > zeta_0)
        self.assertTrue(veblen(1, zeta_0 + 1) > veblen(0, zeta_0 + 1))
        self.assertTrue(veblen(0, epsilon_0 + 1) < veblen(1, 1))
        
        self.assertTrue(veblen(zeta_0, 0) > veblen(omega, 0))
        self.assertTrue(veblen(zeta_0, 0) < veblen(omega, veblen(zeta_0, 0) + 1))
        self.assertTrue(veblen(zeta_0, veblen(zeta_0 + 1, 0)) == veblen(zeta_0 + 1, 0))
        towers = [veblen(veblen(epsilon_0, 0), 0),
                  veblen(veblen(epsilon_0, 0), 1),
                  veblen(veblen(epsilon_0, 1), 0)]
        self.assertTrue(zeta_0 < towers[0])
        self.assertTrue(towers[0] < towers[1])
        self.assertTrue(towers[0] < towers[2])
        self.assertTrue(towers[1] < towers[2])
        self.assertTrue(veblen(zeta_0, towers[2]) == towers[2])
        self.assertTrue(veblen(0, towers[2] + 1) > towers[2])
        self.assertTrue(veblen(omega, towers[2] + 1) > towers[2])
        self.assertTrue(veblen(epsilon_0, towers[2] + 1) > towers[2])
        self.assertTrue(veblen(towers[2], towers[1]) > veblen(towers[1], towers[2]))

    def test_fundamental_sequence(self):
        """
        Test case that takes fundamental sequences of ordinals
        and checks to make sure they're sane.
        There's not much of a point testing against test vectors,
        since fundamental sequences can be chosen differently without
        breaking the math about ordinals. In fact, from just an ordinal,
        nothing is implied about what its fundamental sequence 'should' be.
        """
        from ordinal import veblen, omega, epsilon_0, zeta_0, kind, kind_limit

        # lots of increasing ones!
        As = (
            5,
            omega,
            omega + 3,
            omega * 2,
            omega * 3 + 4,
            omega ** 2,
            omega ** 2 * 3 + omega * 6,
            omega ** 3 * 4 + omega ** 2 * 3 + omega * 2,
            omega ** omega,
            omega ** omega + omega ** 6 + 4,
            omega ** omega * 2,
            omega ** omega * omega,
            omega ** omega ** omega + omega ** (omega ** 2 * 3) + omega ** 4,
            omega ** omega ** omega ** omega,
            epsilon_0,
            epsilon_0 + omega ** omega,
            epsilon_0 * 2,
            epsilon_0 * omega,
            epsilon_0 ** omega,
            epsilon_0 ** epsilon_0,
            veblen(1, 1),
            veblen(1, 4),
            veblen(1, omega),
            veblen(1, veblen(1, veblen(1, 0))),
            zeta_0,
            zeta_0 + epsilon_0,
            zeta_0 + epsilon_0 + omega ** omega + omega + 3,
            zeta_0 + epsilon_0 + omega ** omega + omega * 3,
            zeta_0 + epsilon_0 + omega ** omega + omega ** 3,
            zeta_0 * 2,
            zeta_0 * 2 + omega ** omega,
            zeta_0 * 2 + epsilon_0 * 3,
            zeta_0 * 5 + 1,
            zeta_0 * omega,
            zeta_0 * epsilon_0,
            zeta_0 ** 2,
            zeta_0 ** epsilon_0,
            veblen(1, zeta_0 + 1),
            veblen(2, epsilon_0),
            veblen(2, epsilon_0 + 1),
            veblen(2, veblen(1, 1)),
            veblen(3, 0),
            veblen(5, veblen(6, omega) * 2),
            veblen(omega, 0),
            veblen(omega, 1),
            veblen(omega, omega),
            veblen(omega, omega ** omega ** omega),
            veblen(omega, epsilon_0),
            veblen(omega + 1, 0),
            veblen(omega + 1, 3),
            veblen(omega * 3, 0),
            veblen(zeta_0, zeta_0),
            veblen(veblen(zeta_0, 1), 1)
            )
        # and some integers
        # note: the A[19] < A[20] test is a good way to check that the comparison is efficient
        # since the fundamental sequence values tend to increase in complexity with n
        Ns = (0, 1, 2, 4, 7, 19)
        # test the ordering is correct
        for A,B in zip(As,As[1:]):
            self.assertTrue(A < B)
        for A in As:
            if kind(A) != kind_limit:continue
            # test fundamental sequence is increasing and probably converging correctly
            for n, m in zip(Ns, Ns[1:]):
                self.assertTrue(A[n] < A[m])
            self.assertTrue(A[Ns[-1]] < A)
            # test eventual domination by fundamental sequence of a higher ordinal
            for B in As:
                if B >= A:continue
                passed = False
                # it won't take longer than 10, right?
                for n in range(2, 10):
                    C = A[n]
                    if C >= B:
                        passed = True
                        break
                self.assertTrue(passed)

    def test_deep_comparison_veblen_2(self):
        """
        Very deep/complex ordinals have previously been a performance issue,
        having runtime exponential in the depth.
        This was spotted by the fundamental sequence test.
        Let's test to make sure that issue isn't happening again.

        More specifically, this tests deep expressions of the form
        phi_A(phi_A(...(B)...))
        which differ only in B, and expects that the test completes in
        time linear to the depth. If it's not linear time, we have issues.
        """
        from ordinal import veblen

        # this was originally going to go up to 100,
        # but that exceeds CPython's default recursion depth limit
        for hardness in range(1,50,5):

            # test the classic example
            A = veblen(1,1)[hardness]
            B = veblen(1,1)[hardness+1]

            self.assertTrue(A < B)

            # test a different example
            A = veblen(1,0) + 1
            for B in (
                A + 1,
                A * 2,
                A * A
                ):
                
                modA = A
                modB = B
                
                for _ in range(hardness):
                    modA = veblen(0, modA)
                    modB = veblen(0, modB)
                    
                self.assertTrue(modA < modB)
                
                # also check if it's handled well as a higher
                modA = veblen(modA, 1)
                modB = veblen(modB, 0)
                self.assertTrue(modA < modB)

            # somewhat harder test, using different fixed points
            A = veblen(3,1)+1
            B = veblen(3,2)+1
                
            modA = A
            modB = B
            
            for _ in range(hardness):
                modA = veblen(2, modA)
                modB = veblen(1, modB)

            self.assertTrue(modA < modB)

if __name__ == '__main__':
    unittest.main()
