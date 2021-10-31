from .biteopt import _minimize
import numpy as np

class OptimizeResult(dict):
    r""" Represents the optimization result.

    Attributes
    ----------
    x : ndarray
        The solution of the optimization.
    fun : float
        Value of the objective function.
    nfev : int
        Number of evaluations of the objective function.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in self.items()])
        else:
            return self.__class__.__name__ + "()"

def biteopt(fun, bounds, args=(), iters = 1000, depth = 1, attempts = 10):
    '''
    Optimization via the biteopt algorithm

    Parameters
    ----------
    fun : callable 
        The objective function to be minimized. Must be in the form ``fun(x, *args)``, where ``x`` 
        is the argument in the form of a 1-D array and args is a tuple of any additional fixed 
        parameters needed to completely specify the function.
    bounds : array-like
        Bounds for variables. ``(min, max)`` pairs for each element in ``x``,
        defining the finite lower and upper bounds for the optimizing argument of ``fun``. 
        It is required to have ``len(bounds) == len(x)``.
    args : tuple, optional, default ()
        Further arguments to describe the objective function
    iters : int, optional, default 1000
        Number of function evaluations allowed in one attempt
    depth : int, optional, default 1
        Depth of evolutionary algorithm. Required to be ``<36``. 
        Multiplies allowed number of function evaluations by :math:`\sqrt{depth}`.
        Setting depth to a higher value increases the chance for convergence for high-dimensional problems.
    attempts : int, optional, default 10
        Number of individual optimization attemps
    '''
    lower_bounds = [bound[0] for bound in bounds]
    upper_bounds = [bound[1] for bound in bounds]

    def wrapped_fun(x):
    #
        return fun(x, *args)
    
    f, x_opt = _minimize(wrapped_fun, lower_bounds, upper_bounds, iters, depth, attempts)

    nfev = int(iters * np.sqrt(depth)*attempts)
    result = OptimizeResult(x=x_opt, fun = f, nfev=nfev)
    
    return result