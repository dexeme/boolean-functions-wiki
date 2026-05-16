Correlation immunity and resiliency of Boolean functions
========================================================

Content extracted from ``data/Correlation_immunity_and_resiliency_of_Boolean_functions.txt``.
Original page:

:link:`https://boolean.wiki.uib.no/Correlation_immunity_and_resiliency_of_Boolean_functions <https://boolean.wiki.uib.no/Correlation_immunity_and_resiliency_of_Boolean_functions>`

In the standard model of a stream cipher, the outputs of `n` linear
feedback shift registers are the entries of a Boolean function. The output of
the function produces the keystream, which is then bitwise xored with the
message to produce the cipher. The decryption consists symmetrically in xoring
this same keystream with the ciphertext.

There are a lot of divide-and-conquer attacks on this method of encryption,
see :cite:p:`Canteaut:200000`, :cite:p:`Johansson:199900`, :cite:p:`Goos:199900`,
:cite:p:`Siegenthaler:198501`. To resist these attacks the Boolean function must be
properly chosen: balanceness, large algebraic degree, high nonlinearity, and
high order correlation immunity.

The Boolean functions used in stream ciphers must be balanced for avoiding
statistical dependence between their input and their output. It must also have
large algebraic degree, because its degree conditions are the linear complexity
of the produced running-key. A third usual criterion is that the function
should be far from all affine functions regarding Hamming distance, since the
existence of a "good" approximation of `f` by an affine function makes
fast correlation attacks feasible, see :cite:p:`Carlet:200200`.

A fourth criterion on the combining function is that the distribution
probability of its output should be unaltered when any `m` of its inputs
are fixed, with `m` as large as possible. This property is called
`m`-th order correlation immunity.

Combining function, combiner model, combination generator
---------------------------------------------------------

A combination generator is a running-key generator for stream cipher
applications. It is composed of several linear feedback shift registers whose
outputs are combined by a Boolean function to produce the keystream.

The combining function `f(x_{1},x_{2},\dots ,x_{n})` is a Boolean
function that takes the outputs of `n` individual generators
`(x_{1},x_{2},\dots ,x_{n})` as inputs and produces a single output bit
at each step. The choice of `f` significantly affects the cryptographic
strength of the system, such as its resilience to correlation attacks, balance
properties, and algebraic complexity.

Any combination function `f(x)` used for generating the pseudorandom
sequence in the stream cipher must stay balanced if we keep constant some
coordinates of `f`.

In the 90's, high-order resilient functions with the best possible algebraic
degree and nonlinearity were needed for applications in stream ciphers using
the combiner model. But fast algebraic attacks (FAA) have changed the
situation. The combiner model is now considered as problematic, because of
Siegenthaler's bound and the fact that combiner or filter functions need to
have very high algebraic degree for resisting FAA.

Correlation immunity
--------------------

Definition
..........

The Boolean function `f` is called `m`-th order correlation immune
if the output distribution probability of `f` is unaltered when any
`m` of its input bits are kept constant.

Using Walsh transform below, the Boolean function `f` is `m`-th
order correlation immune if and only if `\widehat{f}(u)=0`, for all
`u \in \mathbb{F}_2^n` such that `1 \leq w_H(u) \leq m`, where
`w_H(u)` is the Hamming weight of `u`.

Importance of correlation-immune functions
..........................................

The notion of correlation-immune function is related to the notion of
orthogonal array. The notion of correlation immunity was introduced by
Siegenthaler :cite:p:`Siegenthaler:198409`.

If a combining function is not `m`-th order correlation-immune, then
there exists a correlation between the output of the function and `m`
coordinates of its input. Moreover, if `m` is small enough, a
divide-and-conquer attack, correlation attack for stream ciphers, and later
improved to fast correlation attack, uses this weakness for attacking the
system.

Resiliency
----------

Definition
..........

Balanced `m`-th order correlation-immune functions are called
`m`-resilient functions.

Using Walsh transform below, the Boolean function `f` is
`m`-resilient if and only if `\widehat{f}(u)=0`, for all
`u \in \mathbb{F}_2^n` such that `w_H(u) \leq m`. The maximum
value of `m` such that `f` is `m`-resilient is called the
resiliency order of `f`.

Dependance between resiliency, nonlinearity and algebraic degree
----------------------------------------------------------------

Siegenthaler proved that an `n` input 1 output, `m`-resilient
(balanced `m`-th order correlation immune) Boolean function with
algebraic degree `d` satisfies the inequality
`m + d \leq n - 1` :cite:p:`Carlet:202011`.

Any `m`-resilient function `f` on `\mathbb{F}^n_2` has
nonlinearity smaller than or equal to `2^{n-1} - 2^{m+1}` :cite:p:`Sarkar:200000`, also
independently obtained by :cite:p:`Tarannikov:200000`.

Walsh transform
---------------

Correlation immunity and resiliency can be characterized through the Walsh
transform of the Boolean function `f` :cite:p:`Xiao:198805`.

The discrete Fourier transform of `f` is by definition the function
`\widehat{f}` defined by

.. math::

   \widehat{f}(u)=\sum_{x \in F_2^n} f(x)(-1)^{u \cdot x}
   \text{ for all } u \in \mathbb{F}_2^n,

where `u \cdot x` is inner product
`u \cdot x = u_1x_1 \oplus \dots \oplus u_n x_n`.

The Walsh transform of `f` is the discrete Fourier transform of
`\chi_f = (-1)^f`, i.e. for all `u \in \mathbb{F}_2^n`,

.. math::

   \widehat{\chi_f}(u)=\sum_{x \in \mathbb{F}_2^n}(-1)^{f(x) \oplus x \cdot u}.

Example
-------

Let `r` be a positive integer smaller than `n`. Let `g` be
any Boolean function on `\mathbb{F}_2^{n-r}` and let `\phi` be a
mapping such that
`\phi : \mathbb{F}_2^{n-r} \mapsto \mathbb{F}_2^{r}`.

Define the function `f_{\phi , g}(x, y)` for
`x \in \mathbb{F}_2^r, \; y \in \mathbb{F}_2^{n-r}` such that

.. math::

   f_{\phi , g}(x, y)=x \cdot \phi(y) \oplus g(y)
   =\bigoplus_{i=1}^r x_i \phi_i(y) \oplus g(y),

where `\phi_i(y)` is the `i`-th coordinate of `\phi(y)`.
Then `f_{\phi , g}(x, y)` is `m`-resilient with `m \geq k`
if every element in `\phi(\mathbb{F}_2^{n-r})` has Hamming weight
strictly greater than `k` :cite:p:``.

References
==========

.. references::
