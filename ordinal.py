"""
Small library for working with ordinal numbers, including transfinite numbers.
Warning: the math here has not been verified by a math expert.
"""

import warnings
import numbers
import functools

class _omega_t(object):
    """
    Type of the internally used omega object.
    """
    def __init__(self):
        self.cnf = [(1, 1)]
        # tier is a shortcut used to speed up comparisons
        self._tier = 1
    def __eq__(self, other):
        if isinstance(other, numbers.Real):return False
        if isinstance(other, _omega_t):return True
        if hasattr(other, 'cnf') and other.cnf == [(1, 1)]:return True
        return False
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        if isinstance(other, (numbers.Real, _omega_t)):return False
        return other > self
    def __le__(self, other):
        return self == other or self < other
    def __ge__(self, other):
        return not (self < other)
    def __gt__(self, other):
        return not (self <= other)
    def __hash__(self):
        return hash(_omega_t)
    def __str__(self):
        return '{\\omega}'
    def __repr__(self):
        return 'omega'
    def __pos__(self):
        return self
    def __neg__(self):
        return - to_ordinal(self)
    def __add__(self, other):
        return to_ordinal(self) + other
    def __radd__(self, other):
        # shortcut: left argument is natural number,
        # result is omega
        if other < self:return self
        return to_ordinal(other) + self
    def __sub__(self, other):
        return to_ordinal(self) - other
    def __rsub__(self, other):
        return to_ordinal(other) - self
    def __mul__(self, other):
        return to_ordinal(self) * other
    def __rmul__(self, other):
        return to_ordinal(other) * self
    def __pow__(self, other):
        # shortcut: derive CNF directly
        return ordinal([(other, 1)])
    def __rpow__(self, other):
        return to_ordinal(other) ** self
    
# the canonical omega object
omega = _omega_t()

def _ordinal_tier(a):
    """
    Returns the "tier" of a.
    Bigger ordinals have higher tier.
    This is used to speed up comparison by seeing when an ordinal is vastly larger than another.
    As currently implemented, this reflects the height of the leading term of the CNF.
    """
    if isinstance(a, numbers.Real):
        return 0
    return a._tier

def to_ordinal(n):
    """
    Returns n. If n is already an instance of
    the ordinal class, returns n unchanged, otherwise converts the type.
    """
    if isinstance(n, ordinal):
        return n
    return ordinal(n)

