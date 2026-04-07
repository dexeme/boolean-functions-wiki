Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;MGF;]
function MGF(f)
R:=Parent(f);
F:=BaseRing(R); n:=Degree(F);
a:=PrimitiveElement(F);

[0;MGF;]
function CF(f)
M:=Matrix( 2*n+1, 2^n, [1: u in F] cat [Trace(a^i * u): u in F, i in [1..n]] cat [Trace(a^i * f(u)): u in F, i in [1..n]]);
return LinearCode( M );
end function;
