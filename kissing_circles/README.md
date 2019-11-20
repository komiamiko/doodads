#  Kissing Circles

We call circles kissing when they are tangent to each other. They can be externally or internally tangent. Cool things happen when you have 3 circles and want to determine a 4th kissing circle.

Descartes' Theorem and Apollonian Gaskets
---

Given 3 circles which are all kissing, what must be the radius of the 4th circle? It's actually easier to express using curvature, which is the reciprocal of radius. Descartes' Theorem looks like:

(k1 + k2 + k3 + k4)^2 = 2(k1^2 + k2^2 + k3^2 + k4^2)

You can find the 4th curvature more directly like so:

k4 = k1 + k2 + k3 ± √(k1k2 + k1k3 + k2k3)

Indeed, there are 2 possible circles. The smaller one, the one that would be externally tangent, would use the +, and the outer circle which is tangent internally would use the -.

Repeatedly generating more circles produces an Apollonian Gasket

Related files:

1. `kissing_circles.py` contains a numeric implementation of Descartes' Theorem and utilities for generating things based on it

Problem of Apollonius
---

Given 3 arbitrary circles defined by center and radius, find a 4th circle tangent to all of them. Depending on the choice of internal/external tangency, there are 8 solutions. Or rather, up to 8, because they may be not unique or not exist.

This looks like a very hard problem indeed! At the time of writing, Komi still considers it the hardest math problem they've ever done. 9 input constants to define the (x, y, r) of the circles, 3 outputs to define the (x, y, r) of the 4th circle. Fortunately, we can use some tricks. For one, using a negative radius will make the circle internally tangent instead of external, so we actually don't need to solve for all 8 separately; we can reuse the method but with inverted radii. Also, there is symmetry inherent in the problem, we can swap input circles without affecting the output. As a bonus, the system as a whole also respects the usual linear transformations that don't deform shapes, being translation, rotation, scaling, and reflection, though this property is harder to use so it is left as a last resort. For the actual derivation, Komi started with `sympy` to find a formula for the output radius and simplify it down to an expression with around 1500 terms, then went through it by hand to look for patterns and exploit the symmetry. Once the radius is calculated, the output x and y are relatively easy to get. The vectorized solver you see now is the result, written about as simple as it can possibly get and capable of finding all 8 solutions in one pass.

Related files:

1. `kissing_circles.py` contains a vectorized solver for the Problem of Apollonius using `numpy`, written around 2018-03-28
