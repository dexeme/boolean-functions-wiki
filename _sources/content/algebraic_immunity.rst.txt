Algebraic Immunity
==================

Content partially extracted from `data/Algebraic_immunity_of_Boolean_functions.txt`.
Original page: `https://boolean.wiki.uib.no/Algebraic_immunity_of_Boolean_functions <https://boolean.wiki.uib.no/Algebraic_immunity_of_Boolean_functions>`_

Algebraic Immunity of Boolean Functions
=======================================

In 2003, the discovery of algebraic immunity and annihilators significantly impacted cryptanalysis by shaping how cryptographers approach the design of secure Boolean functions used in stream ciphers. These concepts have now become integral in defending against algebraic attacks. To achieve optimum resistance, cryptographers generally increased the number of variables in their constructions and chose functions with as high algebraic immunity as possible.

Among impacted designs was the filter generator, a technique used to break linearity in most LFSR-based stream ciphers by filtering the output of an LFSR through a highly non-linear Boolean function. The concept of algebraic immunity changed this paradigm, as functions with all previously required properties (nonlinearity, balancedness, resistance to fast algebraic attacks, and high algebraic immunity) were unknown until 2008, when an infinite class of such functions was discovered [CarKen08]_.

Algebraic Immunity and Annihilators
-----------------------------------

.. sagecell::

   R.<x> = GF(2)[]
   (x^3 + x + 1).factor()

The algebraic immunity of a function `AI(f)` measures its resistance to algebraic attacks. Specifically, it refers to the minimum algebraic degree of a non-zero Boolean function (called the annihilator of `f`) that annihilates `f` or its complement.

Formally, let `f: \mathbb{F}_2^n \rightarrow \mathbb{F}_2`

be a Boolean function. An annihilator of `f` or `f \oplus 1` is a non-zero Boolean function
`g: \mathbb{F}_2^n \rightarrow \mathbb{F}_2`

such that `fg = 0`.

The algebraic immunity of a Boolean function is defined as
`AI(f) = \min(d^\circ(g) \mid g \in An(f))`.

For all Boolean functions, the algebraic immunity is bounded by
`AI(f) \leq \min(d^\circ(f), \lceil\frac{n}{2}\rceil)`.

Example through Code
--------------------

Boolean functions are defined within SageMath by importing the module `sage.crypto.boolean_function`
module and its components which are not loaded by default. With Sagemath a Boolean function can be
created from its truth table or from a Boolean polynomial. The example below illustrates the latter.

.. sagecell::

    from sage.crypto.boolean_function import BooleanFunction

    B.<x0, x1, x2, x3> = BooleanPolynomialRing(4)
    f = x0*x1*x2*x3 + x0*x2*x3 + x1*x2*x3 + x0*x1 + x0*x3 + x1*x2 + x3 + 1
    F = BooleanFunction(f)

    F.algebraic_degree()

    pretty_print("B = ", B)
    pretty_print("F = ", F)

It is possible to compute an annihilator of `F`. Note that `d^\circ(f) = 4` but `AI(f) = 2 = \lceil\frac{n}{2}\rceil` and `f` has optimal algebraic immunity in this example.

.. sagecell::
    from sage.crypto.boolean_function import BooleanFunction

    B.<x0, x1, x2, x3> = BooleanPolynomialRing(4)
    f = x0*x1*x2*x3 + x0*x2*x3 + x1*x2*x3 + x0*x1 + x0*x3 + x1*x2 + x3 + 1
    F = BooleanFunction(f)

    AI, g = F.algebraic_immunity(annihilator=True)

    pretty_print("AI = ", AI)
    pretty_print("g = ", g)

Characterization of Annihilators by the Walsh Transform
-------------------------------------------------------

If `g` is an annihilator of `f`, then `f` and `g` must be orthogonal functions over `F_2^n`.

For Boolean functions: `f + g = f \oplus g + 2fg`.

