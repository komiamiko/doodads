"""
Unit tests for the ordinal library.
"""

from ordinal import _omega_t, omega, ordinal
import itertools
import warnings
import unittest

class TestOmegaClass(unittest.TestCase):
    def test_instance(self):
        self.assertEqual(omega, _omega_t())
    def test_compare(self):
        for n in 0, 1, 4, -1:
            self.assertFalse(omega == n)
            self.assertTrue(omega != n)
            self.assertFalse(omega < n)
            self.assertTrue(omega > n)
            self.assertFalse(omega <= n)
            self.assertTrue(omega >= n)
        self.assertTrue(omega == omega)
        self.assertFalse(omega != omega)
        self.assertFalse(omega < omega)
        self.assertFalse(omega > omega)
        self.assertTrue(omega <= omega)
        self.assertTrue(omega >= omega)

class TestOrdinalClass(unittest.TestCase):
    def test_instance_cnf(self):
        self.assertEqual(ordinal(0).cnf, [])
        self.assertEqual(ordinal(1).cnf, [(0, 1)])
        self.assertEqual(ordinal(7).cnf, [(0, 7)])
        self.assertEqual(ordinal('omega').cnf, [(1, 1)])
        self.assertEqual(ordinal([(4, 3), (2, 1)]).cnf, [(4, 3), (2, 1)])
    def test_instance_eq(self):
        self.assertEqual(ordinal(0), 0)
        self.assertEqual(ordinal(1), 1)
        self.assertEqual(ordinal(3), ordinal(3))
        self.assertEqual(ordinal('omega'), omega)
        self.assertEqual(ordinal(omega), omega)
    def test_compare(self):
        self.assertTrue(ordinal(omega) == omega)
        self.assertTrue(ordinal(omega) >= omega)
        self.assertTrue(ordinal(omega) <= omega)
        self.assertFalse(ordinal(omega) != omega)
        self.assertFalse(ordinal(omega) > omega)
        self.assertFalse(ordinal(omega) < omega)
        self.assertTrue(ordinal(0) == 0)
        self.assertTrue(ordinal(0) < 1)
        self.assertFalse(ordinal(1) < 0)
        self.assertFalse(ordinal(omega) < 0)
        self.assertTrue(ordinal(omega) > 1)
        ord_ref = ordinal([(3, 2), (1, 4), (0, 1)])
        for cnf in [
            [(1, 4), (0, 1)],
            [(1, 9)],
            [(3, 1), (1, 8)],
            [(3, 1), (2, 6), (1, 7), (0, 8)],
            [(3, 2), (1, 3), (0, 7)],
            [(3, 2), (1, 4)]
            ]:
            ord_cmp = ordinal(cnf)
            self.assertTrue(ord_ref > ord_cmp)
            self.assertTrue(ord_ref >= ord_cmp)
            self.assertTrue(ord_ref != ord_cmp)
            self.assertFalse(ord_ref < ord_cmp)
            self.assertFalse(ord_ref <= ord_cmp)
            self.assertFalse(ord_ref == ord_cmp)
        for cnf in [
            [(3, 2), (1, 4), (0, 1)]
            ]:
            ord_cmp = ordinal(cnf)
            self.assertTrue(ord_ref == ord_cmp)
            self.assertTrue(ord_ref >= ord_cmp)
            self.assertTrue(ord_ref <= ord_cmp)
            self.assertFalse(ord_ref < ord_cmp)
            self.assertFalse(ord_ref > ord_cmp)
            self.assertFalse(ord_ref != ord_cmp)
        for cnf in [
            [(3, 2), (1, 4), (0, 2)],
            [(3, 2), (1, 5)],
            [(3, 2), (2, 1)],
            [(3, 3), (0, 1)],
            [(4, 1)]
            ]:
            ord_cmp = ordinal(cnf)
            self.assertTrue(ord_ref < ord_cmp)
            self.assertTrue(ord_ref <= ord_cmp)
            self.assertTrue(ord_ref != ord_cmp)
            self.assertFalse(ord_ref > ord_cmp)
            self.assertFalse(ord_ref >= ord_cmp)
            self.assertFalse(ord_ref == ord_cmp)
    def test_compare_recursive(self):
        n = 20
        seq_a = [ordinal([(1, 1)])]
        seq_b = [ordinal([(1, 1), (0, 1)])]
        while len(seq_a) < n:
            seq_a.append(ordinal([(seq_a[-1], 2), (2, 1)]))
            seq_b.append(ordinal([(seq_b[-1], 1)]))
        for i in range(n):
            a = seq_a[i]
            b = seq_b[i]
            self.assertTrue(a < b)
            self.assertTrue(a <= b)
            self.assertTrue(a != b)
            self.assertFalse(a > b)
            self.assertFalse(a >= b)
            self.assertFalse(a == b)
        for i in range(1, n):
            b = seq_a[i]
            for j in range(i):
                a = seq_a[j]
                self.assertTrue(a < b)
                self.assertTrue(a <= b)
                self.assertTrue(a != b)
                self.assertFalse(a > b)
                self.assertFalse(a >= b)
                self.assertFalse(a == b)
            b = seq_b[i]
            for j in range(i):
                a = seq_b[j]
                self.assertTrue(a < b)
                self.assertTrue(a <= b)
                self.assertTrue(a != b)
                self.assertFalse(a > b)
                self.assertFalse(a >= b)
                self.assertFalse(a == b)
    def test_instance_warn(self):
        warnings.simplefilter('error')
        with self.assertRaises(UserWarning):
            ordinal(-1)
        with self.assertRaises(UserWarning):
            ordinal([], unchecked=True)
        with self.assertRaises(UserWarning):
            ordinal([(1/2, 1)], unchecked=True)
        with self.assertRaises(UserWarning):
            ordinal([(-1, 1)], unchecked=True)
        with self.assertRaises(UserWarning):
            ordinal([(1, 1/2)], unchecked=True)
        with self.assertRaises(UserWarning):
            ordinal([(1, -1)], unchecked=True)
        warnings.resetwarnings()
    def test_add_basic(self):
        operands = [
            ordinal([]), # 0
            ordinal([(0, 1)]), # 1
            ordinal([(0, 4)]), # 4
            ordinal([(1, 1)]), # omega
            ordinal([(2, 9)]), # omega**2 * 9
            ]
        results = [
            [],
            [(0, 1)],
            [(0, 4)],
            [(1, 1)],
            [(2, 9)],
            [(0, 1)],
            [(0, 2)],
            [(0, 5)],
            [(1, 1)],
            [(2, 9)],
            [(0, 4)],
            [(0, 5)],
            [(0, 8)],
            [(1, 1)],
            [(2, 9)],
            [(1, 1)],
            [(1, 1), (0, 1)],
            [(1, 1), (0, 4)],
            [(1, 2)],
            [(2, 9)],
            [(2, 9)],
            [(2, 9), (0, 1)],
            [(2, 9), (0, 4)],
            [(2, 9), (1, 1)],
            [(2, 18)]
            ]
        for (a,b),r in zip(itertools.product(*[operands]*2), results):
            self.assertEqual(r, (a + b).cnf)
    def test_add_large(self):
        small = 2**8191-1
        big = ordinal([(2, 1), (1, 2)])
        huge = ordinal([(big, 3)])
        operands = [
            ordinal([(small, 7), (0, 2)]),
            ordinal([(big, 2), (0, 5)]),
            ordinal([(huge, 1), (small, 8), (0, 3)]),
            ordinal([(huge, 4), (big, 3), (0, 6)])
            ]
        results = [
            [(small, 14), (0, 2)],
            [(big, 2), (0, 5)],
            [(huge, 1), (small, 8), (0, 3)],
            [(huge, 4), (big, 3), (0, 6)],
            [(big, 2), (small, 7), (0, 2)],
            [(big, 4), (0, 5)],
            [(huge, 1), (small, 8), (0, 3)],
            [(huge, 4), (big, 3), (0, 6)],
            [(huge, 1), (small, 15), (0, 2)],
            [(huge, 1), (big, 2), (0, 5)],
            [(huge, 2), (small, 8), (0, 3)],
            [(huge, 5), (big, 3), (0, 6)],
            [(huge, 4), (big, 3), (small, 7), (0, 2)],
            [(huge, 4), (big, 5), (0, 5)],
            [(huge, 5), (small, 8), (0, 3)],
            [(huge, 8), (big, 3), (0, 6)]
            ]
        for (a,b),r in zip(itertools.product(*[operands]*2), results):
            self.assertEqual(r, (a + b).cnf)
    def test_arithmetic_expr(self):
        self.assertEqual(1 + omega, omega)
        self.assertEqual(omega + omega, omega * 2)
        self.assertEqual((omega + 2) * (omega + 3), omega * omega + omega * 3)

if __name__ == '__main__':
    unittest.main()
