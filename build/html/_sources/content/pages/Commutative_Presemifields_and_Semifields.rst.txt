Commutative Presemifields and Semifields
========================================

Content extracted from ``data/Commutative_Presemifields_and_Semifields.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Commutative_Presemifields_and_Semifields <https://boolean.wiki.uib.no/Commutative_Presemifields_and_Semifields>`

Background
----------

For a prime `p` and a positive integer `n`, let
`\mathbb {F} _{p^{n}}` be the finite field with `p^{n}`
elements. Let `F` be a map from the finite field to itself. Such a
function admits a unique representation as a polynomial of degree at most
`p^{n}-1`, i.e.
`F(x)=\sum_{j=0}^{p^n-1}a_jx^j, a_j\in\mathbb{F}_{p^n}`.

The function `F` is:

* linear if `F(x)=\sum_{j=0}^{n-1}a_jx^{p^j}`;
* affine if it is the sum of a linear function and a constant;
* a DO (Dembowski-Ostrim) polynomial if
  `F(x)=\sum_{0\le i\le j<n}a_{ij}x^{p^i+p^j}`;
* quadratic if it is the sum of a DO polynomial and an affine function.

For `\delta` a positive integer, the function `F` is called
differentially `\delta`-uniform if, for any pairs
`a,b\in\mathbb{F}_{p^n}` with `a\ne0`, the equation
`F(x+a)-F(x)=b` admits at most `\delta` solutions.

A function `F` is called planar or perfect nonlinear (PN) if
`\delta_F=1`. Obviously such functions exist only for `p` an odd
prime. In the even case the smallest possible case for `\delta` is two
(`APN <Differential_uniformity.html>`_ function). For planar functions, all
the nonzero derivatives `D_aF(x)=F(x+a)-F(x)` are permutations.

Equivalence Relations
---------------------

Two functions `F` and `F'` from `\mathbb{F}_{p^n}` to itself
are called:

* affine equivalent if `F'=A_1\circ F\circ A_2`, where
  `A_1,A_2` are affine permutations;
* EA-equivalent (extended-affine) if `F'=F''+A`, where `A` is
  affine and `F''` is affine equivalent to `F`;
* CCZ-equivalent if there exists an affine permutation `\mathcal{L}` of
  `\mathbb{F}_{p^n}\times\mathbb{F}_{p^n}` such that
  `\mathcal{L}(G_F)=G_{F'}`, where
  `G_F=\lbrace (x,F(x)) : x\in\mathbb{F}_{p^n}\rbrace`.

CCZ-equivalence is the most general known equivalence relation for functions
which preserves differential uniformity. Affine and EA-equivalence are its
particular cases.

For the case of quadratic planar functions the isotopic equivalence is more
general than CCZ-equivalence, where two maps are isotopic equivalent if the
corresponding presemifields are isotopic.

On Presemifields and Semifields
-------------------------------

A presemifield is a ring with left and right distributivity and with no zero
divisor. A presemifield with a multiplicative identity is called a semifield.

Any finite presemifield can be represented by
`\mathbb{S}=(\mathbb{F}_{p^n},+,\star)`, for `p` a prime,
`n` a positive integer, `\mathbb{S}=(\mathbb{F}_{p^n},+)`
additive group and `x\star y` multiplication linear in each variable.
Every commutative presemifield can be transformed into a commutative
semifield :cite:p:`Coulter:200801`.

Two presemifields `\mathbb{S}_1=(\mathbb{F}_{p^n},+,\star)` and
`\mathbb{S}_2=(\mathbb{F}_{p^n},+,\circ)` are called isotopic if there
exist three linear permutations `T,M,N` of `\mathbb{F}_{p^n}` such
that `T(x\star y)=M(x)\circ N(y)` for any
`x,y\in\mathbb{F}_{p^n}`. If `M=N`, then they are called strongly
isotopic.

Each commutative presemifield of odd order defines a planar DO polynomial and
vice versa:

* given `\mathbb{S}=(\mathbb{F}_{p^n},+,\star)`, let
  `F_\mathbb{S}(x)=\frac{1}{2}(x\star x)`;
* given `F`, let
  `\mathbb{S}_F=(\mathbb{F}_{p^n},+,\star)` be defined by
  `x\star y=F(x+y)-F(x)-F(y)`.

Given `\mathbb{S}=(\mathbb{F}_{p^n},+,\star)` a finite semifield, the
subsets

* `N_l(\mathbb{S})=\{\alpha\in\mathbb{S} : (\alpha\star x)\star y=\alpha\star(x\star y) \text{ for all } x,y\in\mathbb{S}\}`;
* `N_m(\mathbb{S})=\{\alpha\in\mathbb{S} : (x\star\alpha)\star y=x\star(\alpha\star y) \text{ for all } x,y\in\mathbb{S}\}`;
* `N_r(\mathbb{S})=\{\alpha\in\mathbb{S} : (x\star y)\star \alpha=x\star(y\star \alpha) \text{ for all } x,y\in\mathbb{S}\}`;

