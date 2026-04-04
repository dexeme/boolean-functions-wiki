MGF
===

Given a map in the univariate form, return its multiplier group

.. code-block:: text
   :linenos:

   function MGF(f)
   R:=Parent(f);
   F:=BaseRing(R); n:=Degree(F);
   a:=PrimitiveElement(F);

Returns the linear Code with columns (1,x,f(x))

.. code-block:: text
   :linenos:

   function CF(f)
   M:=Matrix( 2*n+1, 2^n, [1: u in F] cat [Trace(a^i * u): u in F, i in [1..n]] cat [Trace(a^i * f(u)): u in F, i in [1..n]]);
   return LinearCode( M );
   end function;
   f1:=func<x | Evaluate(f,x) >;
   MM:=AutomorphismGroup(CF(f1));
   return MM;
   end function;
