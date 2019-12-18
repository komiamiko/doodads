"""
Small library for working with ordinal numbers.
Currently implements ordinals up to the Feferman–Schütte ordinal Γ₀ = φ(1, 0, 0)
Can do arithmetic and take fundamental sequences, and stringifies to LaTeX.
"""

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

def pow_sq(x, y):
    """
    Compute x^y, without calling its pow,
    using exponentiation by squaring.
    """
    r = 1
    while y:
        if y & 1:
            r = r * x
        x = x * x
        y >>= 1
    return r

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

def predecessor(value):
    """
    Commonly used operation which takes the predecessor of a successor ordinal.
    Implemented as its own function because ordinals don't allow subtraction directly.
    """
    if kind(value) != kind_successor:
        raise ValueError('Predecessor not defined for ordinals other than successor ordinals')
    if isinstance(value, numbers.Real):
        return value - 1
    return ordinal(_vnf = value._vnf, _cnf = value._cnf, _nat = value._nat - 1)

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
            elif isinstance(value, int):
                if value < 0:
                    raise ValueError('Integer ordinal cannot be negative')
                self.__init__(_nat = value)
                return
            elif isinstance(value, ordinal):
                _nat = value._nat
                _cnf = value._cnf
                _vnf = value._vnf
                if copy:
                    _cnf = list(_cnf)
                    _vnf = list(_vnf)
                self.__init__(_nat = _nat, _cnf = _cnf, _vnf = _vnf)
            else:
                raise TypeError('Cannot convert from this value type')
        # Is this a specific named ordinal?
        if name in _omega_aliases:
            self.__init__(_cnf = [(1, 1)])
            return
        elif name in _epsilon_0_aliases:
            self.__init__(_vnf = [(1, 0, 1)])
            return
        elif name in _zeta_0_aliases:
            self.__init__(_vnf = [(2, 0, 1)])
            return
        elif name is not None:
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
        _hash = hash(self._nat)
        if self._cnf:
            _hash = hash((_hash, 1, tuple(self._cnf)))
        if self._vnf:
            _hash = hash((_hash, 2, tuple(self._vnf)))
        self._hash = _hash
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
            # for the Veblen hierarchy, tier computation is a bit more complicated
            # there are fixed points and things that aren't fixed points
            # roughly, when evaluating phi_A (B) we compare phi_A (0) to B
            # if B is small, phi_A (B) > phi_A (0) > B
            # in this case A is more useful for calculating the tier
            # if B is big, phi_A (B) >= B >= phi_A (0)
            # in this case B is more useful for calculating the tier
            _tier_sub = tier(self._vnf[0][0])
            _tier_sub = (_tier_sub[0] + 2, _tier_sub[1])
            _tier_index = tier(self._vnf[0][1])
            _tier = max(_tier_sub, _tier_index)
        elif self._cnf:
            # uses the height of the largest term
            _tier = tier(self._cnf[0][0])
            _tier = (1, (_tier[0] and _tier[1]) + 1)
        else:
            _tier = (0, bin_log(self._nat))
        self._tier = _tier
        # fundamental sequence is lazily calculated
        self._fundamental = None
    def __hash__(self):
        return self._hash
    def __str__(self):
        # keep consistent format that makes sense for the hierarchy
        normalize_at = 0
        if self._vnf and self._vnf[0][0] >= omega:
            normalize_at = 2
        elif self._vnf and self._vnf[0][0] >= 3:
            normalize_at = 1
        def _str(self):
            if not isinstance(self, ordinal):
                return '{' + str(self) + '}'
            bits = []
            for s, i, c in self._vnf:
                if s == 0 and normalize_at == 0:
                    bit = '\\omega^{' + \
                          _str(i) + '}'
                elif s == 1 and normalize_at == 0:
                    bit = '\\varepsilon_{' + \
                          _str(i) + '}'
                elif s == 2 and normalize_at == 0:
                    bit = '\\zeta_{' + \
                          _str(i) + '}'
                elif normalize_at <= 1:
                    bit = '\\varphi_' + \
                          _str(s) + '(' + \
                          _str(i) + ')'
                else:
                    bit = '\\varphi(' + \
                          _str(s) + ', ' + \
                          _str(i) + ')'
                if c != 1:
                    bit = bit + ' \\cdot ' + _str(c)
                bits.append(bit)
            for p, c in self._cnf:
                if normalize_at == 0:
                    bit = '\\omega'
                    if p != 1:
                        bit = bit + '^' + _str(p)
                elif normalize_at == 1:
                    bit = '\\varphi_0(' + \
                          _str(p) + ')'
                else:
                    bit = '\\varphi(0, ' + \
                          _str(p) + ')'
                if c != 1:
                    bit = bit + ' \\cdot ' + _str(c)
                bits.append(bit)
            if self._nat:
                bits.append(_str(self._nat))
            if not bits:
                return '0'
            return '{' + ' + '.join(bits) + '}'
        return _str(self)
    def __repr__(self):
        return 'ordinal(_nat = ' + repr(self._nat) + ', _cnf = ' + repr(self._cnf) + ', _vnf = ' + repr(self._vnf) + ')'
    def __int__(self):
        if self._vnf or self._cnf:
            raise ValueError('Cannot convert infinite ordinal to integer')
        return self._nat
    def __bool__(self):
        return self != 0
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
    def _get_fundamental(self):
        """
        Returns the fundamental sequence for this ordinal.
        Constructs it if necessary.
        """
        if self._fundamental is None:
            self._fundamental = fundamental(self)
        return self._fundamental
    def __iter__(self):
        """
        Iterate over this ordinal's fundamental sequence.
        For more information, see the fundamental class.
        """
        return iter(self._get_fundamental())
    def __getitem__(self, index):
        """
        Get the item at some index of this ordinal's fundamental sequence.
        For more information, see the fundamental class.
        """
        return self._get_fundamental()[index]
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
            # there's too much rules, don't bother re-implementing
            other = ordinal(other)
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
            if len(up._vnf) == 1 and not up._cnf and not up._nat and up._vnf[0][0] != 0 and up._vnf[0][2] == 1:
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
                    l_up = ordinal(_vnf = [l_value[:-1] + (1,)]) if l_value[0] != 0 else l_value[1]
                    r_up = r_value[0]
                    return _exp_add(l_up, r_up, r_value[-1])
            if r_h == 2:
                if l_h == 0:
                    return ordinal(_vnf = [r_value])
                if l_h == 1:
                    l_up = l_value[0]
                    r_up = ordinal(_vnf = [r_value[:-1] + (1,)]) if r_value[0] != 0 else r_value[1]
                    return _exp_add(l_up, r_up, r_value[-1])
                if l_h == 2:
                    l_up = ordinal(_vnf = [l_value[:-1] + (1,)]) if l_value[0] != 0 else l_value[1]
                    r_up = ordinal(_vnf = [r_value[:-1] + (1,)]) if r_value[0] != 0 else r_value[1]
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
    def __pow__(self, other):
        """
        Power of 2 ordinals.
        """
        # some small exceptional cases
        # rule: A^0 = 1
        # rule: 1^B = 1
        if other == 0 or self == 1:return 1
        # rule: A^1 = A
        if other == 1:return self
        # rule: 0^B = 0 (except B=0, which we already covered)
        if self == 0:return 0
        # is this a natural number?
        if self < omega:
            s = int(self)
            if other < omega:
                # shortcut, use integer power
                return s ** int(other)
            # self is integer but other is infinite ordinal
            # rule: n^(wB) = w^B
            # thus we must "left decrement" the other exponents
            # Veblen hierarchy is entirely unaffected
            rvnf = other._vnf
            # CNF hierarchy is only affected for finite exponents
            rcnf = []
            rnat = 0
            for p, n in other._cnf:
                if p == 1:
                    # special case 1 -> 0 degrades to natural number
                    rnat = n
                elif p < omega:
                    rcnf.append((int(p) - 1, n))
                else:
                    rcnf.append((p, n))
            # construct the result
            base = veblen(0, ordinal(_vnf = rvnf, _cnf = rcnf, _nat = rnat))
            # and then handle the natural number term if needed
            if other._nat:
                mul = s ** other._nat
                base = base * mul
            # finally, return it
            return base
        # rules from here for A^B
        # if B is a limit ordinal
        #   let C be the largest term of A (erase coefficient)
        #   result = C^B
        # if B = D + 1 for some D
        #   let Cn be the largest term of A
        #   result = C^D n A
        #   note the n only matters if A has a natural number term,
        #   because every other term in A ultimately erases it
        other = ordinal(other)
        osucc = kind(other) == kind_successor
        # also branch based on whether we have self as successor since that tends to be annoying
        if osucc and kind(self) == kind_successor:
            case = 2
        elif osucc:
            case = 1
        else:
            case = 0
        # handle the common exponent part, from the exponent
        if case == 2:
            exp = ordinal(_vnf = other._vnf, _cnf = other._cnf)
        elif case == 1:
            exp = ordinal(_vnf = other._vnf, _cnf = other._cnf, _nat = other._nat - 1)
        else:
            exp = other
        # do a sort of X -> exp(log(X)) thing on the base largest part
        if self._vnf:
            # self falls in Veblen hierarchy
            # extract the coefficient
            exn = self._vnf[0][-1]
            # may or may not be a fixed point of exp
            if self._vnf[0][0] == 0:
                base = self._vnf[0][1]
            else:
                base = ordinal(_vnf = [self._vnf[0][:-1]+(1,)])
        else:
            # self falls in CNF hierarchy
            # extract the coefficient
            exn = self._cnf[0][-1]
            # just grab the exponent, CNF definition allows it
            base = self._cnf[0][0]
        # combine the exponent we got with the other exponent
        base = veblen(0, base * exp)
        # only multiplication left, and that's already implemented!
        if case == 2:
            # there doesn't seem to be an efficient way to telescope this when
            # self is a successor ordinal
            # so let's just do exponentiation by squaring to finish it
            return base * pow_sq(self, other._nat)
        if case == 1:
            return base * exn * self
        return base
    def __rpow__(self, other):
        return ordinal(other) ** self

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

