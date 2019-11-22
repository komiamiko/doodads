# Non-Euclidean geometry

Euclidean geometry is your usual boring geometry, where parallel lines keep the same distance and the sum of interior angles of a triangle is always a half turn. What happens when those assumptions are broken? How does geometry behave in other spaces?

Hyperbolic and elliptic space
---

Without going into the full ugly physical and mathematical detail, hyperbolic and elliptic spaces come from negative and positive curvatures K, while K=0 is Euclidean. What is this curvature? It says, roughly speaking, how fast things turn toward or away from each other, in radians per length unit. In a Euclidean plane, K=0, so parallel lines stay the same distance apart. On the surface of a hemisphere, which is the confusingly named elliptic plane, parallel lines converge. This should make sense to you, as on the surface of the Earth, if you and your friend started walking locally parallel to each other, eventually you'd cross paths due to the curvature of the surface of the Earth, or else you'd need to turn, so it wouldn't be a line anymore. The hyperbolic plane is the most elusive. It evades our normal intuition. K is negative, so parallel lines diverge. In fact, most lines will never cross.

As wonky as these spaces may sound, they do share some familiar concepts and use similar equations. Also, it is typical to only study K=-1, K=0, and K=1, since other values of K behave like the same space but with coordinates scaled by some factor.

Relevant files:

- `hype.py` contains an abstract space class with geometry formulas and implementations for all the K you could want
