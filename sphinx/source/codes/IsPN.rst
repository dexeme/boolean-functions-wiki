IsPN
====

.. code-block:: text
   :linenos:

   // given a function in the univariate form, returns true if PN and false otherwise
   function IsPN(poly)
   R<x>:=Parent(f);
   F<w>:=BaseRing(R);
   n:=Degree(F); p:=Characteristic(F);
       f:= func< x| Evaluate(poly, x)>;
       for i in {0..p^n-2} do
           a:=w^i;
           set_b := {};
           for y in FiniteField(p,n) do
               b:=f(y+a)-f(y);
               if b notin set_b then
                   Include(~set_b,b);
               else
                   return false;
               end if;
           end for;
       end for; 
       return true;
   end function;
