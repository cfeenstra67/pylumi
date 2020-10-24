import botocore
import boto3
import pylumi
import pytest

from tests.conftest import TEST_BUCKET, TEST_REGION


def test_provider_get_schema_bytes(aws):
    schema = aws.get_schema(decode=False)

    assert isinstance(schema, bytes)
    # This is a big blob of bytes
    assert len(schema) > 10_000


def test_provider_get_schema(aws):
    schema = aws.get_schema()

    assert schema['name'] == 'aws'
    assert 'resources' in schema


def test_provider_check_config(aws):
    props, errs = aws.check_config(pylumi.URN('aws'), {'region': 'us-east-2'}, {'region': 'us-east-1'})

    assert props == {'region': 'us-east-1'}
    assert errs is None


def test_provider_diff_config(aws):
    resp = aws.diff_config(pylumi.URN('aws'), {'region': 'us-east-2'}, {'region': 'us-east-1'})

    # AWS provider doesn't really support diffing
    assert resp['Changes'] == 0
    assert list(resp) == [
        'Changes', 'ReplaceKeys', 'StableKeys', 'ChangedKeys',
        'DetailedDiff', 'DeleteBeforeReplace'
    ]


def test_provider_check_invalid(aws):
    new_props = {'key': 'pulumi-test-2', 'content': 'Hello, world! 2'}
    props, errs = aws.check(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        {'bucket': TEST_BUCKET, 'key': 'pulumi-test-1', 'content': 'Hello, world!'},
        new_props
    )

    props['__defaults'].sort()

    assert props == {
        '__defaults': ['acl', 'forceDestroy'],
        'acl': 'private',
        'forceDestroy': False,
        **new_props
    }

    assert errs == [{'Property': '', 'Reason': "Missing required property 'bucket'"}]


def test_provider_check_valid(aws):
    new_props = {'bucket': TEST_BUCKET, 'key': 'pulumi-test-2', 'content': 'Hello, world! 2'}
    props, errs = aws.check(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        {'bucket': TEST_BUCKET, 'key': 'pulumi-test-1', 'content': 'Hello, world!'},
        new_props
    )

    props['__defaults'].sort()

    assert props == {
        '__defaults': ['acl', 'forceDestroy'],
        'acl': 'private',
        'forceDestroy': False,
        **new_props
    }

    assert errs is None


def test_provider_diff_changes(aws):
    new_props = {'bucket': TEST_BUCKET, 'key': 'pulumi-test-2', 'content': 'Hello, world! 2'}
    resp = aws.diff(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        'test-123-1',
        {'bucket': TEST_BUCKET, 'key': 'pulumi-test-1', 'content': 'Hello, world!'},
        new_props
    )

    resp['ChangedKeys'].sort()

    assert resp == {
        'Changes': 2,
        'ReplaceKeys': ['key'],
        'StableKeys': ['bucket'],
        'ChangedKeys': ['content', 'key'],
        'DetailedDiff': {
            'content': {'Kind': 4, 'InputDiff': False},
            'key': {'Kind': 5, 'InputDiff': False}
        },
        'DeleteBeforeReplace': False
    }


def test_provider_diff_stable(aws):
    new_props = {'bucket': TEST_BUCKET, 'key': 'pulumi-test-2', 'content': 'Hello, world! 2'}
    resp = aws.diff(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        'test-123-1',
        new_props,
        new_props
    )

    resp['StableKeys'].sort()

    assert resp == {
        'Changes': 1,
        'ReplaceKeys': None,
        'StableKeys': ['bucket', 'key'],
        'ChangedKeys': None,
        'DetailedDiff': {},
        'DeleteBeforeReplace': False
    }


def test_provider_create_preview(aws, s3_client, s3_key):
    new_props = {'bucket': TEST_BUCKET, 'key': s3_key, 'content': 'Hello, world! 2'}

    resp = aws.create(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        new_props,
        preview=True
    )

    assert resp == {
        'ID': '',
        'Properties': new_props,
        'Status': 0
    }

    with pytest.raises(botocore.exceptions.ClientError):
        s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)


