Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

.. https://dexeme.github.io/boolean-functions-wiki/codes/DDT.html

[0;Orthoderivative,Walsh,DDT;]
function IntToSequence(i,n)
    return PowerSequence(GF(2))!Intseq(i,2,n);
end function;

[0;Orthoderivative,Walsh,DDT;]
function IntToElt(i,n,K)
    return Seqelt(IntToSequence(i,n),K);
end function;

[1;Orthoderivative,Walsh,DDT;IntToSequence,IntToElt]
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

[0;DDT;]
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

[2;DDT;getConvertionFunction,TruthTableToMatrixDDT]
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

[2;DDT;getConvertionFunction,TruthTableToMatrixDDT]
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

