# Non-Euclidean geometry

Euclidean geometry is your usual boring geometry, where parallel lines keep the same distance and the sum of interior angles of a triangle is always a half turn. What happens when those assumptions are broken? How does geometry behave in other spaces?

I just want programs
---

Sure.

Relevant files:

- `hype.py` contains a space class for spaces of constant curvature, geometric formulas, point arithmetic, and more

Hyperbolic and elliptic space
---

It is worth it to understand, physically, what curvature is. Euclidean space is flat in a sense. It has 0 curvature. But that's not very interesting. What happens when we change the curvature?

We may start at 1D curvature, with a simple curve. Draw a curve, whatever you like. Pick a point on your curve. Now draw a circle that kisses the curve at that point, hugging it as close as possible. That's called an osculating circle, by the way. The flatter the curve there, the larger the circle. The tighter the bend, the smaller the circle. Big circle means not much curvature. Small circle means a lot of curvature. Look at how fast you would need to turn to follow it. You could actually measure this in, say, radians per metre. It could be calculated as the reciprocal of the radius of that circle. It would have to have dimension angle/length. Here, the concept of curvature makes sense. Pretty easy, right?

Let's move on to a surface embedded in Euclidean space. Take a round ball, that's roughly a sphere. Pick a point. You can draw a line going through that point. Notice, on the sphere, this is a line because it doesn't bend, but in our 3D space, that's a curve with curvature. We will assign this curvature a sign based on whether it curves away from the surface or toward it, more formally, whether it's toward or away from the normal at that point on the surface. You could draw lines going in different directions. For a ball, these will all have the same curvature, but for another surface, that may not be the case. If you took the minimum and maximum curvatures across all the directions of line that you could draw, called the principal curvatures, and then multiplied them together, you would get a quantity called the Gaussian curvature, denoted by the uppercase latin letter K, with unit angle^2/length^2. In the case of the ball, the principal curvatures are going the same way, so they have the same sign, and their product, K, is positive.

Interestingly, a lot of bent surfaces still have 0 curvature, as you'll find. Try a cylinder. Anywhere on the cylinder, you can draw a line that even in our 3D space is still straight and thus has 0 curvature. We can conclude that the Gaussian curvature is actually 0 everywhere on the cylinder.

To find a place with negative curvature, we can look at the inner side of a donut, more formally a torus. You can draw one line that curves away from the donut, going in a ring inside the donut. This has negative principal curvature.You can draw another line that traces a ring on the outside of the donut. Now these are curving in different directions, so when you multiply the curvatures, they end up being negative.

Things start getting interesting when we talk about spaces of constant curvature. What does constant curvature K = -1 look like? Well we certainly can't embed it in our 3D flat space. We can project it in ways though, and visualize it that way. If you want to get a feel for it, try the game HyperRogue. It's a full game set in the hyperbolic plane, and you'll experience so much more than just a diagram can show.

For dealing with spaces with K other than 0, 1, or -1, you can imagine it being scaled. For example, on a ball of radius 1m, we will have K = 1/m^2. What if we shrink the ball to half the radius? Well then the radius of curvature is 0.5m, so we have K = 4/m^2. What if we double the size of the ball instead. Then the radius of curvature is 2m, so we have K = 0.25/m^2. A similar thing happens in the hyperbolic plane. This idea of scaling turns out to be really useful.

At the limit, when the radius goes to infinity and the curvature goes to 0, we just get the Euclidean plane. Any formula for hyperbolic geometry or elliptic geometry, when you take the limit as K goes to 0, is guaranteed to yield the Euclidean version if it exists. Also, another interesting consequence is that when you really zoom in on a hyperbolic plane or elliptic plane it becomes approximately Euclidean. This makes sense to us! When we draw small triangles on the ground, they might as well be flat to us, but the Earth really is round, and if we drew a big enough triangle the angles wouldn't quite add up to a half turn anymore.

What about higher dimensional spaces? What about lower? Does it make sense to have a 1-dimensional curved space? What would a 0-dimensional space be then?

First of all, all dimensional spaces are described by this same K. It's counterintuitive and not obvious, because K is a 2-dimensional quantity, and why should it describe a N-dimensional space? But that's how it works. The Wikipedia page for Gaussian curvature is not very good at explaining this (at the time of writing), so I'm telling you, in short, this same K is used for every dimensional space.

Even a 1-dimensional space, a line, can be associated with a curvature. We can see this two ways. When breaking down a higher dimensional space, you can extract one line from it, and that line is like its own axis. Will isolating that line erase the curvature? Actually, no, and it shouldn't. See this easiest with positive curvature. If you slice a circle from a sphere, that circle doesn't just become a straight line. In the other direction, we often construct higher dimensional spaces by gluing axes together, like a X axis, Y axis, and Z axis, to form a flat 3D space. But how could this higher dimensional space have a curvature if we never associated the axes with curvatures? We're not gluing the axes together in a different way. We have to associate even a 1D space with a curvature so that math works.

Note from Komi
---

This journey of discovering non-Euclidean spaces started long ago. I had a lot of questions and not many answers. I haven't been working on these problems all that much, in fact, I spent most of my life doing things unrelated to this.

I must thank ZenoRogue, creator of HyperRogue, for lending me a helping hand and a beginning in this journey. I was able to grasp the basic concepts behind these strange spaces. I collected formulas from various sources and came up with a few of the simpler ones on my own.

Most serious mathematicians would do a lot of difficult math to determine how spaces behave in various cases, and put a lot of effort into deriving formulas. For me, I had some formulas to start with, and expectations for how the spaces should behave. Some of these formulas only worked for a specific K, and that was okay. I made test cases and tested what I had implemented so far against my expectations, such as that spaces should scale nicely. With that, I corrected many bugs and brought many formulas to their current correct state which is general enough to handle all possible curvatures. That's some top tier math cheese right there. None of this is proven, yet I am confident in the correctness. My greatest achievement here, at least so far, was the accidental discovery of Gaussain curvature as the true curvature. I started with a 1D fake curvature k, and I kept seeing K=k|k| pop up in so many formulas, and I was forced to conclude that I really should have been using the 2D quantity K all along. It didn't make sense to me why ND spaces should be described by a 2D quantity, but the formulas kept asking for K, not my fake curvature k, so I conceded.

As of 2019-11-26, parallel transport has been implemented. It was interesting the cheesy approach I got here with. To derive the formulas for the transform matrix I mean. I started in 2D, so that would have the 1 extra axis resulting in a 3x3 matrix, which is doable. We could phrase the parallel transport as "rotate the transform point to lie on the x axis, shift to the right by the magnitude of the transform point, then undo the rotation". ZenoRogue already derived the shift matrix S, which was probably the least obvious. I derived the rotation matrix R with some basic trigonometric identities. I then used sympy to calculate the matrix product R S R^-1. From there I went to algebraically manipulate it on my own. The rules were strikingly obvious for the top left corner T[0,0], the top row T[0,i], the left column T[i,0], and the diagonal T[i,i]. It was the other entries where it was less obvious how to extrapolate to higher dimensions. In 2 dimensions, there are only 2 of those entries, after all, and the pattern wasn't obvious. I didn't want to do this all again in 3D to reveal the pattern. So I looked harder at the 2D case. I noticed that T[1,2] looked like x1 x2 D, and T[2,1] looked like x1 x2 D as well. So I made a guess that T[i,j] = xi xj D. That turned out to be correct.

Anyway, this has been a strange and enlightening journey. Go learn and explore, and enjoy this little math library.
