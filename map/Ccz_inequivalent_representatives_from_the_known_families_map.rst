Code Map
======

[DEPENDENCY_LEVEL;DECLARED_IN;USES]

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives6()
	n := 6;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);

	G6 := [
		x^3,
		x^6 + x^9 + p^7*x^48,
		p*x^3 + p^4*x^24 + x^17
	];

	return G6;
end function;

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives7()
	n := 7;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);

	G7 := [
		x^3,
		x^5,
		x^9,
		x^13,
		x^57,
		x^63,
		x^3 + Trace(x^9)
	];

	return G7;
end function;

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives8()
	n := 8;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);

	G8 := [
		x^3,
		x^9,
		x^57,
		x^3 + x^17 + p^48*x^18 + p^3*x^33 + p*x^34 + x^48,
		x^3 + Trace(x^9),
		x^3 + p^(-1)*Trace(p^3*x^9),
		(x + x^16)^3 + p^17*(p*x + p^16*x^16)^12 + p*(x + x^16)*(p*x + p^16*x^16)
	];

	return G8;
end function;

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives9()
	n := 9;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);
	Q := quo< P | ideal < P | x^(2^n) + x > >;
	Trace39 := x + x^8 + x^64;
	G9 := [
		x^3,
		x^5,
		x^17,
		x^13,
		x^241,
		x^19,
		x^255,
		x^3 + Trace(x^9),
		P ! ( Q ! (x^3 + Evaluate(Trace39, x^9 + x^18)) ),
		P ! ( Q ! (x^3 + Evaluate(Trace39,x^18 + x^36)) ),
		p^337*x^129 + p^424*x^66 + p^2*x^17 + p*x^10 + p^34*x^3
	];

	return G9;
end function;

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives10()
	n := 10;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);
	G10 := [
		x^3,
		x^9,
		x^57,
		x^339,
		x^6 + x^33 + p^31*x^192,
		x^72 + x^33 + p^31*x^258,
		x^3 + Trace(x^9),
		x^3 + p^(-1)*Trace(p^3*x^9),
		x^3 + p^341 * x^9 + p^682 * x^96 + x^288,
		x^3 + p^341 * x^129 + p^682 * x^96 + x^36
	];

	return G10;
end function;

[0;Ccz_inequivalent_representatives_from_the_known_families;]
function listAPNRepresentatives11()
	n := 11;
	FF<p> := GF(2^n);
	P<x> := PolynomialRing(FF);
	G11 := [
		x^3,
		x^5,
		x^9,
		x^17,
		x^33,
		x^13,
		x^57,
		x^241,
		x^993,
		x^35,
		x^287,
		x^1023,
		x^3 + Trace(x^9)
	];

	return G11;
end function;
