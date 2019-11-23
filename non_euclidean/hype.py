#!/usr/bin/env python3

"""
Small library for geometry in Euclidean, elliptic, and hyperbolic spaces.
Does point arithmetic, trigonometric functions, and common geometric equations.
Supports using different math contexts.

This library has not been thoroughly tested to work correctly for all curvatures.
If you find a math error, do report it!
"""

import math
import functools
import operator
import enum

def _require_hash(value):
    """
    Utility function that tries to take the hash value of the value normally,
    otherwise, returns its object ID.
    Basically a way to force a value to produce some kind of hash,
    with less worry as to whether that hash reflects its true equality.
    Indeed, not every class that defines equality also defines hashing.
    """
    try:
        return hash(value)
    except TypeError:
        return id(value)

class joined_namespace(object):
    """
    Represents a namespace which may be the result of multiple other namespaces joined.
    Can be used to create a fake library containing objects from multiple others.
    Assumes the __dict__ attribute is accessible.
    """
    def __init__(self, *inherits):
        """
        Construct from other objects or namespace dicts.
        """
        self.join(*inherits)
    def join(self, *inherits):
        """
        Append more objects or namespace dicts.
        Will overwrite existing data in a conflict.
        """
        for parent in inherits:
            if isinstance(parent, dict):
                self.__dict__.update(parent)
            else:
                self.__dict__.update(parent.__dict__)
        

def extend_math_namespace(*inherits):
    """
    Construct a math library like namespace.
    Automatically fills in the following if they are not in the namespace already:
    - tau = 2 pi
    - pi = tau / 2
    - e = exp(1)
    - exp = x -> e^x
    - sqrt = x -> x^(1/2)
    - hypot = (x,y) -> sqrt(x^2 + y^2)
    - asinh = x -> log(x + sqrt(x^2 + 1))
    - acosh = x -> log(x + sqrt(x^2 - 1))
    """
    ns = joined_namespace(*inherits)
    if not hasattr(ns, 'tau'):
        ns.tau = ns.pi * ns.real(2)
    if not hasattr(ns, 'pi'):
        ns.pi = ns.tau / ns.real(2)
    if not hasattr(ns, 'e'):
        ns.e = ns.exp(ns.real(1))
    if not hasattr(ns, 'exp'):
        ns.exp = functools.partial(operator.pow, ns.e)
    if not hasattr(ns, 'sqrt'):
        def _sqrt(ns):
            def i_sqrt(x, y):
                """
                patched math function
                see docs for math.sqrt
                """
                return x ** (ns.real(1) / ns.real(2))
            return i_sqrt
        ns.hypot = _sqrt(ns)
    if not hasattr(ns, 'hypot'):
        def _hypot(ns):
            def i_hypot(x, y):
                """
                patched math function
                see docs for math.hypot
                """
                return ns.sqrt(x*x + y*y)
            return i_hypot
        ns.hypot = _hypot(ns)
    if not hasattr(ns, 'asinh'):
        def _asinh(ns):
            def i_asinh(x):
                """
                patched math function
                see docs for math.asinh
                """
                return ns.log(x + ns.hypot(x, ns.real(1)))
            return i_asinh
        ns.asinh = _asinh(ns)
    if not hasattr(ns, 'acosh'):
        def _acosh(ns):
            def i_acosh(x):
                """
                patched math function
                see docs for math.acosh
                """
                return ns.log(x + ns.sqrt(x*x - ns.real(1)))
            return i_acosh
        ns.asinh = _acosh(ns)

common_math = extend_math_namespace(math, {'real': float})

def mp_namespace(_nonce=[]):
    """
    Returns a namespace using mpmath's multiple precision real numbers
    instead of the built-in floats.
    Will return an identical object in future calls.
    Warning: imports mpmath. You will need mpmath.
    """
    if _nonce:
        return _nonce[0]
    from mpmath import mp
    result = extend_math_namespace(mp, {'real': mp.mpf})
    _nonce.append(result)
    return result

def to_real(real, x):
    """
    Helper function to convert a value x to a type real.
    This exists because not every type has a direct conversion,
    but maybe we can help it?
    """
    try:
        # the obvious way
        return real(x)
    except TypeError as exc:
        # well seems like that won't work
        # let's see what types we can help it with
        if hasattr(x, 'denominator'):
            # ah, it's a fraction!
            return to_real(real, x.numerator) / to_real(real, x.denominator)
        # welp, we failed
        raise exc

