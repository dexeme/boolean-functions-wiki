Boolean Functions
=================

Content partially extracted from ``data/Boolean_Functions.txt``.
Original page:
:link:`https://boolean.wiki.uib.no/Boolean_Functions  <https://boolean.wiki.uib.no/Boolean_Functions>`

Introduction
-------------------------------------------------------------------------------

Let `\mathbb{F}_{2}^{n}` be the vector space of dimension `n` over the finite field with two elements. The vector space can also
be endowed with the structure of the field, the finite field with `2^n` elements, `\mathbb{F}_{2^n}`.
A function `{\displaystyle f:\mathbb {F} _{2}^{n}\rightarrow \mathbb {F} }` is called a Boolean function in dimenstion `n` (or `n`-variable Boolean function ).
Given `{\displaystyle x=(x_{1},\ldots ,x_{n})\in \mathbb {F} _{2}^{n}}`, the support of `x` is the set
`{\displaystyle supp_{x}=\{i\in \{1,\ldots ,n\}:x_{i}=1\}}`. The Hamming weight of `x` is the size of its support
`({\displaystyle w_{H}(x)=|supp_{x}|})`. Similarly the Hamming weight of a Boolean function `f` is the size of its support, i.e. the set
`{\displaystyle \{x\in \mathbb {F} _{2}^{n}:f(x)\neq 0\}}`. The Hamming distance of two functions `f,g (𝖽_{𝐻} (f,g))` is the size of the set
`{\displaystyle \{x\in\mathbb{F}_2^n : f(x)\neq g(x) \}\ (w_{H}(f\oplus g))}`.

Representation of a Boolean function
-------------------------------------------------------------------------------

There exist different ways to represent a Boolean function. A simple, but often not efficient, one is by its truth-table.
For example consider the following truth-table for a 3-variable Boolean function `f`.

Algebraic Normal Form (ANF)
...............................................................................

An `n`-variable Boolean function can be represented by a multivariate polynomial over `\mathbb{F}_2` of the form
`{\displaystyle f(x)=\bigoplus_{I\subseteq\{1,\ldots,n\}}a_I\left(\prod_{i\in I}x_i\right)\in \mathbb{F}_2 /(x_1^2\oplus x_1,\ldots,x_n^2\oplus x_n)}`.
Such representation is unique and is the algebraic normal form of `f` (ANF).

The degree of the ANF is called the algebraic degree of the function:
`d^\circ f = \max\{|I|:a_I\neq 0\}`.
Based on the algebraic degree:

- `f` is affine if `d^\circ f = 1`;
- `f` is linear if `d^\circ f = 1` and `f(0)=0`;
- `f` is quadratic if `d^\circ f = 2`.

Affine functions are of the form `f(x)=u\cdot x + e`, with `u\in\mathbb{F}_2^n` and `e\in\mathbb{F}_2`.

Trace representation
...............................................................................

Identifying the vector space with the finite field, an `n`-variable Boolean function of even weight
(thus with algebraic degree at most `n-1`) admits a unique trace representation:

`{\displaystyle f(x)=\sum_{j\in\Gamma_n}\mathrm{Tr}_{\mathbb{F}_{2^{o(j)}}/\mathbb{F}_2}(A_jx^j),\quad x\in\mathbb{F}_{2^n}}`,

where `\Gamma_n` is a set of representatives of cyclotomic cosets of 2 modulo `(2^n-1)`, `o(j)` is the size of the cyclotomic coset containing `j`,
`A_j\in\mathbb{F}_{2^{o(j)}}`, and `\mathrm{Tr}_{\mathbb{F}_{2^{o(j)}}/\mathbb{F}_2}` is the trace map to `\mathbb{F}_2`.

This is also called the univariate representation.
One may also write `f` as `{\displaystyle \mathrm{Tr}_{\mathbb{F}_{2^n}/\mathbb{F}_2}(P(x))}`, for a polynomial `P` over `\mathbb{F}_{2^n}`,
but this form is not unique in general.

In trace representation, the algebraic degree is given by
`{\displaystyle \max_{j\in\Gamma_n,\ A_j\neq 0} w_2(j)}`,
where `w_2(j)` is the Hamming weight of the binary expansion of `j`.

On the weight of a Boolean function
-------------------------------------------------------------------------------

For an `n`-variable Boolean function `f`, the following relations hold:

