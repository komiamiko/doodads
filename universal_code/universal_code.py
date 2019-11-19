"""
Implements various universal codes,
which map non-negative integers to bit strings as a prefix code.

Recommendations:
- elias_omega or elias_omega_alt are good for integers in the sane range, pick your favourite
- unary if the input stream is almost entirely 0 and 1 and numbers are very small in general
- consider using data compression on top of any code you choose for further compression on real world inputs

We may define a normalized universal code as having additional properties:
- codewords form a complete prefix code that bijects integer sequences and bitstreams
- codewords are lexicographically ordered: enc(n) < enc(n+1)
- codewords have non-decreasing length: |enc(n)| <= |enc(n+1)|
From there, we get some basic facts:
- no codeword is empty
- no codeword has only 1s
- every codeword contains a 0
Finally we can characterize them by some special functions.
Let U(n) be the number of leading 1s in enc(n).
Note that U(n) is nondecreasing, and a slower growing code has slower growing U(n).
Also note that U(n) does not skip any numbers, since that would imply a non-decodable bitstream exists.
Let G(m)=n be the smallest n such that U(n)=m.
If U grows slower, G grows faster, and vice versa.
With the restrictions on what U and G can be, there is a bijection between Us and Gs.
The growth rate of G can be used to characterize the optimality of a universal code.
Since a faster G can always be constructed, a slower U can always be constructed, and there is no perfect slowest growing universal code.
Interesting result aside, we do also give G in the info, or an approximation if the exact G would be too verbose.
"""

def make_decoder(decode_stream, fast):
    def _decode_notfast(s):
        it = iter(s)
        try:
            r = next(decode_stream(it))
        except StopIteration:
            raise ValueError('No full word to decode')
        try:
            next(it)
            raise ValueError('Unread symbols at the end')
        except StopIteration:
            pass
        return r
    def _decode_fast(s):
        return next(decode_stream(it))
    return _decode_fast if fast else _decode_notfast

class universal_code(object):
    """
    Base class for universal codes.
    Requires codewords are lexicographically ordered and in non-decreasing length. This implies no codeword is only 1s.
    Mixes in some other methods.
    Supports separately implemented checked and fast decode for individual words.
    Stream decode may be unchecked, and only consumes as many characters as it needs.
    """
    def __init__(self, encode_func, decode_stream, decode_func=None, decode_fast=None):
        if decode_func is None:
            decode_func = make_decoder(decode_stream=decode_stream, fast=False)
        if decode_fast is None:
            decode_fast = make_decoder(decode_stream=decode_stream, fast=True)
        self.encode = encode_func
        self.decode_checked = decode_func
        self.decode_fast = decode_fast
        self.decode_stream = decode_stream
    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError('Must be an integer index')
        if index < 0:
            raise ValueError('Index cannot be negative')
        return self.encode(index)
    def decode(self, item, fast=False):
        if not isinstance(item, str):
            raise TypeError('Must be a bit string')
        if not item:
            raise ValueError('Empty string will never be assigned to a value')
        if '0' not in item:
            raise ValueError('All 1s is not possible')
        decoder = self.decode_fast if fast else self.decode_checked
        return decoder(item)
    def index(self, item, fast=False):
        return self.decode(index)
    def __contains__(self, val):
        try:
            self.index(val, fast=False)
            return True
        except ValueError:
            return False
    def __iter__(self):
        import itertools
        return iter(map(self.__getitem__, itertools.count()))

