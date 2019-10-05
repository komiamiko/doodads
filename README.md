# transfinite
Small library for working with ordinals and transfinite numbers.

Background
---

This is good for emerging mathematicians who want to explore ordinals and experienced mathematicians who want to do heavy lifting with ordinals. It is based on some serious high level set theory, so do not feel bad if some things look strange!

This started as just a small project to occupy my time, though it does indeed fill a niche - a software package for ordinal numbers.

The project is currently in early development, and no expert mathematicians have reviewed it to make sure all the math is correct.

Ordinals? Transfinite?
---
We should begin our journey at the concept of transfinite numbers. In short, they are not quite finite, and not quite infinite.

Finite numbers are great and all, but only for describing finite things. What is the size of the natural numbers? Well, we can count: *1, 2, 3, 4, ...* and it goes on forever. There's clearly infinity (∞) of them, right?

The issue with infinity is that it causes all sorts of weird issues and paradoxes. A simple demonstration of this is comparing the size of the even natural numbers and the size of the natural numbers.

The natural numbers go like *1, 2, 3, 4, 5, 6, 7, 8, ...*

The even natural numbers go like *2, 4, 6, 8, ...*

Suppose there are *N* natural numbers. Well then, clearly the even natural numbers take up half of the natural numbers, so the number of even natural numbers is *N/2*. But wait, if we divide the even natural numbers in half, suddenly the sequence is exactly the same, so it should be *N*. So we have *N = N/2*. We let this pass because it's infinite. Sometimes, however, we want to quantify the size of the infinitys. How is the size of the rational numbers related to the size of the natural numbers? Saying they're both infinite isn't very helpful, and clearly there's more rational numbers than natural numbers.

What we're looking for is something that is larger than all the finite numbers, yet still behaves somewhat like a finite number and not an infinity. Voila, we have invented transfinite numbers.

As it turns out, in transfinite land, we must differentiate ordinals and cardinals. Ordinals are the order of things, like using the number 4 to say something is 4th in line. Cardinals are the size of things, like using the number 4 to say there are 4 things in a bag. The size of the natural numbers we call aleph 0. The order of the natural numbers we call omega (ω).

The first ordinal number ω is where the fun begins. By definition, it is the smallest limit ordinal, as the ordinal that comes after *1, 2, 3, 4, ...*, or rather, that sequence itself, using each number *N* being equivalent to *1, 2, 3, ..., N*. ω is *1, 2, 3, 4, ...*, through all the natural numbers. What is ω-1? It's not defined. If it were defined, it would be a smaller limit ordinal, and that contradicts our definition.

Here is where the commutativity of addition breaks.

What is commutativity? It means you can change the order of operands and the result is the same.

For natural numbers, addition is commutative. Let us demonstrate that 2+5 and 5+2 both get 7.

2+5: *1, 2, 1', 2', 3', 4', 5'* which looks like *1, 2, 3, 4, 5, 6, 7* which is 7.

5+2: *1, 2, 3, 4, 5, 1', 2'* which looks like *1, 2, 3, 4, 5, 6, 7* which is 7.

Now, let us try with ω+3 and 3+ω.

ω+3: *1, 2, 3, ..., 1', 2', 3'*

3+ω: *1, 2, 3, 1', 2', 3', ...* which looks like *1, 2, 3, 4, 5, 6, ...* which is ω.

So 3+ω = ω but ω+3 is not ω.

It helps to take a moment to understand more precisely what "looks like" means. After all, on the surface they seem to be the same size. Let us think about successors. The successor of 0 is the number after 0, or 1. The successor of 1 is 2. And so on. Every finite number is either 0 or a successor of a smaller number. In reverse, we may think of predecessors. In the expansion of 3+ω, the predecessor of 1' is clearly defined as 3. In fact, there are 3 numbers behind 1'. The 3 can be eaten up by the ω in a sense. Meanwhile, in the expansion of ω+3, we don't have a well defined predecessor for 1', we can only say the entire expansion of ω is behind 1'. So we have no choice but to leave both the ω and 3 intact, and write ω+3.

For multiplication, exponentiation, and other interesting things you can do with transfinite ordinals, go explore on your own. There are plenty of resources online.
