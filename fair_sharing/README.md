# Fair Sharing Sequences

We have an infinite sequence of items of decreasing values, how do we fairly divvy them up? Alternatively, with a pool of items, how should we decide the order of getting to pick items so it gets divided as fairly as possible? For 2 players, the Thue-Morse sequence gives the order: `0, 1, 1, 0, 1, 0, 0, 1, ...`. This means the first player takes the first and most valuable item, the second player takes the second and third items, the first player takes the fourth, and so on. TM(n) with n starting at 0 is just whether the number of 1 bits in n is even or odd.

For more players, the problem gets more difficult. A simple model assigns item n a value of (1-epsilon)^n for some infinitesimally small epsilon. These programs use this model to compute fair sharing sequences.

Relevant files:

1. `fair_sharing.py` computes fair sharing sequences