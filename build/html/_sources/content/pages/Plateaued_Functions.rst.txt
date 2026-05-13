.. _plateaued_functions:

Plateaued Functions
===================

Content extracted from ``data/Plateaued_Functions.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Plateaued_Functions  <https://boolean.wiki.uib.no/Plateaued_Functions>`

Background and Definition
-------------------------

A Boolean function `f:\mathbb{F}_{2^n}\to\mathbb{F}_2` is said to be
plateaued if its Walsh transform takes at most three distinct values, namely
`0` and `\pm\mu` for some positive integer `\mu`, called the amplitude of `f`.

This notion can be naturally extended to vectorial Boolean functions by
applying it to each component. More precisely, if `F` is an `(n,m)`-function,
then `F` is plateaued if all its component functions `u\cdot F`, with
`u\neq 0`, are plateaued.

If all component functions are plateaued and have the same amplitude, then `F`
is plateaued with single amplitude.

The characterization by derivatives suggests the following definition: a
vectorial Boolean function `F` is strongly plateaued if, for every `a` and every
`v`, the size of the set

`\{b\in\mathbb{F}_2^n:D_aD_bF(x)=v\}`

does not depend on `x`. Equivalently, the size of

`\{b\in\mathbb{F}_2^n:D_aF(b)=D_aF(x)+v\}`

does not depend on `x`.

Equivalence Relations
---------------------

The class of functions that are plateaued with single amplitude is
CCZ-invariant.

The class of plateaued functions is EA-invariant.

Relations to Other Classes of Functions
---------------------------------------

All :ref:`bent functions <bent_functions>` and semi-bent Boolean functions are
plateaued.

Any vectorial almost bent function is plateaued with single amplitude.

Constructions of Boolean Plateaued Functions
--------------------------------------------

Generalization of the Maiorana-McFarland Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Maiorana-McFarland :cite:p:`Camion:199200` class of bent functions can be generalized into the
class of functions `f_{\phi,h}` of the form

`f_{\phi,h}(x,y)=x\cdot\phi(y)+h(y)`

for `x\in\mathbb{F}_2^r` and `y\in\mathbb{F}_2^s`, where `r` and `s` are
positive integers, `n=r+s`,
`\phi:\mathbb{F}_2^s\to\mathbb{F}_2^r` is arbitrary, and
`h:\mathbb{F}_2^s\to\mathbb{F}_2` is any Boolean function.

The Walsh transform of `f_{\phi,h}` at `(a,b)` is

`W_{f_{\phi,h}}(a,b)=2^r\sum_{y\in\phi^{-1}(a)}(-1)^{b\cdot y+h(y)}`.

If `\phi` is injective, then `f_{\phi,h}` is plateaued of amplitude `2^r`.
If `\phi` takes each value in its image set two times, then `f_{\phi,h}` is
plateaued of amplitude `2^{r+1}`.

Characterization by the Derivatives
-----------------------------------

Using the fact that a Boolean function `f` is plateaued if and only if the
expression

`\sum_{a,b\in\mathbb{F}_2^n}(-1)^{D_aD_bf(x)}`

does not depend on `x\in\mathbb{F}_2^n`, one can derive the following
characterization :cite:p:`Carlet:201500`.

Let `F` be an `(n,m)`-function. Then `F` is plateaued if and only if, for every
`v\in\mathbb{F}_2^m`, the size of the set

`\{(a,b)\in(\mathbb{F}_2^n)^2:D_aD_bF(x)=v\}`

does not depend on `x`.

The function `F` is plateaued with single amplitude if and only if the size of
this set depends neither on `x` nor on `v\in\mathbb{F}_2^m`, for `v\neq 0`.

Moreover, for every `F`, the value distribution of `D_aD_bF(x)` equals that of
`D_aF(b)+D_aF(x)` when `(a,b)` ranges over `(\mathbb{F}_2^n)^2`. If two
plateaued functions `F` and `G` have the same distribution, then all of their
component functions `u\cdot F` and `u\cdot G` have the same amplitude.

Power Functions
~~~~~~~~~~~~~~~

Let `F(x)=x^d`. Then, for every `v,x,\lambda\in\mathbb{F}_{2^n}` with
`\lambda\neq 0`,

