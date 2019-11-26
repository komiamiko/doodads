#!/usr/bin/env python3

"""
Unit tests for hype.py

We appreciate contributions of unit tests of all kinds!
Please note, however, one crucial thing: since this is a very math focused library,
please do the math yourself and be very sure your answer is correct
before you contribute.
"""

# the unittest library, that lets us test things
import unittest

# the math library
from math import isclose, exp, sqrt, hypot, asinh, acosh

# the fractions library
from fractions import Fraction

# the thing we want to test
from hype import space, space_point, common_math, to_real

def point_isclose(a, b, *args, **kwargs):
    """
    Analogue of math.isclose for space points.
    """
    for x, y in zip(a, b):
        if not isclose(x, y, *args, **kwargs):
            return False
    return True

class TestExtendedMath(unittest.TestCase):
    """
    Collection of tests for the math namespace.
    Ensures that the math namespace actually contains
    correct mathematical objects.
    """

    def test_real(self):
        """
        Test that the real type is sane.
        """

        real = common_math.real

        self.assertTrue(real(3.75) + real(4.75) == real(8.5))
        self.assertTrue(real(2.5) * real(-1.5) == -real(3.75))

        pi_1 = to_real(real, Fraction(311, 99))
        pi_2 = to_real(real, Fraction(333, 106))
        pi_3 = to_real(real, Fraction(355, 113))

        self.assertTrue(pi_1 < pi_2)
        self.assertTrue(pi_2 < pi_3)
        
    def test_constants(self):
        """
        Test that constants, existing or extra, are correct.
        """

        pi_ref = 3.14159265358979323846264338327933
        tau_ref = 6.28318530717958647692528676655867
        e_ref = 2.71828182845904523536028747135281

        self.assertTrue(isclose(
            common_math.pi,
            pi_ref
            ))
        self.assertTrue(isclose(
            common_math.tau,
            tau_ref
            ))
        self.assertTrue(isclose(
            common_math.e,
            e_ref
            ))

    def test_functions(self):
        """
        Test that functions are returning correct values.
        """

        # exp

        e_ref = 2.71828182845904523536028747135281
        ee_ref = 15.1542622414792641897604302726327

        self.assertTrue(isclose(
            common_math.exp(0),
            1
            ))
        self.assertTrue(isclose(
            common_math.exp(1),
            e_ref
            ))
        self.assertTrue(isclose(
            common_math.exp(e_ref),
            ee_ref
            ))

        # sqrt
        
        s2_ref = 1.41421356237309504880168872420977
        s3_ref = 1.73205080756887729352744634150584
        e2_ref = 7.3890560989306502272304274605753
        ef2_ref = 1.6487212707001281468486507878142

        self.assertTrue(isclose(
            common_math.sqrt(0),
            0
            ))
        self.assertTrue(isclose(
            common_math.sqrt(1),
            1
            ))
        self.assertTrue(isclose(
            common_math.sqrt(4),
            2
            ))
        self.assertTrue(isclose(
            common_math.sqrt(2),
            s2_ref
            ))
        self.assertTrue(isclose(
            common_math.sqrt(3),
            s3_ref
            ))
        self.assertTrue(isclose(
            common_math.sqrt(e2_ref),
            e_ref
            ))
        self.assertTrue(isclose(
            common_math.sqrt(e_ref),
            ef2_ref
            ))

        # cbrt
        
        e3_ref = 20.0855369231876677409285296545811
        ef3_ref = 1.39561242508608952862812531960265

        self.assertTrue(isclose(
            common_math.cbrt(0),
            0
            ))
        self.assertTrue(isclose(
            common_math.cbrt(1),
            1
            ))
        self.assertTrue(isclose(
            common_math.cbrt(-1),
            -1
            ))
        self.assertTrue(isclose(
            common_math.cbrt(8),
            2
            ))
        self.assertTrue(isclose(
            common_math.cbrt(-0.125),
            -0.5
            ))
        self.assertTrue(isclose(
            common_math.cbrt(e3_ref),
            e_ref
            ))
        self.assertTrue(isclose(
            common_math.cbrt(e_ref),
            ef3_ref
            ))

        # hypot

        self.assertTrue(isclose(
            common_math.hypot(0, 0),
            0
            ))
        self.assertTrue(isclose(
            common_math.hypot(1, 0),
            1
            ))
        self.assertTrue(isclose(
            common_math.hypot(1, 1),
            s2_ref
            ))
        self.assertTrue(isclose(
            common_math.hypot(1, s2_ref),
            s3_ref
            ))
        self.assertTrue(isclose(
            common_math.hypot(1, s3_ref),
            2
            ))
        self.assertTrue(isclose(
            common_math.hypot(s3_ref, 1),
            2
            ))

        # asinh

        sh1_ref = 1.17520119364380145688238185059568
        she_ref = 7.54413710281697582634182004251749

        self.assertTrue(isclose(
            common_math.asinh(0),
            0
            ))
        self.assertTrue(isclose(
            common_math.asinh(sh1_ref),
            1
            ))
        self.assertTrue(isclose(
            common_math.asinh(-sh1_ref),
            -1
            ))
        self.assertTrue(isclose(
            common_math.asinh(she_ref),
            e_ref
            ))

        # cosh

        ch1_ref = 1.54308063481524377847790562075713
        che_ref = 7.61012513866228836341861023011441

        self.assertTrue(isclose(
            common_math.acosh(1),
            0
            ))
        self.assertTrue(isclose(
            common_math.acosh(ch1_ref),
            1
            ))
        self.assertTrue(isclose(
            common_math.acosh(che_ref),
            e_ref
            ))

        # re

        self.assertTrue(common_math.re(0) == 0)
        self.assertTrue(common_math.re(1) == 1)
        self.assertTrue(common_math.re(e_ref) == e_ref)
        self.assertTrue(common_math.re(2j**2) == -4)
        self.assertTrue(common_math.re(3+4j) == 3)

