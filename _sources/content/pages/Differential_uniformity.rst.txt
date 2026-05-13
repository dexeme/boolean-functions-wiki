Differential uniformity
=======================

Content extracted from ``data/Differential_uniformity.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Differential_uniformity <https://boolean.wiki.uib.no/Differential_uniformity>`

Given a vectorial Boolean function
:math:`F:\mathbb {F} _{2^{n}}\rightarrow \mathbb {F} _{2^{m}}`, it is called
differentially :math:`\delta`-uniform if the equation
:math:`F(x+a)-F(x)=b` admits at most :math:`\delta` solutions for every
non-zero :math:`a\in \mathbb {F} _{2^{n}}` and
:math:`b\in \mathbb {F} _{2^{m}}`.

This definition can be generalized to the case of functions
:math:`F:\mathbb{F}_{p^n}\rightarrow\mathbb{F}_{p^m}`.

Functions with the smallest value for :math:`\delta` contribute an optimal
resistance to the differential attack. The smallest possible value is
:math:`\delta=p^{n-m}`. Such functions are called perfect nonlinear (PN), and
they exist only for :math:`p` odd and :math:`m\le n/2`.

See also `planar functions <Commutative_Presemifields_and_Semifields.html>`_.

For :math:`p=2` and :math:`m=n`, the smallest value is :math:`\delta=2`, and
such optimal functions are called almost perfect nonlinear (APN).

Differential uniformity is invariant under affine, EA- and CCZ-equivalence.

References
==========

.. references::
