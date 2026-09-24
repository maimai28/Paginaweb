"""Comprueba con cálculo exacto todas las respuestas numéricas de las guías.

Uso: python3 verificar.py      (requiere sympy)
Cada guía tiene su lista de pares (descripción, valor calculado, valor que aparece en la guía).
"""
from fractions import Fraction as F
import math
import sympy as sp

x, y, a, b = sp.symbols('x y a b')
GUIAS = {}

def guia(nombre):
    def registrar(fn):
        GUIAS[nombre] = fn
        return fn
    return registrar

def igual(calc, guia):
    if isinstance(calc, (tuple, list)) and isinstance(guia, (tuple, list)):
        return len(calc) == len(guia) and all(igual(c, g) for c, g in zip(calc, guia))
    if isinstance(calc, float) or isinstance(guia, float):
        return math.isclose(float(calc), float(guia), rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(calc, sp.Basic) or isinstance(guia, sp.Basic):
        return sp.simplify(sp.sympify(calc) - sp.sympify(guia)) == 0
    return calc == guia

# ---------------- Matemáticas ----------------

@guia('M01 Números enteros')
def _():
    return [
        ('ej1', -8 + 13, 5), ('ej2', -6 - 9, -15), ('ej3', 7 - (-4), 11), ('ej4', -15 + (-6), -21),
        ('ej5', -3 - (-3), 0), ('ej6', 12 - 20 + 5, -3), ('ej7', (-7) * 8, -56), ('ej8', (-9) * (-6), 54),
        ('ej9', F(-48, 6), -8), ('ej10', (-2) * (-3) * (-4), -24), ('ej11', F(-81, -9), 9),
        ('ej12', 5 - 3 * (-4), 17), ('ej13', (-2) ** 3 + 10, 2), ('ej14', F(-20, -4) - 7 * 2, -9),
        ('ej15', 3 * (-2 + 7) - (-1) ** 4, 14), ('ej16', 13 - (-4), 17), ('ej17', -18 + 7 - 12, -23),
        ('ej18', 350 - 4 * 95, -30), ('ej19', sorted([3, -7, 0, -2, 5, -10]), [-10, -7, -2, 0, 3, 5]),
        ('ejemplo1a', 6 - (-3), 9), ('ejemplo1b', -4 - 8, -12), ('truco', 12 - 20 + 5 - 9, -12),
        ('ejemplo2', (-2) * 3 * (-5), 30), ('ejemplo3', -3 + 4 * (-2) - F(-10, 5), -9),
        ('ejemplo4', 2 - 3 * (4 - 6) ** 2, -10), ('tabla', F(-36, -9), 4), ('tabla2', F(-36, 9), -4),
        ('suma', -7 + (-5), -12), ('suma2', -9 + 4, -5),
    ]

@guia('M03 Potencias y raíces')
def _():
    return [
        ('ej1', 3**4, 81), ('ej2', (-2)**5, -32), ('ej3', -3**2, -9), ('ej4', F(2, 3)**3, F(8, 27)),
        ('ej5', 5**0, 1), ('ej6', F(1, 10**3), F(1, 1000)), ('ej7', 2**3 * 2**5, 2**8), ('ej7b', 2**8, 256),
        ('ej8', F(7**9, 7**6), 343), ('ej9', (x**4)**3, x**12), ('ej10', sp.expand((3*a**2)**3), 27*a**6),
        ('ej11', x**5 * x**-2 / x, x**2), ('ej12', math.isqrt(196), 14), ('ej13', sp.real_root(-125, 3), -5),
        ('ej14', sp.sqrt(72), 6*sp.sqrt(2)), ('ej15', sp.sqrt(sp.Rational(4, 81)), sp.Rational(2, 9)),
        ('ej16', round(math.sqrt(50), 2), 7.07), ('ej17', math.isqrt(2025), 45), ('ej17b', 45**2, 2025),
        ('ej18', round(1.728 ** (1/3), 9), 1.2), ('ej19', 2**10, 1024), ('ej20', 149_600_000, 1.496e8),
        ('ejemplo1', F(2**3 * 2**4, 2**5), 4), ('ejemplo2', (a**3*b**2)**2 / (a**4*b), a**2*b**3),
        ('ejemplo3', sp.sqrt(48), 4*sp.sqrt(3)), ('ejemplo4a', round(7.1**2, 4), 50.41), ('ejemplo4b', round(7.07**2, 4), 49.9849),
        ('leyes', (3**2)**3, 729), ('leyes2', (2*5)**3, 1000), ('leyes3', F(1, 4**2), F(1, 16)), ('prepa', 8**F(2, 3), 4),
    ]

@guia('M02 Fracciones y decimales')
def _():
    return [
        ('mixto', F(7, 3), 2 + F(1, 3)), ('17/5', F(17, 5), 3 + F(2, 5)), ('simpl', F(18, 24), F(3, 4)), ('eq', F(6, 8), F(3, 4)),
        ('ejemplo1', F(2, 3) + F(3, 4), F(17, 12)), ('ejemplo1b', F(17, 12), 1 + F(5, 12)), ('ejemplo2', F(5, 6) - F(1, 4), F(7, 12)),
        ('ejemplo3a', F(2, 3) * F(9, 10), F(3, 5)), ('ejemplo3b', F(3, 4) / F(9, 8), F(2, 3)), ('nota', F(5, 2) * F(4, 3), 3 + F(1, 3)),
        ('nota-error', 2 * 1 + F(1, 2) * F(1, 3), 2 + F(1, 6)), ('mixto-mult', F(5, 2) * F(3, 4), F(15, 8)),
        ('dec', F(3, 8), F(375, 1000)), ('dec2', F(9, 20), F(45, 100)), ('dec3', F(5, 4), F(125, 100)),
        ('ejemplo4a', F(12, 10) * F(35, 100), F(42, 100)), ('ejemplo4b', F(45, 10) / F(15, 100), 30), ('comparar', F(3, 5) > F(58, 100), True),
        ('err1', F(1, 2) + F(1, 3), F(5, 6)), ('err2', F(2, 3) / F(4, 5), F(5, 6)), ('err3', F(3, 10) * F(2, 10), F(6, 100)), ('err4', F(3, 4), F(75, 100)), ('err5', F(5, 7), F(2 + 3, 2 + 5)),
        ('ej1', F(12, 18), F(2, 3)), ('ej2', F(45, 60), F(3, 4)), ('ej3', F(17, 5), 3 + F(2, 5)), ('ej4', F(3, 8) + F(1, 8), F(1, 2)),
        ('ej5', F(2, 5) + F(1, 3), F(11, 15)), ('ej6', F(7, 6) - F(3, 4), F(5, 12)), ('ej7', F(4, 9) * F(3, 8), F(1, 6)), ('ej8', F(5, 6) / F(10, 9), F(3, 4)),
        ('ej9', F(5, 2) + F(7, 4), F(17, 4)), ('ej10', F(7, 20), F(35, 100)), ('ej11', F(5, 11), F(45, 99)), ('ej12', F(625, 1000), F(5, 8)),
        ('ej13', F(12, 10) * F(35, 100), F(42, 100)), ('ej14', F(45, 10) / F(15, 100), 30),
        ('ej15', sorted([F(7, 10), F(2, 3), F(3, 4), F(65, 100)]), [F(65, 100), F(2, 3), F(7, 10), F(3, 4)]),
        ('ej16', F(3, 4) * F(5, 2), 1 + F(7, 8)), ('ej17', F(2, 5) * 1100, 440), ('ej17b', 1100 - 440, 660),
        ('ej18', F(36, 10) / F(45, 100), 8), ('ej19', F(385, 10) * F(2390, 100), F(92015, 100)),
    ]

@guia('M04 Proporcionalidad y porcentajes')
def _():
    return [
        ('razon', F(12, 18), F(2, 3)), ('ejemplo1', F(5 * 105, 3), 175), ('tabla', [F(p, k) for k, p in [(1, 35), (3, 105), (5, 175), (8, 280)]], [35] * 4),
        ('ejemplo2', F(4 * 15, 6), 10), ('taxi2', 30 + 10 * 2, 50), ('taxi4', 30 + 10 * 4, 70),
        ('pct', F(15, 100) * 240, 36), ('que%', F(18, 72) * 100, 25), ('base', F(30) / F(40, 100), 75),
        ('desc', 850 * F(80, 100), 680), ('aum', 500 * F(116, 100), 580), ('ejemplo3', F(600) / F(75, 100), 800), ('ejemplo3b', 800 - F(25, 100) * 800, 600),
        ('sucesivo', 100 * F(110, 100) * F(90, 100), 99),
        ('ej1', F(12 * 5, 8), F(15, 2)), ('ej2', F(3 * 21, 9), 7), ('ej3', F(86, 4) * 7, F(30100, 200)),
        ('ej4', {F(7, 2), F(35, 10) / 1, F(28, 8)}, {F(7, 2)}), ('ej4b', F(175, 10) / 5, F(7, 2)), ('ej5', F(6 * 10, 4), 15), ('ej6', F(80 * 3, 120), 2),
        ('ej7', F(15, 100) * 240, 36), ('ej8', F(18, 72) * 100, 25), ('ej9', F(30) / F(40, 100), 75), ('ej10', 850 * F(8, 10), 680),
        ('ej11', 500 * F(11, 10) * F(9, 10), 495), ('ej12', F(14, 40) * 100, 35), ('ej13', F(600) / F(3, 4), 800),
        ('ej14', 6 * 50000 / 100000, 3), ('ej15', F(300, 4) * 10, 750),
    ]

@guia('M05 Expresiones algebraicas')
def _():
    X = sp.Symbol('x')
    return [
        ('ejemplo1', 4*a**2 - 3*a + 2*a**2 + 7*a, 6*a**2 + 4*a), ('parent', 5 - (x + 4), 1 - x), ('ejemplo2', 4*(x - 2) - (3*x - 5), x - 3),
        ('mono', (3*x**2)*(4*x**3), 12*x**5), ('mono2', (-2*a*b)*(5*a**2), -10*a**3*b), ('dist', 2*x*(3*x - 5), 6*x**2 - 10*x),
        ('ejemplo3', sp.expand((x + 3)*(x - 2)), x**2 + x - 6), ('ejemplo4', (3*X**2 - 2*X + 1).subs(X, -2), 17),
        ('ejemplo5P', 2*(x + 4) + 2*x, 4*x + 8), ('ejemplo5A', sp.expand(x*(x + 4)), x**2 + 4*x),
        ('ejemplo5x3', ((4*X + 8).subs(X, 3), (X**2 + 4*X).subs(X, 3)), (20, 21)), ('ejemplo5real', (2*7 + 2*3, 7*3), (20, 21)),
        ('err', (-X**2).subs(X, -3), -9), ('err2', sp.expand((2*x)**2), 4*x**2),
        ('ej5', 7*x - 3*x + x, 5*x), ('ej6', 5*a - 2*b + 3*a + 6*b, 8*a + 4*b), ('ej7', 2*x**2 - 5*x + 3 - x**2 + 8*x - 1, x**2 + 3*x + 2),
        ('ej8', sp.expand(4*(x - 2) - (3*x - 5)), x - 3), ('ej9', 6 - (2*y - 9) + 4*y, 2*y + 15), ('ej10', (-2*a**3)*(5*a**2), -10*a**5),
        ('ej11', sp.expand(3*x*(2*x**2 - x + 4)), 6*x**3 - 3*x**2 + 12*x), ('ej12', sp.expand((x + 5)*(x - 3)), x**2 + 2*x - 15),
        ('ej13', sp.expand((2*x - 1)*(x + 4)), 2*x**2 + 7*x - 4), ('ej14', (2*X**2 - 3*X + 5).subs(X, -1), 10), ('ej15', 5**2 - (-3)**2, 16),
        ('ej16P', sp.expand(2*(2*x + 3) + 2*(x - 1)), 6*x + 4), ('ej16A', sp.expand((2*x + 3)*(x - 1)), 2*x**2 + x - 3),
        ('ej17', ((6*X + 4).subs(X, 4), (2*X**2 + X - 3).subs(X, 4)), (28, 33)), ('ej17real', (2*11 + 2*3, 11*3), (28, 33)),
    ]

def sol(ec):
    r = sp.solve(ec, x)
    return r[0] if len(r) == 1 else r

@guia('M06 Ecuaciones lineales')
def _():
    E = sp.Eq
    return [
        ('intro', sol(E(2*x + 3, 11)), 4), ('ejemplo1', sol(E(5*x - 7, 18)), 5), ('ejemplo2', sol(E(3*(x - 4) + 2, 5*x - 14)), 2),
        ('ejemplo2comp', (3*(2 - 4) + 2, 5*2 - 14), (-4, -4)), ('ejemplo3', sol(E(x/3 + x/4, 7)), 12), ('ejemplo4', sol(E((2*x - 1)/5, (x + 4)/3)), 23),
        ('ejemplo5', sol(E(x + x + 1 + x + 2, 72)), 23), ('ejemplo6', sol(E(150 + 2*x, 238)), 44),
        ('ej1', sol(E(x + 9, 4)), -5), ('ej2', sol(E(-6*x, 42)), -7), ('ej3', sol(E(4*x - 5, 23)), 7), ('ej4', sol(E(x/5, -3)), -15),
        ('ej5', sol(E(10 - 3*x, 1)), 3), ('ej6', sol(E(7, 2*x + 12)), sp.Rational(-5, 2)), ('ej7', sol(E(5*x + 3, 2*x + 18)), 5),
        ('ej8', sol(E(2*(x - 3), x + 4)), 10), ('ej9', sol(E(4*(2*x + 1) - 3, 5*x + 16)), 5), ('ej10', sp.solve(E(3*(x + 2), 3*x + 5), x), []),
        ('ej11', sol(E(x/2 + x/3, 10)), 12), ('ej12', sol(E((x + 1)/4, (x - 2)/3)), 11), ('ej13', sol(E(3*x/4 - 2, x/2)), 8),
        ('ej14', sol(E(2*x + 15, 49)), 17), ('ej15', sol(E(2*x + 2*(x + 5), 54)), 11), ('ej16', sol(E(3*x + 6, 2*(x + 6))), 6),
        ('ej16comp', (18 + 6, 2 * (6 + 6)), (24, 24)), ('ej17', 1 + sol(E(20 + 12*x, 80)), 6),
    ]

def sis(e1, e2):
    r = sp.solve([e1, e2], [x, y], dict=True)
    if not r:
        return 'ninguna'
    r = r[0]
    return 'infinitas' if len(r) < 2 else (r[x], r[y])

@guia('M07 Sistemas de ecuaciones')
def _():
    E = sp.Eq
    R = sp.Rational
    return [
        ('intro', sis(E(x + y, 10), E(x - y, 4)), (7, 3)), ('intro-no', (6 + 4 == 10, 6 - 4 == 4), (True, False)),
        ('ejemplo1', sis(E(y, 2*x - 1), E(3*x + 2*y, 12)), (2, 3)), ('ejemplo2', sis(E(2*x + 3*y, 12), E(4*x - 3*y, 6)), (3, 2)),
        ('ejemplo3', sis(E(3*x + 2*y, 18), E(5*x - 4*y, 8)), (4, 3)), ('igualacion', sis(E(y, 2*x + 1), E(y, -x + 7)), (2, 5)),
        ('ejemplo4', sis(E(x + 2*y, 4), E(2*x + 4*y, 5)), 'ninguna'),
        ('ejemplo5', sp.solve([E(sp.Symbol('a') + sp.Symbol('n'), 120), E(85*sp.Symbol('a') + 60*sp.Symbol('n'), 9050)], dict=True)[0], {sp.Symbol('a'): 74, sp.Symbol('n'): 46}),
        ('grafica', (30 + 7 * 15, 170 - 3 * 15), (135, 125)),
        ('ej1', sis(E(x + y, 12), E(x - y, 2)), (7, 5)), ('ej2', sis(E(y, 3*x), E(x + y, 20)), (5, 15)), ('ej3', sis(E(x, 2*y + 1), E(3*x - y, 13)), (5, 2)),
        ('ej4', sis(E(3*x + 2*y, 7), E(5*x - 2*y, 9)), (2, R(1, 2))), ('ej5', sis(E(2*x + 5*y, 1), E(3*x - 2*y, 11)), (3, -1)),
        ('ej6', sis(E(4*x - 3*y, -2), E(2*x + y, 9)), (R(5, 2), 4)), ('ej7', sis(E(2*x + y, 5), E(4*x + 2*y, 7)), 'ninguna'),
        ('ej8', sis(E(x - 2*y, 3), E(3*x - 6*y, 9)), 'infinitas'), ('ej9', sis(E(x + y, 45), E(x - y, 9)), (27, 18)),
        ('ej10', sis(E(x + y, 18), E(5*x + 10*y, 130)), (10, 8)), ('ej11', sis(E(2*x + 3*y, 190), E(x + 2*y, 110)), (50, 30)),
        ('ej12', sis(E(y, 3*x), E(2*x + 2*y, 40)), (5, 15)),
    ]

@guia('M08 Productos notables y factorización')
def _():
    ex = sp.expand
    fa = sp.factor
    return [
        ('t1', ex((x + 5)**2), x**2 + 10*x + 25), ('t2', ex((3*x - 2)**2), 9*x**2 - 12*x + 4), ('t3', ex((2*x + 7)*(2*x - 7)), 4*x**2 - 49),
        ('t4', ex((x + 4)*(x - 9)), x**2 - 5*x - 36), ('ejemplo2', ex(6*a**2*(2*a + 3)), 12*a**3 + 18*a**2),
        ('dc1', ex((x + 7)*(x - 7)), x**2 - 49), ('dc2', ex((5 + 2*y)*(5 - 2*y)), 25 - 4*y**2), ('tcp', ex((x - 5)**2), x**2 - 10*x + 25),
        ('ejemplo3a', ex((x + 3)*(x + 4)), x**2 + 7*x + 12), ('ejemplo3b', ex((x - 5)*(x + 3)), x**2 - 2*x - 15), ('ejemplo4', ex(2*(x + 3)*(x - 3)), 2*x**2 - 18),
        ('err', ex((x - 2)*(x - 3)), x**2 - 5*x + 6), ('err2', ex(4*x*(x + 2)), 4*x**2 + 8*x), ('suma-cuadrados', fa(x**2 + 9), x**2 + 9),
        ('ej1', ex((x + 6)**2), x**2 + 12*x + 36), ('ej2', ex((2*a - 5)**2), 4*a**2 - 20*a + 25), ('ej3', ex((x + 8)*(x - 8)), x**2 - 64),
        ('ej4', ex((x - 7)*(x + 2)), x**2 - 5*x - 14), ('ej5', ex((3*x + 1)*(3*x - 1)), 9*x**2 - 1),
        ('ej6', ex(5*x*(x - 3)), 5*x**2 - 15*x), ('ej7', ex(6*a**2*(2*a + 3)), 12*a**3 + 18*a**2), ('ej8', ex((x + 9)*(x - 9)), x**2 - 81),
        ('ej9', ex((4*y + 3)*(4*y - 3)), 16*y**2 - 9), ('ej10', ex((x + 7)**2), x**2 + 14*x + 49), ('ej11', ex((x + 3)*(x + 5)), x**2 + 8*x + 15),
        ('ej12', ex((x - 5)*(x + 4)), x**2 - x - 20), ('ej13', ex((x - 3)*(x - 8)), x**2 - 11*x + 24), ('ej14', ex(2*(x + 3)*(x - 3)), 2*x**2 - 18),
        ('ej15', ex(x*(x - 6)*(x + 2)), x**3 - 4*x**2 - 12*x), ('ej15f', fa(x**3 - 4*x**2 - 12*x), x*(x - 6)*(x + 2)),
        ('ej16', 51**2, 2601), ('ej17', 98 * 102, 9996), ('ej18', fa(x**2 + 10*x + 25), (x + 5)**2), ('ej18P', ex(4*(x + 5)), 4*x + 20),
    ]

def raices(expr):
    return sorted(sp.solve(sp.Eq(expr, 0), x), key=lambda r: sp.N(r))

@guia('M09 Ecuaciones cuadráticas')
def _():
    t = sp.Symbol('t')
    D = lambda A, B, C: B**2 - 4*A*C
    return [
        ('forma', raices(x**2 - 2*x - 15), [-3, 5]), ('inc1', raices(2*x**2 - 50), [-5, 5]), ('inc2', raices(3*x**2 - 12*x), [0, 4]),
        ('ejemplo1', raices(x**2 - 5*x + 6), [2, 3]), ('d1', D(1, -5, 6), 1), ('d2', D(1, -6, 9), 0), ('d3', D(1, 2, 5), -16),
        ('ejemplo2', raices(2*x**2 + 3*x - 2), [-2, sp.Rational(1, 2)]), ('ejemplo2D', D(2, 3, -2), 25),
        ('ejemplo3', raices(x**2 + 4*x - 1), [-2 - sp.sqrt(5), -2 + sp.sqrt(5)]), ('ejemplo3n', [round(float(r), 2) for r in raices(x**2 + 4*x - 1)], [-4.24, 0.24]),
        ('ejemplo4', raices(x*(x + 3) - 40), [-8, 5]), ('ejemplo5', sorted(sp.solve(20*t - 5*t**2, t)), [0, 4]),
        ('err', raices(x**2 - 3*x), [0, 3]),
        ('ej1', raices(x**2 - 49), [-7, 7]), ('ej2', raices(3*x**2 - 48), [-4, 4]), ('ej3', raices(x**2 - 6*x), [0, 6]), ('ej4', raices(5*x**2 + 20*x), [-4, 0]),
        ('ej5', sp.solve(x**2 + 16, x, domain=sp.S.Reals) if False else [r for r in sp.solve(x**2 + 16, x) if r.is_real], []),
        ('ej6', raices(x**2 + 5*x + 6), [-3, -2]), ('ej7', raices(x**2 - 3*x - 10), [-2, 5]), ('ej8', raices(x**2 - 8*x + 16), [4]),
        ('ej9', raices(x**2 - 2*x - 15), [-3, 5]), ('ej10', raices(2*x**2 - 7*x + 3), [sp.Rational(1, 2), 3]),
        ('ej11', raices(x**2 - 2*x - 2), [1 - sp.sqrt(3), 1 + sp.sqrt(3)]), ('ej11n', [round(float(r), 2) for r in raices(x**2 - 2*x - 2)], [-0.73, 2.73]),
        ('ej12', D(3, 2, 1), -8), ('ej13', (D(4, -12, 9), raices(4*x**2 - 12*x + 9)), (0, [sp.Rational(3, 2)])),
        ('ej14', raices(x**2 + 2*x - 48), [-8, 6]), ('ej15', raices(2*x**2 - 72), [-6, 6]), ('ej16', raices(x*(x + 1) - 132), [-12, 11]),
        ('ej17', sorted(sp.solve(20*t - 5*t**2 - 15, t)), [1, 3]),
    ]

@guia('M10 Ángulos y triángulos')
def _():
    import math as m
    ang = m.degrees(m.atan2(150, 160))  # inclinación de la transversal de la figura
    tri = lambda p, q, r: sorted([p, q, r])[0] + sorted([p, q, r])[1] > sorted([p, q, r])[2]
    return [
        ('compl', 90 - 35, 55), ('supl', 180 - 128, 52), ('ejemplo1', (180 / 4, 3 * 180 / 4), (45, 135)),
        ('figura-agudos-iguales', round(ang, 1), round(ang, 1)), ('figura-colaterales', round(ang + (180 - ang), 6), 180),
        ('ejemplo2', sol(sp.Eq(2*x + 10, 3*x - 20)), 30), ('ejemplo2b', 2 * 30 + 10, 70), ('ejemplo3', (180 - 40) / 2, 70),
        ('desig', tri(3, 4, 8), False), ('ejemplo4', 15 * 1.6 / 2, 12),
        ('ej1', 90 - 35, 55), ('ej2', 180 - 128, 52), ('ej3', sol(sp.Eq(x + x + 20, 90)), 35), ('ej4', (65, 65, 180 - 65), (65, 65, 115)),
        ('ej5', sol(sp.Eq(4*x - 15, 2*x + 25)), 20), ('ej5b', 4 * 20 - 15, 65), ('ej6', 180 - 48 - 67, 65), ('ej7', 180 - 2 * 52, 76),
        ('ej8', sol(sp.Eq(6*x, 180)), 30), ('ej9', 120 - 50, 70), ('ej10', (tri(5, 7, 10), tri(2, 3, 6)), (True, False)),
        ('ej12', 18 * 1.5 / 2.25, 12), ('ej13', (4 * 12 / 8, 6 * 12 / 8), (6, 9)),
    ]

@guia('M11 Teorema de Pitágoras')
def _():
    h = lambda p, q: sp.sqrt(p**2 + q**2)
    c = lambda hip, p: sp.sqrt(hip**2 - p**2)
    r2 = lambda v: round(float(v), 2)
    return [
        ('ternas', [p*p + q*q == r*r for p, q, r in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15)]], [True] * 6),
        ('ejemplo1', h(6, 8), 10), ('ejemplo1b', r2(h(3, 5)), 5.83), ('ejemplo2', c(13, 5), 12), ('ejemplo3', (81 + 144 == 225, 49 + 64), (True, 113)),
        ('ejemplo4', c(5, sp.Rational(14, 10)), sp.Rational(48, 10)), ('ejemplo5', h(6, 8), 10),
        ('ej1', h(9, 12), 15), ('ej2', h(8, 15), 17), ('ej3', (h(4, 7), r2(h(4, 7))), (sp.sqrt(65), 8.06)), ('ej4', c(25, 7), 24),
        ('ej5', (c(12, 6), r2(c(12, 6))), (6 * sp.sqrt(3), 10.39)), ('ej6', 10**2 + 24**2 == 26**2, True), ('ej7', 6**2 + 7**2 == 9**2, False),
        ('ej8', c(sp.Rational(13, 2), sp.Rational(5, 2)), 6), ('ej9', h(40, 30), 50), ('ej10', (h(10, 10), r2(h(10, 10))), (10 * sp.sqrt(2), 14.14)),
        ('ej11', h(4 - (-2), 9 - 1), 10), ('ej12', h(12, 5), 13), ('ej13', (c(10, 6), 12 * c(10, 6) / 2), (8, 48)),
    ]

