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
from hype import space, space_point, space_point_transform, common_math, to_real, projection_types, mp_namespace

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

    def test_init_edge_cases(self):
        """
        Possible edge cases for the initializer.
        """

        # use K = 1
        s = space(curvature=1)

        # 0-dimensional point is always [1]
        p = s.make_point((), 1)
        self.assertTrue(p[0] == 1)

        # 1-dimensional negative direction
        p = s.make_point((-1,), 1)
        self.assertTrue(p[1] < 0)

        # 1-dimensional negative magnitude
        p = s.make_point((1,), -1)
        self.assertTrue(p[1] < 0)

        # 1-dimensional looping
        p = s.make_point((1,), 2)
        self.assertTrue(p[1] < 0)

        # 1-dimensional zero point
        p = s.make_point((0,), 1)
        self.assertTrue(p[1] == 0)

        # 1-dimensional zero point again but with normalize flag
        p = s.make_point((0,), 1, normalize=True)
        self.assertTrue(p[1] == 0)

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
    def test_pythagorean_triples(self):
        """
        There's no way we could get the Pythagorean theorem wrong, right?
        """

        s = space(0)
        for a, b, c in (
            (3, 4, 5),
            (8, 15, 17),
            (33, 56, 65)
            ):
            self.assertTrue(isclose(
                s.hypot(a, b),
                c
                ))
            self.assertTrue(isclose(
                s.leg(a, c),
                b
                ))

    def test_special_triangles_euclidean(self):
        """
        There's a few very well known triangles.
        Let's test our trig against them.
        """
        import itertools

        s = space(curvature=0)

        # turning constants in radians
        t1_ref = 6.28318530717958647692528676655867
        t2_ref = t1_ref / 2
        t3_ref = t1_ref / 3
        t4_ref = t1_ref / 4
        t6_ref = t1_ref / 6
        t8_ref = t1_ref / 8
        t12_ref = t1_ref / 12
        # sqrt constants
        sqrt2_ref = 1.41421356237309504880168872420977
        sqrt3_ref = 1.73205080756887729352744634150584

        # test with each known triangle
        for a, C, b, A, c, B, m in (
            (1, t6_ref, 1, t6_ref, 1, t6_ref, sqrt3_ref/4), # 1 1 1 (equilateral)
            (1, t4_ref, 1, t8_ref, sqrt2_ref, t8_ref, 1/2), # 1 1 sqrt2 (right isoceles)
            (1, t4_ref, sqrt3_ref, t12_ref, 2, t6_ref, sqrt3_ref/2), # 1 sqrt3 2 (right)
            (1, t3_ref, 1, t12_ref, sqrt3_ref, t12_ref, sqrt3_ref/4), # 1 1 sqrt3 (obtuse isoceles)
            (sqrt2_ref, t8_ref + t6_ref, 2, t12_ref, 1 + sqrt3_ref, t8_ref, (1 + sqrt3_ref)/2) # sqrt2 2 1+sqrt3 (obtuse scalene)
            ):
            # try scaling them up and down too
            for scale in (1, 2, 1/3):
                a *= scale
                b *= scale
                c *= scale
                m *= scale**2
                # go through all vertex permutations
                for (a, A), (b, B), (c, C) in itertools.permutations([(a, A), (b, B), (c, C)], 3):
                    self.assertTrue(isclose(
                        s.cosine_law_side(a, b, C),
                        c
                        ))
                    self.assertTrue(isclose(
                        s.cosine_law_angle(a, b, c),
                        C
                        ))
                    self.assertTrue(isclose(
                        s.dual_cosine_law_angle(A, B, c),
                        C
                        ))
                    # skip dual_cosine_law_side because it is not defined in K = 0
                    self.assertTrue(isclose(
                        s.sine_law_side(a, A, B),
                        b
                        ))
                    self.assertTrue(isclose(
                        s.sine_law_angle(a, A, b),
                        B,
                        rel_tol = 1e-5 # have to go easier on it since asin is really sensitive around 1
                        ) or B > t4_ref and isclose( # SSA triangle solving strangeness
                            s.sine_law_angle(a, A, b),
                            t2_ref - B
                            ))
                    self.assertTrue(isclose(
                        s.triangle_area_from_sides(a, b, c),
                        m
                        ))

    def test_elliptic_special_triangles(self):
        """
        We test some special triangles in the space with K = 1.
        Some of these are not really triangles because at least
        one of the internal angles is a half turn.
        That's okay. We can have those tricks in elliptic spaces.

        As it turns out, setting an internal angle to a half turn can
        break some math, so we have to explicitly prevent testing
        of some cases.
        """
        import itertools

        s = space(curvature=1)

        # turning constants in radians
        t1_ref = 6.28318530717958647692528676655867
        t2_ref = t1_ref / 2
        t3_ref = t1_ref / 3
        t4_ref = t1_ref / 4
        t5_ref = t1_ref / 5
        t6_ref = t1_ref / 6
        # random number
        magic = 7.77733337337373737373
        tm_ref = t1_ref / magic
        nagic = magic - 4 # strangely named other magic constant
        tn_ref = t1_ref / nagic
        # tetrahedron edge central angle
        p4_ref = 1.91063323624901855632771420503144 # = acos(-1/3)
        # icosahedron edge central angle
        p20_ref = 1.10714871779409050301706546017856 # = atan(2)
        # area constant
        sm = space(0).sphere_s2(1)

        # test with each known triangle
        for a, C, b, A, c, B, m in (
            (t3_ref, t2_ref, t3_ref, t2_ref, t3_ref, t2_ref, sm / 2), # literally a hemisphere, which takes up the entire space
            (t2_ref, t4_ref, t4_ref, t2_ref, t4_ref, t4_ref, sm / 4), # diangle which is 1/4 of the sphere
            (t2_ref, tm_ref, t3_ref, t2_ref, t6_ref, tm_ref, sm / magic), # a different diangle
            (t2_ref, tn_ref, t3_ref, t2_ref, t6_ref, tn_ref, sm / nagic), # a different diangle, obtuse angle this time
            (t4_ref, t4_ref, t4_ref, t4_ref, t4_ref, t4_ref, sm / 8), # triangle with 3 right angles
            (t4_ref, tm_ref, t4_ref, t4_ref, tm_ref, t4_ref, sm / magic / 2), # different slice of the previous one, has 2 right angles
            (t4_ref, tn_ref, t4_ref, t4_ref, tn_ref, t4_ref, sm / nagic / 2), # another one but with an obtuse angle
            (p4_ref, t3_ref) * 3 + (sm / 4,), # regular tetrahedron face, projected onto the sphere
            (p20_ref, t5_ref) * 3 + (sm / 20,) # regular icosahedron face, projected onto the sphere
            ):
            # go through all vertex permutations
            for (a, A), (b, B), (c, C) in itertools.permutations([(a, A), (b, B), (c, C)], 3):
                self.assertTrue(isclose(
                    s.cosine_law_side(a, b, C),
                    c
                    ))
                self.assertTrue(t2_ref in (A, B) or isclose(
                    s.cosine_law_angle(a, b, c),
                    C,
                    rel_tol = 1e-5
                    ))
                self.assertTrue(isclose(
                    s.dual_cosine_law_angle(A, B, c),
                    C,
                    rel_tol = 1e-5
                    ))
                self.assertTrue(t2_ref in (A, B) or isclose(
                    s.dual_cosine_law_side(A, B, C),
                    c
                    ))
                self.assertTrue(A == t2_ref or isclose(
                    s.sine_law_side(a, A, B),
                    b,
                    rel_tol = 1e-5,
                    abs_tol = 1e-15
                    ) or isclose(
                    s.sine_law_side(a, A, B),
                    t2_ref - b,
                    rel_tol = 1e-5,
                    abs_tol = 1e-15
                    ))
                self.assertTrue(A == t2_ref or isclose(
                    s.sine_law_angle(a, A, b),
                    B,
                    rel_tol = 1e-5,
                    abs_tol = 1e-15
                    ) or B > t4_ref and isclose( # SSA triangle solving strangeness
                    s.sine_law_angle(a, A, b),
                    t2_ref - B,
                    rel_tol = 1e-5,
                    abs_tol = 1e-15
                    ))
                self.assertTrue((A, B, C).count(t2_ref) == 1 or isclose(
                    s.triangle_area_from_sides(a, b, c),
                    m,
                    rel_tol = 1e-5
                    ))
                self.assertTrue(isclose(
                    s.triangle_area_from_angles(A, B, C),
                    m
                    ))

    def test_hyperbolic_tiles(self):
        """
        There aren't really "special triangles" in hyperbolic space
        known to us Euclidean dwellers.
        So instead, we test some known hyperbolic tilings.
        We will generate them all on the fly.
        """
        import itertools

        s = space(curvature=-1)

        # turning constants in radians
        t1_ref = 6.28318530717958647692528676655867
        t2_ref = t1_ref / 2
        t4_ref = t1_ref / 4

        def make_triangle(f, v):
            f = t1_ref / f
            v = t1_ref / v / 2
            a = (common_math.cos(f) + 1)/common_math.sin(v)**2 - 1
            a = common_math.sqrt(a**2 - 1)
            b = a / common_math.sin(f) * common_math.sin(v)
            a = common_math.asinh(a)
            b = common_math.asinh(b)
            return a, v, b, f, b, v

        for p, q in itertools.product(*[range(3,11)]*2):
            # skip ones that don't result in hyperbolic tilings
            if p * q < 20:continue

            a, C, b, A, c, B = make_triangle(p, q)

            # try all vertex permutations
            for (a, A), (b, B), (c, C) in itertools.permutations([(a, A), (b, B), (c, C)], 3):
                self.assertTrue(isclose(
                    s.cosine_law_side(a, b, C),
                    c
                    ))
                self.assertTrue(isclose(
                    s.cosine_law_angle(a, b, c),
                    C
                    ))
                self.assertTrue(isclose(
                    s.dual_cosine_law_angle(A, B, c),
                    C
                    ))
                self.assertTrue(isclose(
                    s.dual_cosine_law_side(A, B, C),
                    c
                    ))
                self.assertTrue(isclose(
                    s.sine_law_side(a, A, B),
                    b
                    ))
                self.assertTrue(isclose(
                    s.sine_law_angle(a, A, b),
                    B,
                    rel_tol = 1e-5 # have to go easier on it since asin is really sensitive around 1
                    ) or B > t4_ref and isclose( # SSA triangle solving strangeness
                        s.sine_law_angle(a, A, b),
                        t2_ref - B
                        ))
                self.assertTrue(isclose(
                    s.triangle_area_from_sides(a, b, c),
                    s.triangle_area_from_angles(A, B, C)
                    ))

    def test_scaling(self):
        """
        Assuming that K = -1 and K = 1 are already tested to work,
        let's test to make sure that triangles scale up and down correctly.
        """
        import itertools

        # turning constants in radians
        t1_ref = 6.28318530717958647692528676655867
        t2_ref = t1_ref / 2
        t4_ref = t1_ref / 4

        # test positive and negative curvatures
        for bk in (1, -1):
            # different scaling factors
            for r in (1, 4/5, 5/4, 3/4, 4/3, 2/3, 3/2, 1/2, 2):
                # make the regular spaces
                s1 = space(curvature=bk)
                sr = space(curvature=bk/r**2)
                # try some triangles
                for a1, b1, c1 in (
                    (1, 1, 1),
                    (5/4, 1, 3/4),
                    (5/6, 4/5, 3/4),
                    (3/5, 1/2, 2/5),
                    (1/5, 1/6, 1/7),
                    (1/13, 1/17, 1/19)
                    ):
                    # calculate scaled side lengths
                    ar, br, cr = a1 * r, b1 * r, c1 * r
                    # calculate angles
                    A = s1.cosine_law_angle(b1, c1, a1)
                    B = s1.cosine_law_angle(c1, a1, b1)
                    C = s1.cosine_law_angle(a1, b1, c1)
                    # calculate mass
                    m1 = s1.triangle_area_from_angles(A, B, C)
                    mr = m1 * r**2
                    # try all vertex permutations
                    for (a1, ar, A), (b1, br, B), (c1, cr, C) in itertools.permutations([(a1, ar, A), (b1, br, B), (c1, cr, C)], 3):
                        # do scaling tests
                        self.assertTrue(isclose(
                            sr.cosine_law_side(ar, br, C),
                            cr
                            ))
                        self.assertTrue(isclose(
                            sr.cosine_law_angle(ar, br, cr),
                            C
                            ))
                        self.assertTrue(isclose(
                            sr.dual_cosine_law_angle(A, B, cr),
                            C
                            ))
                        self.assertTrue(isclose(
                            sr.dual_cosine_law_side(A, B, C),
                            cr
                            ))
                        self.assertTrue(isclose(
                            sr.sine_law_side(ar, A, B),
                            br
                            ))
                        self.assertTrue(isclose(
                            sr.sine_law_angle(ar, A, br),
                            B,
                            rel_tol = 1e-5 # have to go easier on it since asin is really sensitive around 1
                            ) or B > t4_ref and isclose( # SSA triangle solving strangeness
                                sr.sine_law_angle(ar, A, br),
                                t2_ref - B
                                ))
                        self.assertTrue(isclose(
                            sr.triangle_area_from_sides(ar, br, cr),
                            mr
                            ))
                        self.assertTrue(isclose(
                            sr.triangle_area_from_angles(A, B, C),
                            mr
                            ))

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
            ((3/7, 0, -6/7, -2/7), 3),
            ((0, -18/25, 0, 0, 11/25, -12/25, -6/25), 3)
            ):
            p = s.make_point(rp[0], rp[1])
            self.assertTrue(isclose(
                abs(-p + p),
                0,
                abs_tol=1e-12
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

    def test_scalar_multiples(self):
        """
        Tests scalar multiplication for points in space.
        """

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 11, -3):
            
            s = space(curvature=k)

            # use a small enough magnitude to not break math for very negative K
            magic = 0.33377777373737737777
            phi_ref = 1.61803398874989484820458683436559
            for rp in (
                (),
                (1,),
                (4/5, -3/5),
                (0, 2/11, -6/11, 9/11),
                ):
                p = s.make_point(rp, magic)

                # ensure: (0) p = 0
                self.assertTrue(point_isclose(
                    p * 0,
                    s.make_origin(len(p)-1)
                    ))

                # ensure: (-1) p = -p
                self.assertTrue(point_isclose(
                    p * -1,
                    -p
                    ))

                # ensure: (2) p = 2p = p + p
                p2 = p + p
                self.assertTrue(point_isclose(
                    p * 2,
                    p2
                    ))

                # ensure: (4) p = (2) (2p)
                p4 = p2 + p2
                self.assertTrue(point_isclose(
                    p * 4,
                    p2 * 2
                    ))

                # ensure: (5) p = 5p = 2(2p) + p
                p5 = p4 + p
                self.assertTrue(point_isclose(
                    p * 5,
                    p5
                    ))
                
                # don't do non-integer tests for K > 0 because looping strangeness
                if k <= 0:
                    # ensure: (phi) (phi p) = (phi) p + p
                    pphi = p * phi_ref
                    self.assertTrue(point_isclose(
                        pphi * phi_ref,
                        pphi + p
                        ))

    def test_transform_compose(self):
        """
        Tests the concatenation/composition of transformations.
        In short, the expected identity is
        (f g) x = f (g x)
        """

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 11, -2):
            
            s = space(curvature=k)

            # use a small enough magnitude to not break math for very negative K
            magic = 0.33377777373737737777

            p = s.make_point((2/11, 6/11, 9/11), magic)
            q = s.make_point((3/7, 6/7, 2/7), magic)
            r = s.make_point((9/17, 8/17, 12/17), magic)

            f, g, h = map(space_point_transform, (p, q, r))

            # check the core principle: (f g) x = f (g x)
            self.assertTrue(point_isclose(
                (f(g))(r),
                f(g(r))
                ))

            # just for good measure, let's do it again with different vars
            self.assertTrue(point_isclose(
                (g(h))(p),
                g(h(p))
                ))

            def check_transform_eq(t1, t2, invert=False):
                for ref in (p, q, r):
                    self.assertTrue(invert ^ point_isclose(
                        t1(ref),
                        t2(ref)
                        ))

            # api says f(g) == f + g
            # this is just a convenience to let you write things with a sum instead of a product
            check_transform_eq(f(g), f + g)

            # non-commutative property
            check_transform_eq(f+g, g+f, invert=(k!=0))

            # associative property
            check_transform_eq(f+g+h, f+(g+h))

            # self commutative property
            f2 = f+f
            check_transform_eq(f2+f, f+f2)
            check_transform_eq(f2+f2, f+f2+f)

    def test_transform_multiples(self):
        """
        Test iterated, inverse, and fractional transforms.
        """
        
        t1_ref = 6.28318530717958647692528676655867
        t4_ref = t1_ref / 4

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 11, -2):

            s = space(curvature=k)

            # use a small enough magnitude to not break math for very negative K
            magic = 0.33377777373737737777

            o = s.make_origin(3)
            p = s.make_point((2/11, 6/11, 9/11), magic)
            q = s.make_point((3/7, 6/7, 2/7), magic)

            f, g, i = map(space_point_transform, (p, q, o))

            def check_transform_eq(t1, t2, invert=False, skip=None):
                if skip:return
                for ref in (
                    s.make_point((9/17, 8/17, 12/17), magic),
                    s.make_point((0, 3/5, 4/5), magic)
                    ):
                    self.assertTrue(invert ^ point_isclose(
                        t1(ref),
                        t2(ref)
                        ))

            def skip_test(n):
                """
                Should we skip this case?
                """
                return k > 0 and magic * n * k**0.5 >= t4_ref

            # check f^0 = I
            check_transform_eq(f * 0, i)
            check_transform_eq(g * 0, i)
            check_transform_eq(i * 0, i)

            # check f^1 = f
            check_transform_eq(f * 1, f)
            check_transform_eq(g * 1, g)
            check_transform_eq(i * 1, i)

            # check f^-1 is correct inverse of f
            check_transform_eq(f * -1,
                               space_point_transform(p * -1))
            check_transform_eq(g * -1,
                               space_point_transform(q * -1))

            # check f^n is correct iterated f
            check_transform_eq(f * 3,
                               space_point_transform(p * 3),
                               skip = skip_test(3))
            check_transform_eq(g * 5,
                               space_point_transform(q * 5),
                               skip = skip_test(5))
            check_transform_eq(f * 19,
                               space_point_transform(p * 19),
                               skip = skip_test(19))
            check_transform_eq(g * 21,
                               space_point_transform(q * 21),
                               skip = skip_test(21))

            # check f^(1/n) f is correct fractional f
            hf = f * 0.5
            check_transform_eq(hf + hf, f)
            hg = g * 0.25
            check_transform_eq(hg * 4, g)
        
    def test_rotation_isometry(self):
        """
        Test that some simple rotation isometries behave as expected.
        """
        import numpy

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 11, -2):
            
            s = space(curvature=k)

            # use a small enough magnitude to not break math for very negative K
            magic = 0.33377777373737737777
            # 1/sqrt(2)
            s2_ref = 0.707106781186547524400844362104785

            o = s.make_origin(2)
            p = s.make_point((1, 0), magic)
            q = s.make_point((s2_ref, s2_ref), magic)

            rot = space_point_transform(
                numpy.array([[1,0,0],[0,s2_ref,-s2_ref],[0,s2_ref,s2_ref]]),
                curvature=k,
                math = common_math
                )

            f, g, i = map(space_point_transform, (p, q, o))

            def check_transform_eq(t1, t2, invert=False):
                for ref in (
                    s.make_point((5/13, 12/13), magic),
                    s.make_point((-3/5, 4/5), magic)
                    ):
                    self.assertTrue(invert ^ point_isclose(
                        t1(ref),
                        t2(ref),
                        abs_tol = 1e-12
                        ))

            # 1/8 turn, times 8
            check_transform_eq(rot*8, i)

            # rotate, shift, rotate
            check_transform_eq(g, rot + f + rot * -1)

            # the other way
            check_transform_eq(f, rot * -1 + g + rot)
            
    def test_polygon_walk(self):
        """
        Attempt to traverse the hyperbolic plane by following
        the edges of a regular tiling.
        """
        import numpy

        s = space(curvature=-1)

        # turning constants in radians
        t1_ref = 6.28318530717958647692528676655867
        t2_ref = t1_ref / 2
        t3_ref = t1_ref / 3
        t4_ref = t1_ref / 4

        def make_triangle(f, v):
            f = t1_ref / f
            v = t1_ref / v / 2
            a = (common_math.cos(f) + 1)/common_math.sin(v)**2 - 1
            a = common_math.sqrt(a**2 - 1)
            b = a / common_math.sin(f) * common_math.sin(v)
            a = common_math.asinh(a)
            b = common_math.asinh(b)
            return a, v, b, f, b, v

        # use {7, 3} tiling

        edge, angle, *_ = make_triangle(7, 3)

        def check_walk_eq(t1, t2, invert=False):
            for ref in (
                s.make_origin(2),
                s.make_point((3/5, 4/5), 1/3)
                ):
                self.assertTrue(invert ^ point_isclose(
                    t1(ref),
                    t2(ref),
                    abs_tol = 1e-12
                    ))

        t1 = t2 = space_point_transform(s.make_origin(2))

        def rotater(angle):
            return space_point_transform(
                numpy.array([
                    [1, 0, 0],
                    [0, numpy.cos(angle), -numpy.sin(angle)],
                    [0, numpy.sin(angle), numpy.cos(angle)]
                    ]),
                curvature = -1,
                math = common_math
                )

        spin_half = rotater(t2_ref)
        spin_left = rotater(angle)
        spin_right = rotater(-angle)
        forward = space_point_transform(s.make_point((1, 0), edge))

        # do some walking in a circle to sanity test

        t1 = forward + spin_half + spin_left + spin_half + spin_right + t1
        t2 = forward + t2

        check_walk_eq(t1, t2)

        # spin around some more

        t1 = forward + spin_left * 6 + spin_half + t1
        t2 = forward + spin_half + t2

        check_walk_eq(t1, t2)

        # walk in a loop
        t1 = (forward + spin_left) * 7 + t1

        check_walk_eq(t1, t2)

        # walk another way in a loop
        t1 = (spin_right + forward) * 7 + t1

        check_walk_eq(t1, t2)

        # walk in a more complicated path

        t2 = ((spin_right + forward) * 5 + spin_left + forward) * 2 + t2

        check_walk_eq(t1, t2)

        # a bigger loop

        t2 = (spin_left + forward + (spin_right + forward) * 3) * 7 + t2

        check_walk_eq(t1, t2)

        # a bigger loop, but in the correct direction

        t2 = t2 + ((forward + spin_right) * 3 + forward + spin_left) * 7

        check_walk_eq(t1, t2)
        
    def test_dot_product(self):
        """
        Test that the dot product behaves as expected,
        first using the properties of the dot product,
        then using test vectors.
        """
        import itertools

        # our little magic constant
        magic = 0.33377777373737737777

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 1 + magic, -1 - magic):
            
            s = space(curvature=k)

            # special points
            o = s.make_origin(3)

            # property: P * P = 0 iff P is the origin
            self.assertTrue(o * o == 0)
            for direction in (
                (1, 0, 0),
                (3/5, 0, 4/5),
                (3/7, 6/7, 2/7),
                (2/11, 6/11, 9/11)
                ):
                for magnitude in (1, 0.01, magic, magic**7):
                    p = s.make_point(direction, magnitude)
                    self.assertTrue(p * p > 0)

            for p, q in itertools.permutations((
                (1, 0, 0),
                (3/5, 0, 4/5),
                (3/7, 6/7, 2/7),
                (2/11, 6/11, 9/11)
                ), 2):
                p = s.make_point(p, magic)
                q = s.make_point(q, magic)
                # property: P * Q == Q * P
                self.assertTrue(isclose(
                    p * q,
                    q * p
                    ))
                # property: bilinear
                # we will only test with colinear points because curved space stuff
                for t in (1, 2, -1, 0, magic, -magic, 1 + magic, magic ** 7):
                    self.assertTrue(isclose(
                        (p * t) * q,
                        p * q * t
                        ))
                    self.assertTrue(isclose(
                        (p * t + p) * q,
                        p * q * (1 + t),
                        abs_tol = 1e-12
                        ))

            # some test vectors
            
            for direction in (
                (1, 0, 0),
                (3/5, 0, 4/5),
                (3/7, 6/7, 2/7),
                (2/11, 6/11, 9/11)
                ):
                p = s.make_point(direction, magic)
                self.assertTrue(isclose(p * p, magic ** 2))

            p = s.make_point((1, 0), magic)
            q = s.make_point((0, 1), magic)
            self.assertTrue(isclose(p * q, 0))

            p = s.make_point((1, 1), magic, normalize=True)
            q = s.make_point((1, -1), magic, normalize=True)
            self.assertTrue(isclose(p * q, 0))

            p = s.make_point((2, 1), 5**0.5 * magic, normalize=True)
            q = s.make_point((3, -1), 10**0.5 * magic, normalize=True)
            self.assertTrue(isclose(p * q, 5 * magic**2))
        
    def test_project(self):
        """
        Test the projections to see that they have the expected properties.
        """
        import itertools
        from numpy import array, dot
        from numpy.linalg import det

        # our little magic constant
        magic = 0.33377777373737737777

        # test for all kinds of curvatures K
        for k in (0, 1, -1, 1/11, -1/11, 1 + magic, -1 - magic):
            
            s = space(curvature=k)

            # test line preserving projection
            # 3 points are colinear when
            # | x1 y1 1 |
            # | x2 y2 1 | = 0
            # | x3 y3 1 |
            # let's test this!

            for p, q in itertools.permutations((
                (1, 0),
                (3/5, 4/5),
                (-5/13, 12/13),
                (-8/17, -15/17),
                ), 2):
                p = s.make_point(p, magic)
                q = s.make_point(q, magic)
                u = p.project(projection_types.preserve_lines)
                v = (p+q).project(projection_types.preserve_lines)
                w = (p+(-magic)*q).project(projection_types.preserve_lines)
                d = det([[*u, 1],[*v, 1],[*w, 1]])
                self.assertTrue(abs(d) < 1e-9)

            # test angle preserving projection
            # map will be conformal, so we do like a secant test

            delta = 1e-9
            vi = s.make_point((1, 0, 0), delta)
            vj = s.make_point((0, 1, 0), delta)
            vk = s.make_point((0, 0, 1), delta)
            for p in (
                (1, 0, 0),
                (0, 3/5, 4/5),
                (-5/13, 12/13, 0),
                (2/11, 6/11, 9/11),
                (3/7, 6/7, 2/7)
                ):
                p = s.make_point(p, magic)
                pp = p.project(projection_types.preserve_angles)
                pi, pj, pk = (array((p+v).project(projection_types.preserve_angles)) - pp for v in (vi, vj, vk))
                # should stay orthogonal and same size
                # note that we're doing a secant thing so it's only approximate
                # thus we set a relatively high tolerance
                self.assertTrue(isclose(
                    dot(pi, pi),
                    dot(pj, pj),
                    rel_tol = 1e-6
                    ))
                self.assertTrue(isclose(
                    dot(pi, pi),
                    dot(pk, pk),
                    rel_tol = 1e-6
                    ))
                self.assertTrue(isclose(
                    dot(pi, pj),
                    0,
                    abs_tol = 1e-6
                    ))
                self.assertTrue(isclose(
                    dot(pi, pk),
                    0,
                    abs_tol = 1e-6
                    ))
                self.assertTrue(isclose(
                    dot(pj, pk),
                    0,
                    abs_tol = 1e-6
                    ))