class ordinal(object):
    """
    Represents an ordinal number.
    """
    def __init__(self, value, unchecked=False):
        """
        Coerce to type ordinal.
        unchecked flag is used to allow fast unchecked construction.
        """
        if value == 0:
            self.cnf = []
        elif isinstance(value, ordinal):
            self.cnf = list(value.cnf)
        elif value in (omega, 'omega'):
            self.cnf = [(1, 1)]
        elif isinstance(value, int):
            if value < 0:
                warnings.warn('Negative value being used to construct an ordinal.\nNegative ordinal numbers are, in general, not well defined. Arithmetic assuming non-negative or strictly positive ordinals may behave strangely.')
            self.cnf = [(0, value)]
        elif isinstance(value, tuple) and len(value) == 2 and isinstance(value[1], int):
            self.cnf = [value]
        elif isinstance(value, list):
            if unchecked:
                warnings.warn('Ordinal is being constructed directly from its Cantor normal form as a list type object, without checks.')
            else:
                old_value = sorted(value, reverse=True)
                value = []
                for p, c in old_value:
                    if not value:
                        value.append((p, c))
                    else:
                        if value[-1][0] == p:
                            value[-1] = p, c+value[-1][1]
                        else:
                            value.append((p, c))
                value = list((p, c) for p, c in value if c != 0)
                if any(c < 0 for p, c in value):
                    warnings.warn('Negative coeficient found in Cantor normal form of ordinal.\nNegative ordinal numbers are, in general, not well defined. Arithmetic assuming non-negative or strictly positive ordinals may behave strangely.')
                if any(c < omega and int(c) != c for p, c in value):
                    warnings.warn('Non-integer coeficient found in Cantor normal form of ordinal.\nNon-integer ordinal numbers are not defined.')
                if any(p < 0 for p, c in value):
                    warnings.warn('Negative exponent of omega found in Cantor normal form of ordinal.\nThese exponents of ordinal numbers are not defined.')
                if any(p < omega and int(p) != p for p, c in value):
                    warnings.warn('Exponent of omega, which is not an integer or a limit ordinal, found in Cantor normal form of ordinal.\nThese exponents of ordinal numbers are not defined.')
            self.cnf = value
        else:
            raise ValueError(f'Could not build an ordinal out of object: {value}')
        # compute tier, which will be used to speed up comparisons
        scnf = self.cnf
        if not scnf or scnf[0][0] == 0:
            self._tier = 0
        else:
            high_tier = _ordinal_tier(scnf[0][0])
            self._tier = high_tier + 1
    def __eq__(self, other):
        otier = _ordinal_tier(other)
        if self._tier != otier:return False
        return self.cnf == to_ordinal(other).cnf
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        otier = _ordinal_tier(other)
        if self._tier < otier:return True
        if self._tier > otier:return False
        return self.cnf < to_ordinal(other).cnf
    def __le__(self, other):
        otier = _ordinal_tier(other)
        if self._tier < otier:return True
        if self._tier > otier:return False
        return self.cnf <= to_ordinal(other).cnf
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return not (self < other)
    def __hash__(self):
        return hash((ordinal,) + tuple(self.cnf))
    def __int__(self):
        scnf = self.cnf
        if not scnf:return 0
        if scnf[0][0] != 0:
            raise TypeError('This ordinal object is not a natural number, and cannot be converted to an integer object')
        return scnf[0][1]
    def __str__(self):
        scnf = self.cnf
        if not scnf:return '0'
        def _istr(term, require_sign=True):
            coeff = str(term[1])
            if term[1] < 0:
                coeff = '\\left('+coeff+'\\right)'
            if term[0] == 0:
                result = coeff
            else:
                result = str(omega)
                if term[0] != 1:
                    result = result+'^{'+str(term[0])+'}'
                if term[1] != 1:
                    result = result+'\\cdot '+coeff
            if require_sign:
                result = '+'+result
            return result
        chunks = [_istr(scnf[0], False)]
        for term in scnf[1:]:
            chunks.append(_istr(term))
        return ' '.join(chunks)
    def __repr__(self):
        return 'ordinal('+repr(self.cnf)+')'
    def __pos__(self):
        return self
    def __neg__(self):
        warnings.warn('Negative ordinal numbers are, in general, not well defined. Arithmetic assuming non-negative or strictly positive ordinals may behave strangely.')
        return ordinal([(p, -c) for p,c in self.cnf])
    @staticmethod
    def sum_cnf(*cnfs):
        def iadd_cnf(rcnf, ocnf):
            # rule: anything plus 0 is left argument
            if not ocnf:return rcnf
            # separate out first (largest) term of right hand side
            ofirst, *ocnf = ocnf
            # rule: smallert left parts are erased
            while rcnf and rcnf[-1][0] < ofirst[0]:
                del rcnf[-1]
            # rule: same size left part is combined
            if rcnf and rcnf[-1][0] == ofirst[0]:
                rcnf[-1] = (ofirst[0], rcnf[-1][1] + ofirst[1])
            else:
                rcnf.append(ofirst)
            # now irreducible
            rcnf += ocnf
            return rcnf
        return functools.reduce(iadd_cnf, cnfs, [])
    def __add__(self, other):
        """
        Sum of 2 ordinal numbers.
        Note that, in general, addition is not commutative.
        To summarize the substitution rules:
        when the right side exponent is larger than the left, the left is erased.
        """
        return ordinal(ordinal.sum_cnf(
            self.cnf,
            to_ordinal(other).cnf
            ))
    def __radd__(self, other):
        return to_ordinal(other) + self
    def __mul__(self, other):
        """
        Product of 2 ordinal numbers.
        Note that, in general, multiplication is not commutative.
        To summarize the substitution rules:
        when the right side is a limit ordinal,
        left side smaller parts get erased,
        then left distribute.
        """
        scnf = self.cnf
        # rule: 0 times anything is 0
        if not scnf:return 0
        # rule: anything times 0 is 0
        if other == 0:return 0
        # rule: anything times 1 is left argument
        if other == 1:return self
        ocnf = to_ordinal(other).cnf
        # if left argument is a natural number
        if scnf[0][0] == 0:
            # non-limit ordinals multiply as usual
            if ocnf[0][0] == 0:return scnf[0][1] * ocnf[0][1]
            # rule: natural number times limit ordinal is right argument
            return other
        # left argument is a limit ordinal
        # if right argument is a natural number
        if ocnf[0][0] == 0:
            rcnf = list(scnf)
            rcnf[0] = (rcnf[0][0], rcnf[0][1] * ocnf[0][1])
            return ordinal(rcnf)
        # right argument is a limit ordinal
        # left argument smaller parts are erased, only first term matters
        p, n = scnf[0]
        rcnf = []
        # left distribute
        for q, m in ocnf:
            # earlier rule again:
            # if right argument is limit ordinal and left argument is natural number,
            # result is right argument
            if q == 0:
                m = n * m
            # exponents are added
            # addition is strictly increasing in the right argument,
            # so this q is guaranteed to be less than the previous q
            q = p + q
            # just add the term
            rcnf.append((q, m))
        return ordinal(rcnf)
    def __rmul__(self, other):
        return to_ordinal(other) * self
    def __pow__(self, other):
        """
        Power of 2 ordinal numbers.
        To summarize the substitution rules:
        natural number to omega times something is omega to that something,
        right side limit ordinal causes only left largest power to be preserved,
        right side successor is similar but keep left coefficient and do exponent with one less and then multiply by the left side.
        """
        # rule: anything to 0 is 1
        if other == 0:return 1
        # rule: anything to 1 is itself
        if other == 1:return self
        scnf = self.cnf
        # rule: 0 to anything is 0
        if not scnf:return 0
        if scnf[0][0] == 0:
            s = int(self)
            # apply rules for natural number to something
            if other < omega:
                # shortcut rule: natural numbers only do power like normal
                return s ** int(other)
            # other is not natural number
            rcnf, n = list(to_ordinal(other).cnf), 1
            # natural number term needs special treatment
            if rcnf[-1][0] == 0:
                n = s ** rcnf[-1][1]
                del rcnf[-1]
            # bump inner exponents down by 1
            for i in range(len(rcnf)):
                r = rcnf[i]
                r = (-1 + r[0], r[1])
                rcnf[i] = r
                # note we use a special case of subtraction
                # we already accounted for 0 separately
                # otherwise, either it is a natural number greater than 0 so it stays greater than or equal to 0
                # or it is at least omega so the -1 will be eaten harmlessly
                # this behaviour is exactly as the rule says, which is, given X, return Y, where X = 1 + Y
            p = ordinal(rcnf)
            return ordinal([(p, n)])
        else:
            # apply rules for not natural number to something
            p, m = scnf[0]
            rcnf = list(to_ordinal(other).cnf)
            bump = rcnf[-1][0] == 0 and rcnf[-1][1] > 0
            if bump:
                # rule: when right is successor, do exponent with its predecessor on the largest term in left side, then multiply by left
                r = rcnf[-1]
                rcnf[-1] = (r[0], r[1] - 1)
                return ordinal([(p * ordinal(rcnf), m)]) * self
            else:
                # rule: when right is limit, do exponent on largest term in left side and erase the coefficient
                return ordinal([(p * ordinal(rcnf), 1)])
    def __rpow__(self, other):
        return to_ordinal(other) ** self

