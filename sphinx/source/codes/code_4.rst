**Codes Item 4**
================

Item 1
------

69: https://boolean.wiki.uib.no/Orthoderivative

.. code-block:: bash
   :linenos:
   :caption: example.py
   :emphasize-lines: 3,5

   //Orthoderivative of quadratic APN (n,n)-functions

   function IntToSequence(i,n)
       return PowerSequence(GF(2))!Intseq(i,2,n);
   end function;


   function IntToElt(i,n,K)
       return Seqelt(IntToSequence(i,n),K);
   end function;


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

   Orthoderivative:=function(F : anf:=false)
       if anf then
           n:=#F;
           D:=getConvertionFunction(n: vector:=true);
           TT:=[([Evaluate(F[j],D[i]): i in [0..(2^n-1)]]): j in [1..n]];
       else
           K:=BaseRing(Parent(F));
           n:=Degree(K);
           a:=K.1;
           D:=getConvertionFunction(n);
           TT:=[([Trace(a^j *Evaluate(F,D[i])): i in [0..(2^n-1)]]): j in [0..(n-1)]];
       end if;
       p:=AssociativeArray();
       p[D[0]]:=D[0];
       for k:=1 to (2^n-1) do
           J:=ZeroMatrix(GF(2),n,n);
           xk:=[BitwiseXor(k,2^i): i in [0..(n-1)]];
           for j:=1 to n do
               Tj:=TT[j];
               for i:=1 to n do
                   J[j][i]:=Tj[xk[i]+1 ]+Tj[k+1]+Tj[2^(i-1)+1]+Tj[1];
               end for;
           end for;
           v:=Rep(Generators(Kernel(J)));
           if anf then
               p[D[k]]:=Eltseq(v);
           else
               p[D[k]]:=D[Seqint([Integers()!v[i]: i in [1..n]],2)];
           end if;
       end for;
       return p;
   end function;