@guia('M12 Perímetros y áreas')
def _():
    out = []
    for PI in (math.pi, 3.1416):  # el resultado redondeado debe coincidir con π real y con la aproximación de la guía
        r = lambda v: round(v, 2)
        out += [
            ('circ-ej3', (r(6 * PI), r(9 * PI)), (18.85, 28.27)), ('sombra', r(100 - 25 * PI), 21.46),
            ('ej7', (r(8 * PI), r(16 * PI)), (25.13, 50.27)), ('ej8', r(25 * PI), 78.54), ('ej9', r(14 * PI), 43.98), ('ej12', r(80 - 4 * PI), 67.43),
        ]
    return out + [
        ('conv', 3.5 * 100 * 100, 35000), ('ejemplo1', (10 + 6) * 4 / 2, 32), ('ejemplo2', (6 * 6, 36 * 5.2 / 2), (36, 93.6)),
        ('ejemplo5', (round(4 * 2.6 - 1.2 * 1, 6), round((4 * 2.6 - 1.2) / 8, 6)), (9.2, 1.15)),
        ('ej1', (2 * 12 + 2 * 7, 12 * 7), (38, 84)), ('ej2', 9 * 6 / 2, 27), ('ej3', 10 * 16 / 2, 80), ('ej4', (14 + 8) * 5 / 2, 55),
        ('ej5', (5 * 8, 40 * 5.5 / 2), (40, 110)), ('ej6', 4 * math.isqrt(64), 32), ('ej10', 9 * (30 - 2 * 9) / 2, 54), ('ej11', 20 * 15 - 25, 275),
        ('ej13', 3.5 * 10000, 35000),
    ]

