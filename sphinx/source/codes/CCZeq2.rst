CCZeq2
======

.. code-block:: text
   :linenos:

   // given two functions in univariate form, returns true if they are CCZ-equivalent and false otherwise
   function CCZeq2(F1,F2)
   R:=Parent(F1);
   F<a>:=BaseRing(R);
   n:=Degree(F);
   // returns the linear Code with columns (1,x,f(x))
   function CF(f)
   M:=Matrix( 2*n+1, 2^n, [1: u in F] cat [Trace(a^i * u): u in F, i in [1..n]] cat [Trace(a^i * f(u)): u in F, i in [1..n]]);
   return LinearCode( M );
   end function;
   f1:=func<x | Evaluate(F1,x) >;
   f2:=func<x | Evaluate(F2,x) >;
   return IsIsomorphic(CF(f1),CF(f2));
   end function;
