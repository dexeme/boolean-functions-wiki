.. _MGF:

MGF
===

Given a map in the univariate form, return its multiplier group

Returns the linear Code with columns (1,x,f(x))

CF is in utils.rst.

.. code-block:: text
   :linenos:

   function MGF(f)
       R:=Parent(f);
       F:=BaseRing(R); n:=Degree(F);
       a:=PrimitiveElement(F);
       f1:=func<x | Evaluate(f,x) >;
       MM:=AutomorphismGroup(CF(f1));
       return MM;
   end function;