@guia('M13 Volúmenes')
def _():
    out = []
    for PI in (math.pi, 3.1416):
        r = lambda v, n=2: round(v, n)
        out += [
            ('cono', r(PI * 9 * 4 / 3), 37.70), ('esfera', r(4 / 3 * PI * 6**3), 904.78), ('ejemplo2', r(PI * 2.5**2 * 10 / 3), 65.45),
            ('tinaco', r(PI * 0.55**2 * 1.2, 3), 1.140), ('ej3', r(90 * PI), 282.74), ('ej5', r(PI * 25 * 12 / 3), 314.16),
            ('ej6', r(4 / 3 * PI * 27), 113.10), ('ej8', r(PI * 3.3**2 * 12, 1), 410.5),
        ]
    return out + [
        ('esfera-exacta', sp.Rational(4, 3) * 6**3, 288), ('cono-exacto', sp.Rational(9 * 4, 3), 12), ('ejemplo1', (6 * 4 / 2) * 10, 120),
        ('piramide', 36 * 10 / 3, 120), ('m3', 100**3, 1_000_000), ('ej1', 5**3, 125), ('ej2', 8 * 5 * 3, 120), ('ej4', 4 * 6 * 9 / 3, 72),
        ('ej6-exacto', sp.Rational(4, 3) * 27, 36), ('ej7', 10 * 5 * 1.5 * 1000, 75000), ('ej8-exacto', round(3.3**2 * 12, 6), 130.68),
        ('ej9', round(27 ** (1 / 3), 9) * 10, 30), ('ej10', (2**2), 4),
    ]

