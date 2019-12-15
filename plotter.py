import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy
from decimal import Decimal
import sys
from numpy import sin, cos, tan, log, sqrt


def make_data(function):
    e = numpy.e
    if 'e' in function:
        x = numpy.arange(-1, 1, 0.1)
        y = numpy.arange(-1, 1, 0.1)
    else:
        x = numpy.arange(-50, 50, 0.1)
        y = numpy.arange(-50, 50, 0.1)
    xgrid, ygrid = numpy.meshgrid(x, y)
    function = function.replace('^', '**').replace('x1', 'xgrid').replace('x2', 'ygrid').replace('ln', 'log')
    zgrid = eval(function)
    return xgrid, ygrid, zgrid


def plot(function):
    x, y, z = make_data(function)
    fig = pylab.figure()
    axes = Axes3D(fig)
    axes.plot_surface(x, y, z, cmap=cm.hot)
    pylab.show()
