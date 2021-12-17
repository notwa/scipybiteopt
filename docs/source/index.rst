.. scipybiteopt documentation master file, created by
   sphinx-quickstart on Mon Nov  1 19:19:33 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to scipybiteopt's documentation!
========================================

``scipybiteopt`` offers a scipy.optimize like API for the global optimizer biteopt.

Installation
--------

.. code:: bash

   pip install scipybiteopt

Note that a C++ compiler is required.

Example: Minimizing the six-hump camel back function
-----

.. code-block:: python

   import scipybiteopt

   def camel(x):
      """Six-hump camelback function"""
      x1 = x[0]
      x2 = x[1]
      f = (4 - 2.1*(x1*x1) + (x1*x1*x1*x1)/3.0)*(x1*x1) + x1*x2 + (-4 + 4*(x2*x2))*(x2*x2)
      return f

   bounds = [(-4, 4), (-4, 4)]

   res = scipybiteopt.biteopt(camel, bounds)
   print("Found optimum: ", res.x)

Which biteopt version is used?
------------
The underyling biteopt version can be accessed via

.. code-block:: python

   import scipybiteopt
   scipybiteopt.__source_version__

Documentation
-----------------
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   scipybiteopt
   Benchmark

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
