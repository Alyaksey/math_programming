from numpy import sin, cos, tan, log, sqrt, abs
from scipy import optimize
from sympy import *


def find_min(function, x1_start, x2_start, Eps=0.001):
    switcher = True
    x1_const = x1_start
    x2_const = x2_start
    x1_old = x1_start
    x2_old = x2_start
    function = function.replace('^', '**').replace('ln', 'log')
    k = 0
    while True:
        if switcher:
            x1 = Symbol('x1')
            x2 = x2_const
            res = optimize.minimize_scalar(lambdify(x1, eval(function)))
            x1_const = res.x
            switcher = False
            k += 1
        else:
            x2 = Symbol('x2')
            x1 = x1_const
            res = optimize.minimize_scalar(lambdify(x2, eval(function)))
            x2_const = res.x
            switcher = True
            k += 1
        if k % 2 == 0:
            if sqrt((x1_const - x1_old) ** 2 + (x2_const - x2_old) ** 2) < Eps:
                break
            else:
                x1_old = x1_const
                x2_old = x2_const
    x1 = x1_const
    x2 = x2_const
    return round(x1, 5), round(x2, 5), round(eval(function), 5)


print(find_min('4*x1^2+4*x1*x2+6*x2^2-17*x1', 0, 0))
