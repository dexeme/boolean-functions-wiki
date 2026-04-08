APN Functions Obtained via Polynomial Expansion in Small Dimensions
===================================================================

Content partially extracted from ``data/APN_functions_obtained_via_polynomial_expansion_in_small_dimensions.txt``.
Original page: `https://boolean.wiki.uib.no/APN_functions_obtained_via_polynomial_expansion_in_small_dimensions <https://boolean.wiki.uib.no/APN_functions_obtained_via_polynomial_expansion_in_small_dimensions>`_

Overview
--------

This page lists APN functions obtained via polynomial expansion over `GF(2^n)` for `n=8,9`.
Functions are partitioned by orthoderivative differential spectra, and one representative is listed per class.

In all entries, `\alpha` is a primitive element of the corresponding field.

Labels in ``Equivalent to``:

- ``SW``: switching classes of Edel and Pott.
- ``B``: quadratic APN functions by Beierle and Leander.
- ``Y``: quadratic APN matrix method by Yuyin Yu.
- ``I``: generalized isotopic shifts by Budaghyan et al.

The source highlights that function ``8.7`` has an orthoderivative differential spectrum
distinct from previously known APN functions.

Selected Representatives (n=8)
------------------------------

- ``8.1``: `{\displaystyle \alpha^{170}x^{192}+\alpha^{85}x^{132}+x^6+x^3}` (equivalent to ``SW 19``)
- ``8.7``: `{\displaystyle \alpha^{170}x^{132}+\alpha^{85}x^{66}+\alpha^{85}x^{18}+x^3}` (``new``)
- ``8.16``: `{\displaystyle x^{160}+x^{132}+x^{80}+x^{68}+x^6+x^3}` (equivalent to ``SW 20``)

Selected Representatives (n=9)
------------------------------

- ``9.1``: `{\displaystyle \alpha^{365}x^{257}+x^{96}+x^{68}+\alpha^{219}x^{33}+x^5}` (equivalent to ``I 4``)
- ``9.8``: `{\displaystyle x^{192}+x^{66}+x^{17}+\alpha^{73}x^{10}+x^3}` (equivalent to ``I 14``)
- ``9.19``: `{\displaystyle \alpha^{73}x^{320}+x^{96}+\alpha^{219}x^{68}+x^{40}+x^{33}+x^5}` (equivalent to ``B 35``)

Further Data
------------

More details are available in the thesis
``Experimental construction of optimal cryptographic functions by expansion``
by Maren Hestad Aleksandersen.

The complete experimental datasets are referenced here https://universityofbergen-my.sharepoint.com/personal/nikolay_kaleyski_uib_no/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnikolay%5Fkaleyski%5Fuib%5Fno%2FDocuments%2Fpolynomial%2Dextension%2Ddata%2Ezip&parent=%2Fpersonal%2Fnikolay%5Fkaleyski%5Fuib%5Fno%2FDocuments&ga=1. The same data sorted by the differential spectrum of the orthoderivative is available here https://universityofbergen-my.sharepoint.com/personal/nadiia_ichanska_uib_no/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnadiia%5Fichanska%5Fuib%5Fno%2FDocuments%2FExpansion%20results&ga=1.