@guia('M14 Medidas de tendencia central')
def _():
    import statistics as st
    def resumen(d):
        modas = st.multimode(d)
        return (F(sum(d), len(d)), F(st.median(d)).limit_denominator(), modas if len(modas) < len(set(d)) else 'sin moda', max(d) - min(d))
    expand = lambda tabla: [v for v, f in tabla for _ in range(f)]
    herm = expand([(0, 3), (1, 8), (2, 6), (3, 2), (4, 1)])
    goles = expand([(0, 4), (1, 6), (2, 5), (3, 3), (4, 2)])
    temps = [31, 33, 35, 34, 36, 38, 37]
    return [
        ('ejemplo-calif', resumen([7, 8, 6, 9, 8, 10, 7, 8]), (F(63, 8), 8, [8], 4)), ('ejemplo1', resumen([4, 9, 7, 4, 6])[:3], (6, 6, [4])),
        ('ejemplo2', (len(herm), sum(herm), F(sum(herm), len(herm)), st.median(herm), st.mode(herm)), (20, 30, F(3, 2), 1, 1)),
        ('ejemplo3', (sum([8000, 9000, 9500, 10000, 60000]), st.mean([8000, 9000, 9500, 10000, 60000]), st.median([8000, 9000, 9500, 10000, 60000])), (96500, 19300, 9500)),
        ('ejemplo4', 5 * 8.8 - 4 * 8.5, 10),
        ('ej1', resumen([12, 15, 11, 18, 15, 13]), (14, 14, [15], 7)),
        ('ej2', (round(sum(temps) / 7, 2), st.median(temps), resumen(temps)[2], max(temps) - min(temps)), (34.86, 35, 'sin moda', 7)),
        ('ej3', (sum(goles) / 20, st.median(goles), st.mode(goles)), (1.65, 1.5, 1)), ('ej4', 5 * 12 - (10 + 14 + 9 + 15), 12),
        ('ej5', (st.mean([5, 7, 8, 20]), st.median([5, 7, 8, 20])), (10, 7.5)), ('ej7', st.mode(['CH', 'M', 'M', 'G', 'M', 'CH', 'G', 'M']), 'M'),
    ]

