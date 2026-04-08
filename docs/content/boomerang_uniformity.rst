Boomerang Uniformity
====================

Content partially extracted from ``data/Boomerang_uniformity.txt``.
Original page: `https://boolean.wiki.uib.no/Boomerang_uniformity <https://boolean.wiki.uib.no/Boomerang_uniformity>`_

Background and Definitions
--------------------------

The boomerang attack (Wagner, 1999) is a cryptanalysis technique against block ciphers based on differential cryptanalysis.
To study resistance to this attack, Cid et al. introduced the Boomerang Connectivity Table (BCT).
Later, Boura and Canteaut introduced the notion of boomerang uniformity.

Boomerang Connectivity Table (BCT)
----------------------------------

Let `F:\mathbb{F}_{2^n}\to\mathbb{F}_{2^n}` be a permutation.
The Boomerang Connectivity Table `T_F` is the `2^n\times 2^n` table defined by

`{\displaystyle T_F(a,b)=\left|\left\{x\in\mathbb{F}_{2^n}:\ F^{-1}(F(x)+a)+F^{-1}(F(x+b)+a)=b\right\}\right|}`.

The boomerang uniformity of `F` is
`{\displaystyle \beta_F=\max_{a,b\in\mathbb{F}_{2^n}^*} T_F(a,b)}`.

Main Properties
---------------

For a permutation `F`, the following properties hold:

- `\beta_F` is invariant under inversion and affine equivalence, but not under EA- and CCZ-equivalence.
- If `F'=A_2\circ F\circ A_1` with affine permutations `A_1,A_2`, then
  `{\displaystyle T_{F'}(a,b)=T_F(L_1(a),L_2^{-1}(b))}`,
  where `L_i` is the linear part of `A_i`.
- For the inverse permutation:
  `{\displaystyle T_{F^{-1}}(a,b)=T_F(b,a)}`.
- Relation with differential uniformity:
  `{\displaystyle \delta_F\le \beta_F}` and `{\displaystyle \delta_F=2\iff \beta_F=2}`.
- Alternative counting form:
  `{\displaystyle T_F(a,b)=\left|\left\{(x,y):\ F(x+a)+F(y+a)=b,\ F(x)+F(y)=b\right\}\right|}`.
- If `F` is a power permutation, then `{\displaystyle \beta_F=\max_{b\neq 0}T_F(1,b)}`.
- If `F` is quadratic, then `{\displaystyle \delta_F\le \beta_F\le \delta_F(\delta_F-1)}`.

SageCell Demo
-------------

.. sagecell::

   2 + 2
