"""
Unit tests for the ordinal library.
"""

import ordinal as _
import itertools
import warnings
import unittest

class TestBisectedFunctions(unittest.TestCase):
    
    def test_reduce(self):
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

    def test_integers(self):
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
        from ordinal import ordinal, omega, epsilon_0, zeta_0

        self.assertEqual(omega, ordinal('omega'))
        self.assertEqual(epsilon_0, ordinal('epsilon_0'))
        self.assertEqual(zeta_0, ordinal('zeta_0'))
        
        self.assertTrue(1 < omega)
        self.assertTrue(omega < epsilon_0)
        self.assertTrue(epsilon_0 < zeta_0)

class TestOrdinalArithmetic(unittest.TestCase):

    def test_addition(self):
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

    def test_veblen(self):
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

if __name__ == '__main__':
    unittest.main()