class fundamental(object):
    """
    Class representing a fundamental sequence for limit ordinals.
    The fundamental sequence of an ordinal is defined
      if and only if it is a limit ordinal.
    Currently does not extend the sequence type. Reason is that this
      is an immutable infinite sequence, and time to construct the Nth
      ordinal in the sequence given the previous ordinal is not always O(1),
      in fact, it is commonly O(N) for ordinals in the Veblen hierarchy,
      which makes it O(N^2) to compute the first N items.
      The person making this does not know if that is the worst case.
    """
    def __init__(self, value, cache_every=16):
        """
        Construct the fundamental sequence object for a given ordinal.
        Raises an error if the ordinal is not a limit ordinal, because the type is undefined.
        To help manage the cost of computation, this class will make a memory tradeoff
          and store the intermediate computations for every Cth item, for some parameter C,
          for ordinals where this kind of optimization can save time.
          By default, C=16, which makes for a small memory footprint while limiting
          improving the worst case by a factor of O(N), where N is the number of items.
        """
        if not isinstance(value, ordinal):
            raise TypeError('Value is not an ordinal number.')
        if kind(value) != kind_limit:
            raise ValueError('Not a limit ordinal, no fundamental sequence exists')
        import functools
        import operator
        # remember where this is coming from
        self.source = value
        # find a formula for it as
        # A[n] = direct(n) with cache
        # or
        # A[n] = step^n (start) with cache
        # or
        # A[n] = index[n] without cache
        # applies "then" function after, if it exists
        start = 0
        self._direct = self._step = self._then = self._index = self._cache = None
        to_index = None
        if len(value._vnf) + len(value._cnf) > 1:
            if value._cnf:
                to_add = ordinal(_vnf=value._vnf, _cnf=value._cnf[:-1])
                to_index = ordinal(_cnf=[value._cnf[-1]])
            else:
                to_add = ordinal(_vnf=value._vnf[:-1])
                to_index = ordinal(_vnf=[value._vnf[-1]])
            self._then = functools.partial(operator.add, to_add)
        elif value._vnf:
            term = value._vnf[0]
            if term[-1] > 1:
                to_add = ordinal(_vnf=[term[:-1] + (term[-1] - 1,)])
                to_index = ordinal(_vnf=[term[:-1] + (1,)])
                self._then = functools.partial(operator.add, to_add)
            elif kind(term[1]) == kind_limit:
                to_index = term[1]
                self._then = functools.partial(veblen, term[0])
            elif term[0] == 0:
                # it's in the veblen hierarchy, so we can skip checking for plain omega^1
                #   (furthermore, something later down eventually invokes the veblen function)
                # we also already checked for limit argument
                # so it must be a successor!
                to_mul = veblen(0, predecessor(term[1]))
                self._direct = (lambda n:n)
                self._then = functools.partial(operator.mul, to_mul)
            elif kind(term[0]) == kind_successor:
                if term[1] != 0:
                    start = veblen(term[0], predecessor(term[1])) + 1
                to_sub = predecessor(term[0])
                self._step = functools.partial(veblen, to_sub)
            else:
                if term[1] == 0:
                    to_arg = 0
                else:
                    to_arg = veblen(term[0], predecessor(term[1])) + 1
                to_index = term[0]
                self._then = (lambda a:veblen(a, to_arg))
        else:
            term = value._cnf[0]
            if term[-1] > 1:
                to_add = ordinal(_cnf=[term[:-1] + (term[-1] - 1,)])
                to_index = ordinal(_cnf=[term[:-1] + (1,)])
                self._then = functools.partial(operator.add, to_add)
            elif term[0] == 1:
                self._direct = (lambda n:n)
            elif kind(term[0]) == kind_successor:
                to_mul = veblen(0, predecessor(term[0]))
                self._direct = (lambda n:n)
                self._then = functools.partial(operator.mul, to_mul)
            else:
                to_index = term[0]
                self._then = functools.partial(veblen, 0)
        if to_index is not None:
            self._index = fundamental(to_index, cache_every = cache_every)
        if self._step is not None:
            self._cache = [start]
        self.cache_every = cache_every
    def __str__(self):
        return str(self.source) + '[\\cdot]'
    def __repr__(self):
        return 'fundamental(' + repr(self.source) + ')'
    def __hash__(self):
        return hash((fundamental, self.source))
    def __eq__(self, other):
        if self is other:return True
        if not hasattr(other, 'source'):return False
        return self.source == other.source
    def __ne__(self, other):
        return not self == other
    def __iter__(self):
        import itertools
        import functools
        import operator
        return iter(map(functools.partial(operator.getitem, self), itertools.count()))
    def __getitem__(self, n):
        if self._direct is not None:
            result = self._direct(n)
        elif self._index is not None:
            result = self._index[n]
        else:
            ce = self.cache_every
            l, s = divmod(n, ce)
            while len(self._cache) <= l:
                last = self._cache[-1]
                for _ in range(ce):
                    last = self._step(last)
                self._cache.append(last)
            last = self._cache[l]
            for _ in range(s):
                last = self._step(last)
            result = last
        if self._then is not None:
            result = self._then(result)
        return result

