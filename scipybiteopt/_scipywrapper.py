from .biteopt import _minimize

__source_version__ = "2021.28"
__source_hash__ = "8ff656353f42df9e97d62d660c7b76a60ce5cd9b"

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

def biteopt(fun, bounds, args=(), iters = 1000, depth = 1, attempts = 10, callback = None):
    '''
    Global optimization via the biteopt algorithm

    Parameters
    ----------
    fun : callable 
        The objective function to be minimized. Must be in the form ``fun(x, *args)``, where ``x`` 
        is the argument in the form of a 1-D numpy array and args is a tuple of any additional fixed 
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
        Depth of evolutionary algorithm. Required to be ``<37``. 
        Multiplies allowed number of function evaluations by :math:`\sqrt{depth}`.
        Setting depth to a higher value increases the chance for convergence for high-dimensional problems.
    attempts : int, optional, default 10
        Number of individual optimization attemps
    callback : callable, optional, default None
        callback function which is also called before every objective function evaluation. 
        Must be in the form ``fun(x, *args)``, where ``x`` 
        is the argument in the form of a 1-D numpy array and args is a tuple of any additional fixed 
        parameters needed to completely specify the function.

    Returns
    -------
    result : :py:class:`~OptimizeResult`
        The optimization result represented as a :py:class:`~OptimizeResult` object.
        Attributes are: ``x`` the solution array, ``fun`` the value
        of the function at the solution, andthe number of function evaluations``nfev``.

    Example
    --------
    Let's as an example minimize a classical example in global optimization: the Ackley function.
    >>> import numpy as np
    >>> from scipybiteopt import biteopt
    >>> bounds = [(-5, 5), (-5, 5)]
    >>> def ackley(pos):
	...        x, y = pos
	...        return -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 20
    >>> result = biteopt(ackley, bounds)
    >>> result.x, result.fun
    array([0., 0.]), 0.0
    '''
    lower_bounds = [bound[0] for bound in bounds]
    upper_bounds = [bound[1] for bound in bounds]

    if callback is not None:

        def wrapped_fun(x):
            
            callback(x)
            return fun(x, *args)
    
    else:

        def wrapped_fun(x):
        
            return fun(x, *args)
    
    f, x_opt = _minimize(wrapped_fun, lower_bounds, upper_bounds, iters, depth, attempts)

    nfev = int(iters * depth**0.5 * attempts)
    result = OptimizeResult(x=x_opt, fun = f, nfev=nfev)
    
    return result