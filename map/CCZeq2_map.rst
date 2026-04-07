Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;CCZeq2;]
function CCZeq2(F1,F2)
R:=Parent(F1);
F<a>:=BaseRing(R);
n:=Degree(F);

[0;CCZeq2;]
function CF(f)
M:=Matrix( 2*n+1, 2^n, [1: u in F] cat [Trace(a^i * u): u in F, i in [1..n]] cat [Trace(a^i * f(u)): u in F, i in [1..n]]);
return LinearCode( M );
end function;
