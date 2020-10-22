# Getting Started

Pylumi is a Python API for the pulumi resource provider interface, which is written in Go.

Note: Pylumi is _not_ a client for all Pulumi functionality and has does not interact with the infrastructure as code application. What it does is just do enough Pulumi setup to interact with its resource providers like `aws` and `gcp`. For each provider, a number of resources are exposed with the following functionality:
- Reading the state of the resource from a remote API.
- CRUD operations on the resource--schemas for particular resources can be found via the `Provider.get_schema()` function. 
- Ability to diff different states of the resource to determine which changes are required to go from one bag of properties to another.

Usage example:
```python
import pylumi


with pylumi.Context() as ctx, \
     ctx.Provider('aws', {'region': 'us-east-1'}) as aws:

    resp = aws.create(
        'urn:pulumi:_::_::aws:s3/bucketObject:BucketObject::_',
        {'bucket': 'some-bucket', 'key': 'some-key', 'content': 'Hello, world!'},
    )
```

## Installation

TODO