.. list-table::
   :widths: 5 40 15 40
   :header-rows: 1

   * - ID
     - Representative
     - Equivalent to
     - Orthoderivative diff. spec.
   * - 8.1
     - :math:`\alpha^{170}x^{192}+\alpha^{85}x^{132}+x^6+x^3`
     - SW 19
     - :math:`0^{37872},2^{22788},4^{4068},6^{492},8^{60}`
   * - 8.2
     - :math:`x^{66}+\alpha^{85}x^{33}+x^{18}+x^9+x^3`
     - SW 11
     - :math:`0^{38040},2^{22461},4^{4218},6^{513},8^{36},10^{12}`
   * - 8.3
     - :math:`x^{66}+\alpha^{85}x^{33}+\alpha^{17}x^9+\alpha^{102}x^6+x^3`
     - SW 13
     - :math:`0^{38076},2^{22311},4^{4374},6^{495},8^{24}`
   * - 8.4
     - :math:`\alpha^{85}x^{132}+\alpha^{85}x^{72}+x^9+x^6+x^3`
     - SW 12
     - :math:`0^{38160},2^{22104},4^{4536},6^{456},8^{24}`
   * - 8.5
     - :math:`x^{66}+x^{12}+\alpha^{85}x^6+x^3`
     - SW 6
     - :math:`0^{38160},2^{22164},4^{4428},6^{492},8^{36}`
   * - 8.6
     - :math:`x^{129}+\alpha^{85}x^{24}+x^{12}+x^9+x^3`
     - SW 8
     - :math:`0^{38184},2^{22179},4^{4338},6^{531},8^{48}`
   * - 8.7
     - :math:`\alpha^{170}x^{132}+\alpha^{85}x^{66}+\alpha^{85}x^{18}+x^3`
     - new
     - :math:`0^{38196},2^{22008},4^{4608},6^{456},8^{12}`
   * - 8.8
     - :math:`\alpha^{85}x^{132}+\alpha^{85}x^{72}+x^{36}+x^{24}+x^3`
     - SW 9
     - :math:`0^{38256},2^{22116},4^{4230},6^{648},8^{30}`
   * - 8.9
     - :math:`\alpha^{85}x^{192}+x^{72}+x^{33}+x^{24}+x^9+\alpha^{153}x^6`
     - SW 17
     - :math:`0^{38388},2^{21723},4^{4626},6^{507},8^{36}`
   * - 8.10
     - :math:`\alpha^{221}x^{96}+\alpha^{221}x^{33}+x^{12}+x^9+x^6+\alpha^{187}x^3`
     - SW 10
     - :math:`0^{38439},2^{21618},4^{4671},6^{528},8^{24}`
   * - 8.11
     - :math:`\alpha^{238}x^{144}+x^{132}+\alpha^{51}x^{96}+\alpha^{119}x^{48}+x^{33}+x^9`
     - SW 16
     - :math:`0^{38457},2^{21552},4^{4743},6^{510},8^{18}`
   * - 8.12
     - :math:`\alpha^{204}x^{160}+\alpha^{51}x^{48}+\alpha^{102}x^{12}+\alpha^{204}x^{10}+x^9`
     - SW 22
     - :math:`0^{38844},2^{20974},4^{4764},6^{654},8^{44}`
   * - 8.13
     - :math:`\alpha^{160}x^{132}+\alpha^{10}x^{72}+x^{48}+\alpha x^{34}+\alpha^3 x^{33}+\alpha^{48}x^{18}+x^{17}+x^3`
     - B 31
     - :math:`0^{39150},2^{20463},4^{4920},6^{675},8^{54},10^{12},12^6`
   * - 8.14
     - :math:`x^{144}+\alpha^{85}x^{96}+\alpha^{170}x^{80}+\alpha^{85}x^{65}+\alpha^{85}x^{17}+x^9+x^5`
     - B 12668
     - :math:`0^{39408},2^{20072},4^{4922},6^{798},8^{70},10^{10}`
   * - 8.15
     - :math:`x^{66}+\alpha^{170}x^{40}+x^{18}+\alpha^{85}x^5+x^3`
     - Y 4346
     - :math:`0^{39408},2^{20218},4^{4692},6^{838},8^{104},10^{12},12^8`
   * - 8.16
     - :math:`x^{160}+x^{132}+x^{80}+x^{68}+x^6+x^3`
     - SW 20
     - :math:`0^{39692},2^{19752},4^{4756},6^{978},8^{72},10^{26},12^4`


