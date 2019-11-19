#  Kruskal's Tree Theorem and related things

Have you heard of TREE(3)? It is a stupidly large number, far too large for a human to grasp the sheer size of it but still well defined and finite. It comes from a simple game about making trees. It asks, roughly speaking, how many trees you can make with bounded size such that no tree contains a previous tree. Do your own research if you want to understand it better.

Of course, we have no business constructing the number, but we can have fun making trees and playing the tree game.

Relevant files:

1. `kruskal_tree.py` for playing with trees in general
2. `ktree_graphviz.py` if you have Graphviz installed, you can make tree images

Friedman's explicit construction of a game with about n(4) trees uses a sequence for n(4). TREE(3) is clearly a lot bigger than that. The point of that construction was to demonstrate that TREE(3) is actually really big and humans can't understand how big it is. What is n(4)? Well...

Friedman's Block Subsequence Theorem
---

A related and much weaker but still fast and easier to grasp function is Friedman's n function. It gives the length N of the longest string S made with that many symbols where for all 1 <= i < j < N/2, the substring S[i], ..., S[2i] is not a subsequence of S[j], ..., S[2j]. So that's a mouthful.

n(1) = 3: 000

n(2) = 11: 01110000000

n(3) = a really big number! lower bounded by A_7198(158386)

n(4) = even bigger!

Clearly n(4) is way overkill since we already can't store n(3) in a computer. So for computational purposes n(3) is good enough.

Relevant files:

1. `block_subsequence.cpp` which uses a dumb method to compute long sequences satisfying the Friedman string property
2. `xoroshiro.cpp` used by `block_subsequence.cpp` as a PRNG

But by the way, what is A?

Ackermann function
---

One of the more boring googological functions but a decent introduction to big numbers. It has been defined many different ways but it generally looks something like this:

- A_0(n) = n+1
- A_m(0) = A_m-1(1)
- A_m(n) = A_m-1(A_m(n-1))

As m gets bigger, this looks like the hyperoperations. A_2(n) is about 2n. A_3(n) is about 2^n. A_4(n) is about 2^2^2^... with n copies of 2, called tetration. A_7198(158386) is clearly too large to fit on a computer.
