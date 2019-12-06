"""
Small library for computing fair sharing sequences for n players.
v2.0.0
"""

def fair_sharing(n=2,*args,**kwargs):
    """
    Generates a fair sharing sequence which should be exactly correct.
    This should be the go-to API method you call.
    Any arguments other than (n) are not guaranteed to be available
    or have an effect in future versions.

    As currently implemented:
    For n=2 this is the Thue-Morse sequence so we take a shortcut.
    Otherwise, uses a polynomial array based method.
    """
    import itertools
    if n < 1:
        raise ValueError('Require n >= 1')
    if n == 1:
        yield from itertools.repeat(0)
    if n == 2:
        for k in itertools.count():
            yield bin(k).count('1') & 1
    yield from _fair_sharing_array(*args,n=n,**kwargs)

def _fair_sharing_array(n=3, degree=2, limit=10**6, use_numpy=False):
    """
    Algorithm for generating the fair sharing sequence for n agents.
    Implemented starting from v2.0.0

    One possible definition of the fair sharing sequence is based on
    a simple game of chance.
    On turn k, player S[k] goes, and has a epsilon chance of winning.
    epsilon is some infinitesimally small number.
    That turn's contribution to the player's expected chance of winning
    is proportional to (1-epsilon)^k
    This, if expanded, is a polynomial.
    An exact calculation would take O(k) for the nth step,
    however, we can cheat a bit!
    We might say that the term epsilon^m
    does not have an effect on the sequence until item k=F(m)
    where all previous terms are equal.
    It is not known how fast F grows, or if it is finite for all m.
    It is known that F(m) ~ 2^m for n=2
    and F grows at least as fast for higher n.
    Thus, we can make an optimization and only keep track of polynomials
    up to a fixed degree, which is the parameter.
    Though, worry not, because if k ever reaches F(degree),
    we'll just make the degree higher, and compute again.

    Another parameter is limit - this function is guaranteed
    to compute the first (limit) items correctly,
    but after that, it may be incorrect.
    If you only need a small prefix of the sequence, please say so,
    and we can use appropriate speed-ups.

    Will use numpy if numpy is available and the flag is set.
    Current version was benchmarked to actually be 10x faster without numpy,
    so by default, will not use numpy.
    If you can write a better vectorized version, please contribute!
    """

    # palindrome/stack optimization
    # when you expand the polynomial thing with the binomial theorem
    # you will see that if you chunk up the sequence into blocks of 2n
    # those blocks must be palindromes
    # (also each block of n is a permutation of 0,1,...,n-1)
    # so we will only compute the first half of the palindrome
    # and then use the stored values for the rest
    # benchmarks say this reduces the runtime by 13%
    # beyond m=2, the behaviour is less regular, and no optimizations
    # are currently implemented based on it
    
    import itertools
    np = None
    try:
        if use_numpy:
            import numpy as np
    except ImportError:
        pass
    
    def reset():
        points = [1] + [0] * degree
        scores = [[0] * (degree + 1) for _ in range(n)]
        stack = list(range(n))
        stack = stack + stack[::-1]
        bstack = []
        if np:
            dtype = np.int64 if limit**degree < 2**63 else object
            points = np.array(points, dtype=dtype)
            scores = np.array(scores, dtype=dtype)
        return points, scores, stack, bstack

    points, scores, stack, bstack = reset()
    skip_first = 0
    k = 0

    while True:
        if stack:
            j = stack.pop()
            expand = False
        else:
            j = 0
            dupli = 0
            for i in range(1, n):
                if np:
                    eq = scores[i] == scores[j]
                    if np.all(eq):
                        dupli += 1
                    else:
                        l = np.argmin(eq)
                        if scores[i,l] < scores[j,l]:
                            j = i
                            dupli = 0
                else:
                    if scores[i] < scores[j]:
                        j = i
                        dupli = 0
                    elif scores[i] == scores[j]:
                        dupli += 1
            expand = dupli != 0 and k >= n
            bstack.append(j)
            if len(bstack) == n:
                stack, bstack = bstack, stack
        if expand:
            degree += 1
            points, scores, stack, bstack = reset()
            skip_first = k
            k = 0
            continue
        if np:
            scores[j] += points
            points[1:] -= points[:-1]
        else:
            for i in range(degree+1):
                scores[j][i] += points[i]
            for i in range(degree,0,-1):
                points[i] -= points[i-1]
        if k >= skip_first:
            yield j
        k += 1
        
def _fair_sharing_mp(n=2,decimals=100,pratio=15,debug=False):
    """
    Algorithm for generating the fair sharing sequence.
    Used in v1.0.0

    Generates the fair sharing sequence for n players.
    First n terms should be range(n).
    Uses a simple game of chance to generate the sequence,
    with tiny fixed probability of winning on a turn.
    Not exact. May break after many terms.

    Note: requires mpmath
    """
    import operator
    import itertools
    from mpmath import mp
    mp.dps=decimals
    p=mp.mpf(10)**-(decimals/pratio)
    acc=mp.mpf(0)
    wins=[mp.mpf(0)]*n
    if debug:
        print('p = '+str(p))
    for i in itertools.count():
        index,_ = min(enumerate(wins),key=operator.itemgetter(1))
        yield index
        inc=p*(1-acc)
        wins[index]+=inc
        acc+=inc
        if debug:
            print('acc = '+str(acc))

def _fair_sharing_mp_checked(decimals=(100,110),*args,**kwargs):
    """
    Algorithm for generating the fair sharing sequence.
    Used in v1.0.0
    
    Does fair_sharing_fast() twice with multiple precision values.
    On the first disagreement, aborts.
    Values are likely to be correct, but are not guaranteed to be.

    With default parameters, was benchmarked to be about 15x slower
    than the new default implementation.
    """
    gs=[iter(_fair_sharing_mp(*args,decimals=dec,**kwargs)) for dec in sorted(set(decimals))]
    while True:
        res=[next(g) for g in gs]
        if len(set(res))!=1:break
        yield res[0]
