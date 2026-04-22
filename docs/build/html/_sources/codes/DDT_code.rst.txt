.. _DDT_code:

DDT
===

The ANF of an n variables Boolean function is a polynomial with n variables and coefficients in GF(2)
The ANF of a vectorial Boolean (n,m)-function is a sequence of m ANFs of n variables Boolean functions
The univariate representation of an n variables Boolean function is an univariate polynomial with coefficients in GF(2^n) such that its image is in GF(2)
The univariate representation of a vectorial Boolean (n,n)-function is an univariate polynomial with coefficients in GF(2^n)

IntToSequence, IntToElt, getConvertionFunction

.. code-block:: text
   :linenos:

   TruthTableToMatrixDDT:=function(TT,n,m)
       DDT:=ZeroMatrix(Integers(), 2^n, 2^m);
       r:=2^n;
       DDT[1][1]:=2^n;
       for i:=1 to (r-1) do 
           for x:=0 to (r-1) do
               DDT[i+1][BitwiseXor(TT[x+1],TT[BitwiseXor(x, i)+1 ])+1]+:=1;
           end for; 
       end for;
       return DDT;  
   end function;

   .. code-block:: text
   :linenos:

   DDT:=function(F:  anf:=false)
       if anf then
           m:=#F;
           n:=Rank(Parent(F[1]));
           D:=getConvertionFunction(n: vector:=true);
           if m eq n then
               cD:=D;
           else 
               cD:=getConvertionFunction(m : vector:=true);
           end if;
           P:=PowerSequence(Integers());
           TT:=[ Seqint(P!([Evaluate(F[j],D[i]): j in [1..m]]),2): i in [0..(2^n-1)] ]; 
       else
           K:=BaseRing(Parent(F));
           m:=Degree(K);
           n:=m;
           D:=getConvertionFunction(n);
           cD:=D;
           P:=PowerSequence(Integers());
           TT:=[ Seqint(P!Eltseq(Evaluate(F,D[i])),2): i in [0..(2^n-1)]]; 
       end if;
       mDDT:=TruthTableToMatrixDDT(TT,n,m);
       DDT:=AssociativeArray();
       for i:=0 to (2^n-1) do
           Di:=D[i];
           DDT[Di]:=AssociativeArray(); 
           for j:=0 to (2^m-1) do
               DDT[Di][cD[j]]:=mDDT[i+1][j+1];
           end for;
       end for;
       return DDT;
   end function;
   
