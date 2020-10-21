import os
import platform

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

from setup_helper import _get_build_ext_cls

extensions = [Extension('libpylumigo', ['go/main.go'])]

platform_args = []

if platform.system() == 'Darwin':
    platform_args.append('-fPIC')
else:
    platform_args.append('-symbolic')

try:
    from Cython.Build import cythonize
except ImportError:
    extensions.append(Extension(
        '_pylumi',
        sources=['_pylumi.c'],
        extra_compile_args=platform_args
    ))
else:
    extensions.extend(cythonize(
        Extension(
            '_pylumi',
            sources=['_pylumi.pyx'],
            extra_compile_args=platform_args
        ),
        language_level='3str'
    ))

setup(
    name='pylumi',
    version='0.0.1',
    description='Python API for interacting with Pulumi resource plugins',
    cmdclass={'build_ext': _get_build_ext_cls(_build_ext, 'github.com/cfeenstra67/pylumi')},
    packages=['pylumi'],
    ext_modules=extensions,
)
