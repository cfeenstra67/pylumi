# Pylumi

**Pylumi** is a Python API providing the ability to manage [pulumi](https://github.com/pulumi/pulumi) resource plugin contexts and interact with the resource [`plugin.Provider`](https://github.com/pulumi/pulumi/blob/89c956d18942c1fcbf687da3052dd26089d8f486/sdk/go/common/resource/plugin/provider.go#L37) interface.

### Usage Example:

```python
import pylumi


with pylumi.Context() as ctx, \
     ctx.Provider('aws', {'region': 'us-east-1'}) as aws:

    resp = provider.create(
        'urn:pulumi:_::_::aws:s3/bucketObject:BucketObject::_',
        {'bucket': 'some-bucket', 'key': 'some-key', 'content': 'Hello, world!'},
    )
```

## Installation

Install this package by running
```bash
$ pip install git+https://github.com/cfeenstra67/pylumi
```
Note: since the build for this package requires compiling a go extension and a c extension that depends on it, the script is slightly fragile and may not work properly with all platforms. It has been tested on OS X and Ubuntu, but not exhaustively on either.
