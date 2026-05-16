Equivalence Algorithms
======================

Content extracted from ``data/Equivalence_Algorithms.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Equivalence_Algorithms <https://boolean.wiki.uib.no/Equivalence_Algorithms>`

The hierarchy of equivalences
-----------------------------

:cite:p:`Dinur:201800`
:cite:p:`Canteaut:202205`

Given two vectorial Boolean functions `F,G:F_{2}^{n}\rightarrow F_{2}^{n}`,
there are various ways to define equivalence between `F` and `G`. We will
study the algorithms for determining Linear, Affine, Extended Affine and
CCZ equivalence between vectorial Boolean functions.

Linear Equivalence
------------------

Given two vectorial Boolean functions `F` and `G`, we want to determine if
there exist linear permutations `A_1` and `A_2` such that
`F = A_2 \circ G \circ A_1`.

The to and from algorithm
.........................

This algorithm was presented at Eurocrypt 2003 :cite:p:`Biryukov:200300`. This
algorithm is mainly intended for when the Boolean functions are permutations,
and we will start by assuming `F` and `G` are permutations.

The idea of the algorithm is to use information gathered about `A_1` to deduce
information about `A_2`, and the other way around. To see how this can work,
say we know some value of `A_1`, for example `A_1(x) = y`. We also know the
value of `G` at `y`, so let `G(y) = z`. Then
`F(x) = A_2 \circ G \circ A_1(x) = A_2 \circ G(y) = A_2(z)`. So we now know
that `A_2(z)` must be equal to `F(x)`.

For the other way around, say we know some value of `A_2`, for example
`A_2(x) = y`. We know the value of `F^{-1}` at `y`; let `F^{-1}(y) = z`.
Then `F(z) = y = A_2 \circ G \circ A_1(z)`, so
`A_2 \circ G \circ A_1(z) = y`. Since we know that `A_2(x) = y`, we need
`G \circ A_1(z) = x`, which means `A_1(z) = G^{-1}(x)`.

This shows how we can deduce information knowing either a value of `A_1` or a
value of `A_2`. Now suppose we know the values of `A_1` at a set of points.
Since `A_1` is linear, we also know its value at any linear combination of
these points. Thus we can assume that we know the values of `A_1` at `k`
linearly independent points, which means that we know the value of `A_1` at
`2^k` points.

If we gain the value of `A_1` at a point which is not in the span of the
already known points, then we can deduce the value of `A_1` at `2^k` new
points using all linear combinations involving this new point. Then we can use
all of these new points to try to deduce points of `A_2`, as explained before.

Given two permutations `F,G : F_2^n \rightarrow F_2^m`, we construct the
linear permutations `A_1,A_2`. The algorithm is a backtracking algorithm, and
whenever we discover a contradiction we backtrack to the last guess.

We first guess two values of `A_1(x)`. Since we now know two values of `A_1`,
we can deduce two values of `A_2`, which means we can deduce a third value by
linearity. Using this third value, we can deduce a value of `A_1`. If this
value is not in the span of the already known values of `A_1`, we can deduce
two more values of `A_1` and use this to deduce further values of `A_2`, and
so on.

If we run out of values before we have finished, we have to make additional
guesses. If we encounter a situation where we deduce a value of `A_1` or
`A_2`, but we have already set it to be something else, we must backtrack to
the last guess.

Runtime
.......

It can be hard to estimate the runtime of this algorithm, as it is hard to
know how many guesses we have to make. Initially we have to make two guesses
(or just one if the S-boxes do not map 0 to 0) to get the algorithm started.
Assuming we do not have to make any more guesses, the algorithm runs in time
`O(n^32^{2n})` (`O(n^32^n)` if the S-boxes do not map 0 to 0).

This assumption seems to hold for random functions, but there are bad cases,
for example when the functions differ in very few points. In general it seems
hard to prove any good runtime guarantee for this algorithm.

Affine Equivalence
------------------

Given vectorial Boolean functions `F,G : F_2^n \rightarrow F_2^m`, find
affine permutations `A_1,A_2` such that `F = A_2 \circ G \circ A_1`. We can
also write this as `F \circ A_1^{-1} = A_2 \circ G`.

If `A_1(x) = L_1(x) +a_1` and `A_2(x) = L_2(x)+a_2`, then `F(x+a_1)` is
linear equivalent with `G(x) + a_2`. So we can guess any affine constants
`a_1,a_2` and check whether `F(x+a_1)` is linear equivalent with
`G(x)+a_2` using any linear equivalence algorithm. This adds a multiplicative
factor of `2^{2n}` to the runtime, but gives an affine equivalence algorithm.

The to and from algorithm (Affine)
..................................

We can adapt the to and from algorithm to the affine case and only add a
multiplicative factor of `2^n` to the runtime. Instead of comparing
`F(x+a_1)` to `G(x)+a_2` for every possible `a_1,a_2`, we will instead find a
representative function for `F(x+a)` for every `a`, and then a representative
function for `G(x) + a` for every possible `a`. We then compare to see if any
of these representative functions are equal. The representative for a function
is the lexicographically smallest linear equivalent function.

