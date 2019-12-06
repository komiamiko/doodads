#!/usr/bin/env python3

"""
Small library for geometry in Euclidean, elliptic, and hyperbolic spaces.
Does point arithmetic, trigonometric functions, and common geometric equations.
Supports using different math contexts.

WARNING: This library is still a work in progress! Don't assume that everything works perfectly. There may be incorrect math.

This library has not been thoroughly tested to work correctly for all curvatures.
If you find a math error, do report it!
"""

import math
import functools
import itertools
import operator
import enum
import collections.abc

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
                for attr in dir(parent):
                    self.__dict__[attr] = getattr(parent, attr)
        
def extend_math_namespace(*inherits):
    """
    Construct a math library like namespace.
    Automatically fills in the following if they are not in the namespace already:
    - tau = 2 pi
    - pi = tau / 2
    - e = exp(1)
    - round = x -> floor(x + 1/2)
    - eps = a small value
    - exp = x -> e^x
    - sqrt = x -> x^(1/2)
    - cbrt = x -> x^(1/3)
    - hypot = (x,y) -> sqrt(x^2 + y^2)
    - asinh = x -> log(x + sqrt(x^2 + 1))
    - acosh = x -> log(x + sqrt(x^2 - 1))
    - asin from arcsin if available
    - acos from arccos if available
    - asin_safe = asin but it accepts values just outside of the usual range
    - acos_safe = acos but it accepts values just outside of the usual range
    - matrix = makes a numpy array by default
    - matrix_pow = pow for matrices, uses numpy by default
    - matmul = matrix multiply
    """
    ns = joined_namespace(*inherits)
    if not hasattr(ns, 'tau'):
        ns.tau = ns.pi * ns.real(2)
    if not hasattr(ns, 'pi'):
        ns.pi = ns.tau / ns.real(2)
    if not hasattr(ns, 'e'):
        ns.e = ns.exp(ns.real(1))
    if not hasattr(ns, 'round'):
        def _round(ns):
            def i_round(x):
                """
                patched math function
                rounds a number to the nearest integer
                """
                return ns.floor(x + ns.real(0.5))
            return i_round
        ns.round = _round(ns)
    if not hasattr(ns, 'eps'):
        ns.eps = ns.exp(-32)
    if not hasattr(ns, 'exp'):
        ns.exp = functools.partial(operator.pow, ns.e)
    if not hasattr(ns, 'sqrt'):
        def _sqrt(ns):
            def i_sqrt(x):
                """
                patched math function
                see docs for math.sqrt
                """
                return x ** (ns.real(1) / ns.real(2))
            return i_sqrt
        ns.sqrt = _sqrt(ns)
    if not hasattr(ns, 'cbrt'):
        def _cbrt(ns):
            def i_cbrt(x):
                """
                patched math function
                see docs for math.cbrt
                """
                invert = x < 0
                x = abs(x)
                result = x ** (ns.real(1) / ns.real(3))
                if invert:
                    result = -result
                return result
            return i_cbrt
        ns.cbrt = _cbrt(ns)
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
                can take some values just outside of the range [1, inf]
                """
                if ns.real(1) - ns.eps <= x <= ns.real(1):return ns.real(0)
                return ns.log(x + ns.sqrt(x*x - ns.real(1)))
            return i_acosh
        ns.acosh = _acosh(ns)
    if not hasattr(ns, 're'):
        def _re(ns):
            def i_re(z):
                """
                The Re function that extracts the real component of a complex number.
                """
                try:
                    return ns.real(z)
                except:
                    pass
                if hasattr(z, 'real'):
                    return z.real
                raise TypeError('Don\'t know how to get the real component of that')
            return i_re
        ns.re = _re(ns)
    if not hasattr(ns, 'asin') and hasattr(ns, 'arcsin'):
        ns.asin = ns.arcsin
    if not hasattr(ns, 'acos') and hasattr(ns, 'arccos'):
        ns.acos = ns.arccos
    if not hasattr(ns, 'asin_safe'):
        def _asin(ns):
            def i_asin(x):
                """
                patched math function
                see docs for math.asin
                can take some values just outside of the range [-1, 1]
                """
                if ns.real(1) <= x <= ns.real(1) + ns.eps:return ns.tau / ns.real(4)
                if -ns.real(1) >= x >= -ns.real(1) - ns.eps:return -ns.tau / ns.real(4)
                return ns.asin(x)
            return i_asin
        ns.asin_safe = _asin(ns)
    if not hasattr(ns, 'acos_safe'):
        def _acos(ns):
            def i_acos(x):
                """
                patched math function
                see docs for math.acos
                can take some values just outside of the range [-1, 1]
                """
                if ns.real(1) <= x <= ns.real(1) + ns.eps:return 0
                if -ns.real(1) >= x >= -ns.real(1) - ns.eps:return ns.pi
                return ns.acos(x)
            return i_acos
        ns.acos_safe = _acos(ns)
    if not hasattr(ns, 'matrix'):
        def _matrix(ns):
            def i_matrix(data):
                """
                extra math function to matrix-ify the input
                constructs a numpy array by default
                """
                import numpy
                return numpy.array(data)
            return i_matrix
        ns.matrix = _matrix(ns)
    if not hasattr(ns, 'matrix_pow'):
        def _matrix_pow(ns):
            def i_matrix_pow(m, r):
                """
                pow but for matrices
                uses numpy and scipy by default
                """
                if isinstance(r, int):
                    from numpy.linalg import matrix_power
                    return matrix_power(m, r)
                from scipy.linalg import fractional_matrix_power
                return fractional_matrix_power(m, r)
            return i_matrix_pow
        ns.matrix_pow = _matrix_pow(ns)
    if not hasattr(ns, 'matmul'):
        def _matmul(ns):
            def i_matmul(a, b):
                """
                mul but for matrices
                """
                try:
                    return a @ b
                except TypeError:
                    return a * b
            return i_matmul
        ns.matmul = _matmul(ns)
    return ns

common_math = extend_math_namespace(math, {'real': float})

def mp_namespace(dps=15, _nonce=[]):
    """
    Returns a namespace using mpmath's multiple precision real numbers
    instead of the built-in floats.
    Will return an identical object in future calls.
    Warning: imports mpmath. You will need mpmath.

    Setting dps through this method will allow for calculating an appropriate
    epsilon value.
    """
    if _nonce:
        return _nonce[0]
    from mpmath import mp, matrix
    mp.dps = 15
    result = extend_math_namespace(mp, {
        'real': mp.mpf,
        'eps': mp.mpf(10) ** -(dps-3),
        'matrix': matrix
        })
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

        Examples:
        K =  0 --> cos(x) = 1
        K =  1 --> cos(x) = cos*(x)
        K = -1 --> cos(x) = cosh(x)
        *regular trig function, not our special one
        """
        raise NotImplementedError
    def sin(self, x):
        """
        The sine function.
        
        Satisfies:
        sin(0) = 0
        d/dx sin(x) = cos(x)

        Examples:
        K =  0 --> sin(x) = x
        K =  1 --> sin(x) = sin*(x)
        K = -1 --> sin(x) = sinh(x)
        *regular trig function, not our special one
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
        # dumb edge case: 0-dimensional space
        if len(direction) == 0:
            return self.make_origin(0)
        
        math = self.math
        real = math.real
        preal = functools.partial(to_real, real)
        direction = tuple(map(preal, direction))
        if normalize:
            divide_by = abs(functools.reduce(math.hypot, direction)) or real(1)
            direction = tuple(map((lambda x: x / divide_by), direction))
        magnitude = preal(magnitude)
        cm = self.cos(magnitude)
        sm = self.sin(magnitude)
        map_with = functools.partial(operator.mul, sm)
        return space_point(
            self,
            (cm,) + tuple(map(map_with, direction))
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
        real = math.real
        if use_quick:
            return self.acos(point[0])
        return self.asin(abs(functools.reduce(math.hypot, point[1:], real(0))))
    def parallel_transport(self, dest, ref):
        """
        What point do we get when parallel transporting
        ref from the origin to dest?
        For K = 0, this is just vector addition, and the order does not matter.
        For other K, however, this operation is in general not commutative.
        """
        
        return space_point_transform(dest)(ref)
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
        Mass (measure) of the 1D boundary of the 2-sphere.
        Commonly called the circumference of a circle.

        Equation is:
        m = tau sin(r)
        m is the mass (measure)
        tau = 2pi is the number of radians in a full turn
        sin is this space's sin function

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
        Mass (measure) of the 2D interior of the 2-sphere.
        Commonly called the area of a circle.

        Equation is:
        m = 2tau sin(r/2)^2
        m is the mass (measure)
        tau = 2pi is the number of radians in a full turn
        sin is this space's sin function

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
        Mass (measure) of the 2D boundary of the 3-sphere.
        Commonly called the surface area of a sphere.

        Equation is:
        m = 2tau sin(r)^2
        m is the mass (measure)
        tau = 2pi is the number of radians in a full turn
        sin is this space's sin function

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
        Mass (measure) of the 3D interior of the 3-sphere.
        Commonly called the volume of a sphere

        Equation is:
        m = tau/K * (r - sin(2r)/2)
        m is the mass (measure)
        tau = 2pi is the number of radians in a full turn
        K is the curvature of the space
        sin is this space's sin function

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.

        This needs to be taken at the limit for K = 0.
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return math.tau / real(self.curvature) * (r - self.sin(r * real(2)) / real(2))
    def inv_sphere_v3(self, m):
        """
        Inverts sphere_v3

        IMPORTANT WARNING
        This function, in general, cannot be expressed in terms of common functions.
        We fallback to using a root finding method provided by scipy.
        scipy is an external library you would need to install.
        This root finder may not work in other math contexts.
        """
        from scipy.optimize import root_scalar
        math = self.math
        real = math.real
        m = to_real(real, m)
        lower, est, upper = self._estimate_inv_sphere_v3(m)
        def objective(r):
            return self.sphere_v3(r) - m
        result = root_scalar(objective, bracket = (lower, upper), x0 = est)
        return result.root
    def _estimate_inv_sphere_v3(self, m):
        """
        Used by root finding methods in inv_sphere_v3
        Returns (lower bound, estimate, upper bound)
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
            self.sin(a) * self.sin(b) * math.cos(C) * real(self.curvature)
            )
    def cosine_law_angle(self, a, b, c):
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
        return math.acos_safe(
            (self.cos(c) - self.cos(a) * self.cos(b)) /
            (self.sin(a) * self.sin(b) * real(self.curvature))
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
        return math.acos_safe(
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
        return self.asin(self.sin(a) / math.sin(A) * math.sin(B))
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
        return math.asin_safe(math.sin(A) / self.sin(a) * self.sin(b))
    def triangle_area_from_angles(self, A, B, C):
        """
        Computes the area of a triangle, given its angles.

        For K = 0, does not work.
        For other K, uses the Gauss-Bonnet formula:
          m = 1/K * (A + B + C - pi)
          pi = tau/2 is the number of radians in a half turn

        This method can handle triangles with infinite side lengths,
        as it never needs the side lengths.
        """
        if self.curvature == 0:
            raise TypeError('3 angles do not uniquely define a triangle for K = 0')
        math = self.math
        real = math.real
        A = to_real(real, A)
        B = to_real(real, B)
        C = to_real(real, C)
        # Gauss-Bonnet formula
        return (A + B + C - math.pi) / self.curvature
    def triangle_area_from_sides(self, a, b, c):
        """
        Computes the area of a triangle, given its side lengths.

        For K = 0, uses Heron's formula:
          s = (a+b+c)/2
          m^2 = s(s-a)(s-b)(s-c)
        For other K, solves the triangle using the cosine law,
        and calls the other method
        triangle_area_from_angles

        Note that this method breaks down for infinite triangles.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        b = to_real(real, b)
        c = to_real(real, c)
        if self.curvature == 0:
            # Heron's formula
            s = (a+b+c)/2
            return math.sqrt(s*(s-a)*(s-b)*(s-c))
        else:
            # solve the triangle and redirect
            A = self.cosine_law_angle(b, c, a)
            B = self.cosine_law_angle(c, a, b)
            C = self.cosine_law_angle(a, b, c)
            return self.triangle_area_from_angles(A, B, C)
    def distance_between(self, p, q):
        """
        Computes the distance between 2 points in this space,
        more specifically, the length of the line segment that would join them.
        
        Distance is calculated based on the following equations:

        x^2 = 1/K (p0 - q0)^2 + (p1 - q1)^2 + (p2 - q2)^2 + (p3 - q3)^2 + ...
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
        x = (p[0] - q[0])**2 / real(self.curvature) + sum(
            map((lambda tup:(tup[0] - tup[1])**2), zip(p[1:], q[1:])),
            real(0))
        return real(2) * self.asin(math.sqrt(x) / real(2))
    def dot_product(self, p, q):
        """
        Computes the dot product for points p, q as vectors from the origin
        Dot product · has the following properties:
        - p·q is bilinear (linear in both p and q)
        - p·q = q·p
        - p·p = |p|^2
        - cos(θ) = p·q/(|p| |q|)

        There really isn't a fancy formula for this.
        We just get the usual magnitudes and combine that with
        the Euclidean dot product formula.
        """
        math = self.math
        square = lambda x:x*x
        pm2 = sum(map(square, p[1:]))
        qm2 = sum(map(square, q[1:]))
        pm = math.sqrt(pm2)
        qm = math.sqrt(qm2)
        dot = sum(itertools.starmap(operator.mul, zip(p[1:], q[1:])))
        if pm != 0:
            dot *= self.asin(pm) / pm
        if qm != 0:
            dot *= self.asin(qm) / qm
        return dot
    def angle_between(self, p, q):
        """
        Get the angle between points.
        Does part of the computation for the dot product,
        but only the work needed to get the angle.
        Special case: if either point is the origin, returns 0.
        """
        math = self.math
        square = lambda x:x*x
        pm2 = sum(map(square, p[1:]))
        qm2 = sum(map(square, q[1:]))
        pm = math.sqrt(pm2)
        qm = math.sqrt(qm2)
        if pm == 0 or qm == 0:return math.real(0)
        dot = sum(itertools.starmap(operator.mul, zip(p[1:], q[1:])))
        return math.acos(dot / (pm * qm))

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

class space_point(collections.abc.Sequence):
    """
    Represents a point in a space of constant curvature.
    By convention, an extra dimension is added to make math easier (see: projected coordinates),
    and this extra dimension comes first.
    So for example, in 3 dimensions with some K,
    the coordinates are (x0, x1, x2, x3)
    satisfying x0^2 = 1 - K(x1^2 + x2^2 + x3^2)
    This reflects the "true shape" of the space, for example,
    the Euclidean plane embeds as a plane,
    the elliptic plane embeds as a half sphere,
    and the hyperbolic plane embeds as a hyperboloid.
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
        # require extra axis coordinate is not negative
        if self.x[0] < self.home.math.real(0):
            self.x = list(map(operator.neg, self.x))
    def __repr__(self):
        return 'space_point('+repr(self.home)+', '+repr(self.x)+')'
    def __str__(self):
        return str(self.x)
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
    def __len__(self):
        return len(self.x)
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
    def __mul__(self, other):
        """
        For scalar other thing:
        Scale the point as a vector, by a scalar factor.

        For point other thing:
        Compute the metric tensor (dot product) value.
        See method space.metric for more information.
        """
        if isinstance(other, space_point):
            return self.home.dot_product(self, other)
        
        home = self.home
        math = home.math
        real = math.real

        magnitude = abs(self) * other
        if magnitude == 0:
            return home.make_origin(len(self) - 1)

        direction = self[1:]
        return home.make_point(direction, magnitude, normalize=True)
    def __rmul__(self, other):
        """
        All multiplication operations are commutative,
        so we just redirect to the regular __mul__
        """
        return self * other
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
        Also the same as projecting from the point (-inf, 0, 0, 0, ...) to the plane x0 = 1

        projection_type = projection_types.preserve_angles
        Projects from the point (-1, 0, 0, 0, ...) to the plane x0 = 1
        Angles are preserved - a corner with a certain angle will be mapped
        to a corner with the same angle, etc.
        Corresponds to
        the elliptic Stereographic projection and
        the hyperbolic Poincaré projection.

        projection_type = projection_types.preserve_lines
        Projects from the origin to the plane x0 = 1
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
            ex = self.x[0] + self.home.math.real(1)
            return tuple(map((lambda x: x / ex), self.x[1:]))
        if projection_type == projection_types.preserve_lines:
            ex = self.x[0]
            return tuple(map((lambda x: x / ex), self.x[1:]))
        raise ValueError('Projection type unknown')

class space_point_transform(object):
    """
    Represents a transformation function on space points,
    more specifically, a kind of isometry.
    """
    def __init__(self, data, curvature=None, math=None):
        """
        The usual constructor.
        Feed it a point as data to have it construct the transform
        as parallel transpart from the origin to that point.
        """
        if isinstance(data, space_point):
            # create transformation data
            s = data.home
            math = s.math
            self.curvature = s.curvature
            if self.curvature == 0:
                self.add = data[1:]
                self.matrix = None
            else:
                self.add = None
                self.matrix = space_point_transform._as_matrix(data)
        elif isinstance(data, space_point_transform):
            # shallow copy
            self.curvature = data.curvature
            self.add = data.add
            self.matrix = data.matrix
            self.math = data.math
        elif isinstance(data, (tuple, list)):
            # should be an addition vector
            self.add = data
            self.matrix = None
            # we take your curvature
            self.curvature = curvature
        elif hasattr(data, '__len__'):
            # probably a numpy array or matrix
            try:
                # access the top left element
                _ = data[0,0]
                # seems like a left transform matrix
                self.add = None
                self.matrix = data
            except:
                # seems like a vector to be added
                self.add = data
                self.matrix = None
            # we take your curvature
            self.curvature = curvature
        else:
            raise TypeError('Not sure how to construct a transform from that data type')
        self.math = math
    def __eq__(self, other):
        if self is other:return True
        if not isinstance(other, space_point_transform):return False
        return self.curvature == other.curvature and self.add == other.add and self.matrix == other.matrix and self.math == other.math
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        return hash((space_point_transform, self.curvature, self.add, _require_hash(self.matrix), _require_hash(self.math)))
    def __repr__(self):
        if self.add is not None:
            data = repr(self.add)
        elif self.matrix is not None:
            data = repr(self.matrix)
        return 'space_point_transform(' + data + ', curvature=' + repr(self.curvature) + ', math=' + repr(self.math) + ')'
    def __str__(self):
        if self.add is not None:
            return '(P -> ' + str(self.add) + ' + P)'
        elif self.matrix is not None:
            return str(self.matrix)
    @staticmethod
    def _as_matrix(point):
        """
        Helper method to construct a transformation matrix from a point.
        Please don\'t use this for K = 0 because that would be dumb.

        Requires numpy*
        numpy is an external library, you may need to install it.
        The matrix class used is numpy.array
        * unless the math context provides a different matrix class

        Equations used:
        D = (x0 - 1)/(x1^2 + x2^2 + ... + xk^2)
        it's just an intermediate constant, it doesn't really mean anything
        T[0,0] = x0
        T[0,i] = -K xi       |  i =/= 0
        T[i,0] = xi          |  i =/= 0
        T[i,i] = 1 + xi^2 D  |
        T[i,j] = xi xj D     |  i =/= j,  i,j =/= 0
        These rules fully describe a direct way to compute every element of the matrix.

        The current implementation is not vectorized,
        so it might seem a little slow for very high dimensions.
        A possible future improvement would be to find a way to vectorize this matrix,
        taking advantage of numpy's very good constant factor.
        """
        # fetch point info
        s = point.home
        math = s.math
        real = math.real
        n = len(point)
        curvature = s.curvature

        # initialize matrix to all zeros of the correct type
        t = math.matrix([[real(0)]*n]*n)

        # extra constant b = x1^2 + x2^2 + ...
        b = sum(map((lambda x:x*x), point[1:]))

        # b = 0 means the point is the origin
        # so let's build the identity matrix
        if b == 0:
            for i in range(n):
                t[i,i] = real(1)
            return t
        
        # extra constant c = -K
        c = -curvature
        # apply the rules for d
        d = (point[0] - 1)/b
        # apply the rules for t
        t[0,0] = point[0]
        for i in range(1, n):
            xi = point[i]
            t[0,i] = xi * c
            t[i,0] = xi
            xid = xi * d
            t[i,i] = 1 + xid * xi
            for j in range(i+1, n):
                xj = point[j]
                t[i,j] = t[j,i] = xid * xj

        # it's done!
        return t
    @staticmethod
    def _flatten_matrix(mat, cast):
        """
        Helper method to flatten the matrix type
        into a tuple with a certain type.
        """
        return tuple(mat[i,0] for i in range(len(mat)))
    def _make_matrix(self):
        """
        Force self to have a matrix.

        Will only have an interesting effect for K = 0,
        because otherwise we always use a matrix anyway.
        """
        if self.matrix is not None:return
        # now we know K =/= 0

        math = self.math
        real = math.real

        n = len(self.add)

        # identity matrix with adding column
        t = [[real(0)]*(n+1) for _ in range(n+1)]
        for i in range(n+1):
            t[i][i] = real(1)
        for i in range(n):
            t[i+1][0] = self.add[i]
        t = math.matrix(t)

        self.matrix = t
    def __call__(self, data):
        """
        Either concatenate (compose) this transformation object with another
        or apply it to a point.

        When concatenating transforms,
        since we use the left transform convention,
        (f g) x = f (g x)
        so the new transform will apply the other one first
        and then this one.
        """
        if isinstance(data, space_point):
            if self.curvature != data.home.curvature:
                raise ValueError('Curvatures do not match')
            if self.add is not None:
                if len(self.add) != len(data) - 1:
                    raise ValueError('Dimensionality does not match')
                return space_point(
                    data.home,
                    (data[0],) + tuple(map(sum, zip(self.add, data[1:])))
                    )
            if self.matrix is not None:
                if len(self.matrix) != len(data):
                    raise ValueError('Dimensionality does not match')
                math = self.math or data.math
                matrified = math.matrix([[dv] for dv in data])
                return space_point(
                    data.home,
                    space_point_transform._flatten_matrix(math.matmul(self.matrix, matrified), data.home.math.real)
                    )
        elif isinstance(data, space_point_transform):
            if self.curvature != data.curvature:
                raise ValueError('Curvatures do not match')
            if self.add is not None:
                if data.add is None:
                    self._make_matrix()
                else:
                    if len(self.add) != len(data.add):
                        raise ValueError('Dimensionality does not match')
                    return space_point_transform(
                        tuple(map(sum, zip(self.add, data.add))),
                        curvature = self.curvature,
                        math = self.math or data.math
                        )
            if self.matrix is not None:
                if data.matrix is None:
                    data._make_matrix()
                math = self.math or data.math
                return space_point_transform(
                    math.matmul(self.matrix, data.matrix),
                    curvature = self.curvature,
                    math = self.math or data.math
                    )
        else:
            print(type(other))
            raise TypeError('Can only apply this transform to a point (moves the point) or a transform (concatenates the transforms), but received some other type')
    def __add__(self, other):
        """
        For convenience, you are also allowed to write
        concatenation (composition)/application as an addition.

        When concatenating transforms,
        since we use the left transform convention,
        (f g) x = f (g x)
        so the new transform will apply the other one first
        and then this one.
        """
        return self(other)
    def __mul__(self, other):
        """
        Computes the iterated transform for this transform object.
        Looks like a scalar power but implemented with the multiply operator.

        Uses numpy.linalg for computation of integer matrix powers.
        You should already have numpy if you got this far, so that's okay.

        For fractional matrix powers, requires scipy.
        You may need to install scipy separately.
        """
        import numbers
        
        if not isinstance(other, numbers.Real):
            raise TypeError('For transforms, this operation (*) is not defined for non-real argument')

        if other == 1:
            return self

        if self.add is not None:
            scale_func = functools.partial(operator.mul, other)

            return space_point_transform(
                tuple(map(scale_func, self.add)),
                curvature = self.curvature,
                math = self.math
                )

        math = self.math

        return space_point_transform(
            math.matrix_pow(self.matrix, other),
            curvature = self.curvature,
            math = self.math
            )
    def __rmul__(self, other):
        """
        Redirects to the regular __mul__ since
        all our defined operations are commutative.
        """
        return self * other

class euclidean_space(abc_space):
    """
    Represents a space with curvature K = 0.
    Please do not use this class directly. Instead, use space.
    """
    def __init__(self, math):
        self.math = math
        self.curvature = 0
    def sin(self, x):
        """
        For K = 0
        sin(x) = x
        """
        return x
    def cos(self, x):
        """
        For K = 0
        cos(x) = 1
        """
        return self.math.real(1)
    def asin(self, x):
        """
        For K = 0
        sin(x) = x
        """
        return x
    def acos(self, x):
        """
        For K = 0
        cos(x) = 1

        This is a constant function, so it is not invertible.
        Calling this will result in an error.
        """
        raise TypeError('cosine function for K = 0 is a constant function, and cannot be inverted')
    def parallel_transport(self, dest, ref):
        """
        Parallel transport in Euclidean space is easy! It's just regular vector addition.
        """
        return space_point(self, (dest[0],) + tuple(map(sum, zip(dest[1:], ref[1:]))))
    def _hypot(self, x, y):
        """
        hypot(x, y)
        assuming correct types
        specially implemented for K = 0 as the Pythagorean theorem
        """
        math = self.math
        return math.hypot(x, y)
    def _leg(self, x, z):
        """
        leg(x, z)
        assuming correct types
        specially implemented for K = 0 as the Pythagorean theorem
        """
        math = self.math
        return math.sqrt(z*z - x*x)
    def magnitude_of(self, point, use_quick=False):
        """
        Return the magnitude of a point in this space, or rather,
        its distance to the origin.

        For K = 0, this is the norm of the vector.

        use_quick flag is ignored.
        """
        return abc_space.magnitude_of(self, point, False)
    def sphere_v3(self, r):
        """
        Mass of the 3D interior of the 3-sphere.
        Commonly called the volume of a sphere.

        Specially implemented for K = 0.

        To be pedantic, mathematicians call the inside a "ball"
        and the boundary a "sphere" but most people don't care
        about that difference. We reflect this here by naming
        the method after a sphere even if it really should be a ball.
        """
        math = self.math
        real = math.real
        r = to_real(real, r)
        return real(2) / real(3) * math.tau * r**3
    def inv_sphere_v3(self, m):
        """
        Inverts sphere_v3
        Note: this is difficult in general, because it can't be
        expressed in terms of common functions
        """
        math = self.math
        real = math.real
        m = to_real(real, m)
        return math.cbrt(m / (real(2) / real(3) * math.tau))
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
        (specific to K = 0)

        c^2 = a^2 + b^2 - 2 a b cos*(C)
        *regular trig

        This specific method takes a, b, C and computes c.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        b = to_real(real, b)
        C = to_real(real, C)
        return math.sqrt(a*a + b*b - a*b*real(2)*math.cos(C))
    def cosine_law_angle(self, a, b, c):
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
        (specific to K = 0)

        c^2 = a^2 + b^2 - 2 a b cos*(C)
        *regular trig

        This specific method takes a, b, c and computes C.
        """
        math = self.math
        real = math.real
        a = to_real(real, a)
        b = to_real(real, b)
        c = to_real(real, c)
        return math.acos_safe((a*a + b*b - c*c)/(a*b*real(2)))
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

        Note that in K = 0 this is redundant, since the interior angles
        always sum to a half turn. The side length c is not needed.
        """
        math = self.math
        real = math.real
        A = to_real(real, A)
        B = to_real(real, B)
        return math.pi - A - B
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

        Does not work in K = 0.

        This specific method takes A, B, C and computes c.
        """
        raise TypeError('Dual cosine law breaks down at K = 0, as knowing only the angles it is impossible to determine a side length')
    def distance_between(self, p, q):
        """
        Computes the distance between 2 points in this space,
        more specifically, the length of the line segment that would join them.

        For K = 0, this is just the magnitude of the vector difference.
        """
        math = self.math
        return math.sqrt(sum(map(
                (lambda tup:(tup[0] - tup[1])**2),
                zip(p[1:], q[1:])
                )))

class elliptic_space(abc_space):
    """
    Represents a space with curvature K = 1.
    Please do not use this class directly. Instead, use space.
    """
    def __init__(self, math):
        self.math = math
        self.curvature = 1
    def cos(self, x):
        """
        The cosine function.

        Satisfies:
        cos(0) = 1
        d/dx cos(x) = -K sin(x)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.cos(x)
    def sin(self, x):
        """
        The sine function.
        
        Satisfies:
        sin(0) = 0
        d/dx sin(x) = cos(x)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.sin(x)
    def acos(self, x):
        """
        The inverse cosine function.
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.acos_safe(x)
    def asin(self, x):
        """
        The inverse sine function.
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.asin_safe(x)
    def distance_between(self, p, q):
        """
        Computes the distance between 2 points in this space,
        more specifically, the length of the line segment that would join them.

        In elliptic space specifically, there are great circles instead (or higher dimensional analogs),
        so the line when extended will loop around,
        and maybe the other direction is actually a shorter distance!

        Note: this method actually breaks on its own,
        because it accesses the attribute .scale .
        It can only be used from the space class.
        """
        dist = abc_space.distance_between(self, p, q)
        return min(dist, self.math.pi * self.scale - dist)
    def _estimate_inv_sphere_v3(self, m):
        math = self.math
        real = math.real
        m /= self.scale**3
        if m > real(6):
            est = m / math.tau
            gap = math.tau / real(12)
            lower = max(est - gap, real(0))
            upper = est + gap
        else:
            est = math.cbrt(m * real(3) / (math.tau * real(2)))
            gap = math.tau / real(12)
            lower = est
            upper = est + gap
        lower *= self.scale
        est *= self.scale
        upper *= self.scale
        return lower, est, upper

class hyperbolic_space(abc_space):
    """
    Represents a space with curvature K = -1.
    Please do not use this class directly. Instead, use space.
    """
    def __init__(self, math):
        self.math = math
        self.curvature = -1
    def cos(self, x):
        """
        The cosine function.

        Satisfies:
        cos(0) = 1
        d/dx cos(x) = -K sin(x)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.cosh(x)
    def sin(self, x):
        """
        The sine function.
        
        Satisfies:
        sin(0) = 0
        d/dx sin(x) = cos(x)
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.sinh(x)
    def acos(self, x):
        """
        The inverse cosine function.
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.acosh(x)
    def asin(self, x):
        """
        The inverse sine function.
        """
        math = self.math
        real = math.real
        x = to_real(real, x)
        return math.asinh(x)
    def _estimate_inv_sphere_v3(self, m):
        math = self.math
        real = math.real
        m /= self.scale**3
        if m > real(10):
            est = math.asinh(m / math.pi) / real(2)
            gap = real(1) / real(2)
            lower = max(est - gap, real(0))
            upper = est + gap
        else:
            est = math.cbrt(m * real(3) / (math.tau * real(2)))
            gap = real(1) / real(8)
            lower = max(est - gap, real(0))
            upper = est
        lower *= self.scale
        est *= self.scale
        upper *= self.scale
        return lower, est, upper

class space(abc_space):
    """
    The unified space class! Works for spaces with constant curvature.
    Just give it a math context and a curvature and it will take care of the rest.
    """
    def __init__(self, curvature = None, fake_curvature = None, radius = None, math = common_math):
        """
        Construct a space.

        Note: curvature is inherently a 2D quantity.
        It may sound counterintuitive that an N-dimensional space
        is always described with a 2D quantity, but that's how it works.
        The curvature is defined as
        K = 1/R^2
        where R is the radius of curvature.
        This means that K = 0 requires an infinite radius,
        and K < 0 requires an imaginary radius.

        We also allow for constructing from a "fake curvature",
        a 1D quantity k satisfying
        K = k |k|
        This allows for avoiding imaginary numbers.
        """
        self.math = math
        if sum(map((lambda x:x is not None), (curvature, fake_curvature, radius))) != 1:
            raise ValueError('Must provide exactly 1 value specifying the curvature')
        if radius is not None:
            # important! this must coerce K to a real number, not complex
            curvature = math.re(math.real(1) / (radius * radius))
        if fake_curvature is not None:
            curvature = fake_curvature * abs(fake_curvature)
        self.curvature = curvature
        if curvature == 0:
            self.base = euclidean_space
            self.scale = math.real(1)
        elif curvature > 0:
            self.base = elliptic_space
            self.scale = math.real(1) / math.sqrt(math.real(curvature))
        else:
            self.base = hyperbolic_space
            self.scale = math.real(1) / math.sqrt(-math.real(curvature))
    def __repr__(self):
        if self.math == common_math:
            ext = ''
        else:
            ext = ', math = ' + repr(self.math)
        return 'space(' + repr(self.curvature) + ext + ')'
    def __str__(self):
        if self.curvature == 0:
            res = 'R'
        elif self.curvature > 0:
            res = 'E'
        else:
            res = 'H'
        if self.scale != self.math.real(1):
            res = '(' + res + '*' + str(self.scale) + ')'
        res = res + '^n'
        return res
    def cos(self, x):
        """
        The cosine function.

        Satisfies:
        cos(0) = 1
        d/dx cos(x) = -K sin(x)
        """
        base = self.base
        math = self.math
        real = math.real
        x = to_real(real, x)
        return base.cos(self, x / self.scale)
    def sin(self, x):
        """
        The sine function.
        
        Satisfies:
        sin(0) = 0
        d/dx sin(x) = cos(x)
        """
        base = self.base
        math = self.math
        real = math.real
        x = to_real(real, x)
        return base.sin(self, x / self.scale) * self.scale
    def acos(self, x):
        """
        The inverse cosine function.
        """
        base = self.base
        math = self.math
        real = math.real
        x = to_real(real, x)
        return base.acos(self, x) * self.scale
    def asin(self, x):
        """
        The inverse sine function.
        """
        base = self.base
        math = self.math
        real = math.real
        x = to_real(real, x)
        return base.asin(self, x / self.scale) * self.scale
    def _hypot(self, x, y):
        """
        hypot(x, y)
        assuming correct types
        """
        return self.base._hypot(self, x / self.scale, y / self.scale) * self.scale
    def _leg(self, x, z):
        """
        leg(x, z)
        assuming correct types
        """
        return self.base._leg(self, x / self.scale, z / self.scale) * self.scale
    def magnitude_of(self, point, use_quick=False):
        return self.base.magnitude_of(self, point, use_quick=use_quick)
    def sphere_s1(self, r):
        return self.base.sphere_s1(self, r)
    def inv_sphere_s1(self, m):
        return self.base.inv_sphere_s1(self, m)
    def sphere_v2(self, r):
        return self.base.sphere_v2(self, r)
    def inv_sphere_v2(self, m):
        return self.base.inv_sphere_v2(self, m)
    def sphere_s2(self, r):
        return self.base.sphere_s2(self, r)
    def inv_sphere_s2(self, m):
        return self.base.inv_sphere_s2(self, m)
    def sphere_v3(self, r):
        return self.base.sphere_v3(self, r)
    def inv_sphere_v3(self, m):
        return self.base.inv_sphere_v3(self, m)
    def _estimate_inv_sphere_v3(self, m):
        return self.base._estimate_inv_sphere_v3(self, m)
    def cosine_law_side(self, a, b, C):
        return self.base.cosine_law_side(self, a, b, C)
    def cosine_law_angle(self, a, b, c):
        return self.base.cosine_law_angle(self, a, b, c)
    def dual_cosine_law_angle(self, A, B, c):
        return self.base.dual_cosine_law_angle(self, A, B, c)
    def dual_cosine_law_side(self, A, B, C):
        return self.base.dual_cosine_law_side(self, A, B, C)
    def sine_law_side(self, a, A, B):
        return self.base.sine_law_side(self, a, A, B)
    def sine_law_angle(self, a, A, b):
        return self.base.sine_law_angle(self, a, A, b)
    def distance_between(self, p, q):
        return self.base.distance_between(self, p, q)