# above: old implementation
# below: unified ordinal class implementation

import abc
import functools
import itertools
import numbers
import operator
import warnings

def bin_log(x):
    """
    Base 2 floor logarithm for integers.
    """
    return len(bin(x)) - 3

def reduce_bisected(func, iterable, nothing=0):
    """
    Like reduce from functools.
    Produces the same results if the operator is associative.
    Uses a combining order like a perfect binary tree, so like
      ((a + b) + (c + d)) + e
      rather than
      (((a + b) + c) + d) + e
    For joining objects that accumulate size like lists, this achieves
      O(N log N) rather than O(N^2)
      which is an improvement.
    The sum of nothing is 0, or whatever else is supplied.
    """
    iterator = iter(iterable)
    try:
        build = [next(iterator)]
    except StopIteration:
        return nothing
    for i, v in enumerate(iterator):
        i += 2
        build.append(v)
        while not i & 1:
            i >>= 1
            rhs = build.pop()
            lhs = build[-1]
            build[-1] = func(lhs, rhs)
    while len(build) > 1:
        rhs = build.pop()
        lhs = build[-1]
        build[-1] = func(lhs, rhs)
    return build[0]

def sum_bisected(iterable):
    return reduce_bisected(operator.add, iterable)

class _named_const(object):
    """
    Represents a named constant value with no relation to anything else.
    All it does it patch str and repr to return the desired values.
    """
    def __init__(self, _str, _repr):
        self._str = _str
        self._repr = _repr
    def __str__(self):
        return self._str
    def __repr__(self):
        return self._repr

