#!/usr/bin/env python3

"""
Playground for the tree game. That same tree game that gave us TREE(3).
"""

import itertools

class extend_generate(object):
    """
    Acts like a list which is automatically extending using a generator when needed.
    Actually works with any iterable.
    """
    def __init__(self, it):
        self.li = []
        self.it = iter(it)
    def __getitem__(self, index):
        while len(self.li) <= index:
            self.li.append(next(self.it))
        return self.li[index]

def _pack_numeral(s):
    """
    Packs a long sequence of small numbers with high regularity.
    Uses bzip2 to compress and base64 to encode.
    Can work directly on a digit string.
    """
    import bz2
    import base64
    def _to_digit(c):
        if isinstance(c, str):return c
        if 0<=c<=9:return chr(c+48)
        if 10<=c<=35:return chr(c+55)
    s = ''.join(map(_to_digit, s))
    return base64.b64encode(bz2.compress(s.encode('utf-8'))).decode('utf-8')

def _unpack_numeral(s):
    """
    The counterpart to _pack_numeral
    """
    import bz2
    import base64
    return map((lambda c:int(c,base=36)),bz2.decompress(base64.b64decode(s.encode('utf-8'))).decode('utf-8'))

brackets = '()[]{}<>⟬⟭⟦⟧⦉⦊⧼⧽'

class subtree(object):
    """
    Represents a subtree.
    Internal ordering uses deepest to shallowest, then by color index, then arbitrarily.
    """
    def __init__(self, color, children=()):
        """
        Construct a subtree from the color index and its children.
        """
        self.color = color
        self.children = tuple(sorted(children))
        self.hash = hash((-3, color, children))
        self.depth = 1 + max((child.depth for child in children), default=0)
        self.sort_key = (-self.depth, self.color, self.hash)
    def __hash__(self):
        return self.hash
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return not self == other
    def __lt__(self, other):
        return self.sort_key < other.sort_key
    def __le__(self, other):
        return self.sort_key <= other.sort_key
    def __gt__(self, other):
        return self.sort_key > other.sort_key
    def __ge__(self, other):
        return self.sort_key >= other.sort_key
    def __add__(self, other):
        if other is None:
            return self
        if isinstance(other, (tuple, list, set)):
            return subtree(self.color, self.children + tuple(other))
        return subtree(self.color, self.children + (other,))
    def __radd__(self, other):
        if other is None:
            return self
    def __str__(self):
        i = self.color
        b = brackets[i*2:i*2+2]
        return b[0] + ''.join(map(str, self.children)) + b[1]
    def __repr__(self):
        return f'subtree({repr(self.color)}, {repr(self.children)})'

s = tuple(subtree(i) for i in range(len(brackets)//2))

def join_linear(ts):
    """
    Constructs a linear chain which is t[0] + (t[1] + (... + t[n]))
    """
    if len(ts) == 0:return None
    return ts[0] + join_linear(ts[1:])

def tail(t, n):
    """
    Constructs a linear chain which is t appended to itself, then appended to t,
      ... with n copies total of t
    """
    return join_linear([t]*n)

def freeze_tree(t):
    """
    Freeze a mutable tree.
    """
    if isinstance(t, subtree):
        return t
    if isinstance(t, int):
        return subtree(t)
    return sum(map(freeze_tree, t), None)

def n_friedman_seq(with_n):
    """
    Generates a long sequence satisfying the block subsequence property
      as defined by Friedman. Also called a Friedman string.
    For more information see:
      https://core.ac.uk/download/pdf/82639534.pdf
    Optimally long for n=1 and n=2. Practically infinite for n>=3.
    There, a lower bound for n(3) was presented as A_7198(158386),
      where A is a version of the Ackermann function.
    """
    if with_n == 1:
        return itertools.repeat(0, 3)
    if with_n == 2:
        yield 0
        yield from itertools.repeat(1, 3)
        yield from itertools.repeat(0, 7)
        return
    if with_n >= 3:
        # precomputed sequence
        # length 22200
        # done by @komiamiko on 2019-11-15
        yield from _unpack_numeral('QlpoOTFBWSZTWRlRhhAAACptt60kALRwGAAIAAMAIEAAIAACAAAAwAAACCAAkCgAGgZMgSakhAA2o9NTr3jGITWtU6ccZDRAeRAY+GAe+1abpT8aW7e+LQDV2on2wXtQ4axtYllSP7NFs0bqsIoAZYQrQkkIsRREIhAP4u5IpwoSAyowwgA=')
        
def tree3_friedman(with_n=3):
    """
    TREE(3) is a very big number!
    Let us play the tree game. With 3 colours, how long can we go for?
    This is a generator using Friedman's explicit construction,
      described here:
      https://cs.nyu.edu/pipermail/fom/2006-March/010260.html
    Friedman showed that this will construct around n(4) trees,
      where n is Friedman's block subsequence function.
      Obviously this is more than you can reasonably ever compute,
      so to us this is basically infinite.
    The reason n(4) comes into this is because its related sequence
      is used to generate the trees.
    Actually n(3) is already larger than A(7) which itself is outside of
      the computable range, so by default the n(3) sequence is used instead.
    """
    # Construct the first 14 trees specially
    ts = [
        s[2],
        s[1]+s[1],
        s[1]+s[0]+s[0],
        s[1]+tail(s[0], 3),
        s[0]+(s[1],)*4,
        s[0]+(s[1],)*3+(s[0]+s[0]),
        s[0]+(s[1],)*2+(s[0]+(s[0],)*3),
        s[0]+(s[1],)*2+(s[0]+s[0]+(s[0]+s[0])),
        ] + [
            s[0]+(s[1],)*2+tail(s[0], k) for k in range(6, 0, -1)
            ]
    yield from ts
    # Trees from here on contain exactly 1 instance of s[1]
    n_seq = extend_generate(n_friedman_seq(with_n))
    xs = [
        tail(s[0], 4),
        s[0] + (s[0],)*3,
        tail(s[0] + s[0], 2),
        s[0] + (s[0] + (s[0],)*2)
        ]
    for index in itertools.count(14):
        vs = [0]*(index-8) + [1]
        for k in range(index-12):
            x = xs[n_seq[index-14+k]]
            vs[k] = [vs[k], x]
        for offset in range(5):
            yield join_linear(list(map(freeze_tree, vs)))
            del vs[-2]