@guia('M15 Gráficas')
def _():
    dep = [14, 10, 6, 4, 6]
    ven = [45, 30, 35, 40, 60, 90]
    tr = [12, 9, 6, 3]
    return [
        ('total', sum(dep), 40), ('pct', [F(f, 40) * 100 for f in dep], [35, 25, 15, 10, 15]), ('ang', [F(f, 40) * 360 for f in dep], [126, 90, 54, 36, 54]),
        ('ang-suma', sum(F(f, 40) * 360 for f in dep), 360), ('lineas', (max([12, 18, 26, 30, 27, 20]), 26 - 18, 30 - 12), (30, 8, 18)),
        ('lineas-mayor-subida', max(b - a for a, b in zip([12, 18, 26, 30, 27], [18, 26, 30, 27, 20])), 8),
        ('ej1', max(ven), 90), ('ej2', sum(ven), 300), ('ej3', (sum(ven) / 6, sum(v > 50 for v in ven)), (50, 2)), ('ej4', F(90, 300) * 100, 30),
        ('ej5', F(90, 300) * 360, 108), ('ej6', ([F(f, 30) * 100 for f in tr], [F(f, 30) * 360 for f in tr]), ([40, 30, 20, 10], [144, 108, 72, 36])),
        ('ej8', F(52 - 50, 50) * 100, 4), ('engañosa', (100 - 96) / (98 - 96), 2),
    ]