class TestSpaceClass(unittest.TestCase):
    """
    Test that the space class can pass basic sanity tests.
    Does not check the actual math methods.
    """
    
    def test_init_attr(self):
        """
        Test that the core class `space` can be instanced,
        and that its attributes are as expected.
        """
        
        for k in (0, -1, 1):
            s = space(curvature=k)
            self.assertTrue(isclose(
                s.curvature,
                k
                ))
        
        for k in (1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(curvature=k)
            self.assertTrue(s.curvature == k)

        for fk in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(fake_curvature=fk)
            self.assertTrue(isclose(
                s.curvature,
                fk * abs(fk)
                ))

        for r in (1, 2, 1j, 2j, float('inf')):
            s = space(radius=r)
            self.assertTrue(s.curvature == 1/r**2)
            
    def test_equality(self):
        """
        Test that equivalent instances of `space` do appear equal,
        and that distinct instances do not appear equal.
        """

        s3 = space(curvature=1/5)
        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s1 = space(fake_curvature=k)
            s2 = space(fake_curvature=k)
            self.assertTrue(s1 == s2)
            self.assertTrue(hash(s1) == hash(s2))
            self.assertTrue(str(s1) == str(s2))
            self.assertTrue(repr(s1) == repr(s2))
            self.assertTrue(s1 != s3)
            
    def test_repr(self):
        """
        Test that the `space` class' repr can actually be used to reconstruct it.
        """
        
        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(fake_curvature=k)
            r = repr(s)
            v = eval(r)
            self.assertTrue(s == v)

class TestSpacePoint(unittest.TestCase):
    """
    Test that the space_point class can pass basic sanity tests.
    Not much math done here.
    """

    def test_init_attr(self):
        """
        Test that some simple points are constructed
        as expected.
        """
        import itertools

        # K = 0

        s = space(curvature=0)
        p = s.make_origin(0)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1]
            ))))
        p = s.make_origin(2)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1, 0, 0]
            ))))
        p = s.make_point((1, 0), 1)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1, 1, 0]
            ))))

        # K = 1

        sn1_ref = 0.841470984807896506652502321630345
        cn1_ref = 0.540302305868139717400936607442955

        s = space(curvature=1)
        p = s.make_origin(0)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1]
            ))))
        p = s.make_origin(2)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1, 0, 0]
            ))))
        p = s.make_point((1, 0), 1)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [cn1_ref, sn1_ref, 0]
            ))))

        # K = -1

        sh1_ref = 1.17520119364380145688238185059568
        ch1_ref = 1.54308063481524377847790562075713

        s = space(curvature=-1)
        p = s.make_origin(0)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1]
            ))))
        p = s.make_origin(2)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [1, 0, 0]
            ))))
        p = s.make_point((1, 0), 1)
        self.assertTrue(all(itertools.starmap(isclose, zip(
            p.x,
            [ch1_ref, sh1_ref, 0]
            ))))

    def test_repr(self):
        """
        Test that the repr of the class can be used to exactly reconstruct a point.
        For this test, we don't care so much what the space or point is,
        only that it is reconstructible exactly.
        """

        direction = (3/13, 4/13, 12/13)
        magnitude = 7.33337377737737773737
        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(fake_curvature=k)
            p = s.make_point(direction, magnitude)
            r = repr(p)
            v = eval(r)
            self.assertTrue(p == v)

    def test_true_shape(self):
        """
        Test the true shape invariant:
        x0^2 = 1 - k(x1^2 + x2^2 + ...)
        and that it holds in various spaces and with various points.
        For this test we don't care so much about what the space or point is.
        """
        
        direction = (3/13, 4/13, 12/13)
        magnitude = 7.33337377737737773737
        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            k2 = k * abs(k)
            s = space(fake_curvature=k)
            p = s.make_point(direction, magnitude)
            self.assertTrue(isclose(
                p[0]**2,
                1 - k2 * sum(map((lambda x:x**2), p[1:]))
                ))

    def test_magnitude(self):
        """
        Test that the magnitude of a point constructed from the
        (direction, magnitude) method
        actually has correct magnitude.
        Also checks that the magnitude matches the distance
        to the origin.
        """

        # test small magnitudes with regular unit vectors
        u1 = (1,)
        u2 = (0, 1/2, 0, 1/2, 1/2, 0, 0, 0, 1/2)
        u3 = (12/13, 4/13, 3/13)
        for k in (0, -1, 1):
            s = space(fake_curvature=k)
            for d in (0, 1, 1/3, 3/2):
                for n in (u1, u2, u3):
                    p = s.make_point(n, d)
                    self.assertTrue(isclose(
                        abs(p),
                        d
                        ))
                    self.assertTrue(isclose(
                        s.distance_between(p, s.make_origin(len(n))),
                        d
                        ))

        # test direction vector normalization
        v1 = (73733,)
        v2 = tuple(range(30))
        v3 = (-11, 1, 0, -1, 11, 1/11)
        for k in (0, -1, 1):
            s = space(fake_curvature=k)
            for d in (0, 1, 1/3, 3/2):
                for n in (v1, v2, v3):
                    p = s.make_point(n, d, normalize=True)
                    self.assertTrue(isclose(
                        abs(p),
                        d
                        ))
                    self.assertTrue(isclose(
                        s.distance_between(p, s.make_origin(len(n))),
                        d
                        ))
                    
        # test elliptic space looping property
        pi_ref = 3.14159265358979323846264338327933
        for r in (1, 2, 3, 1/3):
            k = 1/r
            s = space(fake_curvature=k)
            for j, d in ((2, pi_ref - 2), (pi_ref, 0)):
                j *= r
                d *= r
                for n in (u1, u2, u3):
                    p = s.make_point(n, j)
                    self.assertTrue(isclose(
                        abs(p),
                        d,
                        abs_tol = 1e-15
                        ))
                    self.assertTrue(isclose(
                        s.distance_between(p, s.make_origin(len(n))),
                        d,
                        abs_tol = 1e-15
                        ))

