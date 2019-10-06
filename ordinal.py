"""
Small library for working with ordinal numbers, including transfinite numbers.
Warning: the math here has not been verified by a math expert.
"""

import warnings
import numbers

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
        return to_ordinal(self) ** other
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
    def __add__(self, other):
        """
        Sum of 2 ordinal numbers.
        Note that, in general, addition is not commutative.
        As an easy way to remember: small parts of the left operand are erased.
        """
        ocnf = to_ordinal(other).cnf
        # if other is blank, then we are done
        if not ocnf:return self
        rcnf = list(self.cnf)
        ofirst, *ocnf = ocnf
        # erase small parts
        while rcnf and rcnf[-1][0] < ofirst[0]:
            del rcnf[-1]
        # possibly combine first
        if rcnf and rcnf[-1][0] == ofirst[0]:
            rcnf[-1] = (ofirst[0], rcnf[-1][1] + ofirst[1])
        else:
            rcnf.append(ofirst)
        # attach the rest
        rcnf += list(ocnf)
        return ordinal(rcnf)
