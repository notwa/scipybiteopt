#!/usr/bin/env python
import os
import sys
import numpy
from setuptools import setup, Extension

#include markdown description in pip page
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

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
                  extra_compile_args=['-std=c++11',  '-O3'] if os.name != 'nt' else ['-O3'])

setup(name='scipybiteopt',
    version='1.1.1',
    description="Scipy style wrapper for Aleksey Vaneev's BiteOpt",
    author='dschmitz89',
    author_email='danielschmitzsiegen@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/dschmitz89/scipybiteopt',
    packages = ['scipybiteopt'],
    ext_modules = [module1],
    install_requires=[
    'numpy']
     )
