Crooked Functions
=================

Content extracted from ``data/Crooked_Functions.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Crooked_Functions <https://boolean.wiki.uib.no/Crooked_Functions>`

An :math:`(n,n)`-function :math:`F` is called crooked if, for every nonzero
:math:`a`, the set
:math:`\{D_{a}F(x)\colon x\in \mathbb {F} _{2}^{n}\}` is an affine hyperplane
(i.e. a linear hyperplane or its complement).

Conversely, crooked functions are strongly plateaued and APN. The component
functions of a crooked function are all partially-bent. CCZ equivalence does
not preserve crookedness.

Characterization of Crooked Functions
-------------------------------------

For :math:`n` odd, :math:`F` is crooked if and only if :math:`F` is almost
bent (AB).

:math:`F` is crooked if and only if, for every nonzero :math:`a`, there exists
a unique nonzero :math:`v` such that

.. math::

   W_{D_{a}F}(0,v)\neq 0.

This characterization can be expressed by means of the Walsh transform of
:math:`F` since

.. math::

   W_{D_{a}F}(0,v)
   =\Delta _{v\cdot F}(a)
   =2^{-n}\sum _{u\in \mathbb {F} _{2}^{n}}
   (-1)^{u\cdot a}W_{F}^{2}(u,v).

Known Crooked Functions
-----------------------

* All quadratic APN functions are crooked.
* If a monomial is crooked, then it is quadratic.
* If a binomial is crooked, then it is quadratic.
* An open problem is to find a crooked function that is not quadratic.

References
==========

.. references::