To see why this works, assume `F,G` are affine equivalent with
`F = A_1 \circ G \circ A_2`, where `A_1 = L_1 + a_1` and `A_2 = L_2+a_2`.
Then the functions `F(x+a_1)` and `G(x)+a_2` will be linearly equivalent. If
we have found the minimal linear representative `F'` of `F(x+a_1)`, then since
`G(x)+a_2` is linearly equivalent with `F`, it is also linearly equivalent
with `F'`; hence the minimal linear representative of `G(x)+a_2` is at least
smaller than `F'`. Using this argument the other way around, their linear
representatives have to be the same function.

To compute the minimal representative of a function `F`, we construct `F'`,
the minimal permutation which is linearly equivalent with `F`. We start by
guessing the value of `A_1` at the smallest element of `F_2^n`; say
`A_1(x) = y`. We then go back and forth between `A_1` and `A_2` as before.
The only difference is that we always pick the lowest possible value of `A_1`
to deduce a value of `A_2` and vice versa. Also, whenever we need the value of
an undefined point of `F'`, we set it to the lowest available value.

Rank Algorithm
..............

This algorithm is efficient also for non-permutations, but only functions of
high algebraic degrees.

Rank table
~~~~~~~~~~

The algorithm is based on using the rank table of a Boolean function, which we
now introduce.

Given a Boolean function `F: F_2^n \rightarrow F_2`, we consider this object
algebraically using the ANF (algebraic normal form):

`F = \sum_{u \in F_2^n }\alpha_ux^u`.

We can look at `F` as a vector spanned by all monomials
`x^{u}=x_{1}^{u_{1}}...x_{n}^{u_{n}}`. Let `F_{\geq d}` be the polynomial
containing all monomials of `F` with degree at least `d`.

Given a vectorial Boolean function `F=(F_1,...,F_m)`, we define the symbolic
rank of `F` as the rank of the vectors `\{F_i\}`, where we view each `F_i` as
a vector. Denote this as `SR(F)`.

We compose functions symbolically as
`F \circ A_1 = \sum \alpha_u \cdot (M_u \circ A_1)`. We have
`deg(F \circ A_1) \leq deg(F)`. We can also compose `A_2 \circ F`, where we
replace `x_i` in `A_2` by `F_i`.

Let `A : F_2^{n-1} \rightarrow F_2^n` be an affine transformation with
`A(x) = L(x) + a`. The range of `A` is an affine `n-1` dimensional subspace,
so its orthogonal subspace is 1 dimensional, and hence spanned by a single
vector `h`. We call `h` the half space mask (HSM), since it partitions the
space into two halves. The value `h \cdot a` is the half space free
coefficient (HSC).

Given an HSM and HSC `h` and `c`, there is a canonical affine transformation
`C_{|_{h,c}} : F_2^{n-1} \rightarrow F_2^n`.

We can now define the rank table of `F` with respect to some constant `d`. For
any `h \in F_2^n`, we calculate
`u = SR((F \circ C_{|_{h,0}})_{\geq d})` and
`v = SR((F \circ C_{|_{h,1}})_{\geq d})`. The rank table entry for `h` then
becomes `(max(u,v),min(u,v))`.

For any specific tuple `(u,v)`, the rank group is all `h` such that the rank
table entry for `h` is `(u,v)`. The rank histogram is a mapping from each
`(u,v)` to the size of the rank group.

One last thing we need is the concept of the rank histogram with respect to a
given rank group. Fix an element `h \in F_2^n`. The rank histogram of `h` with
respect to the rank group `(u,v)` is defined as follows. Add `h` to all
elements of the rank group `(u,v)` to get a set `U \subset F_2^n`. For each
element `h'` of `U`, look at the rank group containing `h'`; suppose it is
`(u',v')`. The multiset containing the tuples `(u',v')` for each element
`h' \in U` is the rank histogram of `h` with respect to `(u,v)`.

The rank group `(u,v)` with respect to `(u',v')` is the multiset rank
histogram of each element `h` of the group `(u,v)` with respect to the group
`(u',v')`.

Algorithm
~~~~~~~~~

The main idea of the algorithm is that if `F` and `G` are affine equivalent,
then `SR(F_{\geq d}) = SR(G_{\geq d})`.

If `F` and `G` are affine equivalent with `F = A_2 \circ G \circ A_1`, we
start by trying to reconstruct `A_1`. The idea is that for any element of the
rank table `(u,v)` of `G`, matching rank information constrains where elements
can be mapped. If we find an entry `(u,v)` which contains only one element, we
know one point of `A_1`.

The rank groups can be large, so only doing this may still result in many
guesses. For some group `(u,v)`, we pick another group `(u',v')` and calculate
the rank group of `(u,v)` with respect to `(u',v')`. If this multiset contains
a unique element, then the element `h` of `(u,v)` corresponding to this element
must be matched to the corresponding element of `G`, due to the linearity of
`A_1`.

We can do this for any pair of groups, and if we find any element in the
multiset of low cardinality, we obtain a lot of information about possible
matchings for `A_1`.

Runtime
~~~~~~~

