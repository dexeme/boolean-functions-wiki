Walsh
=====

.. code-block:: text
   :linenos:

   //The ANF of an n variables Boolean function is a polynomial with n variables and coefficients in GF(2)
   //The ANF of a vectorial Boolean (n,m)-function is a sequence of m ANFs of n variables Boolean functions
   //The univariate representation of an n variables Boolean function is an univariate polynomial with coefficients in GF(2^n) such that its image is in GF(2) 
   //The univariate representation of a vectorial Boolean (n,n)-function is an univariate polynomial with coefficients in GF(2^n)
   
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
   
   //Maps a to b such that a\cdot x=\Tr(bx)
   function getDualBasis(n)
       K:=GF(2^n);
       a:=K.1;
       R<x>:=PolynomialRing(K);
       f:=R!DefiningPolynomial(K);
       fa:=(Evaluate(Derivative(f),a) )^(-1);
       gc:=Coefficients(f div (x+a));
       B:=[];
       for i:=1 to n do
           if not IsDefined(gc,i) then
               B[i]:=Zero(K);
           else
               B[i]:=gc[i]*fa;
           end if;
       end for;  
       return B;
   end function;
   
   function getTraceConvertion(D,n)
       B:=getDualBasis(n);
       trD:=AssociativeArray();
       trD[0]:=D[0];
       for i:=1 to (2^n-1) do
           A:=Eltseq(D[i]);
           trD[i]:=&+[B[l]*A[l]: l in [1..n]];
       end for;
       return trD;
   end function;
   
   FourierHadamard:=procedure(~H,n : initialIndex:=0)
       for i:=1 to n do
           for r:=0 to (2^n -1) by 2^i do
               t1:=r;
               t2:=r+2^(i-1);
               for j:=0 to (2^(i-1) -1) do
                   a:=H[t1+initialIndex];
                   b:=H[t2+initialIndex];
                   H[t1+initialIndex]:=a+b;
                   H[t2+initialIndex]:=a-b;
                   t1 +:=1;
                   t2 +:=1;
               end for;
           end for;
       end for;
   end procedure;
   
   TruthTableToWalshMatrix:=function(TT,n)
       m:=#TT;
       WF:=ZeroMatrix(Integers(), 2^n, 2^m);
       r:=2^n;
       c:=2^m;
       for i:=1 to r do 
           WF[i][1]:=1;
       end for;
       for j:=2 to c do
           Sj:=Support(Vector(Intseq(j-1,2,m)));
           for i:=1 to r do 
               u:=Zero(GF(2));
               for k in Sj do
                   u +:=TT[k][i];
               end for;
               if IsZero(u) then
                   WF[i][j]:=1;
               else
                   WF[i][j]:=-1;
               end if;
           end for;
       end for;
       FourierHadamard(~WF,n : initialIndex:=1);
       return WF;  
   end function;
   
   //Walsh transform for Boolean functions
   bWalsh:=function(f: anf:=false)
       Wf:=AssociativeArray();
       if anf then
           n:=Rank(Parent(f));
       else  
           n:=Degree(BaseRing(Parent(f)));
       end if;
       q:=2^n;
       D:=getConvertionFunction(n: vector:=anf);
       for i:=0 to (q-1) do
           if IsZero(Evaluate(f,D[i])) then
               Wf[i]:=1;
           else
               Wf[i]:=-1;
           end if;
       end for;
       FourierHadamard(~Wf,n);
       Wf2:=AssociativeArray();
       if anf then
           for i:=0 to (q-1) do
               Wf2[D[i]]:=Wf[i];
           end for;
       else
           trD:=getTraceConvertion(D,n);
           for i:=0 to (q-1) do
               Wf2[trD[i]]:=Wf[i];
           end for;
       end if;
       return Wf2;
   end function;
   
   //Walsh transform for vectorial Boolean functions
   vWalsh:=function(F:  anf:=false)
       //vWalsh starts here
       if anf then
           m:=#F;
           n:=Rank(Parent(F[1]));
           D:=getConvertionFunction(n: vector:=true);
           if m eq n then
               cD:=D;
           else 
               cD:=getConvertionFunction(m : vector:=true);
           end if;
           TT:=[([Evaluate(F[j],D[i]): i in [0..(2^n-1)]]): j in [1..m]]; 
       else
           K:=BaseRing(Parent(F));
           a:=K.1;   
           m:=Degree(K);
           n:=m;
           D:=getConvertionFunction(n);
           TT:=[([Trace(a^j *Evaluate(F,D[i])): i in [0..(2^n-1)]]): j in [0..(n-1)]]; 
       end if;
       WFm:=TruthTableToWalshMatrix(TT,n);
       WF:=AssociativeArray();
       if anf then
           for i:=0 to (2^n-1) do
               Di:=D[i];
               WF[Di]:=AssociativeArray(); 
               for j:=0 to (2^m-1) do
                   WF[Di][cD[j]]:=WFm[i+1][j+1];
               end for;
           end for;
       else
           trD:=getTraceConvertion(D,n);
           for i:=0 to (2^n-1) do
               trDi:=trD[i];
               WF[trDi]:=AssociativeArray(); 
               for j:=0 to (2^m-1) do
                   WF[trDi][D[j]]:=WFm[i+1][j+1];
               end for;
           end for;
       end if;
       return WF;
   end function;
   
   TruthTableToBoolean:=function(TT)
       n:=Integers()!Log(2,#TT);
       R<[x]>:=PolynomialRing(GF(2),n);
       f:=Zero(R);
       f+:= TT[1];
       for i:=1 to (2^n-1) do
           ai:=Zero(GF(2));
           Si:=Support(Vector(IntToSequence(i,n)));
           for I in Subsets(Si) do
               if IsEmpty(I) then
                   ai +:=TT[1];
               else
                   k:=&+[2^(j-1): j in I]+1;
                   ai +:=TT[k];
               end if;
           end for;
           if IsOne(ai) then
               f+:=(&*[x[j]: j in Si]);
           end if;    
       end for; 
       return f;
   end function;
   
   
   InverseVectorialWalsh:=function(WF : anf:=false)
       n:=Integers()!Log(2,#Keys(WF));
       D:=getConvertionFunction(n :vector:=anf);
       WFc:=AssociativeArray();
       if anf then
           m:=Integers()!Log(2,#Keys(WF[Rep(Keys(WF))]));
           for j:=1 to m do
               vj:=[Zero(GF(2)): k in [1..m]];
               vj[j]:=One(GF(2));
               WFc[j]:=AssociativeArray();
               for i:=0 to (2^n-1) do
                   WFc[j][i]:=WF[D[i]][vj];
               end for;
               FourierHadamard(~WFc[j],n); 
           end for;
           return [TruthTableToBoolean([GF(2)!((1- (WFc[j][i] div 2^n) ) div 2): i in [0..(2^n-1)]]): j in [1..m]];
       else
           m:=n;
           K:=GF(2^n);
           a:=K.1;
           B:=getDualBasis(n);
           WFc:=AssociativeArray();
           trD:=getTraceConvertion(D,n);
           for j:=1 to n do
               vj:=a^(j-1);
               WFc[j]:=AssociativeArray();
               for i:=0 to (2^n-1) do
                   WFc[j][i]:=WF[trD[i]][vj];
               end for;
               FourierHadamard(~WFc[j],n);
           end for;
           return Interpolation([D[i]: i in [0..(2^n-1)]],[ &+[((1-(WFc[j][i] div 2^n)) div 2)*B[j] : j in [1..n]]: i in [0..(2^n-1)]]);  
       end if;  
   end function;
   
