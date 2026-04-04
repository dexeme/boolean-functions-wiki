CCZeq
=====

Given two functions in univariate form, returns true if they are CCZ-equivalent and false otherwise

.. code-block:: text
   :linenos:

   function CCZeq(f1,f2)
   R:=Parent(f1);
   F:=BaseRing(R); 
   n:=Degree(F); p:=Characteristic(F);
   V,phi:=VectorSpace(GF(p^n),GF(p));
   M:=KMatrixSpace(GF(p),2*n+1,p^n);
   f:=function(x)
   return Evaluate(f1,x); end function;
   g:=function(x)
   return Evaluate(f2,x); end function;
   T:=M!0; i:=0;
   for x in GF(p^n) do
   i:=i+1;
   for j in [1..n] do
   T[j,i]:=phi(x)[j];
   T[j+n,i]:=phi(g(x))[j];
   end for;
   T[2*n+1,i]:=1;
   end for;
   C:=LinearCode(T);
   T:=M!0; i:=0;
   for x in GF(p^n) do
   i:=i+1;
   for j in [1..n] do
   T[j,i]:=phi(x)[j];
   T[j+n,i]:=phi(f(x))[j];
   end for;
   T[2*n+1,i]:=1;
   end for;
   D:=LinearCode(T);
   return IsEquivalent(C,D);
   end function;
