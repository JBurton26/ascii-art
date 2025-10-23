from setuptools import setup
from Cython.Build import cythonize
import numpy
setup(
    name='ascii app',
    ext_modules=cythonize("src/functions.pyx"),
    include_dirs=[numpy.get_include()]
)