# A python wrapper for biteopt #

This package provides a scipy.optimize like API for the powerful global optimization algorithm biteopt. It is a fork of [another biteopt wrapper](https://github.com/leonidk/biteopt). 

## Installation ##
```bash
pip install scipybiteopt
```
Note that the installation requires a C++ compiler.

## Example usage: optimizing the six-hump camel back function ##

```python
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
```

## Citing ##
```bibtex
@misc{biteopt2021,
    author = {Aleksey Vaneev},
    title = {{BITEOPT - Derivative-free optimization method}},
    note = {C++ source code, with description and examples},
    year = {2021},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {Available at \url{https://github.com/avaneev/biteopt}},
}
```
