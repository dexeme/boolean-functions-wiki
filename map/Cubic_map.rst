Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;Cubic;]
function generateCubicPolynomial()
	n := 6;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);
	F1 := x^3 + p^17 * (x^17 + x^18 + x^20 + x^24);
	F2 := p^14 * (Trace( p^52 * x^3 + p^6 * x^5 + p^19 * x^7 + p^28 * x^11 + p^2 * x^13) + (p^2*x)^9 + (p^2*x)^18 + (p^2*x)^36 + x^21 + x^42);
	return (F1 + F2);
end function;