class TestTriangles(unittest.TestCase):
    """
    Triangles and trigonometry form some foundation for geometry.
    This collection of tests checks various known triangles and sees
    if the math can correctly solve them.
    """
    pass # TODO

class TestSpheres(unittest.TestCase):
    """
    N-dimensional spheres (and balls, to be pedantic)
    are another simple geometric object.
    Are the surface and volume calculations, and their inverses, correct?
    This collection of tests is for just that.
    """
    def test_volume_surface_empty(self):
        """
        Test empty spheres, calculating forward direction.
        Should always be exactly 0.
        """
        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(fake_curvature=k) 
            for name in ('sphere_s1', 'sphere_v2', 'sphere_s2', 'sphere_v3'):
                self.assertTrue(getattr(s, name)(0) == 0)

    def test_euclidean_unit_spheres(self):
        """
        Test Euclidean unit spheres, which are well known.
        """
        
        s1_ref = 6.28318530717958647692528676655867
        v2_ref = 3.14159265358979323846264338327933
        s2_ref = 12.5663706143591729538505735331173
        v3_ref = 4.18879020478639098461685784437218

        s = space(curvature=0)

        self.assertTrue(isclose(
            s.sphere_s1(1),
            s1_ref
            ))
        self.assertTrue(isclose(
            s.inv_sphere_s1(s1_ref),
            1
            ))
        self.assertTrue(isclose(
            s.sphere_v2(1),
            v2_ref
            ))
        self.assertTrue(isclose(
            s.inv_sphere_v2(v2_ref),
            1
            ))
        self.assertTrue(isclose(
            s.sphere_s2(1),
            s2_ref
            ))
        self.assertTrue(isclose(
            s.inv_sphere_s2(s2_ref),
            1
            ))
        self.assertTrue(isclose(
            s.sphere_v3(1),
            v3_ref
            ))
        self.assertTrue(isclose(
            s.inv_sphere_v3(v3_ref),
            1
            ))

    def test_euclidean_scale(self):
        """
        In Euclidean space, all of the sphere formulas look like a
        monomial in the radius r.
        Thus when we scale the r, we should expect the mass
        to be scaled by r^n, where n is the dimensionality and also
        the exponent in that monomial.
        """

        s = space(curvature=0)

        magic = 77773.333773777773733
        for mul in (2, 5, 1/3, 1/11, magic, 1/magic):
            for name, dim in (
                ('sphere_s1', 1),
                ('sphere_v2', 2),
                ('sphere_s2', 2),
                ('sphere_v3', 3)
                ):
                self.assertTrue(isclose(
                    getattr(s, name)(1) * mul**dim,
                    getattr(s, name)(mul)
                    ))

    def test_hyperbolic_known(self):
        """
        Tests known spheres living in the standard hyperbolic space
        with K = -1.
        """

        s = space(curvature=-1)
        for r, s1, v2, s2, v3 in (
            (
                1.0,
                7.38400687288264534755345768623,
                3.4122762652849023064483572863,
                17.3553873817714370876641814907,
                5.11093270570828897693032500084
                ),
            (
                0.1,
                0.629366251992614535228504721399,
                0.0314421152028826101500700526615,
                0.126083144068540764307450085436,
                0.004197175768278167372264250951
                ),
            (
                10.0,
                69198.1829828835609424193699446,
                69191.9000828325529865724770751,
                1524191407.39366831262439379345,
                762095644.00657373163082028776
                )
            ):
            self.assertTrue(isclose(
                s.sphere_s1(r),
                s1
                ))
            self.assertTrue(isclose(
                s.inv_sphere_s1(s1),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_v2(r),
                v2
                ))
            self.assertTrue(isclose(
                s.inv_sphere_v2(v2),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_s2(r),
                s2
                ))
            self.assertTrue(isclose(
                s.inv_sphere_s2(s2),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_v3(r),
                v3
                ))
            # inv_sphere_v3
            # is not tested
            # this is intentional

    def test_elliptic_known(self):
        """
        Tests known spheres living in the standard elliptic space
        with K = 1.
        """

        s = space(curvature=1)
        for r, s1, v2, s2, v3 in (
            (
                1.0,
                5.28711812816291235777213197934,
                2.88836579751364013754312174055,
                8.89791299620185648000441978084,
                3.42654319113592227685929952373
                ),
            (
                0.1,
                0.627271856640888586303151271167,
                0.0313897553222061208579665325089,
                0.125245385229718577742290413525,
                0.00418042059859385652716262757844
                ),
            (
                1.55,
                6.28182665751126808523746937213,
                6.15252755066186628750014389238,
                12.5609366032633242045384074345,
                9.60830772249653625946806331352
                )
            ):
            self.assertTrue(isclose(
                s.sphere_s1(r),
                s1
                ))
            self.assertTrue(isclose(
                s.inv_sphere_s1(s1),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_v2(r),
                v2
                ))
            self.assertTrue(isclose(
                s.inv_sphere_v2(v2),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_s2(r),
                s2
                ))
            self.assertTrue(isclose(
                s.inv_sphere_s2(s2),
                r
                ))
            self.assertTrue(isclose(
                s.sphere_v3(r),
                v3
                ))
            # inv_sphere_v3
            # is not tested
            # this is intentional

    def test_non_euclidean_scale_curvature(self):
        """
        In non-Euclidean spaces,
        all of the sphere formulas are a monomial in the curvature
        (not the radius, it's the curvature)
        also corresponding to the dimension.
        So of course we should expect that we can scale the curvature
        and the mass scales by the right power.
        """

        magic = 77773.333773777773733
        for kdir in (1, -1):
            for mul in (2, 5, 1/3, 1/11, magic, 1/magic):
                for name, dim in (
                    ('sphere_s1', 1),
                    ('sphere_v2', 2),
                    ('sphere_s2', 2),
                    ('sphere_v3', 3)
                    ):
                    s1 = space(fake_curvature=kdir)
                    s2 = space(fake_curvature=kdir / mul)
                    self.assertTrue(isclose(
                        getattr(s1, name)(1) * mul**dim,
                        getattr(s2, name)(mul)
                        ))
        
    def test_inv_sphere_v3_root_find(self):
        """
        Tests specifically the non-Euclidean inverse 3-sphere volume.
        There is no exact solution in terms of common math functions,
        so a root finding method must be used instead.
        This test measures the accuracy of the root finder when
        applied to this problem.
        """
        import itertools

        for k in (0, -1, 1, 1.75, 0.325, 1/7, -1.75, -0.325, -1/7):
            s = space(fake_curvature=k) 
            for m in itertools.chain(
                range(30),
                range(31,3000,100),
                map((1).__truediv__, range(3, 30, 2)),
                ):
                r = s.inv_sphere_v3(m)
                self.assertTrue(r >= 0)
                v = s.sphere_v3(r)
                self.assertTrue(isclose(
                    m,
                    v
                    ))

