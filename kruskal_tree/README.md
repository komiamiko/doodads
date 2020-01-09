#  Kruskal's Tree Theorem and related things

Have you heard of TREE(3)? It is a stupidly large number, far too large for a human to grasp the sheer size of it but still well defined and finite. It comes from a simple game about making trees. It asks, roughly speaking, how many trees you can make with bounded size such that no tree contains a previous tree. Do your own research if you want to understand it better.

Of course, we have no business constructing the number, but we can have fun making trees and playing the tree game.

*This collection is named after Kruskal because it's Kruskal's Tree Theorem that proves the tree game always ends, though the idea of the trees and original tree/TREE functions were proposed by Harvey Friedman, so perhaps it would be more fitting to name this collection after Friedman. It's Friedman's trees and Kruskal's proof of termination.*

Relevant files:

1. `kruskal_tree.py` for playing with trees in general
2. `tree3_graphviz.py` if you have Graphviz installed, you can make tree images

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

Other TREE and tree sequences
---

tree, the weak tree function, plays a game distinct from but related to the TREE game, and tree grows very fast but nowhere near the incomprehensibly fast of TREE.

Friedman's originally presented strategy for TREE(3) would construct those n(4) trees or so, and then it would have only 1 node label left, so from there it can construct about tree(n(4)) more trees. Since then, other serious researchers and hobbyist mathematicians have come up with various other sequences to play the tree game and TREE game with, and produce better lower bounds for TREE(3). Friedman's original one is already so long that nobody could possibly compute it, so as a programmer that just wants to generate a long sequence of trees, you wouldn't really care what strategy you used.
