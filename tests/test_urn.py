import pytest

import pylumi


@pytest.mark.parametrize('args, kwargs, out', [
    pytest.param(
        ('aws:s3/bucketObject:BucketObject',),
        {},
        'urn:pulumi:_::_::aws:s3/bucketObject:BucketObject::_',
        id='type_only_1'
    ),
    pytest.param(
        ('aws:s3/bucketObject:BucketObject', 'my-name'),
        {},
        'urn:pulumi:_::_::aws:s3/bucketObject:BucketObject::my-name',
        id='type_and_name_1'
    ),
    pytest.param(
        ('urn:pulumi:stack1::project1::aws:s3/bucketObject:BucketObject::name1',),
        {},
        'urn:pulumi:stack1::project1::aws:s3/bucketObject:BucketObject::name1',
        id='full_urn_1'
    ),
    pytest.param(
        ('aws:s3/bucketObject:BucketObject', 'name1', 'stack1', 'project1'),
        {},
        'urn:pulumi:stack1::project1::aws:s3/bucketObject:BucketObject::name1',
        id='all_params_1'
    ),
    pytest.param(
        (),
        {
            'type': 'aws:s3/bucketObject:BucketObject',
            'name': 'name1',
            'project': 'project1',
            'stack': 'stack1'
        },
        'urn:pulumi:stack1::project1::aws:s3/bucketObject:BucketObject::name1',
        id='all_params_2'
    )
])
def test_render_urn(args, kwargs, out):
    assert str(pylumi.URN(*args, **kwargs)) == out
