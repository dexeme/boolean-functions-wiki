DeltaRank
=========

.. code-block:: text
   :linenos:

   // given a vectorial Booleand function in univariate form, returns its delta rank
   function deltaRank(f) 
   R:=Parent(f);
   F:=BaseRing(R); n:=Degree(F);
   Gt<[E]>:=FreeAbelianGroup(2*n);
   G<[E]>:=AbelianGroup(quo<Gt|{2*e=0 : e in E}>);
   A1 := GroupAlgebra(  ComplexField(), G : Rep:="Vector"); A := GroupAlgebra( GF(2), G : Rep:="Vector");
   function rr1(v)
   return &+[E[i]*(Integers()!v[i]): i in [1..n]];
   end function;
   function rr2(v)
   return &+[E[i+n]*(Integers()!v[i]): i in [1..n]];
   end function;
   FF:=ANF(f);
   Gf:=[rr1(v)+rr2([Evaluate(FF[i],[v[j]:j in [1..n]]) : i in [1..n]]) : v in VectorSpace(GF(2),n)];
   
   Gf:=&+[A1!g : g in Gf];
   Df:= Gf*Gf - elt< A1 | 2^n, 0 >;
   Df:=2^(-1)*Df;
   
   DDf:=[];
   V:=VectorSpace(GF(2),2*n);
   for v in V do
   j:=(&+[Integers()!v[i]*E[i]:i in [1..2*n]]);
   if Coefficient(Df,j) eq 1 then Append(~DDf,G!(&+[Integers()!v[i]*E[i]:i in [1..2*n]])); end if;
   end for;
   DDf:=&+[A!g : g in DDf];
   J:=ideal<A|DDf>;
   
   DeltaRank:=Dimension(J);
   return DeltaRank; end function;