def test_provider_create(aws, s3_client, s3_key):
    new_props = {'bucket': TEST_BUCKET, 'key': s3_key, 'content': 'Hello, world! 2'}

    resp = aws.create(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        new_props
    )

    assert resp['Properties'].pop('__meta').startswith('{"')

    assert resp == {
        'ID': 'pulumi-test-2',
        'Properties': {
            'acl': 'private',
            'bucket': 'clf-misc',
            'cacheControl': '',
            'content': 'Hello, world! 2',
            'contentDisposition': '',
            'contentEncoding': '',
            'contentLanguage': '',
            'contentType': 'binary/octet-stream',
            'etag': '53554dd9d7d18fc279ff5546b714465f',
            'forceDestroy': False,
            'id': 'pulumi-test-2',
            'key': 'pulumi-test-2',
            'metadata': {},
            'objectLockLegalHoldStatus': '',
            'objectLockMode': '',
            'objectLockRetainUntilDate': '',
            'serverSideEncryption': '',
            'storageClass': 'STANDARD',
            'tags': {},
            'versionId': '',
            'websiteRedirect': ''
        },
        'Status': 0
    }

    resp = s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)
    assert resp['Body'].read().decode() == new_props['content']


def test_provider_read(aws, s3_client, s3_key):
    new_props = {'bucket': TEST_BUCKET, 'key': s3_key, 'content': 'Hello, world! 2'}

    create_resp = aws.create(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        new_props
    )

    resp = aws.read(
        pylumi.URN('aws:s3/bucketObject:BucketObject', create_resp['ID']),
        create_resp['ID'],
        {},
        new_props,
    )

    assert resp == {
        'ID': 'pulumi-test-2',
        'Inputs': {
            'acl': 'private',
            'bucket': 'clf-misc',
            'cacheControl': '',
            'content': 'Hello, world! 2',
            'contentDisposition': '',
            'contentEncoding': '',
            'contentLanguage': '',
            'contentType': 'binary/octet-stream',
            'etag': '53554dd9d7d18fc279ff5546b714465f',
            'forceDestroy': False,
            'key': 'pulumi-test-2',
            'metadata': {},
            'objectLockLegalHoldStatus': '',
            'objectLockMode': '',
            'objectLockRetainUntilDate': '',
            'serverSideEncryption': '',
            'storageClass': 'STANDARD',
            'tags': {},
            'websiteRedirect': ''
        },
        'Outputs': {
            'acl': 'private',
            'bucket': 'clf-misc',
            'cacheControl': '',
            'content': 'Hello, world! 2',
            'contentDisposition': '',
            'contentEncoding': '',
            'contentLanguage': '',
            'contentType': 'binary/octet-stream',
            'etag': '53554dd9d7d18fc279ff5546b714465f',
            'forceDestroy': False,
            'id': 'pulumi-test-2',
            'key': 'pulumi-test-2',
            'metadata': {},
            'objectLockLegalHoldStatus': '',
            'objectLockMode': '',
            'objectLockRetainUntilDate': '',
            'serverSideEncryption': '',
            'storageClass': 'STANDARD',
            'tags': {},
            'versionId': '',
            'websiteRedirect': ''
        },
        'Status': 0
    }


def test_provider_update(aws, s3_client, s3_key):
    new_props = {'bucket': TEST_BUCKET, 'key': s3_key, 'content': 'Hello, world! 2'}
    new_content = 'Mr. Magoo'

    create_resp = aws.create(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        new_props
    )

    resp = aws.update(
        pylumi.URN('aws:s3/bucketObject:BucketObject', create_resp['ID']),
        create_resp['ID'],
        new_props,
        dict(new_props, content=new_content)
    )

    assert resp['Properties'].pop('__meta').startswith('{"')

    assert resp == {
        'ID': 'pulumi-test-2',
        'Properties': {
            'acl': 'private',
            'bucket': 'clf-misc',
            'cacheControl': '',
            'content': new_content,
            'contentDisposition': '',
            'contentEncoding': '',
            'contentLanguage': '',
            'contentType': 'binary/octet-stream',
            'etag': 'a96e6203ad76aa4969cc0e5e6c5ef9c7',
            'forceDestroy': False,
            'id': 'pulumi-test-2',
            'key': 'pulumi-test-2',
            'metadata': {},
            'objectLockLegalHoldStatus': '',
            'objectLockMode': '',
            'objectLockRetainUntilDate': '',
            'serverSideEncryption': '',
            'storageClass': 'STANDARD',
            'tags': {},
            'versionId': '',
            'websiteRedirect': ''
        },
        'Status': 0
    }

    resp = s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)
    assert resp['Body'].read().decode() == new_content


def test_provider_delete(aws, s3_client, s3_key):
    new_props = {'bucket': TEST_BUCKET, 'key': s3_key, 'content': 'Hello, world! 2'}
    new_content = 'Mr. Magoo'

    create_resp = aws.create(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        new_props
    )

    resp = aws.delete(
        pylumi.URN('aws:s3/bucketObject:BucketObject', create_resp['ID']),
        create_resp['ID'],
        new_props
    )

    assert resp == 0

    with pytest.raises(botocore.exceptions.ClientError):
        s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)
