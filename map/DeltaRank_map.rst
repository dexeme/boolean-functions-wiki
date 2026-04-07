Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;DeltaRank;]
function deltaRank(f)
R:=Parent(f);
F:=BaseRing(R); n:=Degree(F);
Gt<[E]>:=FreeAbelianGroup(2*n);
G<[E]>:=AbelianGroup(quo<Gt|{2*e=0 : e in E}>);
A1 := GroupAlgebra(  ComplexField(), G : Rep:="Vector"); A := GroupAlgebra( GF(2), G : Rep:="Vector");

function rr1(v)
return &+[E[i]*(Integers()!v[i]): i in [1..n]];
end function;

[0;DeltaRank;]
function rr2(v)
return &+[E[i+n]*(Integers()!v[i]): i in [1..n]];
end function;
