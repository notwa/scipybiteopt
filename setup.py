#!/usr/bin/env python
import os
import sys
import numpy
from setuptools import setup, Extension

# https://github.com/pypa/packaging-problems/issues/84
# no sensible way to include header files by default
headers = ['scipybiteopt/biteopt.h',
            'scipybiteopt/biteoptort.h',
            'scipybiteopt/spheropt.h',
            'scipybiteopt/biteaux.h',
            'scipybiteopt/nmsopt.h']

def get_c_sources(files, include_headers=False):
    return files + (headers if include_headers else [])

module1 = Extension('scipybiteopt.biteopt',
                  sources=get_c_sources(['scipybiteopt/biteopt_py_ext.cpp'], include_headers=(sys.argv[1] == "sdist")),
                  language="c++",
                  include_dirs=[numpy.get_include()],
                  extra_compile_args=['-std=c++11'] if os.name != 'nt' else [])

setup(name='scipybiteopt',
      version='0.2.2',
      description="Python Wrapper for Aleksey Vaneev's BiteOpt",
      author='leonidk',
      author_email='lkeselman@gmail.com',
      url = 'https://github.com/leonidk/biteopt',
      packages = ['scipybiteopt'],
      #py_modules=[],
      ext_modules = [module1]
     )
