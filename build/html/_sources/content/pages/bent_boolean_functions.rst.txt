Bent Boolean Functions
======================

Content partially extracted from ``data/Bent_Boolean_Functions.txt``.
Original page:
:link:`https://boolean.wiki.uib.no/Bent_Boolean_Functions  <https://boolean.wiki.uib.no/Bent_Boolean_Functions>`

Definition and Equivalent Characterizations
-------------------------------------------

An `n`-variable Boolean function `f` (with `n` even) is called bent when its distance to the set of all affine `n`-variable functions
(the nonlinearity of `f`) equals `2^{n-1}-2^{n/2-1}`.

Equivalent characterizations include:

- `f` is bent iff `W_f(u)` takes only the values `\pm 2^{n/2}`;
- `f` is bent iff `W_f(u)\equiv 2^{n/2}\ (\mathrm{mod}\ 2^{n/2+1})`;
- the distance from `f` to any affine function equals `2^{n-1}\pm 2^{n/2-1}`;
- for every nonzero `a`, the derivative `D_af(x)=f(x+a)\oplus f(x)` is balanced;
- for any `x\in\mathbb{F}_2^n`, `{\displaystyle \sum_{a,b\in\mathbb{F}_2^n}(-1)^{D_aD_bf(x)}=2^n}`;
- the matrix `H=(( -1 )^{f(x\oplus y)})_{x,y\in\mathbb{F}_2^n}` is Hadamard (`H H^t = 2^n I`);
- the support of `f` is a difference set of the elementary Abelian 2-group `\mathbb{F}_2^n`.

Bent functions are also called perfect nonlinear functions.

Dual of a Bent Function
-----------------------

The dual of a bent function `f` is also bent, and is defined by
`{\displaystyle W_f(u)=2^{n/2}(-1)^{\tilde{f}(u)}}`.

The dual of the dual is the original function.

Bent Functions and Algebraic Degree
-----------------------------------

For even `n\ge 4`, the algebraic degree of any bent Boolean function is at most `n/2`.

The algebraic degrees of a bent function and its dual satisfy
`{\displaystyle \frac{n}{2}-d^\circ f\geq \frac{\frac{n}{2}-d^\circ\tilde{f}}{d^\circ\tilde{f}-1}}`.

No affine function is bent.

When `f` is quadratic, it is affine equivalent to
`{\displaystyle x_1x_2\oplus x_3x_4\oplus\cdots\oplus x_{n-1}x_n\oplus\epsilon,\ (\epsilon\in\mathbb{F}_2)}`.

The characterization of cubic bent functions is known for small dimensions (`n\le 8`).

Constructions
-------------

Maiorana-McFarland Construction
...............................

Let `n=2m` and identify `\mathbb{F}_2^n` with pairs `(\mathbf{x},\mathbf{y})`, where `\mathbf{x},\mathbf{y}\in\mathbb{F}_2^m`.
Define
`{\displaystyle f(x,y)=x\cdot \pi(y)\oplus g(y)}`,
where `\pi` is a permutation of `\mathbb{F}_2^m` and `g` is any `m`-variable Boolean function.

Any such function is bent (bijectivity of `\pi` is necessary and sufficient).

Its dual is
`{\displaystyle \tilde{f}(x,y)=y\cdot\pi^{-1}(x)\oplus g(\pi^{-1}(x))}`.

Up to affine equivalence, this construction contains all quadratic bent functions and all bent functions in at most 6 variables.
