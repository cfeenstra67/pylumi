############
Pylumi
############

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

**Note**: since the build for this package requires compiling a go extension and a c extension that depends on it, the script is slightly fragile and may not work properly with all platforms. It has been tested on OS X and Ubuntu, but not exhaustively on either.

Documentation
##############

Documentation for Pylumi is hosted on Read the Docs: https://pylumi.readthedocs.io/.

Contact
#########

If you have issues using this repository please open a issue or reach out to me at cameron.l.feenstra@gmail.com.
