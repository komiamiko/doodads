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

if __name__ == '__main__':
    unittest.main()