.. list-table::
   :widths: 5 40 10 45
   :header-rows: 1

   * - ID
     - Representative
     - Equivalent to
     - Orthoderivative diff. spec.
   * - 9.1
     - :math:`\alpha^{365}x^{257}+x^{96}+x^{68}+\alpha^{219}x^{33}+x^5`
     - I 4
     - :math:`0^{158529},2^{80829},4^{18144},6^{3283},8^{469},10^{294},12^{84}`
   * - 9.2
     - :math:`\alpha^{438}x^{129}+x^{66}+\alpha^{219}x^{10}+x^3`
     - I 8
     - :math:`0^{159418},2^{79275},4^{18690},6^{3213},8^{742},10^{252},12^{21},16^{21}`
   * - 9.3
     - :math:`x^{136}+x^{24}+x^{17}+\alpha^{73}x^{10}+x^3`
     - I 3
     - :math:`0^{159684},2^{78687},4^{19089},6^{3136},8^{777},10^{147},12^{84},14^{28}`
   * - 9.4
     - :math:`x^{68}+\alpha^{73}x^{40}+x^{33}+x^5`
     - I 10
     - :math:`0^{159684},2^{79590},4^{17871},6^{3283},8^{700},10^{273},12^{147},14^{84}`
   * - 9.5
     - :math:`\alpha^{73}x^{136}+\alpha^{146}x^{66}+\alpha^{219}x^{10}+x^3`
     - I 16
     - :math:`0^{159908},2^{79086},4^{18081},6^{3353},8^{721},10^{336},12^{105},14^{21},16^{21}`
   * - 9.6
     - :math:`x^{264}+\alpha^{73}x^{96}+\alpha^{219}x^{68}+x^5`
     - I 11
     - :math:`0^{160020},2^{79023},4^{17997},6^{3213},8^{868},10^{378},12^{133}`
   * - 9.7
     - :math:`\alpha^{219}x^{136}+x^{10}+x^3`
     - I 12
     - :math:`0^{160657},2^{77910},4^{18312},6^{3360},8^{952},10^{273},12^{147},14^{21}`
   * - 9.8
     - :math:`x^{192}+x^{66}+x^{17}+\alpha^{73}x^{10}+x^3`
     - I 14
     - :math:`0^{162183},2^{76482},4^{17388},6^{3871},8^{1162},10^{252},12^{126},14^{126},16^{21},22^{21}`
   * - 9.9
     - :math:`\alpha^{73}x^{192}+x^{136}+\alpha^{365}x^{129}+x^{17}+x^3`
     - I 5
     - :math:`0^{162708},2^{77175},4^{15498},6^{4270},8^{1260},10^{252},12^{168},14^{84},16^{126},18^{42},22^{42},26^7`
   * - 9.10
     - :math:`\alpha^{73}x^{129}+\alpha^{292}x^{66}+x^{10}+x^3`
     - I 9
     - :math:`0^{163009},2^{75537},4^{17283},6^{4116},8^{1071},10^{168},12^{231},14^{28},16^{84},18^{63},20^{42}`
   * - 9.11
     - :math:`x^{80}+\alpha^{146}x^{66}+\alpha^{73}x^{24}+x^{17}`
     - I 13
     - :math:`0^{163366},2^{75117},4^{17010},6^{4536},8^{966},10^{252},12^{63},14^{154},16^{63},18^{84},22^{21}`
   * - 9.12
     - :math:`x^{129}+\alpha^{73}x^{66}+x^{17}+x^{10}+\alpha^{365}x^3`
     - I 6
     - :math:`0^{163996},2^{74802},4^{16380},6^{4368},8^{1449},10^{231},12^{126},14^{84},16^{42},18^{84},20^{42},22^{21},32^7`
   * - 9.13
     - :math:`\alpha^{73}x^{136}+\alpha^{219}x^{66}+\alpha^{438}x^{10}+x^3`
     - I 15
     - :math:`0^{168994},2^{68712},4^{15141},6^{6279},8^{1659},10^{336},12^{21},14^{21},16^{105},18^{147},20^{189},24^{21},26^7`
   * - 9.14
     - :math:`\alpha^{438}x^{129}+x^{66}+\alpha^{219}x^{17}+x^3`
     - I 2
     - :math:`0^{169428},2^{68040},4^{15561},6^{6034},8^{1533},10^{420},12^{126},14^{21},16^{84},18^{189},20^{126},22^{63},26^7`
   * - 9.15
     - :math:`\alpha^{365}x^{80}+\alpha^{292}x^{24}+\alpha^{219}x^{17}+x^3`
     - I 17
     - :math:`0^{170079},2^{66297},4^{16737},6^{6160},8^{1407},10^{420},12^{21},14^{42},16^{63},18^{210},20^{133},22^{63}`
   * - 9.16
     - :math:`x^{257}+\alpha^{438}x^{68}+\alpha^{219}x^{12}+x^5`
     - I 7
     - :math:`0^{171430},2^{64617},4^{16842},6^{5733},8^{1932},10^{483},12^{105},14^{21},16^{147},18^{105},20^{154},22^{21},24^{42}`
   * - 9.17
     - :math:`x^{80}+\alpha^{73}x^{66}+x^{17}+\alpha^{73}x^{10}+x^3`
     - B 31
     - :math:`0^{160440},2^{78834},4^{17514},6^{3388},8^{777},10^{483},12^{126},14^{49},16^{21}`
   * - 9.18
     - :math:`\alpha^{365}x^{136}+x^{129}+\alpha^{73}x^{80}+x^{24}+x^{17}+x^3`
     - B 34
     - :math:`0^{164199},2^{76734},4^{13524},6^{4312},8^{2205},12^{147},16^{294},18^{147},20^{49},22^{21}`
   * - 9.19
     - :math:`\alpha^{73}x^{320}+x^{96}+\alpha^{219}x^{68}+x^{40}+x^{33}+x^5`
     - B 35
     - :math:`0^{172557},2^{68355},4^{12201},6^{3871},8^{1638},10^{735},12^{1470},14^{49},16^{147},18^{441},20^{147},42^{21}`