`|\{(a,b)\in\mathbb{F}_{2^n}^2:D_aF(b)+D_aF(x)=v\}|=|\{(a,b)\in\mathbb{F}_{2^n}^2:D_aF(b)+D_aF(x/\lambda)=v/\lambda^d\}|`.

Thus `F` is plateaued if and only if, for every `v\in\mathbb{F}_{2^n}`,

`|\{(a,b)\in\mathbb{F}_{2^n}^2:D_aF(b)+D_aF(1)=v\}|=|\{(a,b)\in\mathbb{F}_{2^n}^2:D_aF(b)+D_aF(0)=v\}|`.

The function `F` is plateaued with single amplitude if and only if the size
above does not, in addition, depend on `v\neq 0`.

Functions with Unbalanced Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let `F` be an `(n,m)`-function. Then `F` is plateaued with all components
unbalanced if and only if, for every `v,x\in\mathbb{F}_2^n`,

`|\{(a,b)\in(\mathbb{F}_2^n)^2:D_aD_bF(x)=v\}|=|\{(a,b)\in(\mathbb{F}_2^n)^2:F(a)+F(b)=v\}|`.

Moreover, `F` is plateaued with single amplitude if and only if this value does
not, in addition, depend on `v` for `v\neq 0`.

Strongly Plateaued Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Boolean function is strongly plateaued if and only if it is partially bent.
A vectorial Boolean function is strongly plateaued if and only if all of its
component functions are partially bent.

In particular, bent and quadratic Boolean and vectorial functions are strongly
plateaued. The image set `\operatorname{Im}(D_aF)` of any derivative of a
strongly plateaued function `F` is an affine space.

Characterization by the Auto-Correlation Functions
--------------------------------------------------

Recall that the autocorrelation function of a Boolean function `f` is defined
as

`\Delta_f(a)=\sum_{x\in\mathbb{F}_2^n}(-1)^{f(x)+f(x+a)}`.

An `n`-variable Boolean function `f` is plateaued if and only if, for every
`x\in\mathbb{F}_2^n`,

`2^n\sum_{a\in\mathbb{F}_2^n}\Delta_f(a)\Delta_f(a+x)=\left(\sum_{a\in\mathbb{F}_2^n}\Delta_f^2(a)\right)\Delta_f(x)`.

An `(n,m)`-function `F` is plateaued if and only if, for every
`x\in\mathbb{F}_2^n` and `u\in\mathbb{F}_2^m`,

`2^n\sum_{a\in\mathbb{F}_2^n}\Delta_{u\cdot F}(a)\Delta_{u\cdot F}(a+x)=\left(\sum_{a\in\mathbb{F}_2^n}\Delta_{u\cdot F}^2(a)\right)\Delta_{u\cdot F}(x)`.

Furthermore, `F` is plateaued with single amplitude if and only if, for every
`x\in\mathbb{F}_2^n` and `u\in\mathbb{F}_2^m`,

`\sum_{a\in\mathbb{F}_2^n}\Delta_{u\cdot F}(a)\Delta_{u\cdot F}(a+x)=\mu^2\Delta_{u\cdot F}(x)`.

Alternatively, `F` is plateaued if and only if, for every
`x,v\in\mathbb{F}_2^n`,

`2^n|\{(a,b,c)\in(\mathbb{F}_2^n)^3:F(a)+F(b)+F(c)+F(a+b+c+x)=v\}|`

equals

`|\{(a,b,c,d)\in(\mathbb{F}_2^n)^4:F(a)+F(b)+F(c)+F(a+b+c)+F(d)+F(d+x)=v\}|`.

Characterization by Power Moments of the Walsh Transform
--------------------------------------------------------

First Characterization
~~~~~~~~~~~~~~~~~~~~~~

A Boolean function `f:\mathbb{F}_{2^n}\to\mathbb{F}_2` is plateaued if and
only if, for every `0\neq\alpha\in\mathbb{F}_2^n`,

`\sum_{w\in\mathbb{F}_2^n}W_f(w+\alpha)W_f^3(w)=0`.

An `(n,m)`-function `F` is plateaued if and only if, for every
`u\in\mathbb{F}_2^m` and `0\neq\alpha\in\mathbb{F}_2^n`,

`\sum_{w\in\mathbb{F}_2^n}W_F(w+\alpha,u)W_F^3(w,u)=0`.

Furthermore, `F` is plateaued with single amplitude if and only if, in
addition, the sum

