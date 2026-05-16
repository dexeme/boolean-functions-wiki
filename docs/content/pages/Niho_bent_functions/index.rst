.. _niho_bent_functions:

Niho bent functions
===================

Content extracted from ``data/Niho_bent_functions.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Niho_bent_functions  <https://boolean.wiki.uib.no/Niho_bent_functions>`

Background and Definitions
--------------------------

A power Boolean function `x^d` defined on `\mathbb{F}_{2^n}` is called a Niho
power function if its restriction to `\mathbb{F}_{2^m}` is linear, where
`n=2m`.

Niho bent functions are :ref:`bent functions <bent_functions>` with Niho
exponents.

Niho bent functions can be represented in bivariate form as

`g(x,y)=\begin{cases}\operatorname{Tr}_m\left(xG\left(\frac{y}{x}\right)\right),&\text{ if }x\neq 0,\\ \operatorname{Tr}_m(\mu y),&\text{ if }x=0,\end{cases}`

where `\mu\in\mathbb{F}_{2^m}` and
`G:\mathbb{F}_{2^m}\to\mathbb{F}_{2^m}` satisfy the following conditions:

`\mathcal{F}:z\mapsto G(z)+\mu z` is a permutation over
`\mathbb{F}_{2^m}`.

For any nonzero `\beta\in\mathbb{F}_{2^m}`, the map

`z\mapsto\mathcal{F}(z)+\beta z`

is 2-to-1 on `\mathbb{F}_{2^m}`.

The second condition implies the first one, and it is necessary and sufficient
for `g` to be bent.

One can obtain a univariate representation of a Niho bent function from the
bivariate one by making the substitutions

`x=t+t^{2^m}`

and

`y=\alpha t+(\alpha t)^{2^m}`,

where `\alpha` is a primitive element of `\mathbb{F}_{2^m}`.

Examples
--------

The known Niho-type bent functions in univariate form include the following.

1. Quadratic functions

   `\operatorname{Tr}_m(\alpha t^{2^m+1})`,

   where `\alpha\in\mathbb{F}_{2^m}`.

2. Binomials of the form

   `f(t)=\operatorname{Tr}_n(\alpha_1t^{d_1}+\alpha_2t^{d_2})`,

   where `2d_1\equiv 2^m+1\pmod{2^n-1}` and
   `\alpha_1,\alpha_2\in\mathbb{F}_{2^n}^{*}` are such that

   `(\alpha_1+\alpha_1^{2^m})^2=\alpha_2^{2^m+1}`.

   These functions have algebraic degree `m` and do not belong to the completed
   Maiorana-McFarland class.

3. Let `1<r<m` with `\gcd(r,m)=1`. Then

   `f(t)=\operatorname{Tr}_n\left(a^2t^{2^m+1}+(a+a^{2^m})\sum_{i=1}^{2^{r-1}-1}t^{d_i}\right)`,

   where

   `2^rd_i=(2^m-1)i+2^r`

   and `a\in\mathbb{F}_{2^n}` is such that `a+a^{2^m}\neq 0`.

   This function has algebraic degree `r+1` and belongs to the completed
   Maiorana-McFarland class.

References
==========

.. references::
