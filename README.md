# doodads

Here is a collection of useful small blobs of code. They aren't so small, standalone, and disorganized that they would fit comfortably in a Gist. Yet they are also too small to sensibly get their own repositories. Here they are roughly categorized and sorted into folders by purpose and function.

Given the structure of the code blobs here, there isn't really any maintained standard for them. Take and use what you need. I hope even the jankier programs in here are useful to someone.

## Summary of collections

### fair_sharing

Optimal [picking sequences](https://en.wikipedia.org/wiki/Picking_sequence) for
[fair item assignment](https://en.wikipedia.org/wiki/Fair_item_allocation).
More commonly known as "fair sharing sequences".

[Thue-Morse sequence](https://en.wikipedia.org/wiki/Fair_item_allocation)
is the fair sharing sequence for 2 agents.
We extend the concept to N agents.

### kissing_circles

Circles are kissing when they are tangent to each other.
Related concepts include [Descartes' Theorem](https://en.wikipedia.org/wiki/Descartes%27_theorem) (relates the curvatures of 4 kissing circles)
and the [Problem of Apollonius](https://en.wikipedia.org/wiki/Problem_of_Apollonius) (given 3 circles, find a 4th circle which kisses the other 3).

### kruskal_tree

[Harvey Friedman](https://en.wikipedia.org/wiki/Harvey_Friedman)'s
[TREE game](https://googology.wikia.org/wiki/TREE_sequence)
on finite rooted labelled trees.
Collection is named after Kruskal,
because [Kruskal's Tree Theorem](https://en.wikipedia.org/wiki/Kruskal%27s_tree_theorem)
proves the tree game always ends.

Some other combinatorial problems/concepts due to Friedman are also included here.

### lambda_calculus

Parser and other tools for the
[lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus)
and other systems in a very pure functional model of logic or computing.

### non_euclidean

For N-dimensional spaces of constant [Gaussian curvature](https://en.wikipedia.org/wiki/Gaussian_curvature) K
(see: [Euclidean geometry](https://en.wikipedia.org/wiki/Euclidean_geometry),
[hyperbolic geometry](https://en.wikipedia.org/wiki/Hyperbolic_geometry),
[elliptic geometry](https://en.wikipedia.org/wiki/Elliptic_geometry)),
implements non-coordinate geometry formulas, point operations, and point transforms.

### transfinite

Implements [ordinals](https://en.wikipedia.org/wiki/Ordinal_number)
up to the [Feferman–Schütte ordinal](https://en.wikipedia.org/wiki/Feferman%E2%80%93Sch%C3%BCtte_ordinal).
Supports [arithmetic](https://en.wikipedia.org/wiki/Ordinal_arithmetic),
comparison,
and [fundamental sequences](https://googology.wikia.org/wiki/Fundamental_sequence).
Exports [LaTeX](https://en.wikipedia.org/wiki/LaTeX) math code.

### universal_code

Implements [universal codes](https://en.wikipedia.org/wiki/Universal_code_%28data_compression%29),
including some standard and non-standard ones.
Universal codes are a kind of prefix code, encoding the natural numbers as bitstrings (binary strings).
All universal codes have been
[normalized](https://en.wikipedia.org/wiki/Normal_form_%28abstract_rewriting%29)
to satisfy additional useful normality requirements,
and may differ from other arbitrary "standard" variations.
