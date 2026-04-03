IsAPNdeg2
=========

.. code-block:: text
   :linenos:

   // given f a quadratic function defined over PolynomialRing(FiniteField(2,n)), it returns true if f is APN, false otherwise 
   IsAPNdeg2:= function(f) 
   R<x>:=Parent(f);
   F:=BaseRing(R);
   n:=Degree(F);
   E:=Basis(F);
   for a in F do 
   if a ne 0 then
              m:=Matrix(GF(Characteristic(F)),[Eltseq(Evaluate(f,x)-Evaluate(f,x+a)+Evaluate(f,a)):x in E]);
               if Rank(m) ne (n-1) then return false;
               end if; 
       end if;
    end for;
   return  true;
   end function;
