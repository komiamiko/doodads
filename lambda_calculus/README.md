# Lambda Calculus

While imperative programming and other paradigms make for efficient actual programs,
functional systems have their merits in certain normality properties which make analysis easier.
As you move to progressively more regular functional systems,
they become even less practical,
while yielding traits that make them interesting to theoretical mathematicians.
One might remove function names, remove variable names, remove types other than functions, and reduce the language to a set of combinators,
culminating in the [SKI combinator calculus](https://en.wikipedia.org/wiki/SKI_combinator_calculus),
which has been realized in the esoteric programming language
[Unlambda](https://en.wikipedia.org/wiki/Unlambda).

The [lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus) is one of the more notable functional systems.
It is a sub-language in mathematics, or else an extension when combined with other notations, with one key feature -
functions consisting of input variable declarations and an expression, but no name for the function.
You may recognize this in ["lambda functions"](https://en.wikipedia.org/wiki/Anonymous_function) from programming,
alternatively called "anonymous functions".
While it may seem insignificant, entire theories have been developed analyzing the lambda calculus and related systems.

Relevant files:

- `lambda_calculus.py` - contains a lambda expression parser that produces callable objects of a custom class, and some utilities for working with them 
