############
Pylumi
############

|tests-passing| |build-passing| |docs| |pypi-version| |pypi-license|

Purpose
########

**Pylumi** is a Python API providing the ability to manage `pulumi <https://github.com/pulumi/pulumi>`_ resource plugin contexts and interact with the resource `Provider <https://github.com/pulumi/pulumi/blob/89c956d18942c1fcbf687da3052dd26089d8f486/sdk/go/common/resource/plugin/provider.go#L37>`_ interface.

Usage Example
##############

.. code-block:: python

   import pylumi

   with pylumi.Context() as ctx, \
        ctx.provider('aws', {'region': 'us-east-1'}) as aws:

       resp = aws.create(
           pylumi.URN('aws:s3/bucketObject:BucketObject'),
           {'bucket': 'some-bucket', 'key': 'some-key', 'content': 'Hello, world!'},
       )


Installation
#############

Before installing `pylumi`, you must have Go installed on your system. For additional information, see the `Go Programming Language Installation Page <https://golang.org/doc/install>`_.

Once that is done, install this package using:

.. code-block:: bash
   
   $ pip install pylumi

Compatibility
###############

Tests are passing on Mac OS X and Ubuntu, see recent test runs in `Actions <https://github.com/cfeenstra67/pylumi/actions>`_ for details.

Documentation
##############

Documentation for Pylumi is hosted on Read the Docs: https://pylumi.readthedocs.io/.

Contact
#########

If you have issues using this repository please open a issue or reach out to me at cameron.l.feenstra@gmail.com.


.. |docs| image:: https://readthedocs.org/projects/pylumi/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://pylumi.readthedocs.io/en/latest/?badge=latest

.. |pypi-version| image:: https://pypip.in/v/pylumi/badge.png
    :target: https://pypi.org/project/pylumi/
    :alt: Latest PyPI version

.. |pypi-downloads| image:: https://pypip.in/d/pylumi/badge.png
    :target: https://pypi.org/project/pylumi/
    :alt: Number of PyPI downloads

.. |pypi-license| image:: https://img.shields.io/pypi/l/pylumi.svg
    :target: https://pypi.org/project/pylumi/
    :alt: PyPI License

.. |tests-passing| image:: https://github.com/cfeenstra67/pylumi/workflows/Run%20tests/badge.svg
	:target: https://github.com/cfeenstra67/pylumi/actions?query=workflow%3A%22Run+tests%22
	:alt: Tests Passing

.. |build-passing| image:: https://github.com/cfeenstra67/pylumi/workflows/Upload%20to%20PyPI/badge.svg
	:target: https://github.com/cfeenstra67/pylumi/actions?query=workflow%3A%22Upload+to+PyPI%22
	:alt: Build Passing
