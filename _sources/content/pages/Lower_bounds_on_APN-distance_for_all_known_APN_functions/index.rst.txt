.. _lower_bounds_on_apn_distance_for_all_known_apn_functions:

Lower bounds on APN-distance for all known APN functions
========================================================

Content extracted from ``data/Lower_bounds_on_APN-distance_for_all_known_APN_functions.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Lower_bounds_on_APN-distance_for_all_known_APN_functions <https://boolean.wiki.uib.no/Lower_bounds_on_APN-distance_for_all_known_APN_functions>`

Overview
--------

The following table lists a lower bound on the Hamming distance between a
representative from each known `CCZ`-equivalence class of APN functions up to
dimension `11`, and the closest APN function in terms of Hamming distance.

The lower bound `l(F)` between an `(n,n)`-function `F` and the closest APN
function is a CCZ-invariant, and is calculated via the formula

`l(F)=\lceil {\frac {m_{F}}{3}}\rceil +1`,

where

`m_{F}=\min _{b,\beta \in \mathbb {F} _{2^{n}}}|\{a\in \mathbb {F} _{2^{n}}:(\exists x\in \mathbb {F} _{2^{n}})(F(x)+F(a+x)+F(a+\beta )=b)\}|`.

The representatives for dimensions 7 and 8 are taken from the list of
:ref:`known instances APN polynomial functions over GF(2^7) <known_instances_of_apn_functions_over_gf_2_pow_7>`
and
:ref:`known instances APN polynomial functions over GF(2^8) <known_instances_of_apn_functions_over_gf_2_pow_8>`,
respectively, while the rest are taken from the table of
:ref:`CCZ-inequivalent APN functions from the known APN classes over GF(2^n) for n between 6 and 11 <ccz_inequivalent_apn_functions_from_the_known_apn_classes_over_gf_2_pow_n_for_n_between_6_and_11>`.

The table below shows the lower bounds computed for some of the known APN
functions for dimensions between 4 and 11. The functions in dimensions between
5 and 8 are indexed according to the table of
:ref:`known switching classes of APN functions over GF(2^n) for n = 5,6,7,8 <known_switching_classes_of_apn_functions_over_gf_2_pow_n_for_n_eq_5_6_7_8>`.
The ones between 9 and 11 are indexed according to the table of
:ref:`CCZ-inequivalent APN functions from the known APN classes over GF(2^n) for n between 6 and 11 <ccz_inequivalent_apn_functions_from_the_known_apn_classes_over_gf_2_pow_n_for_n_between_6_and_11>`.

A separate table listing these results for the known APN functions in
dimension 8 is available under
:ref:`Lower bounds on APN-distance for all known APN functions in dimension 8 <lower_bounds_on_apn_distance_for_all_known_apn_functions_in_dimension_8>`.

Note that all known APN functions in dimension 7 from the
:ref:`known instances APN polynomial functions over GF(2^7) <known_instances_of_apn_functions_over_gf_2_pow_7>`
have the same value of the lower bound as, for example, `x^{3}` over
`\mathbb {F} _{2^{7}}`.

.. csv-table::
    :file: Lower_bounds_on_APN-distance_for_all_known_APN_functions.csv
    :header-rows: 1
    :widths: 1 4 8 8
    :font-size: 1 1 1 1

:cite:p:`Budaghyan:202009`

References
==========

.. references::
