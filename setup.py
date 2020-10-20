import os

from Cython.Build import cythonize
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

from setup_helper import _get_build_ext_cls


setup(
    name='pylumi',
    version='1.0',
    description='abc',
    install_requires=[
        'cython'
    ],
    cmdclass={'build_ext': _get_build_ext_cls(_build_ext, 'github.com/cfeenstra67/pylumi')},
    packages=['pylumi'],
    ext_modules=cythonize(
        [
            Extension('libpylumigo', ['go/main.go']),
            Extension(
                '_pylumi',
                sources=['_pylumi.pyx'],
                extra_compile_args=['-fPIC']
            )
        ],
        language_level='3str'
    ),
)
