#!/usr/bin/env python3

"""
Small library for geometry in Euclidean, elliptic, and hyperbolic spaces.
Does point arithmetic, trigonometric functions, and common geometric equations.
Supports using different math contexts.
"""

import math
import functools

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
        for parent in inherits:
            if isinstance(parent, dict):
                self.__dict__.update(parent)
            else:
                self.__dict__.update(parent.__dict__)

common_math = joined_namespace(math, {'real': float})

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
    result = joined_namespace(mp, {'real': mp.mpf})
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

    Note that 
    
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
    def make_point(self, direction, magnitude):
        """
        Take a regular N-dimensional direction unit vector
        and a magnitude scalar, and produces
        the point that far away from the origin in that direction
        but in this space.
        """
        math = self.math
        real = math.real
        magnitude = to_real(real, magnitude)
        def map_with(x):
            return math.sin(to_real(real, x) * magnitude)
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
