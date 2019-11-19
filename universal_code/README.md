#  Universal Codes

There's lots of equivalent variants of universal codes, and different ways to characterize them. Basically they are prefix codes for the positive integers. In practice, a good enough integer encoding and data compression is used for integer sequences; universal codes are just fun and interesting from a theoretical perspective.

Komi's restricted universal codes
---

Komi (@komiamiko) imposes a standard for restricting what can be a universal code. This is much stricter than the common mathematical definition, but it does give some more useful properties.

The core rules are:

1. It must encode all the non-negative integers and nothing else. Thus ENCODE(n) maps non-negative integers to bit strings.
2. It is a prefix code. Thus for all n, m with n =/= m, ENCODE(n) cannot be a prefix of ENCODE(m).
3. All infinite length bit strings must decode (in the sense of decoding a data stream) to a unique infinite integer sequence. Stated less formally, it is not wasteful.
4. Bit string codewords must be lexicographically ordered. Thus for all n, m, n < m if and only if ENCODE(n) < ENCODE(m).
5. Bit string codewords must have non-decreasing length. Thus for all n, m, if n < m then length(ENCODE(n)) <= length(ENCODE(m))

With that, we derive canonical forms for various codes. Unary is `0, 10, 110, 1110, 11110`, Elias gamma is `0, 100, 101, 11000, 11001`, Elias omega is `0, 100, 101, 110000, 110001`, Komi's f4 code is `0, 100, 101, 1100000, 1100001`.

These are implemented in `universal_code.py`.

By the way, Komi had asked a question a long time ago about the possible existence of a slowest growing perfect universal code. In short, no, it does not exist, because there is no fastest growing function.

Notice that codewords cannot be all `1`s because that would make it the last codeword in an infinite sequence and that codewords cannot be empty because then it could not be decoded. Thus every codeword contains a `0` somewhere.

We can count the number of `1`s occuring before the first `0` in ENCODE(n). This is like unary. We will call this number U(n). Note that because of the non-wasteful property, U steps up by at most 1 each time. If it stepped up by more than 1, we would miss a range and that would not be decodable. Note that for the better codes, U grows slowly.

Define G(m) as the smallest number n such that U(n)=m. G grows quickly. Notably, given a G, we can also go backward to find a U satisfying it. The map U <-> G is bijective.

For a slower U, G is faster, and vice versa.

Is there a fastest growing G? No. Suppose we have found f which we think is the fastest growing function. It will definitely grow at least as fast as n -> 2n. That's not impressive but we do need it for the proof. Let G(m) = f(f(...f(m))) with m copies of f. Well clearly this grows faster than f. But we said f is the fastest growing function. Contradiction! Thus there is no fastest growing G, and no slowest growing U.

Komi's f4 code has its G around f_4 in the fast growing hierarchy, however, the constant factor means that Elias Omega is shorter for practical size numbers.

Extra things for a possible future improvement:

- Support a variable size non-recursive base case in the recursive encodings, rather than always using the smallest base case possible, which for all of the currently implemented ones is n=0
- Support radixes higher than 2 and still encode efficiently, may be useful for byte encodings where the radix is 256 instead
