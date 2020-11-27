import os
import platform

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

from setup_helper import _get_build_ext_cls

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

extensions = [Extension('libpylumigo', ['go/main.go'])]

try:
    from Cython.Build import cythonize
except ImportError:
    extensions.append(Extension('_pylumi', ['_pylumi.c']))
else:
    extensions.append(Extension('_pylumi', ['_pylumi.pyx']))
    extensions = cythonize(extensions, language_level='3str')

with open(os.path.join(CURRENT_DIR, 'README.rst')) as f:
    long_description = f.read().strip()

with open(os.path.join(CURRENT_DIR, 'requirements.txt')) as f:
    install_requires = list(filter(None, map(str.strip, f)))

with open(os.path.join(CURRENT_DIR, 'requirements-tests.txt')) as f:
    install_requires_tests = list(filter(None, map(str.strip, f)))

with open(os.path.join(CURRENT_DIR, 'requirements-dev.txt')) as f:
    install_requires_dev = list(filter(None, map(str.strip, f)))

setup(
    name='pylumi',
    version='1.2.0',
    description='Python API for interacting with Pulumi resource plugins.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Cython',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    keywords='go cython terraform pulumi infra-as-code cloudformation',
    url='https://github.com/cfeenstra67/pylumi',
    author='Cam Feenstra',
    author_email='cameron.l.feenstra@gmail.com',
    install_requires=install_requires,
    license='MIT',
    # Actual package data
    cmdclass={'build_ext': _get_build_ext_cls(_build_ext, 'github.com/cfeenstra67/pylumi')},
    packages=['pylumi'],
    py_modules=['setup_helper'],
    ext_modules=extensions,
    extras_require={
        'tests': install_requires_tests,
        'dev': install_requires_dev
    },
    package_data={
        '': [
            'requirements.txt',
            'requirements-dev.txt',
            'requirements-tests.txt',
            'README.md',
            'go/*'
        ],
    },
    include_package_data=True
)