The algorithm is estimated to be `O(n^32^n)` for a random permutation. This is
based on assumptions about the distribution of the rank tables of random
functions.

EA equivalence
--------------

Given two Boolean functions `F,G : F_2^n \rightarrow F_2^m`, find two affine
permutations `A_1,A_2` and an affine transformation `A_3` such that
`F = A_2 \circ G \circ A_1 + A_3`.

Jacobian algorithm
..................

This algorithm can decide EA equivalence for quadratic functions only.

The Jacobian
~~~~~~~~~~~~

Given a vectorial Boolean function, and any element `a \in F_2^n`, the
derivative in direction `a` is defined by

`D_a F(x) = F(x+a) + F(x)`.

The Jacobian for a vectorial Boolean function `F(x) = (F_1(x),...,F_m(x))` is
defined as

`J F(x) = \begin{pmatrix}D_{e_1}F_1(x) & D_{e_2}F_1(x) & ... & D_{e_n}F_1(x) \\ D_{e_1}F_2(x) & D_{e_2}F_2(x) & ... & D_{e_n}F_2(x) \\ \vdots & \vdots & \vdots & \vdots \\ D_{e_1}F_m(x) & D_{e_2}F_m(x) & ... & D_{e_n}F_m(x) \end{pmatrix}`.

Here `e_i` is the `i`-th basis vector of `F_2^n`. We denote the linear part of
the Jacobian by `J_{lin}F(x)`.

The algorithm
~~~~~~~~~~~~~

The algorithm is based on the following two facts. If `F` and `G` are
EA-equivalent quadratic functions with `F = A_2 \circ G \circ A_1 + A_3`, then
we can assume that `A_1` and `A_3` are linear. So we have only
`A_2(x) = L_2(x) + a_2`.

The other fact is that

`J_{lin}F(x) = L_2\cdot J_{lin}G(A_1(x)) \cdot A_1`.

This allows us to start by searching for pairs `(L_2,A_1)` first, and then
deduce the other values later.

To deduce possible pairs `(L_2,A_1)`, the algorithm first tries to find
`A_1`. Since the rank of the matrix `Jac_{lin}F(x)` equals the rank of
`Jac_{lin}G(A_1(x))`, because all matrices and transformations are
permutations, `A_1(x)` can only be mapped to elements which result in the same
rank.

We compute all possible ranks of `Jac_{lin}F(x)` and `Jac_{lin}G(x)`. We then
look at the least common rank of these tables; say this value is `k`. Let
`S_F` be all inputs such that `Jac_{lin} F(x)` has rank `k`, and let `S_G` be
all `x` such that `Jac_{lin}G(x)` has rank `k`. By the previous observation,
`A_1` has to map elements from `S_F` to elements of `S_G`. If these sets
`S_F` and `S_G` are small (we can assume they are the same size), then the
number of guesses will not be too large.

To start, we guess the value of `A_1` on some elements of `S_F`. Having
guessed some values of `A_1`, we deduce values of `L_2`. If we have guessed
that `A_1u = w`, then the pair `(L_2,A_1) = (X,Y)` is a solution to the
linear system of equations

`X\cdot Jac_{lin}F(v) - Jac_{lin}F(w) \cdot Y = 0`,

`Y \cdot v = 0`.

We guess enough values of `A_1` so that this system has a unique solution,
since each guess gives more equations. Having done this and found a pair
`(L_2,A_1)`, we can deduce `A_3` and `a_2` with basic linear algebra.

The algorithm can be described as follows:

1. Compute the rank table of `F`:
   `R(F) = \{x \in F_2^n | rank(Jac_{lin}F(x)) = j \}`. Do the same for `G`.
2. Let `s` be the number of guesses of `A_1` we are going to make. Let
   `i = \min |R(F)|`. Pick `s` elements of `R(F)`. We then guess all possible
   values of `A_1` on these points, but only values inside `R`. Suppose the
   guesses are `A_1u_1 = w_1,...,A_1u_s = w_s`.
3. Try to solve the `s` systems of equations
   `X \cdot Jac_{lin}F(v_i) - Jac_{lin}F(w_i)\cdot Y,\: Y \cdot v_i = 0`. If
   this system has too many solutions, make another guess by temporarily
   increasing the value of `s`.
4. When the system of equations does not have too many solutions, find all
   solutions `(L_2,A_1)`. Then deduce the rest of the values `A_3` and `a_2`.
   If this is possible, we are done; otherwise, go back to step 2 and make
   another guess.

Runtime
~~~~~~~

The runtime of this algorithm is related to the rank table, which is related
to the differential uniformity of the function. Let `R = \min R(F)`. Then we
will at worst have to make around `R^s` guesses. For each such guess we have
to solve some linear equations, which can be done in around `(n^2+m^2)^w`,
where `w` is a matrix multiplication constant.

In total we get a time of

`O(max(n,m)^w2^n + R^s(m^2+n^2)^w)`,

where the first part is for computing the rank table. Note that when `F` is
APN all the values have the same rank, so `R = 2^n`, which is the worst case
for this algorithm.

References
==========

.. references::
