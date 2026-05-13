.. _nonlinearity:

Nonlinearity
============

Content extracted from ``data/Nonlinearity.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Nonlinearity  <https://boolean.wiki.uib.no/Nonlinearity>`

Background and Definition
-------------------------

:ref:`Vectorial Boolean Functions <vectorial_boolean_functions>` play an
essential role in the design of cryptographic algorithms, and as such should be
resistant to various types of cryptanalytic attacks. The notion of nonlinearity
was introduced by Nyberg :cite:p:`Nyberg:199300` in order to measure the resistance of vectorial Boolean
functions to Matsui's linear attack :cite:p:`Matsui:199400`.

This attack attempts to approximate the function used in an encryption
algorithm by a linear function, which is easy to analyze. It is therefore
applicable when the functions used in the encryption algorithm are close to
linear in some sense.

A natural measure of distance between two functions `F` and `G` is the Hamming
distance, i.e.

`d_H(F,G)=|\{x:F(x)\neq G(x)\}|`.

Formally, the nonlinearity `nl(F)` of an `(n,m)`-function `F` is the minimum
distance between any component function of `F` and any affine Boolean function.
In other words,

`nl(F)=\min\{d_H(u\cdot F,f_a):0\neq u\in\mathbb{F}_2^m,\ f_a:\mathbb{F}_2^n\to\mathbb{F}_2\text{ affine}\}`.

Properties
----------

Nonlinearity remains invariant under CCZ-equivalence and, therefore, under
extended affine equivalence and affine equivalence as well.

If `F` is an `(n,n)`-permutation, then `F` and `F^{-1}` have the same
nonlinearity.

The nonlinearity of an `(n,m)`-function `F` can be expressed in terms of its
Walsh transform via the identity

`nl(F)=2^{n-1}-\frac{1}{2}\max\{|W_F(u,v)|:u\in\mathbb{F}_2^n,\ 0\neq v\in\mathbb{F}_2^m\}`.

There is a relation between the maximal possible nonlinearity of vectorial
Boolean functions and the possible parameters of certain linear codes :cite:p:`Carlet:199811`.

If `C` is a linear code containing the Reed-Muller code `RM(1,n)` as a subcode,
let `(b_1,b_2,\ldots,b_K)` be a basis of `C` completing a basis
`(b_1,b_2,\ldots,b_{n+1})` of `RM(1,n)`. Then the `n`-variable Boolean
functions corresponding to the vectors `b_{n+2},\ldots,b_K` are the coordinate
functions of an `(n,K-n-1)`-function with nonlinearity `D`.

Conversely, given an `(n,m)`-function `F` of nonlinearity `D>0`, the linear code
obtained as the union of all cosets

`\{v\cdot F+RM(1,n):v\in\mathbb{F}_2^m\}`

has corresponding parameters.

Bounds on the Nonlinearity of Vectorial Boolean Functions
---------------------------------------------------------

The covering radius bound for Boolean functions can naturally be extended to
vectorial Boolean functions, stating

`nl(F)\leq 2^{n-1}-2^{n/2-1}`

for any `(n,m)`-function `F`.

:ref:`Bent Functions <bent_functions>` are defined as those meeting this bound
with equality.

The Sidelnikov-Chabaud-Vaudenay (SCV) bound :cite:p:`Tietäväinen:199200` :cite:p:`Chabaud:199500` bounds the nonlinearity of any
`(n,m)`-function, with `m\geq n-1`, by

`nl(F)\leq 2^{n-1}-\frac{1}{2}\sqrt{3\cdot 2^n-2-2\frac{(2^n-1)(2^{n-1}-1)}{2^m-1}}`.

The SCV bound coincides with the covering radius bound for `m=n-1`, and is
strictly sharper than the covering radius bound for `m\geq n`. For `m>n`, the
square root in the bound cannot be an integer, and thus the SCV bound can be
tight only for `m=n`.

In this case, the bound becomes

`nl(F)\leq 2^{n-1}-2^{(n-1)/2}`.

This motivates the definition of almost bent functions as those
`(n,n)`-functions that meet the SCV bound with equality.

References
==========

.. references::
