from numpy import sin, cos, tan, log, sqrt, abs, e
from scipy import optimize
from sympy import *
from decimal import Decimal


def find_min(function, x1_start, x2_start, Eps=0.001):
    f = function.replace('^', '**').replace('ln', 'log')
    x1 = Symbol('x1')
    x2 = Symbol('x2')
    dx1 = diff(eval(f), x1)
    dx2 = diff(eval(f), x2)
    x1 = x1_start
    x2 = x2_start
    k = 0
    while sqrt(eval(dx1.__str__()) ** 2 + eval(dx2.__str__()) ** 2) > Eps:
        l = Symbol('l')
        x1 = x1 - l * eval(dx1.__str__())
        x2 = x2 - l * eval(dx2.__str__())
        res = optimize.minimize_scalar(lambdify(l, eval(f)))
        x1 = x1.evalf(subs={l: res.x})
        x2 = x2.evalf(subs={l: res.x})
        k += 1
    return x1, x2, eval(f)
