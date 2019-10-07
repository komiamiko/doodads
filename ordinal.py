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
    def __eq__(self, other):
        return isinstance(other, _omega_t)
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        if isinstance(other, (numbers.Real, _omega_t)):
            return False
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
    def __eq__(self, other):
        return self.cnf == to_ordinal(other).cnf
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return self.cnf < to_ordinal(other).cnf
    def __le__(self, other):
        return self.cnf <= to_ordinal(other).cnf
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return not (self < other)
    def __hash__(self):
        return hash((ordinal,) + tuple(self.cnf))
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
            # result is left argument
            if q != 0:
                m = n * m
            # exponents are added
            # addition is strictly increasing in the right argument,
            # so this q is guaranteed to be less than the previous q
            q = p + q
            # just add the term
            rcnf.append((q, m))
        return ordinal(rcnf)
