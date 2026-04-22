Almost Perfect Nonlinear (APN) Functions
========================================

Content partially extracted from ``data/Almost_Perfect_Nonlinear_(APN)_Functions.txt``.
Original page:
:link:`https://boolean.wiki.uib.no/Almost_Perfect_Nonlinear_(APN)_Functions  <https://boolean.wiki.uib.no/Almost_Perfect_Nonlinear_(APN)_Functions>`

Background and Definition
-------------------------

APN functions are `(n,n)` vectorial Boolean functions with optimal resistance to differential attacks.

For `F:\mathbb{F}_{2^n}\to\mathbb{F}_{2^n}`, define
`{\displaystyle \Delta_F(a,b)=|\{x\in\mathbb{F}_{2^n}:F(x)+F(x+a)=b\}|}`.
The differential uniformity is
`{\displaystyle \Delta_F=\max\{\Delta_F(a,b):a\in\mathbb{F}_{2^n}^*,\ b\in\mathbb{F}_{2^n}\}}`.

Always `\Delta_F\ge 2`; functions achieving `\Delta_F=2` are APN.

Walsh Characterization :zotero:`[1] <DYHN6BVD>`
----------------------

For `(n,m)`-functions:
`{\displaystyle \sum_{a\in\mathbb{F}_{2^n},\ b\in\mathbb{F}_{2^m}^*}W_F^4(a,b)\ge
2^{2n}(3\cdot 2^{n+m}-2^{m+1}-2^{2n})}`,
with equality iff `F` is APN.

For `(n,n)`-functions this becomes:
`{\displaystyle \sum_{a\in\mathbb{F}_{2^n},\ b\in\mathbb{F}_{2^n}^*}W_F^4(a,b)\ge 2^{3n+1}(2^n-1)}`,
again with equality iff APN.

Equivalent formulations summing over all `b\in\mathbb{F}_{2^m}` are also used.

Autocorrelation/Derivative Characterization :zotero:`[2] <WGJ8Y98G>`
-------------------------------------------

For Boolean `f`, define:
`{\displaystyle \mathcal{F}(f)=\sum_{x\in\mathbb{F}_{2^n}}(-1)^{f(x)}=2^n-2wt(f)}`.

For `(n,n)`-functions:
`{\displaystyle \sum_{\lambda\in\mathbb{F}_{2^n}}\mathcal{F}(D_af_\lambda)=2^{2n+1}}`
for all `a\in\mathbb{F}_{2^n}^*`, with equality characterization of APN.

Using the sum-of-square-indicator
`{\displaystyle \nu(f)=\sum_{a\in\mathbb{F}_{2^n}}\mathcal{F}^2(D_af)}`,
one gets:
`{\displaystyle \sum_{\lambda\in\mathbb{F}_{2^n}^*}\nu(f_\lambda)\ge (2^n-1)2^{2n+1}}`,
with equality iff `F` is APN.

