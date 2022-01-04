import os

from setuptools import Extension, setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from Cython.Build import cythonize
except ImportError as err:
    c_file_path = os.path.join(CURRENT_DIR, "go/main.c")
    if not os.path.exists(c_file_path):
        raise RuntimeError(
            "Unable to find main.c file for _pylumi extension, "
            "and Cython is not installed to compile it. If you "
            "are an end-user receiving this error please contact "
            "the maintainers for assistance."
        ) from err
else:
    cythonize(Extension("_pylumi", ["go/main.pyx"]), language_level="3str")

with open(os.path.join(CURRENT_DIR, "README.rst")) as f:
    long_description = f.read().strip()

with open(os.path.join(CURRENT_DIR, "requirements.txt")) as f:
    install_requires = list(filter(None, map(str.strip, f)))

with open(os.path.join(CURRENT_DIR, "requirements-tests.txt")) as f:
    install_requires_tests = list(filter(None, map(str.strip, f)))

with open(os.path.join(CURRENT_DIR, "requirements-dev.txt")) as f:
    install_requires_dev = list(filter(None, map(str.strip, f)))

setup(
    name="pylumi",
    version="1.2.2",
    description="Python API for interacting with Pulumi resource plugins.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="go cython terraform pulumi infra-as-code cloudformation",
    url="https://github.com/cfeenstra67/pylumi",
    author="Cam Feenstra",
    author_email="cameron.l.feenstra@gmail.com",
    install_requires=install_requires,
    license="MIT",
    # Actual package data
    build_golang={"root": "github.com/cfeenstra67/pylumi/go"},
    ext_modules=[Extension("_pylumi", ["go/main.go"])],
    setup_requires=["setuptools-golang"],
    packages=["pylumi"],
    extras_require={"tests": install_requires_tests, "dev": install_requires_dev},
)