class ordinal_type(abc.ABC):
    """
    Represents an ordinal number in the mathematical sense.
    Natural numbers are included, and will be instances of this class, as expected.
    Note that this does not contain any useful methods -
    please use the static functions to work with ordinals instead.
    """
    
ordinal_type.register(int)

# Every ordinal is either zero, a successor ordinal, or a limit ordinal.
# I could not find any standard notation for these sets, so I
#   made names for them that I think are short and simple. 
kind_zero = _named_const("0", "kind_zero")
kind_successor = _named_const("(x+1)", "kind_successor")
kind_limit = _named_const("(\\lim)", "kind_limit")

def kind(value):
    """
    What kind of ordinal is it?
    Returns 1 of these 3:
    - kind_zero (for zero)
    - kind_successor (if there exists a well defined x such that value is x + 1)
    - kind_limit (everything else)
    Every ordinal number is in one of these categories.
    
    Inputs which are not ordinals will, in general, fail,
    and this function will try to check for bad input, however,
    this function does not guarantee that a non-ordinal input will cause
    an error. Whatever value is returned is useless.
    """
    if isinstance(value, numbers.Real):
        int_value = int(value)
        if int_value == value:
            if value == 0:
                return kind_zero
            elif value < 0:
                raise ValueError('Negative numbers are not ordinals.')
            else:
                return kind_successor
        raise ValueError('Non-integer numbers are not ordinals.')
    if isinstance(value, ordinal):
        return value._kind
    raise ValueError('Value is not of a known type representing a mathematical ordinal.')

def tier(value):
    """
    A special function of ordinals which does not
      correspond to any mathematically useful function.
    Maps ordinals to small objects, effectively compressing the range.
    Used to speed up comparisons when the operands are very different sizes.

    In the current version, this is a map from ordinals to 2-tuples of integers,
      however, this is subject to change at any time, so please do not retain
      long lived records of what tier an ordinal number is.
    """
    if isinstance(value, numbers.Real):
        value = ordinal(value)
    if isinstance(value, ordinal):
        return value._tier
    raise ValueError('Value is not of a known type representing a mathematical ordinal.')

