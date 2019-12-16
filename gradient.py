from numpy import sin, cos, tan, log, sqrt, abs
from scipy import optimize
from sympy import *

f = '4*x1^2+4*x1*x2+6*x2^2-17*x1'.replace('^', '**').replace('ln', 'log')


def find_min(x1_start, x2_start, Eps=0.001):
    x1 = Symbol('x1')
    x2 = Symbol('x2')
    dx1 = diff(eval(f), x1)
    dx2 = diff(eval(f), x2)
    x1 = x1_start
    x2 = x2_start
    while sqrt(eval(dx1.__str__()) ** 2 + eval(dx2.__str__()) ** 2) > Eps:
        l = Symbol('l')
        x1 = x1 - l * eval(dx1.__str__())
        x2= x2 - l * eval(dx2.__str__())
        res = optimize.minimize_scalar(lambdify(l, eval(f)))
        x1 = x1.evalf(subs={l: res.x})
        x2 = x2.evalf(subs={l: res.x})
    return round(x1, 5), round(x2, 5), round(eval(f), 5)


print(find_min(-1,1))