@guia('M16 Probabilidad básica')
def _():
    from itertools import product
    dado = range(1, 7)
    dos = list(product(dado, dado))
    mon3 = list(product('AS', repeat=3))
    P = lambda fav, tot: F(len(fav), len(tot)) if not isinstance(fav, int) else F(fav, tot)
    letras = list('DESIERTO')
    return [
        ('ejemplo1', (F(3, 10), F(5 + 3, 10), F(0, 10)), (F(3, 10), F(4, 5), 0)), ('compl', 1 - F(1, 6), F(5, 6)),
        ('ejemplo2', P([r for r in product('AS', repeat=2) if set(r) == {'A', 'S'}], list(product('AS', repeat=2))), F(1, 2)),
        ('suma7', P([d for d in dos if sum(d) == 7], dos), F(1, 6)), ('suma2', P([d for d in dos if sum(d) == 2], dos), F(1, 36)),
        ('tabla', [[i + j for j in dado] for i in dado][0], [2, 3, 4, 5, 6, 7]), ('prod', F(1, 2) * F(1, 2), F(1, 4)), ('fr', F(28, 50), 0.56),
        ('ej1', F(1, 6), F(1, 6)), ('ej2', P([d for d in dado if d % 3 == 0], list(dado)), F(1, 3)), ('ej3', 1 - F(1, 6), F(5, 6)),
        ('ej4', (F(6, 12), 1 - F(4, 12), F(4 + 2, 12)), (F(1, 2), F(2, 3), F(1, 2))), ('ej5', P([c for c in letras if c in 'AEIOU'], letras), F(1, 2)),
        ('ej6', (len(mon3), P([m for m in mon3 if m.count('A') == 2], mon3), P([m for m in mon3 if 'A' in m], mon3)), (8, F(3, 8), F(7, 8))),
        ('ej7', (P([d for d in dos if sum(d) == 10], dos), P([d for d in dos if d[0] == d[1]], dos)), (F(1, 12), F(1, 6))),
        ('ej8', F(1, 6) * F(1, 2), F(1, 12)), ('ej9', (round(13 / 60, 2), round(1 / 6, 2)), (0.22, 0.17)),
    ]

# ---------------- Física ----------------
G = 9.8

@guia('F01 Posición y desplazamiento')
def _():
    return [
        ('ejemplo1', ((10 - 2) + (10 - 6), 6 - 2), (12, 4)), ('ejemplo2', (3 + 4, math.hypot(3, 4)), (7, 5)), ('conv', (2.5 * 1000, 3400 / 1000), (2500, 3.4)),
        ('ej1', 5 - (-3), 8), ('ej2', 1 - 7, -6), ('ej3', (300 + 200, 100 - 0), (500, 100)), ('ej4', (400, 0), (400, 0)),
        ('ej5', (12 + 5, 12 - 5), (17, 7)), ('ej6', (6 + 8, math.hypot(6, 8)), (14, 10)),
    ]

@guia('F02 Velocidad y rapidez')
def _():
    return [
        ('conv', (72 / 3.6, 25 * 3.6), (20, 90)), ('ejemplo1', (round(240 / 3.5, 1), 120 / 1.5, 120 / 2), (68.6, 80, 60)),
        ('ejemplo2', (1.5e8 / 3e5, round(500 / 60, 1)), (500, 8.3)), ('ejemplo3', (360 / 120, 70 * 3, 50 * 3), (3, 210, 150)),
        ('grafica', 50 / 10, 5),
        ('ej1', 150 / 12, 12.5), ('ej2', 54 / 3.6, 15), ('ej3', 25 * 3.6, 90), ('ej4', 80 * 3.5, 280), ('ej5', 450 / 90, 5),
        ('ej6', 20 + 4 * 15, 80), ('ej7', 120 / 1.5, 80), ('ej8', (5400 / 9, 5400 / 9 / 60), (600, 10)), ('ej9', (50 - 10) / 8, 5), ('ej10', 10 + 5 * 20, 110),
    ]

@guia('F03 Aceleración')
def _():
    return [
        ('ejemplo1', (round(100 / 3.6, 1), round(27.8 / 10, 2)), (27.8, 2.78)), ('frena', (0 - 20) / 4, -5),
        ('ejemplo2', (3 * 6, 0.5 * 3 * 36), (18, 54)), ('ejemplo3', (20 / 5, (20 + 0) / 2 * 4, 40**2 / (2 * 5)), (4, 40, 160)),
        ('grafica', ((0 - 20) / 4, 4 * 20 / 2), (-5, 40)),
        ('ej1', (25 - 5) / 4, 5), ('ej2', (12 - 30) / 6, -3), ('ej3', (108 / 3.6) / 12, 2.5), ('ej4', (2 * 8, 0.5 * 2 * 64), (16, 64)),
        ('ej5', (10 + 1.5 * 6, 10 * 6 + 0.5 * 1.5 * 36), (19, 87)), ('ej6', (25 / 5, 25 / 2 * 5), (5, 62.5)), ('ej7', math.sqrt(2 * 4 * 50), 20),
        ('ej8', 20 / 5, 4), ('ej9', 5 * 20 / 2, 50),
    ]

@guia('F04 Caída libre')
def _():
    r = round
    return [
        ('ejemplo1', (r(math.sqrt(40 / G), 2), r(G * math.sqrt(40 / G), 1), r(math.sqrt(2 * G * 20), 1)), (2.02, 19.8, 19.8)),
        ('tabla', [(r(G * t, 1), r(G * t * t / 2, 1)) for t in (1, 2, 3)], [(9.8, 4.9), (19.6, 19.6), (29.4, 44.1)]),
        ('ejemplo2', (19.6 / G, r(19.6**2 / (2 * G), 2), 2 * 19.6 / G), (2, 19.6, 4)),
        ('ej1', (r(G * 3, 2), r(G * 9 / 2, 2)), (29.4, 44.1)), ('ej2', (r(math.sqrt(90 / G), 2), r(math.sqrt(2 * G * 45), 2)), (3.03, 29.70)),
        ('ej3', r(G * 4 / 2, 2), 19.6), ('ej4', (24.5 / G, r(24.5**2 / (2 * G), 1), 2 * 24.5 / G), (2.5, 30.6, 5)),
        ('ej5', r(math.sqrt(2 * G * 5), 2), 9.90),
    ]