Since `g \in An(f)`, this reduces to: `f + g = f \oplus g`.

This leads to:
`g \in An(f) \iff \forall a \neq 0, W_{f \oplus g}(a) = W_f(a) + W_g(a)`.

General form:
`g \in An(f) \iff \forall a \in \mathbb{F}_2^n, W_{f \oplus g}(a) + 2^n \delta_0(a) = W_f(a) + W_g(a)`.


Example through Code
--------------------

.. sagecell::

    from sage.crypto.boolean_function import BooleanFunction

    B.<x0, x1, x2, x3> = BooleanPolynomialRing(4)
    f = x0*x1*x2*x3 + x0*x2*x3 + x1*x2*x3 + x0*x1 + x0*x3 + x1*x2 + x3 + 1
    F = BooleanFunction(f)
    _, g = F.algebraic_immunity(annihilator=True)
    G = BooleanFunction(g)
    F_plus_G = BooleanFunction(f + g)

    wf = F.walsh_hadamard_transform()
    wg = G.walsh_hadamard_transform()
    wfg = F_plus_G.walsh_hadamard_transform()

    pretty_print("wf = ", wf)
    pretty_print("wg = ", wg)
    pretty_print("wfg = ", wfg)

Verification:

.. sagecell::

    from sage.crypto.boolean_function import BooleanFunction

    B.<x0, x1, x2, x3> = BooleanPolynomialRing(4)
    f = x0*x1*x2*x3 + x0*x2*x3 + x1*x2*x3 + x0*x1 + x0*x3 + x1*x2 + x3 + 1
    F = BooleanFunction(f)
    _, g = F.algebraic_immunity(annihilator=True)
    G = BooleanFunction(g)
    F_plus_G = BooleanFunction(f + g)

    wf = F.walsh_hadamard_transform()
    wg = G.walsh_hadamard_transform()
    wfg = F_plus_G.walsh_hadamard_transform()

    n = F.nvariables()
    for a in range(1, 2^n):
       assert wfg[a] == wf[a] + wg[a]


Perfect Algebraic Immune Functions
----------------------------------

A perfect algebraic immune function is a Boolean function
`f: \mathbb{F}_2^n \rightarrow \mathbb{F}_2`

such that for any integers `(e,d)` satisfying `e + d < n`

and `e < \frac{n}{2}`

there is no Boolean function `g` such that `d^\circ(g) \le e`

and `d^\circ(fg) \le d`.


Balanced perfect algebraic immune functions exist only if `n = 2^k + 1`.

Unbalanced perfect algebraic immune functions exist only if `n = 2^k`.


Consequences of Algebraic Attacks
--------------------------------

Let `f` be an `n`-variable Boolean function with algebraic immunity
`\lceil \frac{n}{2} \rceil`

used to filter an LFSR of length `N`.

For realistic parameters: `N = 256, \quad k = 128`.

The attack complexity is approximately: `2^{80}`.


Combining High Algebraic Immunity and Nonlinearity
--------------------------------------------------

The construction defines functions over: `\mathbb{F}_{2^n}`.

Support: `\{\alpha^s, \ldots, \alpha^{2^{n-1} + s - 1}\}`.

Nonlinearity lower bound:
`\mathcal{NL}_f \ge 2^{n-1} - n \ln(2) 2^{n/2} - 1`.


Applications to Cryptanalysis
-----------------------------

Algebraic attacks attempt to recover the key by solving multivariate equations.

Suppose: `f(x) = s_i`.

If: `fg = h`.

Then: `s_i = \begin{cases} 1 & g-h = 0 \\ 0 & h = 0 \end{cases}`.


Linearization
-------------

Number of variables: `D = \sum_{i=0}^{d^\circ(g)} \binom{n}{i}`.

Gaussian elimination complexity: `O(D^\omega)`,

where `\omega \approx 3` is the exponent of Gaussian elimination.