are called left, middle and right nucleus of `\mathbb{S}`. The set
`N(\mathbb{S})=N_l(\mathbb{S})\cap N_m(\mathbb{S})\cap N_r(\mathbb{S})`
is called the nucleus.

All these sets are finite fields and, when `\mathbb{S}` is commutative,
`N_l(\mathbb{S})=N_r(\mathbb{S})\subseteq N_m(\mathbb{S})`. The order of
the different nuclei are invariant under isotopism.

Properties
----------

Hence two quadratic planar functions `F,F'` are isotopic equivalent if
their corresponding presemifields are isotopic. Moreover, we have:

* `F,F'` are CCZ-equivalent if and only if the corresponding
  presemifields are strongly isotopic :cite:p:`Budaghyan:201109`;
* for `n` odd, isotopic coincides with strongly isotopic;
* if `F,F'` are isotopic equivalent, then there exists a linear map
  `L` such that `F'` is EA-equivalent to
  `F(x+L(x))-F(x)-F(L(x))`;
* any commutative presemifield of odd order can generate at most two
  CCZ-equivalence classes of planar DO polynomials;
* if `\mathbb{S}_1` and `\mathbb{S}_2` are isotopic commutative
  semifields of characteristic `p` with order of middle nuclei and
  nuclei `p^m` and `p^k`, respectively, then either one of the
  following is satisfied:

  * `m/k` is odd and the semifields are strongly isotopic;
  * `m/k` is even and the semifields are strongly isotopic;
  * the only isotopisms are of the form `(\alpha\star N,N,L)` with
    `\alpha\in N_m(\mathbb{S}_1)` non-square.

Known cases of planar functions and commutative semifields
----------------------------------------------------------

Among the known examples of planar functions, the only ones that are
non-quadratic are the power functions `x^{\frac{3^t+1}{2}}` defined over
`\mathbb{F}_{3^n}`, with `t` odd and `\gcd(t,n)=1`.

The following is a list of some known infinite families of planar functions
and corresponding commutative semifields:

* `x^2` over `\mathbb{F}_{p^n}` (finite field
  `\mathbb{F}_{p^n}`);
