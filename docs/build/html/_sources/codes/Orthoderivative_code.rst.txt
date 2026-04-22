.. _Orthoderivative_code:

Orthoderivative
===============

Orthoderivative of quadratic APN (n,n)-functions

IntToSequence, IntToElt, getConvertionFunction

.. code-block:: text
   :linenos:
   
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
