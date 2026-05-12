.. _Utils_code:

Utils
=====

Aux funcs

.. code-block:: text
   :linenos:

   function IntToSequence(i,n)
       return PowerSequence(GF(2))!Intseq(i,2,n);
   end function;

   .. code-block:: text
   :linenos:

   function IntToElt(i,n,K)
       return Seqelt(IntToSequence(i,n),K);
   end function;

   .. code-block:: text
   :linenos:

   function getConvertionFunction(n :vector:=false)
       D:=AssociativeArray();
       if vector then
           for i:=0 to (2^n-1) do
               D[i]:=IntToSequence(i,n);
           end for;
       else
           K:=GF(2^n);
           for i:=0 to (2^n-1) do
               D[i]:=IntToElt(i,n,K);
           end for;
       end if;
       return D;
   end function;

   .. code-block:: text
   :linenos:

   function CF(f)
       M:=Matrix( 2*n+1, 2^n, [1: u in F] cat [Trace(a^i * u): u in F, i in [1..n]] cat [Trace(a^i * f(u)): u in F, i in [1..n]]);
       return LinearCode( M );
   end function;