_omega_aliases = {'omega','w','\\omega'}
_epsilon_0_aliases = {'epsilon_0','epsilon0','eps_0','eps0','e_0','e0','\\epsilon_0'}
_zeta_0_aliases = {'zeta_0','zeta0','z_0','z0','\\zeta_0'}

omega = ordinal('omega')
epsilon_0 = ordinal('epsilon_0')
zeta_0 = ordinal('zeta_0')

def fast_growing_hierarchy(sub, value, limit_steps=None, limit_complexity=1.0, convert_to='latex', printer=None):
    """
    Fun function to do an expansion of a
    fast growing hierarchy (FGH) expression.
    FGH in all variants are defined like so:

      f  (n) = n + 1
       0

                 n
      f   (n) = f (n)
       α+1       α

      f (n) = f    (n)
       α       α[n]

    This covers values for zero, successor, and limit ordinals.
    FGH variants differ sometimes in the choice of f_0,
    but mostly in the fundamental sequences used.
    They are useful for quantifying the sizes of large numbers
    due to the simple recursive structure.

    This 

    The expression we will expand is:

      f   (value)
       sub

    We don't want to write out very large numbers
    or unreadable expressions.
    In general, you will never see:
    - numbers above 1 million or so
    - predecessor chains longer than 2
    - nested brackets/subscripts/superscripts chaining more than 2
    The bounds are mostly hardcoded. (see limit_complexity parameter)

    Additional parameters:
    - limit_steps - set a maximum number of steps
    - limit_complexity - factor to tune the maximum allowed complexity, where we allow it
    - convert_to - what type to convert to, can use None to spit out raw data
    - printer - if specified, prints at each step
    """
    if limit_steps is None:
        limit_steps = 2**63-1
    if convert_to is None:
        convert = (lambda x,y:(x,y))
    elif convert_to == 'latex':
        def convert(li, n):
            if not li:return '{' + str(n) + '}'
            def cterm(term):
                result = 'f_{' + str(term[0]) + '}'
                if term[1] > 1:
                    result += '^{' + str(term[1]) + '}'
                return result
            return '{' + ' \\circ '.join(map(cterm, li)) + '(' + str(n) + ')}'
    else:
        raise ValueError(f'Do not know how to convert to type "{convert_to}"')
    li = [(sub, 1)]
    n = value
    if printer:printer(convert(li, n))
    def add_func(tup):
        """
        Adds the function if the iteration count is nonzero.
        """
        if tup[1]:
            li.append(tup)
    def complexity(value):
        """
        Estimate the "complexity" of an ordinal.
        Used to limit deep expansion.
        """
        if value <= 1:return 1
        if value < omega:return 3
        return sum(map(lambda x:6+sum(map(complexity, x)), value._vnf)) + \
               sum(map(lambda x:4+sum(map(complexity, x)), value._cnf)) + \
               complexity(value._nat)
    for _ in range(limit_steps):
        lsub, lcount = li.pop()
        # do our rules permit expanding the last one?
        if lsub <= 2:
            if lsub == 0:
                n += lcount
            elif lsub == 1:
                times = min(lcount, bin_log(10**6//n))
                if times == 0:break
                n *= 2**times
                lcount -= times
                add_func((lsub, lcount))
            elif lsub == 2:
                if n > 16:break
                n = 2**n * n
                lcount -= 1
                add_func((lsub, lcount))
        elif kind(lsub) == kind_successor:
            if (lsub > 4 if lsub < omega else lsub._nat > 2):break
            lcount -= 1
            add_func((lsub, lcount))
            add_func((predecessor(lsub), n))
        else:
            if lsub >= veblen(3, 0) and n > 1 + limit_complexity or \
               lsub >= epsilon_0 and n > 2 + limit_complexity:break
            nx = lsub[n]
            if complexity(nx) >= 30 * limit_complexity:break
            lcount -= 1
            add_func((lsub, lcount))
            add_func((nx, 1))
        if printer:printer(convert(li, n))
        if not li:break
        if len(li) >= 2 + 3 * limit_complexity:break
    return convert(li, n)

fgh = fast_growing_hierarchy