class abc_space(object):
    """
    Abstract base classes for spaces of constant curvature.
    
    Warning: sometimes Euclidean space will actually appear to be the strangest.
    This is because the case K = 0 is sometimes degenerate, and to get a useful result,
    we need to instead take the limit  with K --> 0.
    Due to how geometry works, this limit will result in the same value from below
    (zooming in on hyperbolic space) and from above (zooming in on elliptic space).
    Just be aware that sometimes there's a hidden limit.

    Also, some formulas which you may expect to be similar,
    look quite different in the different spaces.
    This is because they are based on an integral, which simplifies differently
    for K < 0, K = 0, and K > 0.
    """
    def __eq__(self, other):
        if self is other:return True
        if not hasattr(other, 'math') or not hasattr(other, 'curvature'):return False
        return self.math == other.math and self.curvature == other.curvature
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        return hash((abc_space, _require_hash(self.math), self.curvature))
    def cos(self, x):
        """
        The cosine function.

        Satisfies:
        cos(0) = 1
        d/dx cos(x) = -K sin(x)
        """
        raise NotImplementedError
    def sin(self, x):
        """
        The sine function.
        
        Satisfies:
        sin(0) = 0
        d/dx sin(x) = cos(x)
        """
        raise NotImplementedError
    def acos(self, x):
        """
        The inverse cosine function.
        """
        raise NotImplementedError
    def asin(self, x):
        """
        The inverse sine function.
        """
        raise NotImplementedError
    def make_origin(self, dimensions):
        """
        Make the origin point for N dimensions.
        """
        if dimensions < 0:
            raise ValueError('Cannot have negative dimensional space')
        math = self.math
        real = math.real
        return space_point(
            self,
            (to_real(real, 1),) + (to_real(real, 0),) * dimensions
            )
    def make_point(self, direction, magnitude, normalize=False):
        """
        Take a regular N-dimensional direction unit vector
        and a magnitude scalar, and produces
        the point that far away from the origin in that direction
        but in this space.
        Call with normalize if you are not sure
        if the direction vector is a unit vector.
        """
        math = self.math
        real = math.real
        preal = functools.partial(to_real, real)
        if normalize:
            direction = tuple(map(preal, direction))
            divide_by = functools.reduce(math.hypot, direction)
            direction = tuple(map((lambda x: x / divide_by), direction))
        magnitude = to_real(real, magnitude)
        def map_with(x):
            return math.sin(preal(x) * magnitude)
        return space_point(
            self,
            (math.cos(magnitude),) + tuple(map(map_with, direction))
            )
    def magnitude_of(self, point, use_quick=False):
        """
        Return the magnitude of a point in this space, or rather,
        its distance to the origin.

        Based on the point identity:
        x0^2 = 1 - K ( x1^2 + ... + xk^2 )
        and the knowledge that the point
        (cos(t), sin(t), 0, 0, ..., 0)
        represents a point t away from the origin along the first axis,
        we can actually calculate t in 2 different ways:
        with x0 and the inverse cosine ("quick"),
        and with x1...xk and the inverse sine ("not quick").
        The not quick one will take O(N) steps for N dimensions.
        Also, the quick one does not work for K = 0.
        
        Does not check for whether that point object actually belongs to this space.
        """
        math = self.math
        if use_quick:
            return math.acos(point[0])
        return math.asin(functools.reduce(math.hypot, point[1:]))
    def parallel_transport(self, dest, ref):
        """
        What point do we get when parallel transporting
        ref from the origin to dest?
        For K = 0, this is just vector addition, and the order does not matter.
        For other K, however, this operation is in general not commutative.
        """
        # TODO implement parallel transport!
        # I know a cheesy way to do it for dimension N <= 2
        # but I want to have it implemented more generally
        # and I heard it's harder for N >= 3
        # that won't stop me from finding out how!
        raise NotImplementedError
    def hypot(self, x, y):
        """
        If x and y are lengths of the legs of a right triangle,
        what is the length of the hypotenuse?
        Solution z to cos(x) cos(y) = cos(z)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        y = to_real(real, y)
        return self._hypot(x, y)
    def _hypot(self, x, y):
        """
        hypot(x, y)
        assuming correct types
        """
        return self.acos(self.cos(x) * self.cos(y))
    def leg(self, x, z):
        """
        If x is a leg of a right triangle and z is the length of
        the hypotenuse, what is the length of the other leg?
        Solution y to cos(x) cos(y) = cos(z)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        z = to_real(real, z)
        return self._leg(x, z)
    def _leg(self, x, z):
        """
        leg(x, z)
        assuming correct types
        """
        return self.acos(self.cos(z) / self.cos(x))
    def sphere_s1(self, r):
        """
        Mass of the 1D boundary of the 2-sphere.
        Commonly called the circumference of a circle.

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return self.sin(r) * math.tau
    def inv_sphere_s1(self, m):
        """
        Inverts sphere_s1
        """
        math = self.math
        real = math.real
        m = to_real(real, m)
        return self.asin(m / math.tau)
    def sphere_v2(self, r):
        """
        Mass of the 2D interior of the 2-sphere.
        Commonly called the area of a circle.

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return self.sin(r / real(2))**2 * math.tau * real(2)
    def inv_sphere_v2(self, m):
        """
        Inverts sphere_v2
        """
        math = self.math
        real = math.real
        m = to_real(real, m)
        return self.asin(math.sqrt(m / (math.tau * real(2)))) * real(2)
    def sphere_s2(self, r):
        """
        Mass of the 2D boundary of the 3-sphere.
        Commonly called the surface area of a sphere.

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return self.sin(r)**2 * math.tau * 2
    def inv_sphere_s2(self, m):
        """
        Inverts sphere_s2
        """
        math = self.math
        real = math.real
        m = to_real(real, m)
        return self.asin(math.sqrt(m / (math.tau * real(2))))
    def sphere_v3(self, r):
        """
        Mass of the 3D interior of the 3-sphere.
        Commonly called the volume of a sphere

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.

        Note:
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return math.tau / to_real(real, self.curvature) * (r - self.sin(r * real(2)) / real(2))
    def inv_sphere_v3(self, m):
        """
        Inverts sphere_v3
        Note: this is difficult in general, because it can't be
        expressed in terms of common functions
        """
        raise NotImplementedError
    def circle_circumference(self, r):
        """
        Alias for sphere_s1
        """
        return self.sphere_s1(r)
    def circle_area(self, r):
        """
        Alias for sphere_v2
        """
        return self.sphere_v2(r)
    def sphere_surface_area(self, r):
        """
        Alias for sphere_s2
        """
        return self.sphere_s2(r)
    def sphere_volume(self, r):
        """
        Alias for sphere_v3
        """
        return self.sphere_v3(r)
    def cosine_law_side(self, a, b, C):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The cosine law relates a, b, c, and C:

        cos(c) = cos(a) cos(b) + K sin(a) sin(b) cos*(C)
        * not the spatial trig function, always the regular trig function
        (formula not verified)
        The equation degenerates at K=0 and needs to be taken at the limit.

        This specific method takes a, b, C and computes c.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        b = to_real(real, b)
        C = to_real(real, C)
        return self.acos(
            self.cos(a) * self.cos(b) +
            self.sin(a) * self.sin(b) * math.cos(C) * self.curvature
            )
    def cosine_law_angle(self, a, b, C):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The cosine law relates a, b, c, and C:

        cos(c) = cos(a) cos(b) + K sin(a) sin(b) cos*(C)
        * not the spatial trig function, always the regular trig function
        (formula not verified)
        The equation degenerates at K=0 and needs to be taken at the limit.

        This specific method takes a, b, c and computes C.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        b = to_real(real, b)
        c = to_real(real, c)
        return math.acos(
            (self.cos(c) - self.cos(a) * self.cos(b)) /
            (self.sin(a) * self.sin(b) * self.curvature)
            )
    def dual_cosine_law_angle(self, A, B, c):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The dual cosine law (not the original cosine law)
        relates A, B, C, and c:

        cos*(C) = - cos*(A) cos*(B) + sin*(A) sin*(B) cos(c)
        * not the spatial trig function, always the regular trig function

        This specific method takes A, B, c and computes C.
        """
        math = self.math
        real = math.real
        A = to_real(real, A)
        B = to_real(real, B)
        c = to_real(real, c)
        return math.acos(
            -math.cos(A)*math.cos(B) +
            math.sin(A)*math.sin(B)*self.cos(c)
            )
    def dual_cosine_law_side(self, A, B, C):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The dual cosine law (not the original cosine law)
        relates A, B, C, and c:

        cos*(C) = - cos*(A) cos*(B) + sin*(A) sin*(B) cos(c)
        * not the spatial trig function, always the regular trig function

        This specific method takes A, B, C and computes c.
        """
        math = self.math
        real = math.real
        A = to_real(real, A)
        B = to_real(real, B)
        C = to_real(real, C)
        return self.acos(
            (math.cos(C) + math.cos(A)*math.cos(B)) /
            (math.sin(A)*math.sin(B))
            )
    def sine_law_side(self, a, A, B):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The sin law relates a, A, b, and B:

        sin*(A) sin(b) = sin*(B) sin(a)
        * not the spatial trig function, always the regular trig function

        This specific method takes a, A, B and computes b.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        A = to_real(real, A)
        B = to_real(real, B)
        return self.asin(self.sin(a) / math.sin(a) * math.sin(b))
    def sine_law_angle(self, a, A, b):
        """
        A triangle looks like this:

             c
        A -------- B
         \     __/
        b \ __/  a
           C

        By convention, lowercase letter is used to mean the side length
        opposite a vertex, and the uppercase letter is used to mean the
        angle of that vertex.

        The sin law relates a, A, b, and B:

        sin*(A) sin(b) = sin*(B) sin(a)
        * not the spatial trig function, always the regular trig function

        This specific method takes a, A, b and computes B.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        A = to_real(real, A)
        b = to_real(real, b)
        return math.asin(math.sin(A) / self.sin(a) * self.sin(b))
    def distance_between(self, p, q):
        """
        Computes the distance between 2 points in this space,
        more specifically, the length of the line segment that would join them.
        
        Distance is calculated based on the following equations:

        x^2 = K (p0 - q0)^2 + (p1 + q1)^2 + (p2 + q2)^2 + (p3 + q3)^2 + ...
        x is an intermediate value representing the model distance

        d = 2 asin(x/2)
        d is the actual distance
        """
        math = self.math
        real = math.real
        p = p.x
        q = q.x
        n = len(p)
        if len(q) != n:
            raise ValueError('Mismatched dimensions in points')
        x = real(self.curvature) * (p[0] - q[0]) **2 + sum(
            map((lambda tup:(tup[0] - tup[1])**2), zip(p[1:], q[1:])),
            start = real(0))
        return real(2) * self.asin(math.sqrt(x) / real(2))

class _projection_types(enum.Enum):
    drop_extra_axis = 1
    preserve_angles = 2
    preserve_lines = 4
projection_types = joined_namespace(_projection_types)
projection_types.join({
    'drop_first_axis': projection_types.drop_extra_axis,
    'orthographic': projection_types.drop_extra_axis,
    'gans': projection_types.drop_extra_axis,
    'conformal': projection_types.preserve_angles,
    'stereographic': projection_types.preserve_angles,
    'poincare': projection_types.preserve_angles,
    'poincaré': projection_types.preserve_angles,
    'gnomonic': projection_types.preserve_lines,
    'klein': projection_types.preserve_lines,
    'beltrami_klein': projection_types.preserve_lines
    })

class space_point(object):
    """
    Represents a point in a space of constant curvature.
    By convention, an extra dimension is added to make math easier (see: projected coordinates),
    and this extra dimension comes first.
    So for example, in 3 dimensions with some K,
    the coordinates are (x0, x1, x2, x3)
    satisfying x0^2 = 1 - K(x1^2 + x2^2 + x3^2)
    Is mutable.
    """
    def __init__(self, home, x):
        """
        Directly construct a point with no validity checks.
        Not recommended. Please use the space's methods for generating
        a point instead.
        Parameters:
        - home - the space that this point lives in, which will provide
            a math context and a curvature
        - x - the coordinate vector, with the first item being the extra dimension
        """
        self.home = home
        self.x = list(x) # marks mutable
    def __eq__(self, other):
        if self is other:
            return True
        if not hasattr(other, 'home') or not hasattr(other, 'x'):
            return False
        return self.home == other.home and tuple(self.x) == tuple(other.x)
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        return hash((space_point, self.home, self.x))
    def __getitem__(self, index):
        return self.x[index]
    def __setitem__(self, index, value):
        self.x[index] = value
    def __abs__(self):
        return self.home.magnitude_of(self)
    def __add__(self, other):
        return self.home.parallel_transport(self, other)
    def __neg__(self):
        home = self.home
        x = self.x
        return space_point(
            home=home,
            x=(x[0],)+tuple(map(operator.neg, x[1:]))
            )
    def __sub__(self, other):
        return self.home.distance_between(self, other)
    def project(self, projection_type):
        """
        Project this point to the regular boring Euclidean plane
        using some standard projection.
        Use projection_type as...

        projection_type = projection_types.drop_extra_axis
        Simply returns the point vector but with the extra axis stripped off.
        Corresponds to
        the elliptic orthographic projection and
        the hyperbolic Gans projection.

        projection_type = projection_types.preserve_angles
        Projects from the point (-1, 0, 0, 0, ...)
        Angles are preserved - a corner with a certain angle will be mapped
        to a corner with the same angle, etc.
        Corresponds to
        the elliptic Stereographic projection and
        the hyperbolic Poincaré projection.

        projection_type = projection_types.preserve_lines
        Projects from the origin.
        Straightness is preserved - a line (geodesic) will be mapped to a line,
        a polygon to a polygon, etc.
        Corresponds to
        the elliptic Gnomonic projection and
        the hyperbolic Beltrami-Klein projection.
        """
        if isinstance(projection_type, str):
            projection_type = getattr(projection_types, projection_type.lower().replace('-','_').replace(' ','_'))
        if projection_type == projection_types.drop_extra_axis:
            return tuple(self.x[1:])
        if projection_type == projection_types.preserve_angles:
            ex = self.x[0]
            return tuple(map((lambda x: x / ex), self.x[1:]))
        if projection_type == projection_types.preserve_lines:
            ex = self.x[0] + self.home.math.real(1)
            return tuple(map((lambda x: x / ex), self.x[1:]))
        raise ValueError('Projection type unknown')
