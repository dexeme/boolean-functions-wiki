Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;ANF;]
function ANF(f)
R<z>:=Parent(f);
K<a>:=BaseRing(R);
n:=Degree(K);
 V:=VectorSpace(GF(2),n);
function invcorrisp(v)
  return K!(&+[v[i+1]*a^i : i in [0..n-1]]);
end function;