def compare_dominates(a, b, limit=20):
    """
    Compare 2 universal codes which are not asymptotically equal,
    and try to find the smallest input where the asymptotically slower one wins.
    Returned tuple looks like (r, n) where
    - r is -1, 0, or 1 depending on the comparison result (slower is considered higher)
    - n is a number or None, and is the crossing point
    Argument limit is given in log log format,
      meaning the tested n are at most 2^2^limit
    Unreliable for when the asymptotic growth rate is the same.
    """
    # helper functions
    def _cmp_at(x):
        al = len(a[x])
        bl = len(b[x])
        if al < bl:return 1
        if al > bl:return -1
        return 0
    def _samples():
        yield from range(16)
        yield from map((2).__pow__,map((2).__pow__,range(2,limit+1)))
    # find above and below intersection to pinch
    clower,ilower,cupper,iupper = None,None,None,None
    for x in _samples():
        c = _cmp_at(x)
        if clower is None and c != 0:
            clower = c
            ilower = x
        if clower is not None and cupper is None and c == clower:
            ilower = x
        if clower is not None and cupper is None and c == -clower:
            cupper = c
            iupper = x
        if cupper is not None and c == -cupper:
            ilower = x
            cupper = iupper = None
        if cupper is not None and x > 1000:
            break
    # handle special cases
    if clower is None:
        return 0, None
    if cupper is None:
        return -clower, None
    # binary search
    while ilower < iupper:
        imid = (ilower + iupper) >> 1
        cmid = _cmp_at(imid)
        if cmid == cupper:
            iupper = imid
        else:
            ilower = imid + 1
    return cupper, ilower

def unary_encode(n):
    return '1'*n + '0'

def unary_decode(s):
    if s[-1] != '0':raise ValueError('Unary coded bitstring must end in 0')
    r = s.count('1')
    if r != len(s) - 1:raise ValueError('Unary coded bitstring must be all 1 other than final 0')
    return r

def unary_decode_fast(s):
    return len(s) - 1

def unary_decode_stream(it):
    it = iter(it)
    v = 0
    for c in it:
        if c == '1':
            v += 1
        else:
            yield v
            v = 0

unary = universal_code(unary_encode, unary_decode_stream, unary_decode, unary_decode_fast)
unary.__doc__ = """
Unary code. (standard)
Properties:
- looks like:
- - enc(n) = n copies of 1, then 0
- length:
- - |enc(n)| = n + 1
- growth rate:
- - G(n) = n
- mathematical:
- - not actually a universal code, it's sort of the degenerate extreme
"""

def elias_gamma_encode(n):
    b = bin(n+1)[3:]
    return '1'*len(b) + '0' + b

def elias_gamma_decode(s):
    c = s.index('0')
    if len(s) != 2*c+1:
        raise ValueError('VLC bitstring length is wrong')
    b = '1' + s[c+1:]
    n = int(b,2)-1
    return n

def elias_gamma_decode_fast(s):
    c = len(s) >> 1
    n = int(b,2)-1
    return n

def elias_gamma_decode_stream(it):
    it = iter(it)
    d = 0
    for c in it:
        if c == '1':
            d += 1
        else:
            b = ['1']
            for _ in range(d):
                b.append(next(it))
            n = int(''.join(b),2)-1
            yield n
            d = 0

elias_gamma = universal_code(elias_gamma_encode, elias_gamma_decode_stream, elias_gamma_decode, elias_gamma_decode_fast)
elias_gamma.__doc__ = """
Elias Gamma code. (nonstandard)
Properties:
- looks like:
- - enc(n) = unary(log n) || bits(n)
- length:
- - |enc(n)| = 2 log n
- growth rate:
- - G(n) = 2^n
"""

def elias_omega_encode(n):
    n += 1
    if n == 1:return '0'
    b = bin(n)[3:]
    return '1' + elias_omega_encode(len(b)-1) + b

def elias_omega_decode_stream(it):
    it = iter(it)
    for c in it:
        if c == '0':
            yield 0
            continue
        d = next(elias_omega_decode_stream(it)) + 1
        b = ['1']
        for _ in range(d):
            b.append(next(it))
        n = int(''.join(b),2)-1
        yield n

