from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("funcoes_c.pyx")
)
