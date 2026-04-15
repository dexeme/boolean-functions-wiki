Known infinite families of quadratic APN polynomials over GF(2^n)
=================================================================

Content partially extracted from ``data/Known_infinite_families_of_quadratic_APN_polynomials_over_GF(2%5En).txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Known_infinite_families_of_quadratic_APN_polynomials_over_GF(2%5En)  <https://boolean.wiki.uib.no/Known_infinite_families_of_quadratic_APN_polynomials_over_GF(2%5En)>`

The mathematical expressions below are kept as literals (`...`) to avoid parsing failures from the original source.

.. list-table::
   :header-rows: 1

   * - `N^\circ`
     - Functions
     - Conditions
     - References
   * - C1-C2
     - `x^{2^{s}+1}+u^{2^{k}-1}x^{2^{ik}+2^{mk+s}}`
     - `n=pk,\gcd(k,3)=\gcd(s,3k)=1,p\in\{3,4\}; i=sk \bmod p,\ m=p-i,\ n\geq 12,\ u primitive in \mathbb{F}_{2^{n}}^*`
     - :zotero:`[1] <AZRATQP5>`
   * - C3
     - `sx^{q+1}+x^{2^{i}+1}+x^{q(2^{i}+1)}+cx^{2^{i}q+1}+c^{q}x^{2^{i}+q}`
     - `q=2^{m},\ n=2m,\ gcd(i,m)=1,\ c\in\mathbb{F}_{2^{n}},\ s\in\mathbb{F}_{2^{n}}\setminus\mathbb{F}_{q}; X^{2^{i}+1}+cX^{2^{i}}+c^{q}X+1 has no solution x with x^{q+1}=1`
     - :zotero:`[2] <RT6SSYTS>`
   * - C4
     - `x^{3}+a^{-1}\mathrm{Tr}_{n}(a^{3}x^{9})`
     - `a\neq 0`
     - :zotero:`[3] <WG23SAIY>`
   * - C5
     - `x^{3}+a^{-1}\mathrm{Tr}_{n}^{3}(a^{3}x^{9}+a^{6}x^{18})`
     - `3\mid n,\ a\neq 0`
     - :zotero:`[4] <FMFAN2SB>`
   * - C6
     - `x^{3}+a^{-1}\mathrm{Tr}_{n}^{3}(a^{6}x^{18}+a^{12}x^{36})`
     - `3\mid n,\ a\neq 0`
     - :zotero:`[5] <TUQMNMDA>`
   * - C7-C9
     - `ux^{2^s+1}+u^{2^k}x^{2^{-k}+2^{k+s}}+vx^{2^{-k}+1}+wu^{2^k+1}x^{2^{s}+2^{k+s}}`
     - `n=3k,\ \gcd(k,3)=\gcd(s,3k)=1,\ v,w\in\mathbb{F}_{2^k};\ vw\neq 1,\ 3\mid(k+s),\ u primitive in \mathbb{F}_{2^n}^*`
     - :zotero:`[6] <F85SBE8Q>`
   * - C10
     - `(x+x^{2^m})^{2^k+1}+u'(ux+u^{2^m}x^{2^m})^{(2^k+1)2^i}+u(x+x^{2^m})(ux+u^{2^m}x^{2^m})`
     - `n=2m,\ m\geq 2\ even,\ gcd(k,m)=1,\ i\geq 2\ even,\ u primitive in \mathbb{F}_{2^n}^*,\ u' \in \mathbb{F}_{2^m} not a cube`
     - :zotero:`[6] <F85SBE8Q>`
   * - C11
     - `L(x)^{2^i}x+L(x)x^{2^i}`
     - `n=km,\ m>1,\ gcd(n,i)=1,\ L(x)=\sum_{j=0}^{k-1}a_jx^{2^{jm}},\ and L satisfies the conditions in Theorem 6.3`
     - :zotero:`[7] <DNIN3C7W>`
   * - C12
     - `ut(x)(x^q+x)+t(x)^{2^{2i}+2^{3i}}+at(x)^{2^{2i}}(x^q+x)^{2^i}+b(x^q+x)^{2^i+1}`
     - `n=2m,\ q=2^m,\ gcd(m,i)=1,\ t(x)=u^qx+x^qu;\ X^{2^i+1}+aX+b has no solution over \mathbb{F}_{2^m}`
     - :zotero:`[8] <VDSS6RPJ>`
   * - C13
     - `x^3+a(x^{2^i+1})^{2^k}+bx^{3\cdot 2^m}+c(x^{2^{i+m}+2^m})^{2^k}`
     - `(1)\ n=2m=10,\ (a,b,c)=(\beta,0,0),\ i=3,\ k=2,\ \beta primitive in \mathbb{F}_{2^2}; (2)\ n=2m,\ m\ odd,\ 3\nmid m,\ (a,b,c)=(\beta,\beta^2,1),\ \beta primitive in \mathbb{F}_{2^2},\ i\in\{m-2,m,2m-1,(m-2)^{-1}\bmod n\}`
     - :zotero:`[9] <DSJCF8WD>`