elias_omega = universal_code(elias_omega_encode, elias_omega_decode_stream)
elias_omega.__doc__ = """
Elias Omega code. (nonstandard)
Properties:
- looks like:
- - enc(n) = unary(log* n) || bits(log^(log* n - 1) n) || ... || bits(log n) || bits(n)
           = 1 || enc(log n) || bits(n)
- length:
- - |enc(n)| ~ log n + log^2 n + ... + log^(log* n) n + log* n
- growth rate:
- - G(n) = 2^^n ~ f_3(n)
"""

def elias_omega_alt_encode(n):
    if n == 0:return '00'
    if n == 1:return '01'
    b = bin(n)[3:]
    return '1' + elias_omega_alt_encode(len(b)-1) + b

def elias_omega_alt_decode_stream(it):
    it = iter(it)
    for c in it:
        if c == '0':
            c = next(it)
            yield 1 if c == '1' else 0
            continue
        d = next(elias_omega_alt_decode_stream(it)) + 1
        b = ['1']
        for _ in range(d):
            b.append(next(it))
        n = int(''.join(b),2)
        yield n

elias_omega_alt = universal_code(elias_omega_alt_encode, elias_omega_alt_decode_stream)
elias_omega_alt.__doc__ = """
Elias Omega code, modified to map 0 to 00, by Komi. (nonstandard)
Properties:
- looks like:
- - enc(n) = unary(log* n) || bits(log^(log* n - 1) n) || ... || bits(log n) || bits(n)
           = 1 || enc(log n) || bits(n)
- length:
- - |enc(n)| ~ log n + log^2 n + ... + log^(log* n) n + log* n
- growth rate:
- - G(n) = 2^^n ~ f_3(n)
"""

def code_f4_encode(n):
    n += 1
    if n == 1:return '0'
    ls = []
    while n > 1:
        b = bin(n)[3:]
        ls.append(b)
        n = len(b)
    return '1' + code_f4_encode(len(ls)-1) + ''.join(ls[::-1])

def code_f4_decode_stream(it):
    it = iter(it)
    for c in it:
        if c == '0':
            yield 0
            continue
        k = next(code_f4_decode_stream(it)) + 1
        n = 1
        for _ in range(k):
            b = ['1']
            for _ in range(n):
                b.append(next(it))
            n = int(''.join(b),2)
        yield n - 1

code_f4 = universal_code(code_f4_encode, code_f4_decode_stream)
code_f4.__doc__ = """
f4 code, by Komi. (nonstandard)
Properties:
- looks like:
- - enc(n) = unary(log** n) || ... || bits(n)
           = 1 || enc(log* n) || bits(log^(log* n - 1) n) || ... || bits(log n) || bits(n)
- length:
- - |enc(n)| ~ log n + log^2 n + ... + log log* n + ... + log** n
- growth rate:
- - G(n) = 2^^^n ~ f_4(n)
"""

def code_f4_alt_encode(n):
    if n == 0:return '00'
    if n == 1:return '01'
    ls = []
    while n > 1:
        b = bin(n)[3:]
        ls.append(b)
        n = len(b)
    return '1' + code_f4_alt_encode(len(ls)-1) + ''.join(ls[::-1])

def code_f4_alt_decode_stream(it):
    it = iter(it)
    for c in it:
        if c == '0':
            c = next(it)
            yield 1 if c == '1' else 0
            continue
        k = next(code_f4_alt_decode_stream(it)) + 1
        n = 1
        for _ in range(k):
            b = ['1']
            for _ in range(n):
                b.append(next(it))
            n = int(''.join(b),2)
        yield n

code_f4_alt = universal_code(code_f4_alt_encode, code_f4_alt_decode_stream)
code_f4_alt.__doc__ = """
f4 code, alternate version mapping 0 to 00, by Komi. (nonstandard)
Properties:
- looks like:
- - enc(n) = unary(log** n) || ... || bits(n)
           = 1 || enc(log* n) || bits(log^(log* n - 1) n) || ... || bits(log n) || bits(n)
- length:
- - |enc(n)| ~ log n + log^2 n + ... + log log* n + ... + log** n
- growth rate:
- - G(n) = 2^^^n ~ f_4(n)
"""