class TestµMPMath(unittest.TestCase):
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
    def test_hyper_3_7(self):
        """
        Examine the order-7 triangular tiling, which lives in
        the hyperbolic plane and has Schlafi symbol {3,7}.
        Start at any vertex.
        How many vertices are at minimum distance n from that vertex?
        The sequence goes like this:
        1, 7, 21, ...
        for n >= 2, S[n] =3 S[n-1] - S[n-2]
        This sequence is given in HyperRogue.
        Why do we care? Well, think about it, what happens when we try
        to actually walk out all these points in our model of hyperbolic space?
        The sequence grows exponentially, and the represented points
        also use exponentially larger values.
        Floats lose precision compared to this exponential growth,
        and eventually, the whole thing collapses.
        Multiple precision floats let you keep going for a lot longer.

        This test is forced to be one of the last tests because it takes an extremely long time.

        HyperRogue: Playing with Hyperbolic Geometry
          Kopczyński, Celińska, and Čtrnáct, 2017
          http://archive.bridgesmathart.org/2017/bridges2017-9.pdf
          (no DOI)
        """
        import numpy
        import logging
        
        # calculate the first some number of terms of the sequence
        S = [1, 7, 21]
        while len(S) < 40:
            S.append(S[-1]*3 - S[-2])
        # make it cumulative
        S = numpy.cumsum(S)

        normal_ns = common_math
        mp_ns = mp_namespace(dps=17, _nonce=[])

        def fails_at(ns, stop_at=None):
            """
            Given a certain math namespace,
            when does it fail?
            """

            s = space(curvature=-1, math=ns)

            # turning constants in radians
            t1_ref = ns.tau

            def make_triangle(f, v):
                f = t1_ref / f
                v = t1_ref / v / 2
                a = (ns.cos(f) + 1)/ns.sin(v)**2 - 1
                a = ns.sqrt(a**2 - 1)
                b = a / ns.sin(f) * ns.sin(v)
                a = ns.asinh(a)
                b = ns.asinh(b)
                return a, v, b, f, b, v

            # use {3, 7} tiling

            edge, angle, *_ = make_triangle(3, 7)
            angle *= 2

            def rotater(angle):
                return space_point_transform(
                    ns.matrix([
                        [1, 0, 0],
                        [0, ns.cos(angle), -ns.sin(angle)],
                        [0, ns.sin(angle), ns.cos(angle)]
                        ]),
                    curvature = -1,
                    math = ns
                    )

            spin_half = rotater(t1_ref/2)
            spin_left = rotater(angle)
            forward = space_point_transform(s.make_point((1, 0), edge))
            origin = s.make_origin(2)

            def r_soft_hash(x):
                """
                Generates a hashable value that mushes together very close reals.
                """
                if abs(x) < 1e-9:return 0
                # round it to some number of bits
                b = ns.round(ns.log(abs(x)) / ns.log(2))
                gran = 2**(b-30)
                return ns.round(x / gran) * gran

            def soft_hash(p):
                """
                Generates a hashable value that mushes together very close points.
                """
                return tuple(map(r_soft_hash, p))

            active = [space_point_transform(origin)]
            seen = {soft_hash(active[0](origin))}

            logging.log(logging.INFO, f'3-7 tiling sequence test with math as {ns}')
            for i, si in enumerate(S):
                old_active = active
                active = []
                logging.log(logging.INFO, f'Iteration {i}, sequence expecting {si}, got {len(seen)}')
                if len(seen) != si or stop_at is not None and i >= stop_at:
                    return i
                for t in old_active:
                    t = t + spin_half
                    for _ in range(7):
                        t = t + spin_left
                        tfw = t + forward
                        sh = soft_hash(tfw(origin))
                        if sh not in seen:
                            seen.add(sh)
                            active.append(tfw)

        self.assertTrue(fails_at(normal_ns, stop_at=8) == 8)
        
        self.assertTrue(fails_at(mp_ns, stop_at=8) == 8)

        fail_normal = fails_at(normal_ns)

        self.assertTrue(fail_normal > 10)
        
        fail_mp = fails_at(mp_ns, stop_at=fail_normal+1)
        
        self.assertTrue(fail_normal < fail_mp)

# run unittest's main
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()
    
