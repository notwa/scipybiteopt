#from . import biteopt
#from .scipywrapper import biteopt_minimize
'''
try:
    __BITEOPT_PY_SETUP__

except NameError:
    __BITEOPT_PY_SETUP__ = False

if not __BITEOPT_PY_SETUP__:
'''
#from .biteopt import *
from ._scipywrapper import biteopt, OptimizeResult

__all__ = ["biteopt",
        "OptimizeResult"]