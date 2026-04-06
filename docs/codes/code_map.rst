Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USED_BY]

[0;Orthoderivative,Walsh,DDT;]
function IntToSequence(i,n)
    return PowerSequence(GF(2))!Intseq(i,2,n);
end function;

[0;Orthoderivative,Walsh,DDT;]
function IntToElt(i,n,K)
    return Seqelt(IntToSequence(i,n),K);
end function;