@guia('F05 Leyes de Newton')
def _():
    return [
        ('neta', (30 + 45, 45 - 30), (75, 15)), ('ejemplo1', 1200 * 2, 2400), ('ejemplo2', ((80 - 30), (80 - 30) / 10), (50, 5)),
        ('ej1', (75, 15), (75, 15)), ('ej2', 20 / 4, 5), ('ej3', 60 * 1.5, 90), ('ej4', (120 - 80) / 40, 1), ('ej5', 300 / 2.5, 120),
        ('ej6', 1000 * (0 - 20) / 5, -4000),
    ]

@guia('F06 Masa y peso')
def _():
    g = {'Tierra': 9.8, 'Luna': 1.62, 'Marte': 3.71, 'Jupiter': 24.79}
    r = lambda v: round(v, 2)
    return [
        ('ejemplo1', (50 * G, 245 / G), (490, 25)), ('tabla', [r(50 * v) for v in g.values()], [490, 81, 185.5, 1239.5]),
        ('seis', round(9.8 / 1.62), 6), ('ejemplo2', (37.1 / 3.71, 10 * G), (10, 98)), ('err', 60 * G, 588),
        ('ej1', 70 * G, 686), ('ej2', 5 * G, 49), ('ej3', 245 / G, 25), ('ej4', r(80 * 1.62), 129.6), ('ej5', r(60 * 24.79), 1487.4),
        ('ej6', round(9.8 / 3.71, 1), 2.6), ('ej7', (r(16.2 / 1.62), 10 * G), (10, 98)),
    ]

@guia('F07 Presión')
def _():
    return [
        ('ejemplo1', (0.5 * 0.4, 600 / (0.5 * 0.4), 600 / 0.1), (0.2, 3000, 6000)), ('ejemplo2', 1000 * G * 10, 98000),
        ('ejemplo3', (200 * 0.5 / 0.01, 0.5 / 0.01), (10000, 50)),
        ('ej1', 50 / 0.02, 2500), ('ej2', (600 / 0.04, 600 / 0.0001, (600 / 0.0001) / (600 / 0.04)), (15000, 6_000_000, 400)),
        ('ej3', 200000 * 0.003, 600), ('ej4', 1000 * G * 5, 49000), ('ej5', 29400 / (1000 * G), 3), ('ej6', 12000 * 0.002 / 0.2, 120),
    ]

@guia('F08 Tipos de energía')
def _():
    return [
        ('ejemplo1', (0.5 * 1000 * 20**2, 0.5 * 1000 * 40**2), (200000, 800000)), ('ejemplo2', round(2 * G * 1.5, 6), 29.4),
        ('ejemplo3', (150 * 8, 150 * 8 / 20), (1200, 60)),
        ('ej1', 0.5 * 60 * 25, 750), ('ej2', 50 * G * 10, 4900), ('ej3', math.sqrt(2 * 25 / 0.5), 10), ('ej4', 196 / (4 * G), 5),
        ('ej5', 3**2, 9), ('ej7', 180 * 5, 900), ('ej8', (900 / 15, 900 / 10), (60, 90)),
    ]

@guia('F09 Conservación de la energía')
def _():
    r = round
    return [
        ('tabla', [(r(1 * G * h, 6), r(1 * G * (20 - h), 6)) for h in (20, 15, 10, 5, 0)], [(196, 0), (147, 49), (98, 98), (49, 147), (0, 196)]),
        ('ejemplo1', r(math.sqrt(392), 1), 19.8), ('ejemplo2', (r(math.sqrt(2 * G * 20), 1), r(math.sqrt(2 * G * 8), 1)), (19.8, 12.5)),
        ('ejemplo3', (20 * G * 5, 0.5 * 20 * 64, 20 * G * 5 - 0.5 * 20 * 64), (980, 640, 340)), ('eficiencia', 350 / 500 * 100, 70),
        ('ej1', (3 * G * 10, math.sqrt(2 * G * 10)), (294, 14)), ('ej2', 49 / (2 * G), 2.5), ('ej3', (r(math.sqrt(2 * G * 45), 1), r(math.sqrt(2 * G * 45) * 3.6)), (29.7, 107)),
        ('ej4', r(4 / (2 * G), 2), 0.20), ('ej5', (30 * G * 2.5, 0.5 * 30 * 25, 30 * G * 2.5 - 0.5 * 30 * 25), (735, 375, 360)), ('ej6', 1500 / 2000 * 100, 75),
    ]

@guia('F10 Calor y temperatura')
def _():
    F_ = lambda c: 1.8 * c + 32
    C_ = lambda f: (f - 32) / 1.8
    r = round
    return [
        ('escala', (F_(0), F_(100), 0 + 273, 100 + 273), (32, 212, 273, 373)), ('ejemplo1', (F_(40), 40 + 273, C_(23)), (104, 313, -5)),
        ('ejemplo2', 2 * 4186 * 60, 502320), ('arena', r(4186 / 830), 5),
        ('ej1', (25 + 273, F_(25)), (298, 77)), ('ej2', r(C_(98.6), 6), 37), ('ej3', 300 - 273, 27), ('ej4', 0.5 * 4186 * 75, 156975),
        ('ej5', 3 * 900 * 50, 135000), ('ej6', r(10000 / 4186, 2), 2.39),
    ]

@guia('F11 Carga eléctrica')
def _():
    k, e = 9e9, 1.6e-19
    return [
        ('coulomb-e', 1 / e, 6.25e18), ('ejemplo1', k * 1e-6 * 2e-6 / 0.3**2, 0.2),
        ('ej1', -2 * e, -3.2e-19), ('ej3', 1 / e, 6.25e18), ('ej5', k * 3e-6 * 4e-6 / 0.2**2, 2.7), ('ej6', 36 / 3**2, 4), ('ej7', 2 * 5, 10),
    ]