class TestPointOperations(unittest.TestCase):
    """
    Collection of tests focusing on operations on space points.
    """
    def _test_parallel_transport(self, k=None):
        """
        Ensures that parallel transport in a space behaves as expected.
        Is a fake test. You have to give it a k.
        """
        import itertools

        if k is None:raise ValueError('This should not get called')

        s = space(curvature=k)

        # require -P + P = 0
        # require P + P = 2P
        # require P + P + P = 3P
        # for all K
        for rp in (
            ((), 1),
            ((1,), 1),
            ((1,), 3),
            ((3/5, 4/5), 1),
            ((-4/5, 3/5), 2),
            ((3/7, 0, -6/7, -2/7), 7),
            ((0, -18/25, 0, 0, 11/25, -12/25, -6/25), 6)
            ):
            p = s.make_point(rp[0], rp[1])
            self.assertTrue(isclose(
                abs(-p + p),
                0,
                abs_tol=p[0]*1e-12
                ))
            p2 = s.make_point(rp[0], rp[1] * 2)
            self.assertTrue(point_isclose(
                p + p,
                p2
                ))
            p3 = s.make_point(rp[0], rp[1] * 3)
            self.assertTrue(point_isclose(
                p + p + p,
                p3
                ))

        # require P + Q = Q + P
        # but only if K = 0
        for p, q in itertools.permutations(
            map(
                (lambda tup:s.make_point(tup, 3)),
                (
                    (15/35, -18/35, -10/35, 24/35),
                    (0, 0, 3/5, 4/5),
                    (4/21, 8/21, 0, 19/21),
                    (4/21, 1/21, -18/21, 10/21)
                    )
                ),
            2
            ):
            self.assertTrue(point_isclose(p + q, q + p) == (k==0))

    def test_euclidean_parallel_transport(self):
        """
        Tests parallel transport's basic properties in Euclidean space.
        """
        
        self._test_parallel_transport(k=0)

    def test_elliptic_parallel_transport(self):
        """
        Tests parallel transport's basic properties in elliptic space.
        """
        
        self._test_parallel_transport(k=1)

    def test_hyperbolic_parallel_transport(self):
        """
        Tests parallel transport's basic properties in hyperbolic space.
        """
        
        self._test_parallel_transport(k=0)

    def test_scaled_parallel_transport(self):
        """
        Tests parallel transport's basic properties in spaces with weird curvature numbers.
        Very negative K, meaning very curvy hyperbolic space,
        tends to cause math to break, because its sin and cos
        (actually sinh and cosh) grow exponentially.
        Thus we only test down to K = -2 here.
        """
        
        for k in (1/11, -1/11, 11, -2):
            self._test_parallel_transport(k=k)
        
    def test_rotation_isometry(self):
        pass # TODO
    def test_polygon_walk(self):
        pass # TODO
    def test_metric(self):
        pass # TODO
    def test_project(self):
        pass # TODO

class TestMPMath(unittest.TestCase):
    """
    Another provided math context runs on the mpmath library.
    This collection of test cases ensures that the math
    does hold up under a different math context.
    It is assumed that all math is known to work correctly already
    under the common math context, so all we test for is whether
    the extra precision is respected.
    Presumably if it works in the mpmath context it will work
    in any math context.
    """
    pass # TODO

# run unittest's main
if __name__ == '__main__':
    unittest.main()
    
