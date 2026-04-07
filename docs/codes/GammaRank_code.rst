.. _GammaRank_code:

GammaRank
=========

Given a vectorial Boolean function in univariate form, returns its gamma-rank

.. code-block:: text
   :linenos:

   function gammaRank(f)
           R:=Parent(f);
           Fn:=BaseRing(R);
           n:=2*Degree(Fn);
           M:=ZeroMatrix(GF(2),2^n,2^n);
           W:=VectorSpace(GF(2),n);
   
           Gf:={W!(Eltseq(v) cat Eltseq(Evaluate(f,v))): v in Fn};
           for w in W do
                   ww:=[Integers()!w[i]:i in [1..n]];
                   j:=SequenceToInteger(ww,2)+1;
                   GFtilde:={r+w:r in Gf};
                   for v in GFtilde do
                           vv:=[Integers()!v[i]:i in [1..n]];
                           i:=SequenceToInteger(vv,2)+1;
                           M[i][j]:=1;
                   end for;
           end for;
           return Rank(M);
   end function;
