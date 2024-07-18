#!/usr/bin/env python
"""Setup file for the Python nitime package.

This file only contains cython components.
See pyproject.toml for the remaining configuration.
"""
import sys
from setuptools import setup, Extension
from Cython.Build import cythonize
from numpy import get_include


stable_abi = sys.version_info[:2] >= (3, 11)
cmdclass = {}

macros = [
    ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
]

if stable_abi:
    from wheel.bdist_wheel import bdist_wheel

    class bdist_wheel_abi3(bdist_wheel):
        def get_tag(self):
            python, abi, plat = super().get_tag()

            if python.startswith('cp3'):
                python, abi = 'cp311', 'abi3'

            return python, abi, plat

    cmdclass['bdist_wheel'] = bdist_wheel_abi3

    macros += [
        ('CYTHON_LIMITED_API', '1'),
        ('Py_LIMITED_API', '0x030b0000'),
    ]

exts = [
    Extension(
        'nitime._utils',
        ['nitime/_utils.pyx'],
        include_dirs=[get_include()],
        define_macros=macros,
        py_limited_api=stable_abi,
    )
]

setup(
    ext_modules=cythonize(exts, language_level='3'),
    cmdclass=cmdclass,
)
