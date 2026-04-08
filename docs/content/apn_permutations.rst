APN Permutations
================

Content partially extracted from ``data/APN_Permutations.txt``.
Original page: `https://boolean.wiki.uib.no/APN_Permutations <https://boolean.wiki.uib.no/APN_Permutations>`_

Characterization of Permutations
--------------------------------

For an `(n,n)`-function `F`, permutation can be characterized by balanced component functions:
`F` is a permutation iff all nonzero components `f_\lambda` are balanced.

Using directional derivatives and
`{\displaystyle \mathcal{F}(f)=\sum_{x\in\mathbb{F}_{2^n}}(-1)^{f(x)}=2^n-2wt(f)}`,
equivalent criteria are:

`{\displaystyle \sum_{a\in\mathbb{F}_{2^n}^*}\mathcal{F}(D_af_\lambda)=-2^n}`
for all `\lambda\in\mathbb{F}_{2^n}^*`,
or equivalently
`{\displaystyle \sum_{\lambda\in\mathbb{F}_{2^n}^*}\mathcal{F}(D_af_\lambda)=-2^n}`
for all `a\in\mathbb{F}_{2^n}^*`.

Characterization of APN Permutations
------------------------------------

Known APN permutations (up to CCZ-equivalence) belong to a few families:

1. APN monomials in odd dimension.
2. One infinite quadratic family in dimension `3n` (odd `n`, `\gcd(n,3)=1`).
3. Dillon's APN permutation in dimension 6.
4. Two sporadic quadratic APN permutations in dimension 9.

For APN maps, no component has degree 1.
For even `n`, components are not partially bent, hence not quadratic.

Autocorrelation Characterization
--------------------------------

An `(n,n)`-function `F` is an APN permutation iff, for every `a\in\mathbb{F}_{2^n}^*`:

`{\displaystyle \sum_{\lambda\in\mathbb{F}_{2^n}^*}\mathcal{F}(D_af_\lambda)=-2^n}`
and
`{\displaystyle \sum_{\lambda\in\mathbb{F}_{2^n}^*}\mathcal{F}^2(D_af_\lambda)=2^{2n}}`.

APN Power Functions
-------------------

If `F(x)=x^d` is APN over `\mathbb{F}_{2^n}`:

- for odd `n`, `\gcd(d,2^n-1)=1`, so APN power functions are permutations;
- for even `n`, `\gcd(d,2^n-1)=3`, so they are 3-to-1 on `\mathbb{F}_{2^n}^*`.

Codes and APN Permutations
--------------------------

APN properties can be expressed via associated binary linear codes.
In particular, `F` is APN iff the associated code has minimum distance 5.

Also, `F` is CCZ-equivalent to an APN permutation iff the dual associated code is a double simplex code.

Dimension 6 and the Open Problem
--------------------------------

The long-standing conjecture against APN permutations in even dimension was broken in dimension 6
by Dillon (2009), with a function CCZ-equivalent to the Kim function.

The existence of APN permutations for even dimensions `n\ge 8` remains open.
