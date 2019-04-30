size(n).
row(0..n-1).
column(0..n-1).
color(black;white).

% A cada círculo se le asigna un color, blanco o negro.
1 {dot(X,Y,C): color(C)} 1 :- row(X), column(Y).

% No puede haber más de dos círculos blancos o negros consecutivos en una fila o una columna.
:- dot(X,Y,C), dot(X+1,Y,C), dot(X+2,Y,C).
:- dot(X,Y,C), dot(X,Y+1,C), dot(X,Y+2,C).

% No puede haber más círculos blancos que negros para una fila o una columna.
:- row(X), B=#count{Y: dot(X,Y,C), C==black}, W=#count{Y: dot(X,Y,C), C==white}, B!=W.
:- column(Y), B=#count{X: dot(X,Y,C), C==black}, W=#count{X: dot(X,Y,C), C==white}, B!=W.

% No puede haber dos filas o dos columnas con la misma combinación de círculos.
:- row(X1), row(X2), X1<X2, S=#count{Y: dot(X1,Y,C), dot(X2,Y,C)}, size(S).
:- column(Y1), column(Y2), Y1<Y2, S=#count{X: dot(X,Y1,C), dot(X,Y2,C)}, size(S).

#show dot/3.
