Is_APN
======

Given a function in its univariate form, return true if it is APN and false otherwise

.. code-block:: text
   :linenos:

   function IsAPN(f)
      P:=Parent(f);
      F<al>:=BaseRing(P);
      n:=Degree(F);
      for i in [0..2^n-2] do
         a:=al^i;
         set_b:={}; set_a:={};
            for y in F do if not y in set_a then
            b:=Evaluate(f,y+a)-Evaluate(f,y);
               if b notin set_b then Include(~set_b,b);
               else return false;
               end if;
      Include(~set_a,y+a);
      end if;
            end for;
         end for;
      return true;
   end function;
