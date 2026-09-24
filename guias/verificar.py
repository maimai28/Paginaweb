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
    if isinstance(calc, sp.Set) or isinstance(guia, sp.Set):
        return calc == guia
    if isinstance(calc, set) or isinstance(guia, set):
        return set(map(sp.nsimplify, calc)) == set(map(sp.nsimplify, guia))
    if isinstance(calc, sp.Basic) or isinstance(guia, sp.Basic):
        if sp.sympify(calc).is_infinite or sp.sympify(guia).is_infinite:
            return sp.sympify(calc) == sp.sympify(guia)
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

# ---------------- Preparatoria · Matemáticas ----------------

def dominio(expr_cond, var=x):
    if isinstance(expr_cond, sp.And):
        return sp.Intersection(*[dominio(c, var) for c in expr_cond.args])
    return sp.solve_univariate_inequality(expr_cond, var, relational=False)

@guia('PM01 Funciones y sus gráficas')
def _():
    f = lambda t: t**2 - 3*t + 2
    F_ = lambda t: 2*t + 1
    g = lambda t: t**2
    h = lambda t: (3*t - 2) / 5
    hinv = (5*x + 2) / 3
    return [
        ('ejemplo1a', (lambda t: t**2 - 4*t + 1)(-2), 13), ('ejemplo1b', sp.expand((lambda t: t**2 - 4*t + 1)(a + 3)), a**2 + 2*a - 2),
        ('ejemplo1c', sp.expand(a**2 - 4*a + 1 + 3), a**2 - 4*a + 4),
        ('ejemplo2', sp.calculus.util.continuous_domain(sp.sqrt(x + 2) / (x - 1), x, sp.S.Reals), sp.Union(sp.Interval.Ropen(-2, 1), sp.Interval.open(1, sp.oo))),
        ('ejemplo4', sp.expand((x + 2)**2), x**2 + 4*x + 4), ('ejemplo5', sp.simplify(4 * (x + 3) / 4 - 3), x),
        ('ej1', f(0), 2), ('ej2', f(-2), 12), ('ej3', f(3), 2), ('ej4', sp.expand(f(a + 1)), a**2 - a),
        ('ej5', sp.calculus.util.continuous_domain(sp.sqrt(x - 4), x, sp.S.Reals), sp.Interval(4, sp.oo)),
        ('ej6', sp.calculus.util.continuous_domain(1 / (x + 3), x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(-3)),
        ('ej7', sp.calculus.util.continuous_domain(sp.sqrt(6 - 2*x), x, sp.S.Reals), sp.Interval(-sp.oo, 3)),
        ('ej8', sp.calculus.util.continuous_domain((x + 1) / (x**2 - 9), x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(-3, 3)),
        ('ej10', max(4 - abs(t) for t in range(-50, 51)), 4),
        ('ej11', sp.calculus.util.function_range(sp.sqrt(x - 1) + 2, x, sp.Interval(1, sp.oo)), sp.Interval(2, sp.oo)),
        ('ej13', sp.expand(F_(g(x))), 2*x**2 + 1), ('ej14', sp.expand(g(F_(x))), 4*x**2 + 4*x + 1), ('ej15', F_(g(3)), 19),
        ('ej16', sp.simplify(F_((x - 1) / 2)), x), ('ej17', sp.simplify(h(hinv)), x),
    ]

@guia('PM02 Polinomios')
def _():
    P, Q = 2*x**2 - 3*x + 1, x**2 + 4*x - 5
    div = lambda n, d: tuple(sp.div(n, d, x))
    return [
        ('ejemplo1', div(x**3 + 2*x - 1, x**2 + 1), (x, x - 1)),
        ('ejemplo2', div(2*x**3 - 3*x**2 + 4*x - 5, x - 2), (2*x**2 + x + 6, 7)),
        ('residuo', (2*x**3 - 3*x**2 + 4*x - 5).subs(x, 2), 7),
        ('ejemplo3', sp.factor(x**3 - 2*x**2 - 5*x + 6), (x - 1)*(x - 3)*(x + 2)),
        ('atajo', sp.LT(sp.expand((2*x**3 - 1)*(5*x**2 + x))), 10*x**5),
        ('ej1', sp.expand(P + Q), 3*x**2 + x - 4), ('ej2', sp.expand(P - Q), x**2 - 7*x + 6),
        ('ej3', sp.expand(P * (x - 2)), 2*x**3 - 7*x**2 + 7*x - 2),
        ('ej4', (sp.degree(sp.expand((3*x**2 - 1)*(2*x**3 + x)), x), sp.LC(sp.expand((3*x**2 - 1)*(2*x**3 + x)))), (5, 6)),
        ('ej5', div(x**3 - 4*x**2 + x + 6, x - 3), (x**2 - x - 2, 0)),
        ('ej6', div(2*x**3 + 5*x**2 - x + 4, x + 2), (2*x**2 + x - 3, 10)),
        ('ej7', div(x**4 - 16, x - 2), (x**3 + 2*x**2 + 4*x + 8, 0)),
        ('ej8', (x**100 - 1).subs(x, -1), 0),
        ('ej9', sp.factor(x**3 - 7*x + 6), (x - 1)*(x - 2)*(x + 3)),
        ('ej10', set(sp.solve(2*x**3 - 3*x**2 - 3*x + 2, x)), {2, sp.Rational(1, 2), -1}),
        ('ej11', set(sp.solve(x**4 - 5*x**2 + 4, x)), {1, -1, 2, -2}),
        ('ej12', sp.solve((x**3 + a*x**2 - 4*x + 2).subs(x, 1), a), [1]),
        ('ej15', sp.expand((x + 1)*(x - 2)*(x - 4)), x**3 - 5*x**2 + 2*x + 8),
    ]

@guia('PM03 Desigualdades')
def _():
    I, oo = sp.Interval, sp.oo
    return [
        ('ejemplo1', dominio(3 - 2*x <= 11), I(-4, oo)),
        ('ejemplo2', dominio(sp.And(-1 < 2*x + 3, 2*x + 3 <= 9)), I.Lopen(-2, 3)),
        ('ejemplo3', dominio(x**2 - x - 6 > 0), sp.Union(I.open(-oo, -2), I.open(3, oo))),
        ('ejemplo4', dominio((x + 1) / (x - 2) <= 0), I.Ropen(-1, 2)),
        ('ejemplo5a', dominio(sp.Abs(x - 3) < 5), I.open(-2, 8)),
        ('ejemplo5b', dominio(sp.Abs(2*x + 1) >= 7), sp.Union(I(-oo, -4), I(3, oo))),
        ('ej1', dominio(5*x - 7 > 3), I.open(2, oo)), ('ej2', dominio(4 - 3*x >= 16), I(-oo, -4)),
        ('ej3', dominio(x / 2 + 1 < x / 3 + 2), I.open(-oo, 6)),
        ('ej4', dominio(sp.And(-3 <= 2*x - 1, 2*x - 1 < 5)), I.Ropen(-1, 3)),
        ('ej5', dominio(x**2 - 9 < 0), I.open(-3, 3)),
        ('ej6', dominio(x**2 + 2*x - 8 >= 0), sp.Union(I(-oo, -4), I(2, oo))),
        ('ej7', dominio(2*x**2 - 5*x - 3 <= 0), I(-sp.Rational(1, 2), 3)),
        ('ej8', dominio(x**2 + 4 > 0), sp.S.Reals),
        ('ej9', dominio((x - 4) / (x + 1) > 0), sp.Union(I.open(-oo, -1), I.open(4, oo))),
        ('ej10', dominio((2*x + 6) / (x - 5) <= 0), I.Ropen(-3, 5)),
        ('ej11', dominio(3 / (x - 2) > 1), I.open(2, 5)), ('ej11b', sp.simplify(3 / (x - 2) - 1 - (5 - x) / (x - 2)), 0),
        ('ej12', dominio(sp.Abs(x + 2) <= 6), I(-8, 4)),
        ('ej13', dominio(sp.Abs(3*x - 1) > 8), sp.Union(I.open(-oo, -sp.Rational(7, 3)), I.open(3, oo))),
        ('ej14', (max(g for g in range(200) if 150 + 2.5*g < 299), 150 + 2.5*59, 150 + 2.5*60), (59, 297.5, 300.0)),
        ('ej15', dominio(20*x - 5*x**2 > 15), I.open(1, 3)),
    ]

@guia('PM04 Exponentes y logaritmos')
def _():
    L = lambda v, b: sp.log(v, b)
    return [
        ('ejemplo1', (sp.Integer(27)**sp.Rational(2, 3), sp.Integer(16)**sp.Rational(-3, 4)), (9, sp.Rational(1, 8))),
        ('log-def', (L(32, 2), sp.log(sp.Rational(1, 1000), 10), sp.log(sp.E**4)), (5, -3, 4)),
        ('suma-no', (round(math.log10(10), 9), round(math.log10(16), 1)), (1.0, 1.2)),
        ('ejemplo3', (sp.solve(3**(x + 1) - 81, x), round(math.log(20) / math.log(5), 3)), ([3], 1.861)),
        ('ejemplo4', [s for s in sp.solve(x*(x - 2) - 8, x) if s > 2], [4]),
        ('ejemplo5', round(math.log(2) / math.log(1.08), 1), 9.0), ('ejemplo6', 2 * 5730, 11460),
        ('ej1', sp.Integer(8)**sp.Rational(2, 3), 4), ('ej2', sp.Integer(81)**sp.Rational(-1, 4), sp.Rational(1, 3)),
        ('ej3', sp.powsimp(x**sp.Rational(1, 2) * x**sp.Rational(3, 2) / x), x), ('ej4', sp.expand((2 / a * b**2)**3), 8*b**6 / a**3),
        ('ej5', L(81, 3), 4), ('ej6', L(sp.Rational(1, 25), 5), -2), ('ej7', sp.log(1000, 10) + sp.log(sp.Rational(1, 100), 10), 1),
        ('ej8', sp.simplify(L(40, 2) - L(5, 2)), 3),
        ('ej11', [s for s in sp.solve(2**(3*x - 1) - 32, x) if s.is_real], [2]), ('ej12', sp.solve(sp.Eq(2*x, 3*(x - 1)), x), [3]),
        ('ej13', round(math.log(50) / math.log(3), 2), 3.56), ('ej14', sp.solve(2*x + 1 - 9, x), [4]),
        ('ej15', [s for s in sp.solve(x*(x - 3) - 10, x) if s > 3], [5]), ('ej16', round(math.log(7) / 2, 3), 0.973),
        ('ej17', round(5000 * 1.06**10, 2), 8954.24), ('ej18', round(math.log(2) / math.log(1.06), 1), 11.9),
        ('ej19', F(1, 2)**(24 // 8), F(1, 8)), ('ej20', round(math.log(10) / 0.3, 1), 7.7),
    ]

def trig_sol(ecuacion):
    """Soluciones en [0, 2π) de una ecuación trigonométrica en x."""
    # Numérico e independiente de solveset (que a veces pierde soluciones): busca mínimos de |f| y los refina.
    e = (ecuacion.lhs - ecuacion.rhs) if isinstance(ecuacion, sp.Equality) else ecuacion
    f = sp.lambdify(x, e, 'math')
    N, raices = 7200, []
    def val(t):
        try: return abs(f(t))
        except (ValueError, ZeroDivisionError): return float('inf')
    for i in range(N):
        t0, t1, t2 = (2*math.pi*(i - 1)/N, 2*math.pi*i/N, 2*math.pi*(i + 1)/N)
        if val(t1) <= val(t0) and val(t1) < val(t2) and val(t1) < 1e-2:
            try: r = float(sp.nsolve(e, x, t1))
            except Exception: continue
            r = r % (2*math.pi)
            if abs(f(r)) < 1e-9 and all(abs(r - q) > 1e-6 for q in raices): raices.append(r)
    return [sp.nsimplify(r / math.pi, tolerance=1e-9, rational=True) * sp.pi for r in sorted(raices)]

@guia('PM05 Razones trigonométricas')
def _():
    r = math.radians
    S = lambda d: sp.sin(sp.pi * d / 180)
    C = lambda d: sp.cos(sp.pi * d / 180)
    T = lambda d: sp.tan(sp.pi * d / 180)
    return [
        ('ejemplo1', (math.hypot(5, 12), F(5, 13), F(12, 13), F(5, 12)), (13.0, F(5, 13), F(12, 13), F(5, 12))),
        ('sin35', round(math.sin(r(35)), 4), 0.5736), ('notables', (S(30), C(30), T(30), S(45), T(45), S(60), C(60), T(60)),
         (sp.Rational(1, 2), sp.sqrt(3)/2, sp.sqrt(3)/3, sp.sqrt(2)/2, 1, sp.sqrt(3)/2, sp.Rational(1, 2), sp.sqrt(3))),
        ('ejemplo2', (sp.Rational(150, 180) * sp.pi, sp.Rational(3, 4) * 180), (5*sp.pi/6, 135)),
        ('calc-rad', round(math.sin(30), 3), -0.988),
        ('ejemplo3', (round(10*math.sin(r(35)), 2), round(10*math.cos(r(35)), 2), round(5.74**2 + 8.19**2)), (5.74, 8.19, 100)),
        ('ejemplo4', round(math.degrees(math.atan(3/4)), 2), 36.87), ('ejemplo5', round(40*math.tan(r(52)), 1), 51.2),
        ('ej1-3', (math.hypot(8, 15), F(8, 17), F(15, 17), F(8, 15)), (17.0, F(8, 17), F(15, 17), F(8, 15))),
        ('ej4', (math.sqrt(1 - 0.36), 0.6 / 0.8), (0.8, 0.75)),
        ('ej5', S(30) + C(60), 1), ('ej6', T(45) * S(60), sp.sqrt(3)/2), ('ej7', 2*S(45)*C(45), 1), ('ej8', T(60)**2, 3),
        ('ej9', sp.Rational(45, 180)*sp.pi, sp.pi/4), ('ej10', sp.Rational(240, 180)*sp.pi, 4*sp.pi/3),
        ('ej11', sp.Rational(5, 3)*180, 300), ('ej12', round(math.degrees(2), 1), 114.6),
        ('ej13', (round(20*math.sin(r(40)), 2), round(20*math.cos(r(40)), 2)), (12.86, 15.32)),
        ('ej14', (round(math.sqrt(130), 2), round(math.degrees(math.atan(7/9)), 1)), (11.40, 37.9)),
        ('ej15', round(6*math.sin(r(70)), 2), 5.64), ('ej16', round(80/math.tan(r(25)), 1), 171.6),
        ('ej17', round(math.degrees(math.atan(4/6.5)), 1), 31.6),
    ]

@guia('PM06 Ley de senos y ley de cosenos')
def _():
    r, d = math.radians, math.degrees
    sen = lambda g: math.sin(r(g))
    ang = lambda a_, b_, c_: d(math.acos((a_*a_ + b_*b_ - c_*c_) / (2*a_*b_)))
    B1 = d(math.asin(10*sen(40)/8))
    h = 40*sen(30)/sen(20)
    return [
        ('ejemplo1', (round(10*sen(60)/sen(40), 2), round(10*sen(80)/sen(40), 2)), (13.47, 15.32)),
        ('ejemplo2', (round(10*sen(40)/8, 4), round(B1, 2), round(180 - B1, 2), round(180 - 40 - B1, 2), round(B1 - 40, 2)), (0.8035, 53.46, 126.54, 86.54, 13.46)),
        ('ejemplo3', 25 + 49 - 2*5*7*F(1, 2), 39), ('ejemplo3b', round(math.sqrt(39), 2), 6.24),
        ('ejemplo4', (F(49 + 64 - 81, 2*7*8), round(ang(7, 8, 9), 2)), (F(32, 112), 73.40)),
        ('ejemplo5', 0.5*6*9*0.5, 13.5), ('ejemplo6', (round(144 + 324 - 432*math.cos(r(50)), 1), round(math.sqrt(468 - 432*math.cos(r(50))), 2)), (190.3, 13.80)),
        ('ej1', round(12*sen(45)/sen(30), 2), 16.97), ('ej2', round(12*sen(105)/sen(30), 2), 23.18),
        ('ej3', (round(d(math.asin(7*sen(50)/9)), 2), 180 - d(math.asin(7*sen(50)/9)) + 50 > 180), (36.57, True)),
        ('ej4', 8*F(1, 2)/3 > 1, True), ('ej5', 36 + 100 - 120*sp.cos(sp.pi*2/3), 196),
        ('ej6', round(ang(5, 6, 7), 2), 78.46), ('ej7', round(ang(4, 7, 10), 2), 128.68),
        ('ej8', round(0.5*8*11*sen(40), 2), 28.28), ('ej9', sp.Rational(1, 2)*36*sp.sin(sp.pi/3), 9*sp.sqrt(3)),
        ('ej10', math.sqrt(21*8*7*6), 84.0),
        ('ej11', round(math.sqrt(120**2 + 150**2 - 2*120*150*math.cos(r(65))), 2), 147.26),
        ('ej12', (round(h, 2), round(h*sen(50), 2)), (58.48, 44.80)), ('ej13', round(math.sqrt(105*55*35*15), 2), 1741.23),
    ]

@guia('PM07 Círculo unitario y funciones trigonométricas')
def _():
    pi = sp.pi
    return [
        ('ejemplo1', (sp.sin(pi*150/180), sp.cos(pi*150/180)), (sp.Rational(1, 2), -sp.sqrt(3)/2)),
        ('ejemplo2', (sp.cos(5*pi/4), sp.tan(5*pi/4)), (-sp.sqrt(2)/2, 1)),
        ('coterminal', (sp.cos(pi*420/180) - sp.cos(pi/3), sp.sin(-pi/3) - sp.sin(5*pi/3)), (0, 0)),
        ('ejemplo3', (2*pi/2, -1 - 3, -1 + 3), (pi, -4, 2)),
        ('ejemplo4', trig_sol(sp.Eq(sp.sin(x), -sp.Rational(1, 2))), [7*pi/6, 11*pi/6]),
        ('calc', round(math.degrees(math.asin(-0.5))), -30),
        ('ej1', sp.sin(pi*210/180), -sp.Rational(1, 2)), ('ej2', sp.cos(pi*135/180), -sp.sqrt(2)/2), ('ej3', sp.tan(pi*300/180), -sp.sqrt(3)),
        ('ej4', sp.cos(5*pi/3), sp.Rational(1, 2)), ('ej5', sp.sin(-pi/2), -1), ('ej6', sp.tan(3*pi/4), -1),
        ('ej7', -100 % 360, 260), ('ej8', 360 - 330, 30), ('ej9', (-sp.sqrt(1 - sp.Rational(9, 25)), (-sp.Rational(4, 5)) / (-sp.Rational(3, 5))), (-sp.Rational(4, 5), sp.Rational(4, 3))),
        ('ej10', (4, 2*pi/3), (4, 2*pi/3)), ('ej11', (2*pi/sp.Rational(1, 2), 1 - 2, 1 + 2), (4*pi, -1, 3)),
        ('ej12', sp.simplify(sp.sin(2*(x + pi/2)) - sp.sin(2*x + pi)), 0), ('ej13', 2*pi/2, pi),
        ('ej14', trig_sol(sp.Eq(sp.sin(x), sp.sqrt(3)/2)), [pi/3, 2*pi/3]), ('ej15', trig_sol(sp.Eq(2*sp.cos(x) + 1, 0)), [2*pi/3, 4*pi/3]),
        ('ej16', trig_sol(sp.Eq(sp.tan(x), 1)), [pi/4, 5*pi/4]), ('ej17', (12 + 10, 12 - 10, 2*pi/(pi/15)), (22, 2, 30)),
    ]

@guia('PM08 Identidades trigonométricas')
def _():
    pi, s_, c_ = sp.pi, sp.sin(x), sp.cos(x)
    cero = lambda e: sp.simplify(sp.expand_trig(e)) == 0
    return [
        ('ejemplo1', cero(1/c_ - c_ - s_*sp.tan(x)), True), ('ejemplo2', cero((1 - c_**2)*(1 + sp.cot(x)**2) - 1), True),
        ('ejemplo3', cero(s_/(1 + c_) - (1 - c_)/s_), True), ('ejemplo4', sp.nsimplify(sp.sin(5*pi/12)), (sp.sqrt(6) + sp.sqrt(2))/4),
        ('ejemplo4b', round(math.sin(math.radians(75)), 4), 0.9659),
        ('ejemplo5', (2*F(3, 5)*F(4, 5), F(16, 25) - F(9, 25)), (F(24, 25), F(7, 25))),
        ('ejemplo6', trig_sol(2*s_**2 - s_ - 1), [pi/2, 7*pi/6, 11*pi/6]),
        ('ej1', cero(sp.tan(x)*c_ - s_), True), ('ej2', cero(s_**2 + c_**2 + sp.tan(x)**2 - sp.sec(x)**2), True),
        ('ej3', cero((1 + sp.tan(x)**2)*c_**2 - 1), True), ('ej4', cero(s_/sp.csc(x) + c_/sp.sec(x) - 1), True),
        ('ej5', cero(sp.csc(x) - s_ - c_*sp.cot(x)), True), ('ej6', cero((1 + s_)*(1 - s_) - c_**2), True),
        ('ej7', cero(sp.tan(x) + sp.cot(x) - sp.sec(x)*sp.csc(x)), True), ('ej8', cero(c_/(1 - s_) - (1 + s_)/c_), True),
        ('ej9', sp.nsimplify(sp.cos(pi/12)), (sp.sqrt(6) + sp.sqrt(2))/4), ('ej10', sp.simplify(sp.tan(pi/12)), 2 - sp.sqrt(3)),
        ('ej11', (2*F(-12, 13)*F(5, 13), F(25, 169) - F(144, 169)), (F(-120, 169), F(-119, 169))),
        ('ej12', cero(2*sp.sin(3*x)*sp.cos(3*x) - sp.sin(6*x)), True), ('ej13', sp.cos(pi/8)**2 - sp.sin(pi/8)**2, sp.sqrt(2)/2),
        ('ej14', trig_sol(2*c_**2 - 1), [pi/4, 3*pi/4, 5*pi/4, 7*pi/4]),
        ('ej15', trig_sol(sp.sin(2*x) - s_), [0, pi/3, pi, 5*pi/3]), ('ej16', trig_sol(2*s_**2 + 3*c_ - 3), [0, pi/3, 5*pi/3]),
    ]

def recta_por(p1, p2):
    """Coeficientes (A, B, C) enteros y primitivos de la recta por dos puntos, con A > 0."""
    (x1, y1), (x2, y2) = p1, p2
    A, B = sp.Integer(y2 - y1), sp.Integer(x1 - x2)
    C = -(A*x1 + B*y1)
    g = sp.gcd_list([A, B, C]) or 1
    A, B, C = A/g, B/g, C/g
    if A < 0 or (A == 0 and B < 0): A, B, C = -A, -B, -C
    return (A, B, C)

def misma_recta(e1, e2):
    return sp.simplify(sp.solve(e1, y)[0] - sp.solve(e2, y)[0]) == 0 if e1.has(y) else sp.solve(e1, x) == sp.solve(e2, x)

def dist_pr(P, A, B, C):
    return sp.Abs(A*P[0] + B*P[1] + C) / sp.sqrt(A**2 + B**2)

def completar(expr):
    """Centro y lado derecho de una cónica sin término xy: devuelve (h, k, coef_x2, coef_y2, derecho)."""
    P = sp.Poly(sp.expand(expr), x, y)
    A_, C_ = P.coeff_monomial(x**2), P.coeff_monomial(y**2)
    D_, E_, F_ = P.coeff_monomial(x), P.coeff_monomial(y), P.coeff_monomial(1)
    h = -D_/(2*A_) if A_ else None
    k = -E_/(2*C_) if C_ else None
    der = -F_ + (A_*h**2 if A_ else 0) + (C_*k**2 if C_ else 0)
    return (h, k, A_, C_, der)

@guia('PM09 La recta')
def _():
    X, Y = sp.symbols('X Y')
    return [
        ('ejemplo1', (sp.sqrt(6**2 + 8**2), (F(-2 + 4, 2), F(3 - 5, 2)), F(-8, 6)), (10, (1, -1), F(-4, 3))),
        ('inclinacion', (round(math.degrees(math.atan(-4/3)), 2), round(math.degrees(math.atan(-4/3)) + 180, 2)), (-53.13, 126.87)),
        ('ejemplo2', recta_por((-2, 3), (4, -5)), (4, 3, -1)), ('ejemplo2b', 4*4 + 3*(-5) - 1, 0),
        ('ejemplo3', misma_recta(sp.Eq(y - 4, -sp.Rational(3, 2)*(x - 1)), sp.Eq(3*x + 2*y - 11, 0)), True),
        ('ejemplo3b', sp.Rational(2, 3) * -sp.Rational(3, 2), -1),
        ('ejemplo4', dist_pr((3, 1), 4, 3, -5), 2),
        ('ej1', sp.sqrt(6**2 + 8**2), 10), ('ej2', (F(1 + 7, 2), F(2 + 10, 2)), (4, 6)), ('ej3', F(8, 6), F(4, 3)),
        ('ej4', round(math.degrees(math.atan(4/3)), 2), 53.13),
        ('ej5', sp.expand(-2*(x - 3) + 1), -2*x + 7), ('ej6', sp.expand(4 - 2*(x + 1)), -2*x + 2),
        ('ej7', recta_por((5, 0), (0, -3)), (3, -5, -15)), ('ej8', sp.solve(6*x - 2*y + 8, y)[0], 3*x + 4),
        ('ej9', sp.expand(4*(x - 2) + 3), 4*x - 5),
        ('ej10', misma_recta(sp.Eq(y, sp.Rational(4, 3)*x), sp.Eq(4*x - 3*y, 0)), True), ('ej10b', -sp.Rational(3, 4) * sp.Rational(4, 3), -1),
        ('ej11', -sp.Rational(2, 5) * sp.Rational(5, 2), -1), ('ej12', sp.solve([x + y - 5, 2*x - y - 1], [x, y]), {x: 2, y: 3}),
        ('ej13', dist_pr((2, -3), 3, -4, 2), 4), ('ej14', dist_pr((2, 1), 3, 4, 5), 3), ('ej14b', 3*2 + 4*1 - 10, 0),
        ('ej15', recta_por((1, 1), (5, 2)), (1, -4, 3)),
        ('ej15b', sp.Rational(1, 2) * sp.sqrt(17) * dist_pr((2, 6), 1, -4, 3), sp.Rational(19, 2)),
        ('ej15c', sp.Rational(1, 2) * abs(1*(2 - 6) + 5*(6 - 1) + 2*(1 - 2)), sp.Rational(19, 2)),
    ]

@guia('PM10 La circunferencia')
def _():
    return [
        ('ejemplo1', sp.expand((x - 2)**2 + (y + 3)**2 - 16), x**2 + y**2 - 4*x + 6*y - 3),
        ('ejemplo2', completar(x**2 + y**2 + 6*x - 4*y - 12)[::4], (-3, 25)), ('ejemplo2k', completar(x**2 + y**2 + 6*x - 4*y - 12)[1], 2),
        ('ejemplo3', ((F(-1 + 5, 2), F(2 + 10, 2)), sp.sqrt(36 + 64) / 2), ((2, 6), 5)),
        ('ejemplo4', dist_pr((1, -2), 3, -4, 4), 3),
        ('ejemplo5', recta_por((3, 4), (7, 1)), (3, 4, -25)), ('ejemplo5b', F(4, 3) * F(-3, 4), -1),
        ('ej3', sp.sqrt(3**2 + 4**2), 5), ('ej4', sp.expand((x + 4)**2 + (y - 1)**2 - 9), x**2 + y**2 + 8*x - 2*y + 8),
        ('ej5', completar(x**2 + y**2 - 10*x + 4*y + 13), (5, -2, 1, 1, 16)),
        ('ej6', completar(x**2 + y**2 + 8*y), (0, -4, 1, 1, 16)),
        ('ej7', completar(x**2 + y**2 - 6*x + 4*y - 12), (3, -2, 1, 1, 25)),
        ('ej8', completar(x**2 + y**2 - 2*x + 4*y + 10)[4], -5),
        ('ej9', ((F(-3 + 5, 2), F(4 - 2, 2)), sp.sqrt(64 + 36) / 2), ((1, 1), 5)),
        ('ej11', dist_pr((4, -1), 5, 12, 18), 2), ('ej12', (4 - 1)**2 + (1 + 3)**2, 25),
        ('ej13', ((2*2 + 3*3), 2**2 + 3**2), (13, 13)),
        ('ej14', misma_recta(sp.Eq(y - 6, -sp.Rational(3, 4)*(x - 4)), sp.Eq(3*x + 4*y - 36, 0)), True),
        ('ej14b', (4 - 1)**2 + (6 - 2)**2, 25),
    ]

@guia('PM11 La parábola')
def _():
    return [
        ('ejemplo1', (F(12, 4), F(-8, 4)), (3, -2)),
        ('ejemplo2', (3 - (-1), 4*4, -1 - 4), (4, 16, -5)),
        ('ejemplo3', sp.expand((y - 3)**2 - 8*(x + 1)), y**2 - 6*y - 8*x + 1),
        ('ejemplo4', (F(900, 40), 22.5 - 10), (22.5, 12.5)),
        ('ej1', F(8, 4), 2), ('ej2', F(20, 4), 5), ('ej3', F(-6, 4), F(-3, 2)), ('ej4', F(-12, 4), -3),
        ('ej5', 4*(-4), -16), ('ej6', 4*3, 12), ('ej7', (5 - 2, 4*3), (3, 12)), ('ej8', (-1 - (-3), 4*2), (2, 8)),
        ('ej9', sp.expand((x - 2)**2 - 8*(y - 1)), x**2 - 4*x - 8*y + 12),
        ('ej10', sp.expand((y + 1)**2 + 4*(x - 2)), y**2 + 2*y + 4*x - 7), ('ej10b', (2 + (-1), 2 - (-1)), (1, 3)),
        ('ej11', sp.expand((x - 3)**2 - 12*(y - 2)), x**2 - 6*x - 12*y + 33),
        ('ej12', sp.solve(sp.Eq(1, 4*a*sp.Rational(1, 4)), a), [1]),
        ('ej13', (sp.solve(sp.Eq(400, 4*a*(0 - 10)), a), 10 - sp.Rational(25, 40)), ([-10], sp.Rational(75, 8))),
        ('ej13b', 75/8, 9.375),
    ]

@guia('PM12 La elipse')
def _():
    return [
        ('figura', round(math.hypot(5*math.cos(math.pi/3) - 4, 3*math.sin(math.pi/3)) + math.hypot(5*math.cos(math.pi/3) + 4, 3*math.sin(math.pi/3)), 9), 10.0),
        ('ejemplo1', (math.sqrt(25 - 9), F(4, 5), F(2*9, 5)), (4.0, F(4, 5), F(18, 5))),
        ('ejemplo2', 100 - 36, 64),
        ('ejemplo3', completar(4*x**2 + 9*y**2 - 16*x + 18*y - 11), (2, -1, 4, 9, 36)), ('ejemplo3c', 9 - 4, 5),
        ('ejemplo4', (round((147.1 + 152.1) / 2, 1), round(152.1 - 149.6, 1), round(2.5 / 149.6, 4)), (149.6, 2.5, 0.0167)),
        ('ej1', (math.sqrt(100 - 36), 8/10), (8.0, 0.8)), ('ej2', (math.sqrt(25 - 16), 3/5), (3.0, 0.6)),
        ('ej3', 9 - 4, 5), ('ej4', 2*36/10, 7.2), ('ej5', 169 - 144, 25), ('ej6', (10**2, 6**2), (100, 36)),
        ('ej8', (3 / F(1, 2), 36 - 9), (6, 27)),
        ('ej9', completar(9*x**2 + 25*y**2 - 36*x + 50*y - 164), (2, -1, 9, 25, 225)), ('ej9c', (math.sqrt(25 - 9), 2 + 4, 2 - 4), (4.0, 6, -2)),
        ('ej10', completar(4*x**2 + y**2 + 8*x - 6*y + 9), (-1, 3, 4, 1, 4)), ('ej10c', 4 - 1, 3),
        ('ej11', round(6*math.sqrt(1 - 16/100), 2), 5.50), ('ej12', round(math.sqrt(15**2 - 10**2), 2), 11.18),
        ('ej13', (round(1.524*(1 - 0.0934), 3), round(1.524*(1 + 0.0934), 3)), (1.382, 1.666)),
    ]

@guia('PM13 La hipérbola')
def _():
    return [
        ('ejemplo1', (math.sqrt(16 + 9), F(3, 4), F(5, 4)), (5.0, F(3, 4), F(5, 4))),
        ('ejemplo2', (math.sqrt(25 + 144), F(5, 12)), (13.0, F(5, 12))), ('ejemplo3', 25 - 9, 16),
        ('ejemplo4', completar(9*x**2 - 4*y**2 - 36*x - 8*y - 4), (2, -1, 9, -4, 36)), ('ejemplo4c', 4 + 9, 13),
        ('degenerada', sp.factor(4*x**2 - 9*y**2), (2*x - 3*y)*(2*x + 3*y)),
        ('ej1', (math.sqrt(36 + 64), F(8, 6), F(10, 6)), (10.0, F(4, 3), F(5, 3))), ('ej2', (math.sqrt(9 + 16), F(3, 4)), (5.0, F(3, 4))),
        ('ej3', (sp.sqrt(4 + 16), F(4, 2)), (2*sp.sqrt(5), 2)), ('ej4', 169 - 25, 144), ('ej5', 4 / 2, 2.0),
        ('ej6', (10 / 2, 100 - 25), (5.0, 75)), ('ej7', 25 - 9, 16),
        ('ej8', completar(x**2 - 4*y**2 - 2*x - 16*y - 19), (1, -2, 1, -4, 4)), ('ej8c', 4 + 1, 5),
        ('ej9', completar(16*y**2 - 9*x**2 + 54*x + 64*y - 161), (3, -2, -9, 16, 144)), ('ej9c', (math.sqrt(9 + 16), -2 + 5, -2 - 5), (5.0, 3, -7)),
        ('ej10', completar(3*x**2 + 3*y**2 - 6*x + 12*y), (1, -2, 3, 3, 15)),
        ('ej12', completar(x**2 - y**2 + 4*x), (-2, 0, 1, -1, 4)),
    ]

t, h = sp.symbols('t h')
D = lambda e, v=x: sp.simplify(sp.diff(e, v))
iguales = lambda e1, e2: sp.simplify(e1 - e2) == 0
lim = sp.limit
oo = sp.oo

def por_definicion(f):
    return sp.limit(sp.simplify((f.subs(x, x + h) - f) / h), h, 0)

def implicita(ec):
    Y = sp.Function('Y')(x)
    e = ec.subs(y, Y)
    d = sp.solve(sp.diff(e, x), sp.diff(Y, x))[0]
    return d.subs(Y, y)

@guia('PM14 Límites')
def _():
    tabla = [round(((v**2 - 4) / (v - 2)), 3) for v in (1.9, 1.99, 1.999, 2.001, 2.01, 2.1)]
    return [
        ('tabla', tabla, [3.9, 3.99, 3.999, 4.001, 4.01, 4.1]),
        ('ejemplo1', (lim(sp.Abs(x)/x, x, 0, '-'), lim(sp.Abs(x)/x, x, 0, '+')), (-1, 1)),
        ('ejemplo2', lim((x**2 - 4)/(x - 2), x, 2), 4), ('ejemplo3', lim((sp.sqrt(x + 9) - 3)/x, x, 0), sp.Rational(1, 6)),
        ('infinito', (lim((2*x + 1)/(x**2 - 3), x, oo), lim((3*x**2 - 5*x)/(2*x**2 + 1), x, oo), lim(x**3/(x + 1), x, oo)), (0, sp.Rational(3, 2), oo)),
        ('asintota', (lim(1/(x - 3), x, 3, '+'), lim(1/(x - 3), x, 3, '-')), (oo, -oo)),
        ('notables', (lim(sp.sin(x)/x, x, 0), lim((1 - sp.cos(x))/x, x, 0), lim(sp.sin(3*x)/x, x, 0)), (1, 0, 3)),
        ('ej1', lim(2*x**2 - x + 1, x, 3), 16), ('ej2', lim((x + 5)/(x - 3), x, -1), -1), ('ej3', lim(sp.sqrt(x + 5), x, 4), 3),
        ('ej4', lim((x**2 - 9)/(x - 3), x, 3), 6), ('ej5', lim((x**2 + 2*x - 3)/(x**2 - 1), x, 1), 2),
        ('ej6', lim((x**3 + 8)/(x + 2), x, -2), 12), ('ej7', lim((sp.sqrt(x) - 2)/(x - 4), x, 4), sp.Rational(1, 4)),
        ('ej8', lim(((2 + h)**2 - 4)/h, h, 0), 4),
        ('ej9', lim((5*x**3 - 2*x)/(2*x**3 + 7), x, oo), sp.Rational(5, 2)), ('ej10', lim((4*x + 1)/(x**2 + 3), x, oo), 0),
        ('ej11', lim((x**2 - 1)/(3*x + 2), x, oo), oo), ('ej12', lim(sp.sqrt(x**2 + 1)/(2*x), x, oo), sp.Rational(1, 2)),
        ('ej13', (2 + 1, 2**2 - 1), (3, 3)), ('ej14', (2*1, 1 + 3), (2, 4)), ('ej15', lim(3/(x - 5), x, 5, '-'), -oo),
        ('ej16', lim(sp.sin(5*x)/(2*x), x, 0), sp.Rational(5, 2)), ('ej17', lim(sp.tan(x)/x, x, 0), 1),
    ]

@guia('PM15 Continuidad')
def _():
    f3 = lambda v: v**3 + v - 1
    g = lambda v: v**3 - 3*v + 1
    k = sp.Symbol('k')
    return [
        ('ejemplo1', lim((x**2 - 1)/(x - 1), x, 1), 2), ('ejemplo2', sp.solve(sp.Eq(2*k + 1, 4 - k), k), [1]), ('ejemplo2b', 4 - 1, 3),
        ('ejemplo3', (f3(0), f3(1), f3(0.5), f3(0.75)), (-1, 1, -0.375, 0.171875)),
        ('ejemplo3r', round(float(sp.nsolve(x**3 + x - 1, x, 0.7)), 4), 0.6823),
        ('ej1', lim((x**2 - 4)/(x + 2), x, -2), -4), ('ej2', sp.solve(x**2 - 9, x), [-3, 3]),
        ('ej3', (1 + 2, 5 - 1), (3, 4)), ('ej4', (lim((x - 3)/(x**2 - 5*x + 6), x, 3), lim((x - 3)/(x**2 - 5*x + 6), x, 2, '+')), (1, oo)),
        ('ej5', (1**2, 2*1 - 1), (1, 1)), ('ej6', lim(sp.sin(x)/x, x, 0), 1),
        ('ej7', sp.solve(sp.Eq(6 - k, 2*k + 1), k), [sp.Rational(5, 3)]), ('ej8', sp.solve(sp.Eq(9 - k, 3*k), k), [sp.Rational(9, 4)]),
        ('ej9', lim((x**2 - 16)/(x - 4), x, 4), 8), ('ej10', (g(0), g(1)), (1, -1)),
        ('ej11', (g(0.5), g(0.25)), (-0.375, 0.265625)), ('ej11r', round(float(sp.nsolve(x**3 - 3*x + 1, x, 0.35)), 4), 0.3473),
        ('ej12', (math.cos(0) - 0 > 0, math.cos(math.pi/2) - math.pi/2 < 0), (True, True)),
    ]

@guia('PM16 Definición de derivada')
def _():
    return [
        ('ejemplo1', F(9 - 1, 2), 4), ('ejemplo2', por_definicion(x**2), 2*x), ('ejemplo3', por_definicion(1/x), -1/x**2),
        ('ejemplo4', por_definicion(sp.sqrt(x)), 1/(2*sp.sqrt(x))), ('ejemplo5', sp.expand(6*(x - 3) + 9), 6*x - 9),
        ('ejemplo6', por_definicion(5*x**2).subs(x, 2), 20),
        ('ej1', F(8 - 1, 1), 7), ('ej2', F((3*4 + 2) - (3*(-1) + 2), 5), 3), ('ej3', round((4.9*9 - 4.9) / 2, 9), 19.6),
        ('ej4', por_definicion(5*x - 3), 5), ('ej5', por_definicion(x**2 + 3*x), 2*x + 3), ('ej6', por_definicion(2*x**2 - x), 4*x - 1),
        ('ej7', por_definicion(3/x), -3/x**2), ('ej8', por_definicion(sp.sqrt(x + 1)), 1/(2*sp.sqrt(x + 1))),
        ('ej9', sp.expand(4 + 5*(x - 1)), 5*x - 1), ('ej10', sp.expand(1 - sp.Rational(1, 3)*(x - 3)), -x/3 + 2),
        ('ej11', (sp.solve(2*x - 8, x), 4**2), ([4], 16)), ('ej12', round(float(por_definicion(4.9*x**2).subs(x, 3)), 6), 29.4),
        ('ej13', (lim(sp.Abs(h)/h, h, 0, '+'), lim(sp.Abs(h)/h, h, 0, '-')), (1, -1)),
        ('ej14', por_definicion(sp.Rational(1, 50)*x**2 + 50*x).subs(x, 100), 54),
    ]

@guia('PM17 Reglas de derivación')
def _():
    return [
        ('ejemplo1', D(4*x**5 - 3*x**2 + 7*x - 2), 20*x**4 - 6*x + 7), ('ejemplo2', D(3/x**2 + sp.sqrt(x)), -6/x**3 + 1/(2*sp.sqrt(x))),
        ('ejemplo3', D(x**2*sp.sin(x)), 2*x*sp.sin(x) + x**2*sp.cos(x)), ('ejemplo4', D((x**2 + 1)/(x - 3)), (x**2 - 6*x - 1)/(x - 3)**2),
        ('ejemplo5', D(sp.tan(x)), sp.sec(x)**2), ('ejemplo6', D(sp.exp(x)*sp.log(x)), sp.exp(x)*(sp.log(x) + 1/x)),
        ('ejemplo7', (D(t**3 - 6*t**2, t).subs(t, 3), sp.diff(t**3 - 6*t**2, t, 2).subs(t, 3)), (-9, 6)),
        ('tabla', (D(sp.sec(x)), D(sp.csc(x)), D(sp.cot(x)), D(5**x), D(sp.log(x, 3))),
         (sp.sec(x)*sp.tan(x), -sp.csc(x)*sp.cot(x), -sp.csc(x)**2, 5**x*sp.log(5), 1/(x*sp.log(3)))),
        ('ej1', D(7*x**3 - 4*x + 9), 21*x**2 - 4), ('ej2', D(x**-4 + 2/x), -4*x**-5 - 2*x**-2),
        ('ej3', D(5*sp.sqrt(x) - 2*sp.cbrt(x)), 5/(2*sp.sqrt(x)) - 2/(3*x**sp.Rational(2, 3))),
        ('ej4', D((2*x + 1)**2), 8*x + 4), ('ej5', D((x**3 - 2*x)/x), 2*x),
        ('ej6', D(x**3*sp.exp(x)), x**2*sp.exp(x)*(x + 3)), ('ej7', D((x**2 + 1)*(3*x - 5)), 9*x**2 - 10*x + 3),
        ('ej8', D(x/(x + 1)), 1/(x + 1)**2), ('ej9', D(sp.sin(x)/x), (x*sp.cos(x) - sp.sin(x))/x**2),
        ('ej10', D((2*x - 3)/(x**2 + 4)), (-2*x**2 + 6*x + 8)/(x**2 + 4)**2),
        ('ej11', D(3*sp.cos(x) - 2*sp.exp(x)), -3*sp.sin(x) - 2*sp.exp(x)), ('ej12', D(x*sp.log(x)), sp.log(x) + 1),
        ('ej13', D(sp.exp(x)*sp.sin(x)), sp.exp(x)*(sp.sin(x) + sp.cos(x))), ('ej14', D(5**x), 5**x*sp.log(5)),
        ('ej15', D(sp.tan(x) - x), sp.tan(x)**2),
        ('ej16', (D(x**3 - 2*x).subs(x, 2), (x**3 - 2*x).subs(x, 2)), (10, 4)), ('ej16b', sp.expand(4 + 10*(x - 2)), 10*x - 16),
        ('ej17', (sp.solve(D(t**3 - 9*t**2 + 24*t, t), t), sp.diff(t**3 - 9*t**2 + 24*t, t, 2).subs(t, 2)), ([2, 4], -6)),
        ('ej18', sp.diff(x**4 - 3*x**2, x, 2), 12*x**2 - 6),
    ]

@guia('PM18 Regla de la cadena')
def _():
    return [
        ('ejemplo1', D((3*x**2 + 1)**5), 30*x*(3*x**2 + 1)**4), ('ejemplo2', D(sp.sqrt(1 - x**2)), -x/sp.sqrt(1 - x**2)),
        ('tabla', (D(sp.sin(4*x)), D(sp.cos(x**2)), D(sp.tan(3*x)), D(sp.exp(x**2)), D(sp.log(x**2 + 1))),
         (4*sp.cos(4*x), -2*x*sp.sin(x**2), 3*sp.sec(3*x)**2, 2*x*sp.exp(x**2), 2*x/(x**2 + 1))),
        ('nota', (D(sp.sin(x)**2), D(sp.sin(x**2))), (2*sp.sin(x)*sp.cos(x), 2*x*sp.cos(x**2))),
        ('ejemplo3', D(sp.cos(2*x)**3), -6*sp.cos(2*x)**2*sp.sin(2*x)),
        ('ejemplo4', D(20 + 60*sp.exp(-sp.Rational(1, 10)*t), t).subs(t, 0), -6),
        ('ejemplo5', D(x*sp.exp(-3*x)), sp.exp(-3*x)*(1 - 3*x)),
        ('ej1', D((2*x - 5)**4), 8*(2*x - 5)**3), ('ej2', D((x**3 + 2*x)**-2), -2*(3*x**2 + 2)/(x**3 + 2*x)**3),
        ('ej3', D(sp.sqrt(3*x + 4)), 3/(2*sp.sqrt(3*x + 4))), ('ej4', D(1/(x**2 + 1)**3), -6*x/(x**2 + 1)**4),
        ('ej5', D(sp.cos(5*x)), -5*sp.sin(5*x)), ('ej6', D(sp.tan(x**2)), 2*x*sp.sec(x**2)**2), ('ej7', D(sp.exp(3*x - 1)), 3*sp.exp(3*x - 1)),
        ('ej8', D(sp.log(5*x)), 1/x), ('ej9', D(sp.log(sp.cos(x))), -sp.tan(x)), ('ej10', D(sp.sin(x)**3), 3*sp.sin(x)**2*sp.cos(x)),
        ('ej11', D(x**2*(x - 1)**5), x*(x - 1)**4*(7*x - 2)), ('ej12', D(sp.exp(2*x)*sp.cos(x)), sp.exp(2*x)*(2*sp.cos(x) - sp.sin(x))),
        ('ej13', D(sp.sqrt(x**2 + 9)).subs(x, 4), sp.Rational(4, 5)), ('ej14', D(((x + 1)/(x - 1))**2), -4*(x + 1)/(x - 1)**3),
        ('ej15', (sp.sqrt(9), D(sp.sqrt(2*x + 1)).subs(x, 4), sp.expand(3 + sp.Rational(1, 3)*(x - 4))), (3, sp.Rational(1, 3), x/3 + sp.Rational(5, 3))),
        ('ej16', (D(3*sp.sin(2*t), t), D(3*sp.sin(2*t), t).subs(t, 0), sp.diff(3*sp.sin(2*t), t, 2)), (6*sp.cos(2*t), 6, -12*sp.sin(2*t))),
        ('ej17', round(float(D(500*sp.exp(sp.Rational(1, 5)*t), t).subs(t, 5))), 272),
    ]

@guia('PM19 Derivación implícita')
def _():
    return [
        ('ejemplo1', (implicita(x**2 + y**2 - 25), implicita(x**2 + y**2 - 25).subs({x: 3, y: 4})), (-x/y, -sp.Rational(3, 4))),
        ('ejemplo2', (2 + 8, implicita(x**2*y + y**3 - 10), implicita(x**2*y + y**3 - 10).subs({x: 1, y: 2})), (10, -2*x*y/(x**2 + 3*y**2), -sp.Rational(4, 13))),
        ('ejemplo3', (implicita(x**3 + y**3 - 6*x*y), implicita(x**3 + y**3 - 6*x*y).subs({x: 3, y: 3}), 27 + 27 - 54), ((2*y - x**2)/(y**2 - 2*x), -1, 0)),
        ('ejemplo4', sp.simplify(sp.diff(-x/y, x).subs(sp.Derivative(y, x), 0) + x*(-x/y)/y**2 - (-(x**2 + y**2)/y**3)), 0),
        ('inversas', (D(sp.asin(x)), D(sp.acos(x)), D(sp.atan(x))), (1/sp.sqrt(1 - x**2), -1/sp.sqrt(1 - x**2), 1/(1 + x**2))),
        ('ejemplo5', D(x**x), x**x*(sp.log(x) + 1)),
        ('ej1', implicita(x**2 + y**2 - 16), -x/y), ('ej2', implicita(4*x**2 + 9*y**2 - 36), -4*x/(9*y)), ('ej3', implicita(x*y - 12), -y/x),
        ('ej4', implicita(x**2*y + x*y**2 - 6), -(2*x*y + y**2)/(x**2 + 2*x*y)), ('ej5', implicita(y**3 - 3*y - x**2), 2*x/(3*y**2 - 3)),
        ('ej6', implicita(sp.exp(y) - x - y), 1/(sp.exp(y) - 1)),
        ('ej7', (implicita(x**2 + y**2 - 25).subs({x: -3, y: 4}), recta_por((-3, 4), (1, 7))), (sp.Rational(3, 4), (3, -4, 25))),
        ('ej8', (9 - 6 + 4, implicita(x**2 - x*y + y**2 - 7).subs({x: 3, y: 2}), sp.expand(2 - 4*(x - 3))), (7, -4, -4*x + 14)),
        ('ej9', sp.solve([x, x**2 + y**2 - 25], [x, y]), [(0, -5), (0, 5)]),
        ('ej10', D(sp.atan(2*x)), 2/(1 + 4*x**2)), ('ej11', D(sp.asin(x/3)), 1/sp.sqrt(9 - x**2)),
        ('ej12', D(x**sp.sin(x)), x**sp.sin(x)*(sp.cos(x)*sp.log(x) + sp.sin(x)/x)),
        ('ej13', sp.simplify(-(x**2 + y**2)/y**3).subs(x**2 + y**2, 4), -4/y**3),
    ]

@guia('PM20 Máximos y mínimos')
def _():
    f = x**3 - 3*x**2 - 9*x + 5
    crit = lambda e: sp.solve(D(e), x)
    val = lambda e, v: e.subs(x, v)
    V = x*(12 - 2*x)**2
    return [
        ('ejemplo1', (sp.factor(D(f)), crit(f), val(f, -1), val(f, 3)), (3*(x - 3)*(x + 1), [-1, 3], 10, -22)),
        ('ejemplo2', (sp.diff(f, x, 2).subs(x, -1), sp.diff(f, x, 2).subs(x, 3), sp.solve(sp.diff(f, x, 2), x), val(f, 1)), (-12, 12, [1], -6)),
        ('ejemplo3', ([v for v in crit(x**3 - 3*x) if 0 <= v <= 2], [val(x**3 - 3*x, v) for v in (0, 1, 2)]), ([1], [0, -2, 2])),
        ('ejemplo4', (sp.factor(D(V)), crit(V), val(V, 2)), (sp.factor((12 - 2*x)*(12 - 6*x)), [2, 6], 128)),
        ('ejemplo5', (crit(x*(100 - 2*x)), 100 - 50, val(x*(100 - 2*x), 25)), ([25], 50, 1250)),
        ('ej1', (crit(x**2 - 6*x + 1), val(x**2 - 6*x + 1, 3)), ([3], -8)),
        ('ej2', (crit(2*x**3 - 3*x**2 - 12*x), val(2*x**3 - 3*x**2 - 12*x, -1), val(2*x**3 - 3*x**2 - 12*x, 2)), ([-1, 2], 7, -20)),
        ('ej3', (crit(x**4 - 2*x**2), [val(x**4 - 2*x**2, v) for v in (-1, 0, 1)]), ([-1, 0, 1], [-1, 0, -1])),
        ('ej4', (crit(x*sp.exp(-x)), val(x*sp.exp(-x), 1)), ([1], sp.exp(-1))),
        ('ej5', (sp.solve(sp.diff(x**3 - 6*x**2 + 4, x, 2), x), val(x**3 - 6*x**2 + 4, 2)), ([2], -12)),
        ('ej6', (crit(x**3 - 12*x), val(x**3 - 12*x, -2), val(x**3 - 12*x, 2)), ([-2, 2], 16, -16)),
        ('ej7', [val(x**2 - 4*x + 3, v) for v in (0, 2, 5)], [3, -1, 8]),
        ('ej8', [val(x**3 - 12*x, v) for v in (-3, -2, 2, 5)], [9, 16, -16, 65]),
        ('ej9', (crit(x*(20 - x)), 10*10), ([10], 100)), ('ej10', ([v for v in crit(x + 1/x) if v > 0], 1 + 1), ([1], 2)),
        ('ej11', (crit(x*(30 - 2*x)**2), val(x*(30 - 2*x)**2, 5)), ([5, 15], 2000)),
        ('ej12', (round((500/math.pi)**(1/3), 2), round(1000/(math.pi*(500/math.pi)**(2/3)), 2)), (5.42, 10.84)),
        ('ej13', (crit(x*(200 - 4*x)), val(x*(200 - 4*x), 25)), ([25], 2500)),
    ]

@guia('PM21 Razones de cambio relacionadas')
def _():
    pi = sp.pi
    return [
        ('ejemplo1', sp.Rational(100) / (4*pi*25), 1/pi), ('ejemplo1b', round(1/math.pi, 3), 0.318),
        ('ejemplo2', (math.sqrt(25 - 9), -3*1/4), (4.0, -0.75)),
        ('ejemplo3', (sp.expand(sp.Rational(1, 3)*pi*(x/2)**2*x), 2 / (pi*9/4)), (pi*x**3/12, 8/(9*pi))), ('ejemplo3b', round(8/(9*math.pi), 3), 0.283),
        ('ej1', 2*pi*10*3, 60*pi), ('ej2', 2*5*2, 20), ('ej3', F(12, 3*4), 1), ('ej4', 4*pi*36*(-sp.Rational(1, 2)), -72*pi),
        ('ej4b', round(-72*math.pi, 1), -226.2), ('ej5', (math.sqrt(100 - 36), -6*2/8), (8.0, -1.5)),
        ('ej6', (math.hypot(160, 120), (160*80 + 120*60)/200), (200.0, 100.0)),
        ('ej7', (math.sqrt(100 - 36), 8*500/10), (8.0, 400.0)),
        ('ej8', 5 / (pi*4/4), 5/pi), ('ej8b', round(5/math.pi, 2), 1.59),
        ('ej9', (sp.solve(sp.Eq(y/sp.Rational(18, 10), (x + y)/6), y), round(3/7*1.5, 2), round(1.5 + 3/7*1.5, 2)), ([3*x/7], 0.64, 2.14)),
        ('ej10', F(-4, 1)*F(1, 2)/3, F(-2, 3)),
    ]

I = lambda e, v=x: sp.integrate(e, v)
Idef = lambda e, a_, b_, v=x: sp.simplify(sp.integrate(e, (v, a_, b_)))

def antider(F_, f_, v=x):
    """F es antiderivada de f (comprueba derivando)."""
    return sp.simplify(sp.diff(F_, v) - f_) == 0

@guia('PM22 Antiderivadas')
def _():
    return [
        ('ejemplo1a', antider(2*x**3 - 2*x**2 + 5*x, 6*x**2 - 4*x + 5), True),
        ('ejemplo1b', antider(3*sp.sin(x) - 2*sp.exp(x) + 4*sp.log(x), 3*sp.cos(x) - 2*sp.exp(x) + 4/x), True),
        ('ejemplo2', antider(sp.Rational(2, 3)*x**sp.Rational(3, 2) - 1/x, sp.sqrt(x) + 1/x**2), True),
        ('ejemplo3', antider(x**2/2 + sp.log(x), (x**2 + 1)/x), True),
        ('tabla', all(antider(F_, f_) for F_, f_ in [(2**x/sp.log(2), 2**x), (sp.sec(x), sp.sec(x)*sp.tan(x)), (sp.asin(x), 1/sp.sqrt(1 - x**2))]), True),
        ('ejemplo4', sp.solve(1 - 2 + a - 4, a), [5]), ('ejemplo5', (I(-sp.Float(9.8), t) + 20, I(20 - sp.Float(9.8)*t, t)), (20 - 9.8*t, 20*t - 4.9*t**2)),
        ('ej1', antider(x**4 - 3*x**2 + x, 4*x**3 - 6*x + 1), True), ('ej2', antider(-1/(2*x**2), x**-3), True),
        ('ej3', antider(sp.Rational(10, 3)*x**sp.Rational(3, 2), 5*sp.sqrt(x)), True),
        ('ej4', antider(-1/x**2 + sp.Rational(9, 4)*x**sp.Rational(4, 3), 2/x**3 + 3*sp.cbrt(x)), True),
        ('ej5', antider(x**3/3 + 2*x**2 + 4*x, (x + 2)**2), True), ('ej6', antider(x**3/3 - 4*x, (x**3 - 4*x)/x), True),
        ('ej7', antider(-sp.cos(x) + 2*sp.sin(x), sp.sin(x) + 2*sp.cos(x)), True), ('ej8', antider(sp.tan(x), sp.sec(x)**2), True),
        ('ej9', antider(sp.exp(x) - 3*sp.log(x), sp.exp(x) - 3/x), True), ('ej10', antider(sp.atan(x), 1/(1 + x**2)), True),
        ('ej11', antider(2**x/sp.log(2), 2**x), True),
        ('ej12', (antider(x**2 + 3*x - 1, 2*x + 3), (x**2 + 3*x - 1).subs(x, 0)), (True, -1)),
        ('ej13', (antider(2*x**3 - 2*x**2 + 5, 6*x**2 - 4*x), (2*x**3 - 2*x**2 + 5).subs(x, 1)), (True, 5)),
        ('ej14', (sp.diff(2*x**3 + 2*x + 1, x, 2), sp.diff(2*x**3 + 2*x + 1, x).subs(x, 0), 1), (12*x, 2, 1)),
        ('ej15', (sp.sin(x) + 2).subs(x, sp.pi/2), 3),
        ('ej16', (I(3*t**2 - 2*t, t) + 4, (t**3 - t**2 + 4).subs(t, 2)), (t**3 - t**2 + 4, 8)),
        ('ej17', (F('14.7')/F('9.8'), F('14.7')*F(3, 2) - F('4.9')*F(9, 4)), (F(3, 2), F('11.025'))),
        ('ej18', (25/5, 25*5 - 2.5*25), (5.0, 62.5)),
    ]

@guia('PM23 Integral definida y TFC')
def _():
    G = sp.Integral(sp.sqrt(1 + t**3), (t, 0, x))
    H = sp.Integral(sp.cos(t), (t, 1, x**2))
    v = t**2 - 4*t + 3
    return [
        ('ejemplo1', (sum(q**2 for q in (0.5, 1, 1.5, 2)) * 0.5, Idef(x**2, 0, 2)), (3.75, sp.Rational(8, 3))),
        ('ejemplo2', (Idef(x**2, 0, 2), Idef(2*x + 1, 1, 3), Idef(sp.sin(x), 0, sp.pi)), (sp.Rational(8, 3), 10, 2)),
        ('ejemplo3', (Idef(x**2 - 1, -1, 2), Idef(x**2 - 1, -1, 1), Idef(x**2 - 1, 1, 2)), (0, -sp.Rational(4, 3), sp.Rational(4, 3))),
        ('ejemplo4', (sp.diff(G, x), sp.diff(H, x)), (sp.sqrt(1 + x**3), 2*x*sp.cos(x**2))),
        ('promedio', Idef(x**2, 0, 3) / 3, 3),
        ('ej1', sum(q + 1 for q in range(4)), 10), ('ej2', sum(q + 1 for q in range(1, 5)), 14), ('ej1b', Idef(x + 1, 0, 4), 12),
        ('ej3', Idef(3*x**2 - 2*x, 0, 2), 4), ('ej4', Idef(sp.sqrt(x), 1, 4), sp.Rational(14, 3)), ('ej5', Idef(1/x, 1, sp.E), 1),
        ('ej6', Idef(sp.cos(x), 0, sp.pi/2), 1), ('ej7', Idef(sp.exp(x), 0, 1), sp.E - 1), ('ej8', Idef(x**3, -2, 2), 0),
        ('ej9', Idef((x**2 + 1)/x**2, 1, 2), sp.Rational(3, 2)),
        ('ej10', sp.diff(sp.Integral(t**3 + 1, (t, 2, x)), x), x**3 + 1), ('ej11', sp.diff(sp.Integral(sp.sin(t), (t, 0, x**2)), x), 2*x*sp.sin(x**2)),
        ('ej12', sp.diff(sp.Integral(sp.exp(t**2), (t, x, 5)), x), -sp.exp(x**2)),
        ('ej13', Idef(4 - x**2, -2, 2), sp.Rational(32, 3)), ('ej14', (Idef(sp.sin(x), 0, sp.pi)/sp.pi, round(2/math.pi, 3)), (2/sp.pi, 0.637)),
        ('ej15', (Idef(v, 0, 3, t), Idef(v, 0, 1, t), Idef(v, 1, 3, t), Idef(sp.Abs(v), 0, 3, t)), (0, sp.Rational(4, 3), -sp.Rational(4, 3), sp.Rational(8, 3))),
        ('ej16', Idef(20 - 2*t, 0, 10, t), 100),
    ]

@guia('PM24 Integración por sustitución')
def _():
    return [
        ('ejemplo1', antider((x**2 + 1)**6/6, 2*x*(x**2 + 1)**5), True), ('ejemplo2', antider(sp.Rational(1, 3)*(x**2 + 4)**sp.Rational(3, 2), x*sp.sqrt(x**2 + 4)), True),
        ('lineal', (antider(sp.sin(3*x)/3, sp.cos(3*x)), antider(-sp.exp(-2*x)/2, sp.exp(-2*x))), (True, True)),
        ('ejemplo3', (antider(-sp.log(sp.cos(x)), sp.tan(x)), antider(sp.log(x)**2/2, sp.log(x)/x)), (True, True)),
        ('ejemplo4', (Idef(x*sp.exp(x**2), 0, 1), round((math.e - 1)/2, 3)), ((sp.E - 1)/2, 0.859)),
        ('ejemplo5', antider(x + 1 - sp.log(x + 1), x/(x + 1)), True),
        ('ej1', antider((x**3 - 5)**5/5, 3*x**2*(x**3 - 5)**4), True), ('ej2', antider((x**2 + 3)**8/16, x*(x**2 + 3)**7), True),
        ('ej3', antider((2*x + 1)**sp.Rational(3, 2)/3, sp.sqrt(2*x + 1)), True), ('ej4', antider(sp.sqrt(x**2 + 9), x/sp.sqrt(x**2 + 9)), True),
        ('ej5', antider(sp.log(3*x - 2)/3, 1/(3*x - 2)), True), ('ej6', antider(-sp.cos(5*x)/5, sp.sin(5*x)), True),
        ('ej7', antider(sp.sin(x**2)/2, x*sp.cos(x**2)), True), ('ej8', antider(sp.exp(4*x)/4, sp.exp(4*x)), True),
        ('ej9', antider(sp.log(1 + sp.exp(x)), sp.exp(x)/(1 + sp.exp(x))), True), ('ej10', antider(-sp.cos(x)**4/4, sp.sin(x)*sp.cos(x)**3), True),
        ('ej11', antider(sp.log(x)**3/3, sp.log(x)**2/x), True), ('ej12', antider(sp.atan(2*x)/2, 1/(1 + 4*x**2)), True),
        ('ej13', Idef(x*(x**2 + 1)**2, 0, 2), sp.Rational(62, 3)), ('ej14', Idef(sp.sin(x)*sp.cos(x), 0, sp.pi/2), sp.Rational(1, 2)),
        ('ej15', Idef(sp.log(x)/x, 1, sp.E), sp.Rational(1, 2)), ('ej16', (Idef(x/(x**2 + 1), 0, 1), round(math.log(2)/2, 3)), (sp.log(2)/2, 0.347)),
        ('ej17', antider(sp.Rational(2, 5)*(x - 1)**sp.Rational(5, 2) + sp.Rational(2, 3)*(x - 1)**sp.Rational(3, 2), x*sp.sqrt(x - 1)), True),
        ('ej18', (antider(4000*sp.exp(t/20), 200*sp.exp(t/20), t), round(4000*math.exp(0.5))), (True, 6595)),
    ]

@guia('PM25 Integración por partes')
def _():
    return [
        ('ejemplo1', antider(x*sp.exp(x) - sp.exp(x), x*sp.exp(x)), True), ('ejemplo2', antider(x*sp.sin(x) + sp.cos(x), x*sp.cos(x)), True),
        ('ejemplo3', antider(x*sp.log(x) - x, sp.log(x)), True), ('ejemplo4', antider(sp.exp(x)*(x**2 - 2*x + 2), x**2*sp.exp(x)), True),
        ('ejemplo5', antider(sp.exp(x)*(sp.sin(x) - sp.cos(x))/2, sp.exp(x)*sp.sin(x)), True), ('ejemplo6', Idef(x*sp.sin(x), 0, sp.pi), sp.pi),
        ('ej1', antider(sp.exp(2*x)*(x/2 - sp.Rational(1, 4)), x*sp.exp(2*x)), True), ('ej2', antider(-x*sp.cos(x) + sp.sin(x), x*sp.sin(x)), True),
        ('ej3', antider(x**2/2*sp.log(x) - x**2/4, x*sp.log(x)), True), ('ej4', antider(x*sp.atan(x) - sp.log(1 + x**2)/2, sp.atan(x)), True),
        ('ej5', antider(x*sp.tan(x) + sp.log(sp.cos(x)), x*sp.sec(x)**2), True),
        ('ej6', antider(x**2*sp.sin(x) + 2*x*sp.cos(x) - 2*sp.sin(x), x**2*sp.cos(x)), True),
        ('ej7', antider(sp.exp(x)*(x**3 - 3*x**2 + 6*x - 6), x**3*sp.exp(x)), True),
        ('ej8', antider(x*sp.log(x)**2 - 2*x*sp.log(x) + 2*x, sp.log(x)**2), True),
        ('ej9', antider(sp.exp(x)*(sp.sin(x) + sp.cos(x))/2, sp.exp(x)*sp.cos(x)), True),
        ('ej10', antider(sp.exp(2*x)*(2*sp.sin(x) - sp.cos(x))/5, sp.exp(2*x)*sp.sin(x)), True),
        ('ej11', Idef(x*sp.exp(x), 0, 1), 1), ('ej12', Idef(sp.log(x), 1, sp.E), 1),
        ('ej13', (Idef(x*sp.cos(x), 0, sp.pi/2), round(math.pi/2 - 1, 3)), (sp.pi/2 - 1, 0.571)),
        ('ej14', (Idef(sp.log(x), 1, sp.E)/(sp.E - 1), round(1/(math.e - 1), 3)), (1/(sp.E - 1), 0.582)),
    ]

@guia('PM26 Fracciones parciales')
def _():
    ap = sp.apart
    return [
        ('ejemplo1', ap((5*x - 1)/(x**2 - 1)), 2/(x - 1) + 3/(x + 1)), ('ejemplo2', ap(1/(x**2 - 4)), 1/(4*(x - 2)) - 1/(4*(x + 2))),
        ('nota', antider(sp.log(x**2 - 1), 2*x/(x**2 - 1)), True),
        ('ejemplo3', ap((x + 3)/(x - 1)**2), 1/(x - 1) + 4/(x - 1)**2), ('ejemplo3b', antider(-4/(x - 1), 4/(x - 1)**2), True),
        ('ejemplo4', ap(1/(x*(x**2 + 1))), 1/x - x/(x**2 + 1)), ('ejemplo5', ap((x**2 + 1)/(x**2 - 1)), 1 + 1/(x - 1) - 1/(x + 1)),
        ('ej1', ap(1/(x*(x + 2))), 1/(2*x) - 1/(2*(x + 2))), ('ej2', ap((3*x + 5)/((x + 1)*(x + 3))), 1/(x + 1) + 2/(x + 3)),
        ('ej3', ap((x + 7)/(x**2 - x - 6)), 2/(x - 3) - 1/(x + 2)), ('ej4', ap(2*x/(x**2 - 1)), 1/(x - 1) + 1/(x + 1)),
        ('ej5', ap((2*x + 1)/(x + 1)**2), 2/(x + 1) - 1/(x + 1)**2), ('ej5b', antider(2*sp.log(x + 1) + 1/(x + 1), (2*x + 1)/(x + 1)**2), True),
        ('ej6', ap(1/(x**2*(x - 1))), -1/x - 1/x**2 + 1/(x - 1)), ('ej6b', antider(-sp.log(x) + 1/x + sp.log(x - 1), 1/(x**2*(x - 1))), True),
        ('ej7', antider(sp.log(x**2 + 1) + 3*sp.atan(x), (2*x + 3)/(x**2 + 1)), True),
        ('ej8', ap((x**2 + 2)/(x*(x**2 + 1))), 2/x - x/(x**2 + 1)),
        ('ej9', ap(x**2/(x + 1)), x - 1 + 1/(x + 1)), ('ej9b', antider(x**2/2 - x + sp.log(x + 1), x**2/(x + 1)), True),
        ('ej10', (sp.nsimplify(Idef(1/(x**2 - 1), 2, 3) - sp.log(sp.Rational(3, 2))/2), round(math.log(1.5)/2, 3)), (0, 0.203)),
        ('ej11', (sp.simplify(Idef(1/((x + 1)*(x + 2)), 0, 1) - sp.log(sp.Rational(4, 3))), round(math.log(4/3), 3)), (0, 0.288)),
    ]

@guia('PM27 Áreas entre curvas')
def _():
    return [
        ('ejemplo1', (sp.solve(x**2 - x - 2, x), Idef(x + 2 - x**2, -1, 2)), ([-1, 2], sp.Rational(9, 2))),
        ('ejemplo1b', ((x**2/2 + 2*x - x**3/3).subs(x, 2), (x**2/2 + 2*x - x**3/3).subs(x, -1)), (sp.Rational(10, 3), -sp.Rational(7, 6))),
        ('ejemplo2', (Idef(sp.Abs(sp.cos(x) - sp.sin(x)), 0, sp.pi/2).evalf(), round(2*(math.sqrt(2) - 1), 3)), (2*(math.sqrt(2) - 1), 0.828)),
        ('ejemplo3', (Idef(sp.Abs(x - x**3), -1, 1), Idef(x - x**3, -1, 1)), (sp.Rational(1, 2), 0)),
        ('ejemplo4', Idef(y + 2 - y**2, -1, 2, y), sp.Rational(9, 2)),
        ('ej1', Idef(4 - x**2, -2, 2), sp.Rational(32, 3)), ('ej2', Idef(2*x - x**2, 0, 2), sp.Rational(4, 3)),
        ('ej3', (sp.solve(x**2 + x - 6, x), Idef(6 - x**2 - x, -3, 2)), ([-3, 2], sp.Rational(125, 6))),
        ('ej4', Idef(sp.sqrt(x) - x, 0, 1), sp.Rational(1, 6)), ('ej5', (Idef(sp.exp(x) - x, 0, 1), round(math.e - 1.5, 3)), (sp.E - sp.Rational(3, 2), 1.218)),
        ('ej6', Idef(sp.Abs(sp.sin(x)), 0, 2*sp.pi), 4), ('ej7', (Idef(4 - x**2, 0, 2) + Idef(x**2 - 4, 2, 3), Idef(4 - x**2, 0, 2), Idef(x**2 - 4, 2, 3)), (sp.Rational(23, 3), sp.Rational(16, 3), sp.Rational(7, 3))),
        ('ej8', Idef(4 - y**2, -2, 2, y), sp.Rational(32, 3)), ('ej9', Idef((1 - y**2) - (y**2 - 1), -1, 1, y), sp.Rational(8, 3)),
        ('ej10', Idef(2*t - t**2, 0, 2, t), sp.Rational(4, 3)),
    ]

@guia('PM28 Volúmenes de revolución')
def _():
    pi = sp.pi
    r_, h_ = sp.symbols('r h', positive=True)
    return [
        ('ejemplo1', pi*Idef(x, 0, 4), 8*pi), ('cono', sp.simplify(pi*Idef((r_/h_*x)**2, 0, h_)), pi*r_**2*h_/3),
        ('esfera', sp.simplify(pi*Idef(r_**2 - x**2, -r_, r_)), sp.Rational(4, 3)*pi*r_**3),
        ('ejemplo3', pi*Idef(x**2 - x**4, 0, 1), 2*pi/15), ('ejemplo4', 2*pi*Idef(x*(x - x**2), 0, 1), pi/6),
        ('ejemplo5', pi*Idef(y, 0, 4, y), 8*pi),
        ('ej1', pi*Idef(x**2, 0, 3), 9*pi), ('ej2', pi*Idef(x**4, 0, 2), 32*pi/5),
        ('ej3', (pi*Idef(sp.exp(2*x), 0, 1), round(math.pi/2*(math.e**2 - 1), 2)), (pi*(sp.E**2 - 1)/2, 10.04)),
        ('ej4', pi*Idef(x**-2, 1, 3), 2*pi/3), ('ej5', pi*Idef(x - x**2, 0, 1), pi/6), ('ej6', pi*Idef(16 - x**4, -2, 2), 256*pi/5),
        ('ej7', 2*pi*Idef(x**3, 0, 2), 8*pi), ('ej8', 2*pi*Idef(x*(4 - x**2), 0, 2), 8*pi), ('ej9', 2*pi*Idef(x**2 - x**3, 0, 1), pi/6),
        ('ej10', pi*Idef(9 - x**2, -3, 3), 36*pi), ('ej11', (pi*Idef(4*y, 0, 4, y), round(32*math.pi, 1)), (32*pi, 100.5)),
    ]

from math import comb as C_
from statistics import NormalDist
PHI = NormalDist().cdf

@guia('PM29 Estadística descriptiva')
def _():
    import statistics as st
    cal = [6, 7, 7, 8, 8, 8, 8, 9, 9, 10]
    A = [3, 5, 5, 6, 7, 8, 8, 8, 10]
    Cd = [11, 12, 13, 14, 15, 15, 18, 20]
    ss = lambda d: sum((F(v) - F(sum(d), len(d)))**2 for v in d)
    return [
        ('ejemplo1', ([round(f/30, 3) for f in (5, 12, 8, 5)], [5, 17, 25, 30]), ([0.167, 0.4, 0.267, 0.167], [5, 17, 25, 30])),
        ('ejemplo2', (F(sum(cal), 10), st.median(cal), st.mode(cal)), (8, 8.0, 8)),
        ('ejemplo2b', (F(5*5 + 15*12 + 25*8 + 35*5, 30), round(580/30, 1)), (F(580, 30), 19.3)),
        ('sueldos', (F(8 + 9 + 10 + 11 + 62, 5), st.median([8, 9, 10, 11, 62])), (20, 10)),
        ('ejemplo3', (ss(cal), ss(cal)/10, round(st.pstdev(cal), 2), round(float(ss(cal)/9), 2), round(st.stdev(cal), 2)), (12, F(6, 5), 1.10, 1.33, 1.15)),
        ('ejemplo4', (st.median(sorted(cal)[:5]), st.median(sorted(cal)[5:])), (7, 9)),
        ('ejemplo5', F(82 - 70, 8), F(3, 2)),
        ('ej1', F(sum(A), 9), F(20, 3)), ('ej2', st.median(A), 7), ('ej3', st.mode(A), 8), ('ej4', max(A) - min(A), 7),
        ('ej5', (ss(A), ss(A)/9, st.pstdev(A)), (36, 4, 2.0)), ('ej6', (ss(A)/8, round(st.stdev(A), 2)), (F(9, 2), 2.12)),
        ('ej7', (st.median(A[:4]), st.median(A[5:])), (5.0, 8.0)),
        ('ej8', F(10, 30), F(1, 3)), ('ej9', 4 + 10, 14), ('ej10', (F(5*4 + 15*10 + 25*11 + 35*5, 30), round(620/30, 2)), (F(62, 3), 20.67)),
        ('ej11', (st.mean(Cd), st.median(Cd), ss(Cd), round(st.stdev(Cd), 2)), (14.75, 14.5, F(127, 2), 3.01)),
        ('ej12', F(176 - 160, 8), 2), ('ej13', (F(85 - 75, 5), F(90 - 80, 10)), (2, 1)),
    ]

@guia('PM30 Técnicas de conteo')
def _():
    fact = math.factorial
    P_ = math.perm
    return [
        ('ejemplo1', 26**3 * 10**3, 17576000), ('ejemplo2', P_(8, 3), 336), ('ejemplo3', fact(6) // (fact(3)*fact(2)), 60),
        ('ejemplo4', C_(6, 2)*C_(5, 3), 150), ('ejemplo5', C_(4, 2)*2**2, 24), ('ejemplo6', F(C_(5, 2), C_(8, 2)), F(5, 14)),
        ('comite', C_(10, 3), 120), ('pascal', [C_(4, k) for k in range(5)], [1, 4, 6, 4, 1]),
        ('ej1', 3*4*2, 24), ('ej2', (10**4, P_(10, 4)), (10000, 5040)), ('ej3', fact(6), 720), ('ej4', P_(12, 3), 1320),
        ('ej5', fact(10) // (fact(2)*fact(3)*fact(2)), 151200), ('ej5b', sorted('MATEMATICA'), sorted('AAACEIMMTT')),
        ('ej6', fact(4), 24), ('ej7', C_(12, 5), 792), ('ej8', (C_(10, 8), C_(7, 5)), (45, 21)),
        ('ej9', C_(5, 2)*C_(7, 2), 210), ('ej10', (C_(12, 4) - C_(7, 4), sum(C_(5, k)*C_(7, 4 - k) for k in range(1, 5))), (460, 460)),
        ('ej11', C_(6, 2) - 6, 9), ('ej12', sp.Poly(sp.expand((2*x - 1)**5), x).coeff_monomial(x**3), 80),
        ('ej13', C_(56, 6), 32468436), ('ej14', F(C_(4, 2), C_(52, 2)), F(1, 221)),
    ]

@guia('PM31 Probabilidad condicional')
def _():
    dados = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    Pd = lambda cond: F(sum(1 for d in dados if cond(d)), 36)
    return [
        ('ejemplo1', F(3, 6) + F(2, 6) - F(1, 6), F(2, 3)),
        ('ejemplo2', (F(140, 200), F(90, 120), round(90/140, 3)), (F(7, 10), F(3, 4), 0.643)),
        ('ejemplo3', F(4, 52)*F(3, 51), F(1, 221)),
        ('ejemplo4', (0.6*0.02 + 0.4*0.05, round(0.012/0.032, 3)), (0.032, 0.375)),
        ('ejemplo5', (round(0.01*0.95 + 0.99*0.05, 4), round(0.0095/0.059, 3)), (0.059, 0.161)),
        ('ej1', Pd(lambda d: sum(d) == 7), F(1, 6)), ('ej2', Pd(lambda d: sum(d) >= 10), F(1, 6)), ('ej3', Pd(lambda d: 6 in d), F(11, 36)),
        ('ej4', (0.5 + 0.4 - 0.2, 0.5*0.4), (0.7, 0.2)),
        ('ej5', F(150, 250), F(3, 5)), ('ej6', F(70, 130), F(7, 13)), ('ej7', F(60, 100), F(3, 5)), ('ej8', F(80, 120) == F(150, 250), False),
        ('ej9', F(6, 10)*F(5, 9), F(1, 3)), ('ej10', 2*F(4, 10)*F(6, 9), F(8, 15)), ('ej11', F(6, 10)**2, F(9, 25)), ('ej12', 1 - F(1, 8), F(7, 8)),
        ('ej13', (F(3, 10)*F(1, 10) + F(7, 10)*F(2, 10), F(3, 100) / F(17, 100)), (F(17, 100), F(3, 17))),
        ('ej14', (round(0.02*0.9 + 0.98*0.03, 4), round(0.018/0.0474, 3)), (0.0474, 0.380)),
    ]

@guia('PM32 Distribución binomial y normal')
def _():
    b = lambda n, k, p: C_(n, k) * p**k * (1 - p)**(n - k)
    tabla = [round(PHI(z), 4) for z in (0, 0.5, 0.75, 1, 1.25, 1.43, 1.5, 1.645, 1.96, 2, 2.5, 3)]
    return [
        ('tabla', tabla, [0.5, 0.6915, 0.7734, 0.8413, 0.8944, 0.9236, 0.9332, 0.95, 0.975, 0.9772, 0.9938, 0.9987]),
        ('ejemplo1', 100*F(1, 10) - 20*F(9, 10), -8),
        ('ejemplo2', (round(b(5, 3, 0.25), 4), round(1 - 0.75**5, 3), 5*0.25, round(math.sqrt(5*0.25*0.75), 2)), (0.0879, 0.763, 1.25, 0.97)),
        ('regla', (round(PHI(1) - PHI(-1), 2), round(PHI(2) - PHI(-2), 2), round(PHI(3) - PHI(-3), 3)), (0.68, 0.95, 0.997)),
        ('ejemplo3', (165 - 7, 165 + 7, (179 - 165)/7), (158, 172, 2.0)),
        ('ejemplo4', (round((175 - 165)/7, 2), round(165 + 1.645*7, 1), round(NormalDist().inv_cdf(0.95), 3)), (1.43, 176.5, 1.645)),
        ('ej1', F(5000, 200) - 50, -25), ('ej2', 0*0.1 + 1*0.3 + 2*0.4 + 3*0.2, 1.7),
        ('ej3', F(C_(6, 4), 2**6), F(15, 64)), ('ej4', round(0.9**8, 3), 0.430), ('ej5', round(b(8, 0, 0.1) + b(8, 1, 0.1), 3), 0.813),
        ('ej6', (8*0.1, round(math.sqrt(8*0.1*0.9), 2)), (0.8, 0.85)), ('ej7', round(b(5, 4, 0.7) + b(5, 5, 0.7), 3), 0.528),
        ('ej10', round(1 - 0.9332, 4), 0.0668), ('ej11', round(1 - 0.8944, 4), 0.1056), ('ej12', round(0.9332 - (1 - 0.7734), 4), 0.7066),
        ('ej10-12 exactos', (round(1 - PHI(1.5), 4), round(PHI(-1.25), 4), round(PHI(1.5) - PHI(-0.75), 4)), (0.0668, 0.1056, 0.7066)),
        ('ej13', round(500 + 1.645*100, 1), 664.5), ('ej14', (F(592 - 600, 4), round(PHI(-2), 4)), (-2, 0.0228)),
    ]

# ---------------- Preparatoria · Física ----------------
R_ = lambda v, n=2: round(v, n)
rad = math.radians
deg = math.degrees
def polar(xc, yc):
    ang = deg(math.atan2(yc, xc))
    return math.hypot(xc, yc), ang
def cuad(a_, b_, c_):
    """Raíz positiva mayor de a t^2 + b t + c = 0."""
    return (-b_ + math.sqrt(b_*b_ - 4*a_*c_)) / (2*a_)

@guia('PF01 Vectores')
def _():
    ax, ay = 10*math.cos(rad(30)), 10*math.sin(rad(30))
    bx, by = 15*math.cos(rad(120)), 15*math.sin(rad(120))
    Rm, Ra = polar(ax + bx, ay + by)
    return [
        ('ejemplo1', (R_(50*math.cos(rad(30))), R_(50*math.sin(rad(30)))), (43.30, 25.0)),
        ('cuadrante', (R_(deg(math.atan(8/-6))), R_(polar(-6, 8)[1])), (-53.13, 126.87)),
        ('ejemplo2', (R_(ax), R_(ay), R_(bx), R_(by), R_(ax + bx), R_(ay + by), R_(Rm), R_(Ra, 1), R_(math.hypot(10, 15))), (8.66, 5.0, -7.5, 12.99, 1.16, 17.99, 18.03, 86.3, 18.03)),
        ('unitario', math.hypot(3, 4), 5.0), ('ejemplo3', (R_(5/math.sqrt(50), 3), R_(deg(math.acos(5/math.sqrt(50))))), (0.707, 45.0)),
        ('ejemplo4', (R_(math.hypot(200, 50), 1), R_(deg(math.atan(50/200)), 1)), (206.2, 14.0)),
        ('ej1', (R_(20*math.cos(rad(60))), R_(20*math.sin(rad(60)))), (10.0, 17.32)),
        ('ej2', (R_(12*math.cos(rad(210))), R_(12*math.sin(rad(210)))), (-10.39, -6.0)),
        ('ej3', tuple(R_(v) for v in polar(-6, 8)), (10.0, 126.87)), ('ej4', tuple(R_(v) for v in polar(5, -12)), (13.0, -67.38)),
        ('ej5', ((6, 4), R_(math.hypot(6, 4)), (-2, 6)), ((2 + 4, 5 - 1), 7.21, (2 - 4, 5 + 1))),
        ('ej6', (3*2 - 2*4, 3*5 - 2*(-1)), (-2, 17)), ('ej7', tuple(R_(v) for v in polar(300, 400)), (500.0, 53.13)),
        ('ej8', tuple(R_(v) for v in polar(60 - 50, 80)), (80.62, 82.87)),
        ('ej9', tuple(R_(v, 1) for v in polar(100*math.cos(rad(45)) + 100*math.cos(rad(135)), 200*math.sin(rad(45)))), (141.4, 90.0)),
        ('ej10', (math.hypot(4, 3), 80/4, 3*80/4), (5.0, 20.0, 60.0)), ('ej11', 3*4 + 4*(-3), 0),
        ('ej12', R_(deg(math.acos(2/(2*2)))), 60.0),
    ]

@guia('PF02 Cinemática en una dimensión')
def _():
    t = cuad(4.9, -15, -20)
    return [
        ('ejemplo1', (-900/120, -30/-7.5), (-7.5, 4.0)),
        ('ejemplo2', (R_(t), 225 + 2*9.8*20, R_(math.sqrt(617), 1)), (4.07, 617.0, 24.8)),
        ('ejemplo3', (0.5*2*2 + 2*6 + 0.5*2*2, 2/2, -2/2), (16.0, 1.0, -1.0)),
        ('ejemplo4', (sp.solve(sp.Eq(sp.Rational(3, 2)*sp.Symbol('T')**2, 30*sp.Symbol('T')), sp.Symbol('T')), 30*20, 3*20), ([0, 20], 600, 60)),
        ('ej1', (18/3, 18/3.6), (6.0, 5.0)), ('ej2', R_(100/3.6/8), 3.47), ('ej3', R_(100/3.6/2*8, 1), 111.1),
        ('ej4', (25/1.25, 25/2*20), (20.0, 250.0)), ('ej5', R_(math.sqrt(16 + 200)), 14.70),
        ('ej6', (R_(math.sqrt(90/9.8)), R_(math.sqrt(882), 1)), (3.03, 29.7)),
        ('ej7', (R_(29.4/9.8, 6), R_(29.4**2/19.6, 6), R_(2*29.4/9.8, 6)), (3.0, 44.1, 6.0)),
        ('ej8', (R_(cuad(4.9, 5, -30)), R_(math.sqrt(25 + 588), 1)), (2.02, 24.8)),
        ('ej9', (12/4, 0, -12/3, 0.5*4*12 + 6*12 + 0.5*3*12), (3.0, 0, -4.0, 114.0)),
        ('ej10', (150/(25 - 15), 25*15), (15.0, 375)), ('ej11', (300/150, 80*2), (2.0, 160)),
    ]

@guia('PF03 Tiro parabólico')
def _():
    vx = 20*math.cos(rad(30))
    t8 = cuad(4.9, -7.5, -20)
    return [
        ('ejemplo1', (R_(math.sqrt(2.5/9.8), 3), R_(3*math.sqrt(2.5/9.8))), (0.505, 1.52)),
        ('ejemplo2', (R_(vx), R_(20/9.8), R_(100/19.6), R_(vx*20/9.8, 1), R_(400*math.sin(rad(60))/9.8, 1)), (17.32, 2.04, 5.10, 35.3, 35.3)),
        ('ejemplo3', (R_(10 - 9.8*1.5, 1), R_(math.hypot(vx, 4.7), 1), R_(deg(math.atan(4.7/vx)), 1)), (-4.7, 17.9, 15.2)),
        ('ejemplo4', (math.hypot(12, 9), R_(cuad(4.9, -9, -10)), R_(12*cuad(4.9, -9, -10), 1)), (15.0, 2.62, 31.4)),
        ('ej1', (R_(math.sqrt(1000/9.8)), round(60*math.sqrt(1000/9.8))), (10.10, 606)),
        ('ej2', R_(1.2/math.sqrt(1.6/9.8)), 2.97),
        ('ej3', (R_(math.hypot(60, 9.8*math.sqrt(1000/9.8)), 1), R_(deg(math.atan(9.8*math.sqrt(1000/9.8)/60)), 1)), (115.8, 58.8)),
        ('ej4', (R_(40/9.8), R_(400/19.6, 1), R_(15*40/9.8, 1)), (4.08, 20.4, 61.2)),
        ('ej5', R_(900/9.8, 1), 91.8), ('ej6', R_(math.sin(rad(60)), 9) == R_(math.sin(rad(2*30)), 9) and R_(math.sin(rad(120)), 9) == R_(math.sin(rad(60)), 9), True),
        ('ej7', R_(20*math.sin(rad(45))*(20/(20*math.cos(rad(45)))) - 4.9*(20/(20*math.cos(rad(45))))**2, 6), 10.2),
        ('ej8', (R_(t8), R_(15*math.cos(rad(30))*t8, 1)), (2.93, 38.0)),
    ]

@guia('PF04 Movimiento circular')
def _():
    T = 365.25*86400
    v3 = 2*math.pi*1.5e11/T
    w7 = 6000*2*math.pi/60
    w8 = 3000*2*math.pi/60
    return [
        ('ejemplo1', (1200/60, 1/20, R_(2*math.pi*20, 1), R_(2*math.pi*20*0.25, 1)), (20.0, 0.05, 125.7, 31.4)),
        ('ejemplo2', (400/50, 1200*8, R_(400/490)), (8.0, 9600, 0.82)), ('ejemplo3', R_(math.sqrt(98), 1), 9.9),
        ('ejemplo4', (30/6, 0.5*5*36, R_(90/(2*math.pi), 1)), (5.0, 90.0, 14.3)),
        ('ej1', (R_(2*math.pi/40, 3), R_(2*math.pi/40*15), R_((2*math.pi/40)**2*15, 3)), (0.157, 2.36, 0.370)),
        ('ej2', (R_(45*2*math.pi/60), R_(60/45)), (4.71, 1.33)),
        ('ej3', (R_(v3/1e4), R_(v3**2/1.5e11*1e3)), (2.99, 5.95)),
        ('ej4', R_(0.2*(2*math.pi*0.8*3)**2/0.8, 1), 56.8), ('ej5', (R_(math.sqrt(392), 1), R_(math.sqrt(392)*3.6, 1)), (19.8, 71.3)),
        ('ej6', R_(math.sqrt(9.8)), 3.13), ('ej7', round(w7**2*0.1/9.8), 4028),
        ('ej8', (R_(w8/5, 1), round(0.5*(w8/5)*25/(2*math.pi))), (62.8, 125)),
    ]

@guia('PF05 Leyes de Newton')
def _():
    g = 9.8
    return [
        ('ejemplo1', (20*g, R_(0.3*196, 1), R_((100 - 58.8)/20)), (196.0, 58.8, 2.06)),
        ('ejemplo2', (R_(g*(0.5 - 0.2*math.cos(rad(30)))), g*0.5), (3.20, 4.9)),
        ('ejemplo3', (2*g/8, 3*(g + 2*g/8)), (2.45, 36.75)), ('ejemplo3b', (3*g, 5*g), (29.4, 49.0)),
        ('ejemplo4', (70*(g + 2), R_(826/g, 1)), (826.0, 84.3)), ('letrero', 5*g/(2*0.5), 49.0),
        ('ej1', 50/10, 5.0), ('ej2', (R_(0.4*15*g, 1), R_((60 - 0.3*15*g)/15)), (58.8, 1.06)),
        ('ej3', (5000/1000, 400/(2*5)), (5.0, 40.0)), ('ej4', (R_(g*0.6, 2), R_(5*g*0.8, 1)), (5.88, 39.2)),
        ('ej5', R_(math.tan(rad(25))), 0.47), ('ej6', (R_(2*g/6), R_(2*(g + 2*g/6), 1)), (3.27, 26.1)),
        ('ej7', (R_(2*g/6), R_(4*2*g/6, 1)), (3.27, 13.1)), ('ej8', R_(60*(g - 1.5), 6), 498.0),
        ('ej9', R_(20*g/(2*0.5), 6), 196.0),
    ]

@guia('PF06 Trabajo, energía y potencia')
def _():
    g = 9.8
    return [
        ('ejemplo1', round(50*10*math.cos(rad(30))), 433), ('ejemplo2', 0.5*1000*(400 - 100), 150000.0),
        ('ejemplo3', R_(math.sqrt(2*g*15), 1), 17.1), ('ejemplo4', (0.5*200*0.1**2, R_(math.sqrt(1/0.025))), (1.0, 6.32)),
        ('ejemplo5', (R_(0.2*2*g*5, 6), R_(math.sqrt(36 - 19.6))), (19.6, 4.05)), ('ejemplo6', R_(60*g*3/4, 6), 441.0),
        ('kwh', 1000*3600, 3.6e6),
        ('ej1', 200*15, 3000), ('ej2', R_(20*g*1.5, 6), 294.0), ('ej3', R_(80*5*math.cos(rad(60)), 6), 200.0),
        ('ej4', round(0.5*0.145*1600), 116), ('ej5', (0.5*1500*625, 0.5*1500*625/50), (468750.0, 9375.0)),
        ('ej6', R_(math.sqrt(2*g*30), 1), 24.2), ('ej7', R_(math.sqrt(2*g*0.8)), 3.96),
        ('ej8', (0.5*500*0.2**2, R_(10/(0.5*g))), (10.0, 2.04)), ('ej9', R_(70*g*40 - 0.5*70*400, 6), 13440.0),
        ('ej10', (R_(500*g*12/20, 6), R_(500*g*12/20/0.7, 6)), (2940.0, 4200.0)), ('ej11', 30000/25, 1200.0), ('ej12', 60*5*30/1000, 9.0),
    ]

@guia('PF07 Cantidad de movimiento y choques')
def _():
    g = 9.8
    V = math.sqrt(2*g*0.2)
    return [
        ('ejemplo1', (R_(0.15*(30 - (-20)), 6), R_(7.5/0.01, 6)), (7.5, 750.0)), ('ejemplo2', -0.01*400/4, -1.0),
        ('ejemplo3', (1200*20/2000, 0.5*1200*400, 0.5*2000*144, (240000 - 144000)/240000), (12.0, 240000.0, 144000.0, 0.4)),
        ('ejemplo4', (R_(V), round(2.02*V/0.02)), (1.98, 200)),
        ('ej1', 5000*15, 75000), ('ej2', 200*0.05, 10.0), ('ej3', R_(0.4*25/0.008, 6), 1250.0),
        ('ej4', (R_(0.06*5/0.002, 6), R_(0.06*5/0.1, 6)), (150.0, 3.0)), ('ej5', -50*2.1/70, -1.5),
        ('ej6', (30000/15000, 0.5*10000*9 - 0.5*15000*4), (2.0, 15000.0)),
        ('ej7', ((1 - 1)/2*5, 2*1/2*5), (0.0, 5.0)), ('ej8', ((1 - 2)/3*6, 2*1/3*6), (-2.0, 4.0)),
        ('ej8b', (1*6, 1*(-2) + 2*4, 0.5*36, 0.5*4 + 0.5*2*16), (6, 6, 18.0, 18.0)),
        ('ej9', (0.01*300/1.5, R_(4/19.6)), (2.0, 0.20)),
        ('ej10', tuple(R_(v) for v in polar(20000/3000, 20000/3000)), (9.43, 45.0)),
    ]

@guia('PF08 Gravitación universal')
def _():
    G, M, Rt = 6.674e-11, 5.97e24, 6.371e6
    GM = G*M
    r6 = 7.371e6
    return [
        ('personas', R_(G*70*70*1e7, 1), 3.3), ('ejemplo1', (R_(GM/Rt**2), R_(GM/6.771e6**2), round(GM/6.771e6**2/(GM/Rt**2)*100)), (9.82, 8.69, 89)),
        ('ejemplo2', (round(math.sqrt(GM/6.771e6), -1), round(2*math.pi*6.771e6/math.sqrt(GM/6.771e6)/60)), (7670.0, 92)),
        ('GM', R_(GM/1e14), 3.98),
        ('ejemplo3', (R_((GM*86164**2/(4*math.pi**2))**(1/3)/1e7), round(((GM*86164**2/(4*math.pi**2))**(1/3) - Rt)/1e5)*100), (4.22, 35800)),
        ('escape', (R_(math.sqrt(2*GM/Rt)/1000, 1), R_(math.sqrt(2*GM/Rt)/math.sqrt(GM/Rt), 4)), (11.2, R_(math.sqrt(2), 4))),
        ('ej1', R_(G*M*7.35e22/(3.84e8)**2/1e20), 1.99), ('ej2', F(1, 3**2), F(1, 9)),
        ('ej3', R_(G*6.42e23/(3.39e6)**2), 3.73), ('ej4', round((math.sqrt(2) - 1)*6371, -1), 2640.0), ('ej5', R_(60*1.62, 6), 97.2),
        ('ej6', (round(math.sqrt(GM/r6), -1), round(2*math.pi*r6/math.sqrt(GM/r6)/60)), (7350.0, 105)),
        ('ej7', R_(1.524**1.5), 1.88), ('ej8', R_(4*math.pi**2*(1.496e11)**3/(G*(3.156e7)**2)/1e30), 1.99),
        ('ej9', R_(math.sqrt(2*G*7.35e22/1.737e6)/1000), 2.38),
    ]

@guia('PF09 Densidad y presión hidrostática')
def _():
    g = 9.8
    return [
        ('ejemplo1', 337.5/5**3, 2.7), ('ejemplo2', (round(60*g/1e-4), round(60*g/0.02)), (5880000, 29400)),
        ('ejemplo3', (round(1025*g*10), round(101325 + 1025*g*10, -3)), (100450, 202000.0)),
        ('ejemplo4', R_(800*12/1000, 6), 9.6), ('barometro', round(13600*g*0.76, -2), 101300.0),
        ('ej1', 540/200, 2.7), ('ej2', R_(920*0.002, 6), 1.84), ('ej3', R_(1/19300*1e6, 1), 51.8), ('ej3b', R_((1/19300)**(1/3)*100, 1), 3.7),
        ('ej4', 1.2*5000, 6000.0), ('ej5', round(5000*g/0.4), 122500), ('ej5b', round(5.88e6/122500), 48),
        ('ej6', (round(1000*g*3), R_((101325 + 1000*g*3)/1000, 1)), (29400, 130.7)), ('ej7', R_(2*101325/(1000*g), 1), 20.7),
        ('ej8', round(1000*g*40), 392000), ('ej9', R_(1000*20/13600), 1.47), ('ej10', R_(101325/(1000*g), 1), 10.3),
    ]

@guia('PF10 Pascal y Arquímedes')
def _():
    g = 9.8
    return [
        ('ejemplo1', (R_(1500*g/100, 6), 100*1), (147.0, 100)), ('ejemplo2', R_(1000*g*0.002, 6), 19.6),
        ('ejemplo3', R_(917/1025, 3), 0.895),
        ('ejemplo4', (R_(20/(1000*g)*1000), round((50/g)/(20/(1000*g))), 50/20), (2.04, 2500, 2.5)),
        ('ej1', 200*500/10, 10000.0), ('ej2', R_(2000*g/(15/3)**2, 6), 784.0), ('ej3', 50/(15/3)**2, 2.0),
        ('ej4', R_(1000*g*0.07, 6), 686.0), ('ej5', 600/1000, 0.6),
        ('ej6', (R_(7870*g*0.001, 1), R_(1000*g*0.001, 6), R_(7870*g*0.001 - 9.8, 1)), (77.1, 9.8, 67.3)),
        ('ej7', round(5e6/1025), 4878), ('ej8', (R_(7.84 - 6.86, 6), round((7.84/g)/((7.84 - 6.86)/(1000*g)))), (0.98, 8000)),
        ('ej9', 1000*2 - 500*2, 1000),
    ]

@guia('PF11 Continuidad y Bernoulli')
def _():
    g = 9.8
    Q = math.pi*0.01**2*1.5
    return [
        ('ejemplo1', (R_(Q*1e4), round(0.020/Q), 1.5*(2/0.5)**2), (4.71, 42, 24.0)),
        ('ejemplo2', (2*2, 150000 - 0.5*1000*(16 - 4)), (4, 144000.0)), ('ejemplo3', R_(math.sqrt(2*g*5), 1), 9.9),
        ('ejemplo4', R_(300000 - 1000*g*10, 6), 202000.0),
        ('ej1', (10/25, 10e-3/25), (0.4, 4e-4)), ('ej2', R_(4e-4/(math.pi*0.02**2)), 0.32), ('ej3', 1/(0.5**2), 4.0),
        ('ej4', R_(20*2*0.5/(10*1.5)), 1.33), ('ej5', R_(math.sqrt(2*g*1.25)), 4.95),
        ('ej6', R_(math.sqrt(2*g*3.2)*math.sqrt(2*1.25/g), 1), 4.0),
        ('ej7', (3*(6/3)**2, 200000 - 500*(144 - 9)), (12.0, 132500)), ('ej8', R_(350000 - 1000*g*8, 6), 271600.0),
        ('ej9', (R_(0.5*1.2*900, 6), R_(0.5*1.2*900*100, 6)), (540.0, 54000.0)),
    ]

@guia('PF12 Temperatura y dilatación')
def _():
    CtoF = lambda c: F(9, 5)*c + 32
    FtoC = lambda f: F(5, 9)*(f - 32)
    return [
        ('tabla', (CtoF(0), CtoF(100), CtoF(F('-273.15'))), (32, 212, F('-459.67'))),
        ('ejemplo1', (FtoC(F('98.6')), F(37) + F('273.15')), (37, F('310.15'))),
        ('ejemplo2', R_(1.2e-5*12*50*1000, 6), 7.2),
        ('ejemplo3', (R_(60*9.5e-4*25), R_(60*3*1.2e-5*25, 3), R_(60*9.5e-4*25 - 60*3.6e-5*25)), (1.43, 0.054, 1.37)),
        ('ej1', CtoF(25), 77), ('ej2', R_(float(FtoC(-10)), 1), -23.3), ('ej3', R_(300 - 273.15, 6), 26.85),
        ('ej4', sp.solve(sp.Eq(x, sp.Rational(9, 5)*x + 32), x), [-40]),
        ('ej5', R_(1.2e-5*500*50, 6), 0.3), ('ej6', R_(2.4e-5*2*100*1000, 6), 4.8),
        ('ej7', (round(0.01/(1.9e-5*5)), round(20 + 0.01/(1.9e-5*5))), (105, 125)),
        ('ej8', R_(2*1.7e-5*1*100*1e4, 6), 34.0), ('ej9', R_(1.8e-4*1000*50, 6), 9.0),
    ]

@guia('PF13 Calorimetría')
def _():
    c = 4186
    return [
        ('ejemplo1', 2*c*80, 669760), ('ejemplo2', (0.2*80 + 0.3*20)/0.5, 44.0),
        ('ejemplo3', R_((225*200 + c*20)/(225 + c), 1), 29.2),
        ('latentes', (round(2.26e6/3.34e5, 1), round(2.26e6/(c*100), 1)), (6.8, 5.4)),
        ('ejemplo4', (1*2100*10, 334000, c*20, 21000 + 334000 + c*20), (21000, 334000, 83720, 438720)),
        ('ej1', 0.5*c*80, 167440.0), ('ej2', R_(1000/(0.1*900), 1), 11.1), ('ej3', (1*90 + 2*15)/3, 40.0),
        ('ej4', (round(0.5*c*3/(0.2*77)), 0.5*c*3), (408, 6279.0)), ('ej5', 0.2*334000, 66800.0), ('ej6', 0.5*2.26e6, 1.13e6),
        ('ej7', (0.2*2100*5, 0.2*334000, 0.2*c*100, 0.2*2.26e6, 0.2*2100*5 + 0.2*334000 + 0.2*c*100 + 0.2*2.26e6), (2100.0, 66800.0, 83720.0, 452000.0, 604620.0)),
        ('ej8', (0.2*c*40 > 0.05*334000, R_(0.2*c*40, 6), R_(0.05*334000, 6), R_((0.2*c*40 - 0.05*334000)/(0.05*c + 0.2*c), 1), R_(0.05*c + 0.2*c, 6)), (True, 33488.0, 16700.0, 16.0, 1046.5)),
        ('ej9', 250*1000*4.186, 1046500.0),
    ]

@guia('PF14 Leyes de la termodinámica')
def _():
    Rg = 8.314
    return [
        ('ejemplo1', (round(2*Rg*300/0.05, -2), R_(2*Rg*300/0.05/101325)), (99800.0, 0.98)),
        ('ejemplo2', (2e5*(0.030 - 0.010), 10000 - 4000), (4000.0, 6000)),
        ('ejemplo3', ((2000 - 1500)/2000, 1 - 300/500), (0.25, 0.4)),
        ('ej1', (R_(101325/(Rg*273.15), 1), R_(Rg*273.15/101325*1000, 1)), (44.6, 22.4)), ('ej2', 2*450/300, 3.0),
        ('ej3', R_(1.5e5*3e-3, 6), 450.0), ('ej4', 800 - 300, 500), ('ej5', -50 - (-200), 150), ('ej6', 1200 - 0, 1200),
        ('ej7', 0 - 400, -400), ('ej8', (R_(600/0.3, 6), R_(600/0.3 - 600, 6)), (2000.0, 1400.0)),
        ('ej9', 1 - 300/800, 0.625), ('ej10', 1 - 300/600 < 0.6, True), ('ej11', (300/100, 300 + 100), (3.0, 400)),
        ('carnot-C', R_(1 - 27/227, 3) != R_(1 - 300/500, 3), True),
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
