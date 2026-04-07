.. _CCZeq2:

CCZeq2
======

Given two functions in univariate form, returns true if they are CCZ-equivalent and false otherwise

Returns the linear Code with columns (1,x,f(x))

CF is in utils.rst.

.. code-block:: text
   :linenos:

   function CCZeq2(F1,F2)
       R:=Parent(F1);
       F<a>:=BaseRing(R);
       n:=Degree(F);
       f1:=func<x | Evaluate(F1,x) >;
       f2:=func<x | Evaluate(F2,x) >;
       return IsIsomorphic(CF(f1),CF(f2));
   end function;
