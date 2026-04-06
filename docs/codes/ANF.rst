ANF
===

Given a vectorial Boolean function in the univariate form, return its algebraic normal form

.. code-block:: text
   :linenos:

   function ANF(f)
   R<z>:=Parent(f);
   K<a>:=BaseRing(R);
   n:=Degree(K);
    V:=VectorSpace(GF(2),n);
   function invcorrisp(v)
     return K!(&+[v[i+1]*a^i : i in [0..n-1]]);
   end function;
   I:=Matrix(GF(2), 2^n, n, []);
   V1:=[i : i in V];
   K1:=[i : i in K];
   for k in [1..2^n] do
   z:=invcorrisp(V1[k]);
   for i in [1..2^n] do
   if Evaluate(f,z) eq invcorrisp(V1[i]) then
   I[k]:=V1[i];
   break; end if; end for; end for;
   B:=Matrix(GF(2), 2^n, 2^n, []);
   P<[x]>:=PolynomialRing(GF(2), n);
   M:=[ &*[x[i]^(Integers()!a[i]) : i in [1..n]] : a in V];
   // M = all possible monomials in n variables
   for i in [1..2^n] do
   for j in [1..2^n] do
   B[i, j]:=Evaluate(M[j], Eltseq(V1[i]));
   end for; end for;
   S:= Solution(Transpose(B) ,Transpose(I));
   pN:=[];
   for j in [1..n] do
   pn:=0;
   for i in [1..2^n] do
   pn:=M[i]*S[j][i]+pn;
   end for;
   pN:= Append (pN,pn);
   end for;
   return pN;
   end function;
