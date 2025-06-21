% --- Léxico ---

% Determinantes
det(m, sg) --> [el].
det(f, sg) --> [la].
det(m, pl) --> [los].
det(f, pl) --> [las].
det(m, sg) --> [un].
det(f, sg) --> [una].

% Nombres
n(m, sg) --> [empleado].
n(f, sg) --> [empleada].
n(m, pl) --> [empleados].
n(f, pl) --> [empleadas].
n(m, sg) --> [sueldo].
n(m, pl) --> [sueldos].

vi(sg) --> [trabaja].
vi(pl) --> [trabajan].

vt(sg) --> [cobra].
vt(pl) --> [cobran].

% --- Sintagmas con árbol ---
sn(sn(DET, N), Num, Gen) --> det(Gen, Num), n(Gen, Num).
sv(sv(VI), Num) --> vi(Num), {VI = vi(_)}.
sv(sv(vt(VT), SN), Num) --> vt(Num), sn(SN, _, _), {VT = vt(_)}.
o(o(SN, SV)) --> sn(SN, Num, _), sv(SV, Num).

% --- Versión sin árbol, para phrase(o, [...]) ---
sn(_, Num, Gen) --> det(Gen, Num), n(Gen, Num).
sv(_, Num) --> vi(Num).
sv(_, Num) --> vt(Num), sn(_, _, _).
o --> sn(_, Num, _), sv(_, Num).




% ------- Pruebas de consulta esperadas -------
% Estas consultas sirven como guía para validar la gramática.

%?- phrase(o, [el, empleado, trabaja, un, sueldo]).
%false

%?- phrase(o, [el, empleado, trabaja, una, empeada]).
%false

%?- phrase(o, [el, empleada, trabaja]).
%false

%?- phrase(o, [la, empleada, trabaja]).
%true

%?- phrase(o, [los, empleada, sobran, sueldo]).
%false

%?- phrase(o, [los, empleados, cobram, sueldo]).
%false

%?- phrase(o, [los, empleados, cobran, los, sueldos]).
%true

%?- phrase(o(A), [los, empleados, cobran, los, sueldos]).
%A = o(sn(det(los), n(empleados)), sv(vt(cobran), sn(det(los), n (sueldos)))).

%?- phrase(o(A),[los, empleados, trabajan, los, sueldos]).
%false

