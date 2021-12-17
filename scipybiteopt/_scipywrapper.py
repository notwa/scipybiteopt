from .biteopt import _minimize
import numpy as np

__source_version__ = "2021.28.1"

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

def biteopt(fun, bounds, args=(), iters = 1000, depth = 1, attempts = 10, tol = 'hard', callback = None):
    '''
    Global optimization via the biteopt algorithm

    .. note::
        biteopt does not handle Python Exceptions and will not exit gracefully in case of errors. 
        Take care that your objective function always returns a double. 

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
        Maximal number of function evaluations allowed in one attempt
    depth : int, optional, default 1
        Depth of evolutionary algorithm. Required to be ``<37``. 
        Multiplies allowed number of function evaluations by :math:`\sqrt{depth}`.
        Setting depth to a higher value increases the chance for convergence for high-dimensional problems.
    attempts : int, optional, default 10
        Number of individual optimization attemps
    tol : string, optional, default "strong"
        Convergence criterion. Must be one of ``hard``, ``weak``, or ``None``.
        Stops optimization if no significant decrease of the objective function was achieved within 
        a certain number of iterations: 64*n_dim for ``hard``, 128*n_dim for ``weak``. If ``None``, optimization 
        will run for the maximal number of function evaluations ``iter`` per attempt.
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
        of the function at the solution, and the number of function evaluations ``nfev``.

    Example
    --------
    Let's minimize a classical example in global optimization: the Ackley function.

    >>> import numpy as np
    >>> from scipybiteopt import biteopt
    >>> bounds = [(-5, 5), (-5, 5)]
    >>> def ackley(x):
    ...     arg1 = -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))
    ...     arg2 = 0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))
    ...     return -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e
    >>> result = biteopt(ackley, bounds)
    >>> result.x, result.fun
    array([0., 0.]), 0.0

    '''

    #get lower and upper bounds
    if isinstance(bounds, list):

        lower_bounds = [bound[0] for bound in bounds]
        upper_bounds = [bound[1] for bound in bounds]
    
    else:
        raise ValueError("'bounds' must be of type list.")

    if tol not in ["hard", "weak", None]:
        raise ValueError("tol must be one of 'hard', 'weak', None.")
    elif tol == "hard":
        tol_c = 1
    elif tol == "weak":
        tol_c = 2
    else: 
        tol_c = 0

    #further input validation
    if not isinstance(iters, int):
        raise ValueError("'iters' must be of type integer.")
    if iters < 1:
        raise ValueError("'iters' must be >=1.")

    if not isinstance(attempts, int):
        raise ValueError("'attempts' must be of type integer.")
    if attempts < 1:
        raise ValueError("'attempts' must be >=1.")

    if not isinstance(depth, int):
        raise ValueError("'attempts' must be of type integer.")
    if depth < 1 or depth > 36:
        raise ValueError("'depth' must be between 1 and 36.")
    
    if not isinstance(args, tuple):
        raise ValueError("'args' must be between of type list.")

    #generate wrapper function which passes args to the objective

    if callback is not None:

        def wrapped_fun(x):
            
            callback(x)
            return fun(x, *args)
    
    else:

        def wrapped_fun(x):
        
            return fun(x, *args)
    
    f, x_opt, n_eval = _minimize(wrapped_fun, lower_bounds, upper_bounds, iters, depth, attempts, tol_c)

    result = OptimizeResult(x=x_opt, fun = f, nfev=n_eval)
    
    return result