`\sum_{w\in\mathbb{F}_2^n}W_F^4(w,u)`

does not depend on `u` for `u\neq 0`.

Second Characterization
~~~~~~~~~~~~~~~~~~~~~~~

A Boolean function `f:\mathbb{F}_{2^n}\to\mathbb{F}_2` is plateaued if and
only if, for every `b\in\mathbb{F}_2^n`,

`\sum_{a\in\mathbb{F}_2^n}W_f^4(a)=2^n(-1)^{f(b)}\sum_{a\in\mathbb{F}_2^n}(-1)^{a\cdot b}W_f^3(a)`.

An `(n,m)`-function `F` is plateaued if and only if, for every
`b\in\mathbb{F}_2^n` and every `u\in\mathbb{F}_2^m`,

`\sum_{a\in\mathbb{F}_2^n}W_F^4(a,u)=2^n(-1)^{u\cdot F(b)}\sum_{a\in\mathbb{F}_2^n}(-1)^{a\cdot b}W_F^3(a,u)`.

Moreover, `F` is plateaued with single amplitude if and only if the two sums
above do not depend on `u` for `u\neq 0`.

Third Characterization
~~~~~~~~~~~~~~~~~~~~~~

Any Boolean function `f` in `n` variables satisfies

`\left(\sum_{a\in\mathbb{F}_2^n}W_f^4(a)\right)^2\leq 2^{2n}\left(\sum_{a\in\mathbb{F}_2^n}W_f^6(a)\right)`,

with equality if and only if `f` is plateaued.

Any `(n,m)`-function `F` satisfies

`\sum_{u\in\mathbb{F}_2^m}\left(\sum_{a\in\mathbb{F}_2^n}W_F^4(a,u)\right)^2\leq 2^{2n}\sum_{u\in\mathbb{F}_2^m}\left(\sum_{a\in\mathbb{F}_2^n}W_F^6(a,u)\right)`,

with equality if and only if `F` is plateaued.

In addition, every `(n,m)`-function satisfies

`\sum_{u\in\mathbb{F}_2^m}\sum_{a\in\mathbb{F}_2^n}W_F^4(a,u)\leq 2^n\sum_{u\in\mathbb{F}_2^m}\sqrt{\sum_{a\in\mathbb{F}_2^n}W_F^6(a,u)}`,

with equality if and only if `F` is plateaued.

Characterization of APN among Plateaued Functions
-------------------------------------------------

Characterization by the Derivatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One useful property of quadratic functions, which extends to plateaued
functions, is that it suffices to consider the number of solutions to the
differential equation

`D_aF(x)=D_aF(0)`

in order to decide whether a given function `F` is APN.

More precisely, a plateaued `(n,n)`-function `F` is APN if and only if the
equation

`F(x)+F(x+a)=F(0)+F(a)`

has at most two solutions for any `0\neq a\in\mathbb{F}_2^n`.

Characterization by the Walsh Transform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose `F` is a plateaued `(n,n)`-function with `F(0)=0`. Then `F` is APN if
and only if

`|\{(x,b)\in\mathbb{F}_{2^n}^2:F(x)+F(x+b)+F(b)=0\}|=3\cdot 2^n-2`,

or, equivalently,

`\sum_{a\in\mathbb{F}_{2^n},\,u\in\mathbb{F}_{2^n}^{*}}W_F^3(a,u)=2^{2n+1}(2^n-1)`.

Any `(n,n)`-function satisfies the inequality

`3\cdot 2^{3n}-2^{2n+1}\leq\sum_{u\in\mathbb{F}_2^n}\sqrt{\sum_{a\in\mathbb{F}_2^n}W_F^6(a,u)}`,

with equality if and only if `F` is APN plateaued.

If `2^{\lambda_u}` denotes the amplitude of the component function `u\cdot F`
of a given plateaued function `F`, then `F` is APN if and only if

`\sum_{0\neq u\in\mathbb{F}_2^n}2^{2\lambda_u}\leq 2^{n+1}(2^n-1)`.

Functions with Unbalanced Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let `F` be an `(n,n)`-plateaued function with all components unbalanced. Then

`|\{(a,b)\in(\mathbb{F}_2^n)^2:a\neq b,\ F(a)=F(b)\}|\geq 2\cdot(2^n-1)`,

with equality if and only if `F` is APN.

References
==========

.. references::