* `x^{p^t+1}` over `\mathbb{F}_{p^n}` with
  `n/\gcd(t,n)` odd (Albert's commutative twisted fields);
* `L(t^2(x))+\frac{1}{2}x^2` over `\mathbb{F}_{p^{2km}}` with
  `L(x)=\frac{1}{8}(x^{p^k}-x), t(x)=x^{p^{km}}-x`
  (Dickson semifields);
* `(ax)^{p^s+1}-(ax)^{p^k(p^s+1)}+x^{p^k+1}` and
  `bx^{p^s+1}+(bx^{p^s+1})^{p^k}+cx^{p^k+1}` over
  `\mathbb{F}_{p^{2k}}`, where
  `a,b\in\mathbb{F}^\star_{2^{2k}}`, `b` is not square,
  `c\in\mathbb{F}_{2^{2k}}\setminus\mathbb{F}_{2^k}`,
  `\gcd(k+s,2k)=\gcd(k+s,k)`, and for the first one also
  `\gcd(p^s+1,p^k+1)\ne \gcd(p^s+1,(p^k+1)/2)`. Without loss of
  generality it is possible to take `a=1` and fix a value for
  `c`;
* `x^{p^{s}+1}-a^{p^{t}-1}x^{p^{t}+p^{2t+s}}` over
  `\mathbb{F}_{p^{3t}}`, `a` primitive,
  `\gcd(3,t)=1`, `t-s\equiv0 \pmod 3`, and
  `3t/\gcd(s,3t)` odd;
* `x^{p^s+1}-a^{p^t-1}x^{p^{3t}+p^{t+s}}` over
  `\mathbb{F}_{p^{4t}}`, `a` primitive,
  `p^s\equiv p^t\equiv1 \pmod 4`, and
  `2t/\gcd(s,2t)` odd;
* `a^{1-p}x^2+x^{2p^m}+a^{1-p}T(x)-T(x)^{p^m}`, with
  `T(x)=\sum_{i=0}^k(-1)^ix^{p^{2i}(p^2+1)}+a^{p-1}\sum_{j=0}^{k-1}(-1)^{k+j}x^{p^{2j+1}(p^2+1)}`,
  over `\mathbb{F}_{p^{2m}}` for
  `a\in\mathbb{F}^\star_{p^2}, m=2k+1`.

Cases defined for p = 3
-----------------------

* `x^{10}\pm x^6-x^2` over `\mathbb{F}_{p^n}` with `n` odd
  (Coulter-Matthews and Ding-Yuan semifields);
* `L(t^2(x))+D(t(x))+\frac{1}{2}x^2` over
  `\mathbb{F}_{3^{2k}}` with `k` odd,
  `t(x)=x^{3^k}-x`,
  `\beta\in\mathbb{F}_{3^{2k}}\setminus\mathbb{F}_{3^k}`,
  `\alpha=t(\beta)`, `L(x)=\alpha^{-5}x^3+x`, and
  `D(x)=-\alpha^{-10}x^{10}` (Ganley semifields);
* `L(t^2(x))+\frac{1}{2}x^2` over `\mathbb{F}_{3^{2k}}` with
  `k` odd, `t(x)=x^{3^k}-x`,
  `\beta\in\mathbb{F}_{3^{2k}}\setminus\mathbb{F}_{3^k}`,
  `\alpha=t(\beta)`, and
  `L(x)=-x^9-\alpha x^3+(1-\alpha^4)x` (Cohen-Ganley semifields);
* `L(t^2(x))+\frac{1}{2}x^2` over `\mathbb{F}_{3^{10}}` with
  `t(x)=x^{243}-x`,
  `\beta\in\mathbb{F}_{3^{10}}\setminus\mathbb{F}_{3^5}`,
  `\alpha=t(\beta)`, and
  `L(x)=-(\alpha^{-53}x^{27}+\alpha^{-18}x^9-x)`
  (Penttila-Williams semifields);
* `L(t^2(x))+D(t(x))+\frac{1}{2}x^2` over
  `\mathbb{F}_{3^{8}}` with `t(x)=x^9-x`,
  `L(x)=x^{243}+x^9`, and `D(x)=x^{246}+x^{82}-x^{10}`
  (Coulter-Henderson-Kosick semifield);
* `x^2+x^{90}` over `\mathbb{F}_{3^5}`.

Known cases of APN functions in odd characteristic
--------------------------------------------------

* `x^3` over `\mathbb{F}_{p^n}`, `p \neq 3`;
* `x^{p^n-2}` over `\mathbb{F}_{p^n}` with
  `p^n \equiv 2 \pmod 3`;
* `x^{\frac{p^n-3}{2}}` over `\mathbb{F}_{p^n}` with
  `p^n \equiv 3,7 \pmod {20}`, `p^n>7`, `p^n \neq 27`,
  and `n` odd;
* `x^{\frac{p^n+1}{4}+\frac{p^n-1}{2}}` over
  `\mathbb{F}_{p^n}` with `p^n \equiv 3 \pmod 8`;
* `x^{\frac{p^n+1}{4}}` over `\mathbb{F}_{p^n}` with
  `p^n \equiv 7 \pmod 8` and `n>1`;
* `x^{\frac{2p^n-1}{3}}` over `\mathbb{F}_{p^n}` with
  `p^n \equiv 2 \pmod 3`;
* `x^{p^m+2}` over `\mathbb{F}_{p^n}` with
  `p^m \equiv 1 \pmod 3` and `n=2m`;
* `x^{3^n-3}` over `\mathbb{F}_{3^n}` with `n>1` odd;
* `x^{\frac{3^\frac{n+1}{2}-1}{2}}` over `\mathbb{F}_{3^n}` with
  `n \equiv 3 \pmod 4` and `n>3`;
* `x^{\frac{3^\frac{n+1}{2}-1}{2}+\frac{3^n-1}{2}}` over
  `\mathbb{F}_{3^n}` with `n \equiv 1 \pmod 4` and `n>1`;
* `x^{\frac{3^{n+1}-1}{8}}` over `\mathbb{F}_{3^n}` with
  `n \equiv 3 \pmod 4`;
* `x^{\frac{3^{n+1}-1}{8}+\frac{3^{n}-1}{4}}` over
  `\mathbb{F}_{3^n}` with `n \equiv 1 \pmod 4`;
* `x^{\frac{3^{n+1}-1}{3^L+1}}` over
  `\mathbb {F} _{3^{n}}`, where
  `L={\frac{n+1}{2^{\ell}}}` with
  `n \equiv -1 \pmod {2^\ell}`;
* `x^{\frac{5^\ell+1}{2}}` over `\mathbb{F}_{5^n}` with
  `\gcd(2n, \ell)=1`;
* `x^{\frac{5^n-1}{4}+ \frac{5^{\frac{n+1}{2}}-1}{2}}` over
  `\mathbb{F}_{5^n}` with `n` odd;
* `x^{\frac{5^{n+1}-1}{2(5^L+1)}+ \frac{5^n-1}{4}}` over
  `\mathbb{F}_{5^n}`, where
  `L={\frac{n+1}{2^{\ell}}}`, `n \equiv -1 \pmod {2^\ell}`,
  and `\ell \geq 2`.

References
==========

.. references::