@guia('F12 Circuitos eléctricos')
def _():
    par = lambda a, b: 1 / (1 / a + 1 / b)
    return [
        ('ejemplo1', 127 / 254, 0.5), ('ejemplo2', (4 + 8, 12 / 12, 1 * 4, 1 * 8), (12, 1, 4, 8)),
        ('ejemplo3', (12 / 4, 12 / 8, 12 / 4 + 12 / 8, round(12 / 4.5, 2), round(par(4, 8), 2)), (3, 1.5, 4.5, 2.67, 2.67)),
        ('ejemplo4', (1.2 * 0.25 * 30, round(9 * 1.20, 2)), (9, 10.80)),
        ('ej1', 12 / 4, 3), ('ej2', 0.5 * 254, 127), ('ej3', 9 / 0.03, 300), ('ej4', (12 / 24, 0.5 * 6, 0.5 * 18), (0.5, 3, 9)),
        ('ej5', (12 / 6, 12 / 3, 12 / 6 + 12 / 3, par(6, 3)), (2, 4, 6, 2)), ('ej7', round(1000 / 127, 2), 7.87),
        ('ej8', (round(0.010 * 5 * 30, 6), round(1.5 * 1.20, 2)), (1.5, 1.80)),
    ]

@guia('F13 Magnetismo')
def _():
    # Figura: los picos de las líneas de campo (Bézier) deben coincidir con las flechas dibujadas.
    pico = lambda y0, yc: 0.25 * y0 + 0.75 * yc
    return [
        ('ej2', (3, 3 * 2), (3, 6)),
        ('figura-arriba', [pico(80, 45), pico(78, 15), pico(76, -12)], [53.75, 30.75, 10]),
        ('figura-abajo', [pico(90, 125), pico(92, 155), pico(94, 182)], [116.25, 139.25, 160]),
    ]

@guia('F14 Ondas')
def _():
    return [
        ('ejemplo1', (2 / 4, 1 / 0.5, 4 * 0.5), (0.5, 2, 2)), ('ejemplo2', 3e8 / 100e6, 3),
        ('figura', (60 - 20, 220 - 60), (160 / 4, 160)),
        ('ej1', 1 / 5, 0.2), ('ej2', 1 / 0.04, 25), ('ej3', 10 / 2, 5), ('ej4', 0.5 * 8, 4), ('ej5', 340 / 680, 0.5), ('ej6', 3e8 / 1e6, 300),
    ]

@guia('F15 El sonido')
def _():
    return [
        ('ejemplo1', 340 * 6, 2040), ('regla', 340 * 3, 1020), ('ejemplo2', 340 * 0.8 / 2, 136),
        ('ej1', 340 * 4, 1360), ('ej2', 340 * 1.5 / 2, 255), ('ej3', 1500 * 2 / 2, 1500), ('ej4', (1000 / 5000, round(1000 / 340, 2)), (0.2, 2.94)),
        ('ej5', round(340 / 440, 2), 0.77), ('ej6', [20 <= f <= 20000 for f in (10, 440, 15000, 40000)], [False, True, True, False]),
    ]

@guia('F16 La luz y los colores')
def _():
    c = 3e8
    return [
        ('año-luz (c exacta)', round(299792458 * 365.25 * 24 * 3600 / 1e15, 2), 9.46), ('ejemplo1', c / 1.5, 2e8),
        ('ej1', 3.84e8 / c, 1.28), ('ej2', round(c / 1.33 / 1e8, 2), 2.26), ('ej3', c / 2.5e8, 1.2), ('ej4', 35, 35),
    ]

@guia('F17 Modelo cinético')
def _():
    moleculas_vaso = 250 / 18.015 * 6.022e23
    return [
        ('vaso>estrellas(1e24, cota alta)', moleculas_vaso > 1e24, True),
        ('ejemplo1', 100 * 60 / 30, 200), ('ejemplo2', (27 + 273, 87 + 273, 2 * 360 / 300), (300, 360, 2.4)), ('ejemplo2-mal', round(2 * 87 / 27, 1), 6.4),
        ('ej4', 100 * 4 / 1, 400), ('ej5', 200 * 3 / 150, 4), ('ej6', 1.5 * 360 / 300, 1.8), ('ej7', (300 * 2 / 3, 300 * 2 / 3 - 273), (200, -73)),
    ]

@guia('F18 Estados de agregación')
def _():
    Lf, Lv = 334000, 2260000
    # Punto de ebullición en Juárez (≈1140 m): presión barométrica y ecuación de Antoine para el agua.
    P = 101.325 * (1 - 2.25577e-5 * 1140) ** 5.25588  # kPa
    Teb = 1730.63 / (8.07131 - math.log10(P * 7.50062)) - 233.426
    return [
        ('ejemplo1', (2 * Lf, 2 * Lv, round(Lv / Lf, 1)), (668000, 4520000, 6.8)), ('ebullicion-juarez', round(Teb), 96),
        ('ej2', 0.5 * Lf, 167000), ('ej3', 0.5 * Lv, 1130000), ('ej4', (4186 * 80, 4186 * 80 + Lv), (334880, 2594880)),
    ]

@guia('F19 Sistema Solar y universo')
def _():
    UA, c, al_km = 1.5e8, 3e8, 9.46e12
    UA_por_al = 9.4607e12 / 1.495978707e8  # con valores exactos
    return [
        ('ejemplo1', (5.2 * UA, 5.2 * UA * 1000 / c, round(5.2 * UA * 1000 / c / 60)), (7.8e8, 2600, 43)),
        ('escala-proxima', 4.24 * UA_por_al / 1000 > 260, True), ('luz-sol-tierra', round(1.495978707e11 / 299792458 / 60, 1), 8.3),
        ('ej4', 30.1 * UA, 4.515e9), ('ej5', (30.1 * UA * 1000 / c, round(30.1 * UA * 1000 / c / 3600, 1)), (15050, 4.2)),
        ('ej6', round(4.24 * al_km / 1e13, 2), 4.01),
        ('orden', sorted(['Saturno', 'Tierra', 'Neptuno', 'Mercurio', 'Júpiter', 'Marte', 'Urano', 'Venus'],
                         key=['Mercurio', 'Venus', 'Tierra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Neptuno'].index),
         ['Mercurio', 'Venus', 'Tierra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Neptuno']),
    ]

if __name__ == '__main__':
    fallas = 0
    for nombre, fn in GUIAS.items():
        malos = [(d, c, g) for d, c, g in fn() if not igual(c, g)]
        total = len(fn())
        if malos:
            fallas += len(malos)
            print(f'✗ {nombre}: {len(malos)} de {total} no coinciden')
            for d, c, g in malos:
                print(f'    {d}: calculado {c} · en la guía {g}')
        else:
            print(f'✓ {nombre}: {total} comprobaciones')
    raise SystemExit(1 if fallas else 0)
