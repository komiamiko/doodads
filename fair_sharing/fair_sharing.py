"""
Small library for computing fair sharing sequences for n players.
"""

def fair_sharing(n=2,*args,**kwargs):
    """
    Generates a fair sharing sequence which should be exactly correct.
    For n=2 this is the Thue-Morse sequence so we take a shortcut.
    The extra args and kwargs are passed on to the next function, if applicable.
    """
    import itertools
    if n < 1:
        raise ValueError('Require n >= 1')
    if n == 1:
        yield from itertools.repeat(0)
    if n == 2:
        for k in itertools.count():
            yield bin(k).count('1') & 1
    yield from fair_sharing_fast_checked(*args,n=n,**kwargs)

def fair_sharing_fast(n=2,decimals=100,pratio=15,debug=False):
    """
    Generates the fair sharing sequence for n players.
    First n terms should be range(n).
    Uses a simple game of chance to generate the sequence,
    with tiny fixed probability of winning on a turn.
    Not exact. May break after many terms.

    Note: re-imports mpmath
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

def fair_sharing_fast_checked(decimals=(100,110),*args,**kwargs):
    """
    Does fair_sharing_fast() twice with multiple precision values.
    On the first disagreement, aborts.
    Values are likely to be correct, but are not guaranteed to be.
    """
    gs=[iter(fair_sharing_fast(*args,decimals=dec,**kwargs)) for dec in sorted(set(decimals))]
    while True:
        res=[next(g) for g in gs]
        if len(set(res))!=1:break
        yield res[0]