class ordinal(ordinal_type):
    """
    Programmatic implementation of ordinal numbers.
    Treat them like immutable objects.
    Works by separating the ordinal into additive pieces, and
      arranging those pieces into the smallest hierarchy that contains it.
    Current hierarchies are the ordinals up to
      omega, epsilon_0, gamma_0 (Feferman–Schütte ordinal)
      represented by the
      natural numbers, Cantor normal form, Veblen normal form
      respectively.
    This means it is theoretically possible, using this class,
      to represent ordinals up to but not including gamma_0
      using this class.
    Arithmetic operations work fine below epsilon_0, but some may
      break above epsilon_0, because the Veblen normal form cannot
      represent the results. Note however, that if you only ever use
      addition and the Veblen function, then all values can be represented,
      and nothing breaks. You cannot actually get to epsilon_0 using
      only the basic arithmetic operators and without limits, so,
      in summary, do not mix (multiplication and exponetiation) and the
      Veblen function.
    All ordinal operations in this module are implemented by this class,
      but it is recommended to use the regular operator symbols
      and static utility functions
      rather than call the methods directly.
    """
    def __init__(self, value=None, name=None, _nat=None, _cnf=None, _vnf=None, copy=False):
        """
        Ordinal constructor.
        Simple usage is to hand it some value and let it take care of the conversion.
        If given an ordinal, prefers to not make copies of objects,
          unless the flag is set to True, then it makes a shallow copy.
        Detailed construction parameters are meant for internal use,
          and invariants will not be checked.
        """
        # Try to construct from value - how it is usually used by a user
        if value is not None:
            if isinstance(value, str):
                self.__init__(name = value)
                return
            if isinstance(value, int):
                if value < 0:
                    raise ValueError('Integer ordinal cannot be negative')
                self.__init__(_nat = value)
                return
            if isinstance(value, ordinal):
                _nat = value._nat
                _cnf = value._cnf
                _vnf = value._vnf
                if copy:
                    _cnf = list(_cnf)
                    _vnf = list(_vnf)
                self.__init__(_nat = _nat, _cnf = _cnf, _vnf = _vnf)
            raise TypeError('Cannot convert from this value type')
        # Is this a specific named ordinal?
        if name in _omega_aliases:
            self.__init__(_cnf = [(1, 1)])
            return
        if name in _epsilon_0_aliases:
            self.__init__(_vnf = [(1, 0, 1)])
            return
        if name in _zeta_0_aliases:
            self.__init__(_vnf = [(2, 0, 1)])
            return
        if name is not None:
            raise ValueError('Named ordinal unknown')
        # Use the internal representation
        # VNF + CNF + NAT
        # In CNF, (p, c) represents omega^p dot c
        #   every term is at least omega, so p > 0
        # In VNF, (s, i, c) represents phi_s(i) dot c
        #   every term is at least epsilon_0, but this does not guarantee s > 0
        if _nat is None:
            _nat = 0
        if _cnf is None:
            _cnf = []
        if _vnf is None:
            _vnf = []
        self._nat = _nat
        self._cnf = _cnf
        self._vnf = _vnf
        # Precompute the hash
        self._hash = hash((ordinal, self._nat) + tuple(self._cnf) + tuple(self._vnf))
        # Precompute the kind
        if self._nat == 0:
            if self._cnf or self._vnf:
                self._kind = kind_limit
            else:
                self._kind = kind_zero
        else:
            self._kind = kind_successor
        # Precompute the tier
        if self._vnf:
            _tier = tier(self._vnf[0][0])
            _tier = (_tier[0] + 2, _tier[1])
        elif self._cnf:
            _tier = tier(self._cnf[0][0])
            _tier = (1, (_tier[0] and _tier[1]) + 1)
        else:
            _tier = (0, bin_log(self._nat))
        self._tier = _tier
    def __hash__(self):
        return self._hash
    def __str__(self):
        bits = []
        for s, i, c in self._vnf:
            if s == 0:
                bit = '\\omega^{' + str(i) + '}'
            else:
                bit = '\\varphi_' + str(s) + '(' + str(i) + ')'
            if c != 1:
                bit = bit + ' \\cdot ' + str(c)
            bits.append(bit)
        for p, c in self._cnf:
            bit = '\\omega'
            if p != 1:
                bit = bit + '^{' + str(p) + '}'
            if c != 1:
                bit = bit + ' \\cdot ' + str(c)
            bits.append(bit)
        if self._nat:
            bits.append(str(self._nat))
        if not bits:
            return '0'
        return '{' + ' + '.join(bits) + '}'
    def __repr__(self):
        return 'ordinal(_nat = ' + repr(self._nat) + ', _cnf = ' + repr(self._cnf) + ', _vnf = ' + repr(self._vnf) + ')'
    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, numbers.Real):
            if self._cnf or self._vnf:
                return False
            return self._nat == other
        if not isinstance(other, ordinal):
            return False
        if hash(self) != hash(other):return False
        if self._tier != other._tier:return False
        return self._vnf == other._vnf and self._cnf == other._cnf and self._nat == other._nat
    def __ne__(self, other):
        return not self == other
    @staticmethod
    def _veblen_cmp(a, b):
        """
        For internal use:
        return the sign of a - b
        where a and b represent terms in the VNF
        """
        # comparator-like function for other types
        def _cmp(x, y):
            if x == y:return 0
            if x < y:return -1
            return 1
        # unwrap a and b
        asub, aindex, acount = a
        bsub, bindex, bcount = b
        # fixed point unwrapping:
        #   phi_A (B) N <> phi_C (D) M
        #   this is the magic step
        #   (phi_A (B), N) <> (phi_C (D), M)
        #     why can we do this?
        #     suppose phi_A (B) = phi_C (D)
        #     then
        #       phi_A (B) N <> phi_C (D) M
        #       is the same as
        #       N <> M
        #     now suppose without loss of generality that phi_A (B) > phi_C (D)
        #     the Veblen function grows really fast
        #     the absolute lower bound is phi_A (B) >= phi_C (D) omega
        #     this occurs with ex. phi_0 (E + 1) <> phi_0 (E)
        #     this omega multiply is already bigger than any constant
        #     so the constants won't matter
        #   let us see how to handle phi_A (B) <> phi_C (D)
        #   since N <> M is really easy
        #   suppose A < C
        #   phi_A (B) <> phi_C (D)
        #   phi_A (B) <> phi_A ( phi_C (D))
        #   B <> phi_C (D)
        if asub < bsub:
            a2 = aindex
            b2 = ordinal(_vnf = [b[:-1] + (1,)])
            return _cmp((a2, acount), (b2, bcount))
        if asub > bsub:
            a2 = ordinal(_vnf = [a[:-1] + (1,)])
            b2 = bindex
            return _cmp((a2, acount), (b2, bcount))
        # asub == bsub
        return _cmp((aindex, acount), (bindex, bcount))
    def __lt__(self, other):
        if self is other:
            return False
        if isinstance(other, numbers.Real):
            if self._cnf or self._vnf:
                return False
            return self._nat < other
        if not isinstance(other, ordinal):
            raise TypeError('Cannot compare an ordinal with this type')
        if hash(self) == hash(other):return False
        if self._tier < other._tier:return True
        if self._tier > other._tier:return False
        vnf_key = functools.cmp_to_key(ordinal._veblen_cmp)
        return (tuple(map(vnf_key, self._vnf)), self._cnf, self._nat) < (tuple(map(vnf_key, other._vnf)), other._cnf, other._nat)
    def __le__(self, other):
        if self is other:
            return True
        if isinstance(other, numbers.Real):
            if self._cnf or self._vnf:
                return False
            return self._nat <= other
        if not isinstance(other, ordinal):
            raise TypeError('Cannot compare an ordinal with this type')
        if hash(self) == hash(other):return True
        if self._tier < other._tier:return True
        if self._tier > other._tier:return False
        vnf_key = functools.cmp_to_key(ordinal._veblen_cmp)
        return (tuple(map(vnf_key, self._vnf)), self._cnf, self._nat) <= (tuple(map(vnf_key, other._vnf)), other._cnf, other._nat)
    def __gt__(self, other):
        return not self <= other
    def __ge__(self, other):
        return not self < other
    def __pos__(self):
        return self
    def __neg__(self):
        if self == 0:return 0
        raise ValueError('Cannot negate a positive ordinal')
    def __add__(self, other):
        """
        Sum of 2 ordinal numbers.
        """
        # We first handle the type stuff
        if isinstance(other, int):
            if other < 0:
                raise ValueError('Cannot add negative integers to ordinals')
            rvnf = self._vnf
            rcnf = self._cnf
            rnat = self._nat + other
            return ordinal(_nat = rnat, _cnf = rcnf, _vnf = rvnf)
        if not isinstance(other, ordinal):
            raise TypeError('Unknown type being added to an ordinal')
        # Addition is pretty simple!
        # Addition is associative, so we can break up left and right operands however we want
        # Here is the key rule for reducing a term:
        #   omega^A N + omega^B M =
        #     A < B --> omega^B M
        #     A = B --> omega^A (N + M)
        #     A > B --> no reduction possible
        # To summarize: when the left is smaller, it gets erased,
        #   and multiplication left distributes over addition.
        if other._vnf:
            # Right argument has largest term in the VNF range
            rvnf = list(self._vnf)
            ovnf = other._vnf
            while rvnf and ordinal._veblen_cmp(rvnf[-1][0:2] + (1,), ovnf[0][0:2] + (1,)) < 0:
                del rvnf[-1]
            if rvnf and ordinal._veblen_cmp(rvnf[-1][0:2] + (1,), ovnf[0][0:2] + (1,)) == 0:
                last = rvnf[-1]
                rvnf[-1] = (last[0], last[1], last[2] + ovnf[0][2])
                ovnf = ovnf[1:]
            rvnf += ovnf
            rcnf = other._cnf
            rnat = other._nat
            return ordinal(_nat = rnat, _cnf = rcnf, _vnf = rvnf)
        if other._cnf:
            # Right argument has largest item in the CNF range
            rvnf = self._vnf
            rcnf = list(self._cnf)
            ocnf = other._cnf
            while rcnf and rcnf[-1][0] < ocnf[0][0]:
                del rcnf[-1]
            if rcnf and rcnf[-1][0] == ocnf[0][0]:
                last = rcnf[-1]
                rcnf[-1] = (last[0], last[1] + ocnf[0][1])
                ocnf = ocnf[1:]
            rcnf += ocnf
            rnat = other._nat
            return ordinal(_nat = rnat, _cnf = rcnf, _vnf = rvnf)
        # Right argument is a natural number
        rvnf = self._vnf
        rcnf = self._cnf
        rnat = self._nat + other._nat
        return ordinal(_nat = rnat, _cnf = rcnf, _vnf = rvnf)
    def __radd__(self, other):
        return ordinal(other) + self
    def __mul__(self, other):
        """
        Product of 2 ordinal numbers.
        """
        # some small exceptional cases
        if other == 0:
            # rule: A * 0 --> 0
            return 0
        if other == 1:
            # rule: A * 1 --> A
            return self
        if self == 0:
            # rule: 0 * A --> 0
            return 0
        if self == 1:
            # rule: 1 * A --> A
            return other
         # We first handle the type stuff
        if isinstance(other, int):
            if other < 0:
                raise ValueError('Cannot multiply ordinals by negative numbers')
            rvnf = [(s, i, c * other) for s,i,c in self._vnf]
            rcnf = [(p, c * other) for p,c in self._cnf]
            rnat = self._nat * other
            return ordinal(_nat = rnat, _cnf = rcnf, _vnf = rvnf)
        if not isinstance(other, ordinal):
            raise TypeError('Unknown type trying to multiply an ordinal by')
        pieces = []
        # we will left distribute and multiply
        # it is important to know which hierarchy the left operand lands in
        if self._vnf:
            self_h = 2
            self_top = self._vnf[0]
        elif self._cnf:
            self_h = 1
            self_top = self._cnf[0]
        else:
            self_h = 0
            self_top = self._nat
        def _exp_add(l_up, r_up, rc):
            """
            Computes the ordinal omega^(A + B) C
            Intended for when the result is known to fall in the Veblen hierarchy.
            """
            up = l_up + r_up
            if len(up._vnf) == 1 and up._vnf[0][0] != 0 and up._vnf[0][2] == 1:
                uv = up._vnf[0]
                return ordinal(_vnf = [uv[:-1] + (uv[-1] * rc,)])
            else:
                return ordinal(_vnf = [(0, up, rc)])
        def _term_mul(l_h, l_value, r_h, r_value):
            """
            Product of a multiplicative term.
            """
            # since all of these are additively indecomposable
            #   (multiplicative terms)
            #   they are either natural numbers or limit ordinals
            if r_h == 0:
                if l_h == 0:
                    return ordinal(_nat = l_value * r_value)
                if l_h == 1:
                    return ordinal(_cnf = [l_value[:-1] + (l_value[-1] * r_value,)])
                if l_h == 2:
                    return ordinal(_vnf = [l_value[:-1] + (l_value[-1] * r_value,)])
            if r_h == 1:
                if l_h == 0:
                    return ordinal(_cnf = [r_value])
                if l_h == 1:
                    return ordinal(_cnf = [(l_value[0] + r_value[0], r_value[1])])
                if l_h == 2:
                    l_up = ordinal(_vnf = [l_value]) if l_value[0] != 0 else l_value[1]
                    r_up = r_value[0]
                    return _exp_add(l_up, r_up, r_value[-1])
            if r_h == 2:
                if l_h == 0:
                    return ordinal(_vnf = [r_value])
                if l_h == 1:
                    l_up = l_value[0]
                    r_up = ordinal(_vnf = [r_value]) if r_value[0] != 0 else r_value[1]
                    return _exp_add(l_up, r_up, r_value[-1])
                if l_h == 2:
                    l_up = ordinal(_vnf = [l_value]) if l_value[0] != 0 else l_value[1]
                    r_up = ordinal(_vnf = [r_value]) if r_value[0] != 0 else r_value[1]
                    return _exp_add(l_up, r_up, r_value[-1])
        for otup in other._vnf:
            pieces.append(_term_mul(self_h, self_top, 2, otup))
        for otup in other._cnf:
            pieces.append(_term_mul(self_h, self_top, 1, otup))
        if other._nat != 0:
            pieces.append(_term_mul(self_h, self_top, 0, other._nat))
            if self_h == 2:
                rem = ordinal(_vnf = self._vnf[1:], _cnf = self._cnf, _nat = self._nat)
            elif self_h == 1:
                rem = ordinal(_cnf = self._cnf[1:], _nat = self._nat)
            elif self_h == 0:
                rem = 0
            pieces.append(rem)
        return sum_bisected(pieces)
    def __rmul__(self, other):
        return ordinal(other) * self