- If `d^\circ f=1`, then `w_H(f)=2^{n-1}`.
- If `d^\circ f=2`, then `w_H(f)=2^{n-1}` or `w_H(f)=2^{n-1}\pm 2^{n-1-h}`, with `0\leq h\leq n/2`.
- If `d^\circ f\le r` and `f\neq 0`, then `w_H(f)\ge 2^{n-r}`.
- `w_H(f)` is odd if and only if `d^\circ f=n`.

The Walsh transform
-------------------------------------------------------------------------------

The Walsh transform `W_f` is the discrete Fourier transform of the sign function `(-1)^{f(x)}`.
With inner product `x\cdot u` in `\mathbb{F}_2^n`, the Walsh value at `u\in\mathbb{F}_2^n` is

`{\displaystyle W_f(u)=\sum_{x\in\mathbb{F}_2^n}(-1)^{f(x)+x\cdot u}}`.

The Walsh support of `f` is the set
`{\displaystyle \{u\in\mathbb{F}_2^n:W_f(u)\neq 0\}}`.

Properties of the Walsh transform
...............................................................................

For every `n`-variable Boolean function `f`, we have:

- Inverse Walsh transform:
  `{\displaystyle \sum_{u\in\mathbb{F}_2^n}W_f(u)(-1)^{u\cdot x}=2^n(-1)^{f(x)}}`.
- Parseval relation:
  `{\displaystyle \sum_{u\in\mathbb{F}_2^n}W_f(u)^2=2^{2n}}`.
- Poisson summation formula:
  for any subspace `E\subseteq\mathbb{F}_2^n` and `a,b\in\mathbb{F}_2^n`,
  `{\displaystyle \sum_{u\in a+E^\perp}(-1)^{b\cdot u}W_f(u)=|E^\perp|(-1)^{a\cdot b}\sum_{x\in b+E}(-1)^{f(x)+a\cdot x}}`,
  where `E^\perp=\{u\in\mathbb{F}_2^n:u\cdot x=0,\ \forall x\in E\}`.

Equivalences of Boolean functions
-------------------------------------------------------------------------------

Two `n`-variable Boolean functions `f,g` are affine equivalent if there exist a linear automorphism `L`
and a vector `a` such that `g(x)=f(L(x)+a)`.

They are extended-affine equivalent (EA-equivalent) if there exist a linear automorphism `L`,
an affine Boolean function `\ell`, and a vector `a` such that
`g(x)=f(L(x)+a)+\ell(x)`.

A parameter preserved by an equivalence relation is called an invariant.
The algebraic degree is invariant under affine equivalence, and for non-affine functions also under EA-equivalence.

If `f` and `g` are affine equivalent, then
`{\displaystyle W_g(u)=(-1)^{u\cdot L^{-1}(a)}W_f(L^{-1}(u))}`.

Properties important for cryptographic applications
-------------------------------------------------------------------------------

Balanced functions
...............................................................................

An `n`-variable Boolean function `f` is balanced if `w_H(f)=2^{n-1}`, i.e. its output is uniformly distributed.
Balanced functions do not have maximal algebraic degree.
Most cryptographic applications use balanced Boolean functions.

The Nonlinearity
...............................................................................

The nonlinearity of `f` is its minimal Hamming distance to the set `\mathcal{A}` of affine `n`-variable functions:
`{\displaystyle \mathcal{NL}(f)=\min_{g\in\mathcal{A}}d_H(f,g)}`.

Equivalent Walsh expression:
`{\displaystyle \mathcal{NL}(f)=2^{n-1}-\frac{1}{2}\max_{u\in\mathbb{F}_2^n}|W_f(u)|}`.

From Parseval relation, the covering radius bound is
`{\displaystyle \mathcal{NL}(f)\le 2^{n-1}-2^{n/2-1}}`.

A function attaining this bound is called bent (`n` even, and the function is not balanced).
`f` is bent iff `W_f(u)=\pm 2^{n/2}` for every `u\in\mathbb{F}_2^n`.
Equivalently, `f` is bent iff for every nonzero `a`, the derivative
`D_af(x)=f(x+a)+f(x)` is balanced.

Correlation-immunity order
...............................................................................

A Boolean function `f` is `m`-th order correlation-immune if the output distribution is unchanged
when any `m` input variables are fixed.

Balanced `m`-th order correlation-immune functions are called `m`-resilient.
If `f` is an `n`-variable function with correlation-immunity order `m`, then
`m+d^\circ f\le n`.
If `f` is also balanced, then
`m+d^\circ f\le n-1`.
