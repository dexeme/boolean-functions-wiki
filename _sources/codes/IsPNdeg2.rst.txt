.. _IsPNdeg2:

IsPNdeg2
========

Given f a quadratic function defined over PolynomialRing(FiniteField(p,n)), it returns true if f is PN, false otherwise

.. code-block:: text
   :linenos:

   IsPNdeg2:= function(f)
   R<x>:=Parent(f);
   F:=BaseRing(R);
   n:=Degree(F);
   E:=Basis(F);
   for a in F do 
   if a ne 0 then
              m:=Matrix(GF(Characteristic(F)),[Eltseq(Evaluate(f,x)-Evaluate(f,x+a)+Evaluate(f,a)):x in E]);
               if Rank(m) ne n then return false;
               end if; 
       end if;
    end for;
   return  true;
   end function;