def veblen(sub, value):
    """
    Computes phi_sub(value) where phi is the Veblen function.
    In summary,
    - phi_0(x) = omega^x
    - phi_y(0) is the smallest ordinal z such that for all
        w < y, phi_w(z) = z
    - phi_y(x+1) is the smallest ordinal z greater than phi_y(x)
        and such that for all
        w < y, phi_w(z) = z
    As an example, phi_1(0) = epsilon_0 which is the first
      fixed point of x = omega^x.
    For more of the mathematical fine details
      and to see how the Veblen function handles transfinite arguments,
      do your own research.
    A full explanation will not fit nicely in this doc comment.
    """
    # there might be fixed points!
    if isinstance(value, ordinal) and len(value._vnf) == 1 and not value._cnf and not value._nat and value._vnf[0][0] > sub and value._vnf[0][2] == 1:
        # yes, it is a fixed point
        return value
    # do the Veblen stuff normally
    if sub == 0:
        # subscript 0 is the special case that ends the recursive definition
        if value == 0:
            return 1
        # if ordinal is in the Veblen hierarchy, we must stay in the Veblen hierarchy
        if isinstance(value, ordinal) and value._vnf:
            return ordinal(_vnf = [(0, value, 1)])
        # below epsilon_0
        return ordinal(_cnf = [(value, 1)])
    # otherwise we just build the Veblen normal form directly
    return ordinal(_vnf = [(sub, value, 1)])

_omega_aliases = {'omega','w','\\omega'}
_epsilon_0_aliases = {'epsilon_0','epsilon0','eps_0','eps0','e_0','e0','\\epsilon_0'}
_zeta_0_aliases = {'zeta_0','zeta0','z_0','z0','\\zeta_0'}

omega = ordinal('omega')
epsilon_0 = ordinal('epsilon_0')
zeta_0 = ordinal('zeta_0')
