from setuptools import setup
from Cython.Build import cythonize

setup(
    name='ascii app',
    ext_modules=cythonize("src/functions.pyx"),
)