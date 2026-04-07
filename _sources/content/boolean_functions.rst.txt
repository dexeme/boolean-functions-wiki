Boolean Functions
=================

Conteudo parcial extraido de ``data/Boolean_Functions.txt``.

Introduction
-------------------------------------------------------------------------------

Let `\mathbb{F}_{2}^{n}` be the vector space of dimension `n` over the finite field with two elements. The vector space can also
be endowed with the structure of the field, the finite field with `2^n` elements, `\mathbb{F}_{2^n}`.
A function `{\displaystyle f:\mathbb {F} _{2}^{n}\rightarrow \mathbb {F} }` is called a Boolean function in dimenstion `n` (or `n`-variable Boolean function ).
Given `{\displaystyle x=(x_{1},\ldots ,x_{n})\in \mathbb {F} _{2}^{n}}`, the support of `x` is the set
`{\displaystyle supp_{x}=\{i\in \{1,\ldots ,n\}:x_{i}=1\}}`. The Hamming weight of `x` is the size of its support
`({\displaystyle w_{H}(x)=|supp_{x}|})`. Similarly the Hamming weight of a Boolean function `f` is the size of its support, i.e. the set
`{\displaystyle \{x\in \mathbb {F} _{2}^{n}:f(x)\neq 0\}}`. The Hamming distance of two functions `f,g (𝖽_{𝐻} (f,g))` is the size of the set
`{\displaystyle \{x\in\mathbb{F}_2^n : f(x)\neq g(x) \}\ (w_{H}(f\oplus g))}`.

Representation of a Boolean function
-------------------------------------------------------------------------------
Algebraic Normal Form (ANF)
...............................................................................

Trace representation
...............................................................................

On the weight of a Boolean function
-------------------------------------------------------------------------------

The Walsh transform
-------------------------------------------------------------------------------

Properties of the Walsh transform
...............................................................................

Equivalences of Boolean functions
-------------------------------------------------------------------------------

Properties important for cryptographic applications
-------------------------------------------------------------------------------

Balanced functions
...............................................................................

The Nonlinearity
...............................................................................

Correlation-immunity order
...............................................................................
