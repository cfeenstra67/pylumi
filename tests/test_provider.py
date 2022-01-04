import asyncio
import os

import botocore
import boto3
import pylumi
import pytest

from tests.conftest import TEST_BUCKET, TEST_REGION, TEST_KEY


def test_provider_get_plugin_info(aws):
    info = aws.get_plugin_info()

    assert isinstance(info.pop("InstallTime"), str)
    assert isinstance(info.pop("LastUsedTime"), str)
    assert isinstance(info.pop("PluginDir"), str)
    assert isinstance(info.pop("PluginDownloadURL"), str)
    assert info == {
        "Name": "aws",
        "Path": os.path.expanduser(
            "~/.pulumi/plugins/resource-aws-v4.33.0/pulumi-resource-aws"
        ),
        "Kind": "resource",
        "Version": "4.33.0",
        "Size": 0,
    }


def test_provider_get_schema_bytes(aws):
    schema = aws.get_schema(decode=False)

    assert isinstance(schema, bytes)
    # This is a big blob of bytes
    assert len(schema) > 10_000


def test_provider_get_schema(aws):
    schema = aws.get_schema()

    assert schema["name"] == "aws"
    assert "resources" in schema


def test_provider_check_config(aws):
    props, errs = aws.check_config(
        pylumi.URN("aws"), {"region": "us-east-2"}, {"region": "us-east-1"}
    )

    assert props == {"region": "us-east-1"}
    assert errs is None


def test_provider_diff_config(aws):
    resp = aws.diff_config(
        pylumi.URN("aws"), {"region": "us-east-2"}, {"region": "us-east-1"}
    )

    # AWS provider doesn't really support diffing
    assert resp["Changes"] == 0
    assert list(resp) == [
        "Changes",
        "ReplaceKeys",
        "StableKeys",
        "ChangedKeys",
        "DetailedDiff",
        "DeleteBeforeReplace",
    ]


def test_provider_check_invalid(aws):
    new_props = {"key": TEST_KEY, "content": "Hello, world! 2"}
    props, errs = aws.check(
        pylumi.URN("aws:s3/bucketObject:BucketObject"),
        {"bucket": TEST_BUCKET, "key": "pulumi-test-1", "content": "Hello, world!"},
        new_props,
    )

    props["__defaults"].sort()

    assert props == {
        "__defaults": ["acl", "forceDestroy"],
        "acl": "private",
        "forceDestroy": False,
        **new_props,
    }

    assert errs == [
        {
            "Property": "",
            "Reason": (
                'Missing required argument: The argument "bucket" is required, but '
                "no definition was found.. Examine values at 'BucketObject.Bucket'."
            ),
        }
    ]


def test_provider_check_valid(aws):
    new_props = {"bucket": TEST_BUCKET, "key": TEST_KEY, "content": "Hello, world! 2"}
    props, errs = aws.check(
        pylumi.URN("aws:s3/bucketObject:BucketObject"),
        {"bucket": TEST_BUCKET, "key": "pulumi-test-1", "content": "Hello, world!"},
        new_props,
    )

    props["__defaults"].sort()

    assert props == {
        "__defaults": ["acl", "forceDestroy"],
        "acl": "private",
        "forceDestroy": False,
        **new_props,
    }

    assert errs is None


def test_provider_check_unknowns(aws):
    new_props = {
        "bucket": pylumi.UnknownValue.STRING,
        "key": TEST_KEY,
        "content": "Hello, world! 2",
    }
    props, errs = aws.check(
        pylumi.URN("aws:s3/bucketObject:BucketObject"),
        {"bucket": TEST_BUCKET, "key": "pulumi-test-1", "content": "Hello, world!"},
        new_props,
        allow_unknowns=True,
    )

    assert props == {
        "__defaults": ["acl", "forceDestroy"],
        "acl": "private",
        "forceDestroy": False,
        "bucket": pylumi.UnknownValue.STRING,
        "content": new_props["content"],
        "key": new_props["key"],
    }

    assert errs is None


def test_provider_diff_changes(aws):
    new_props = {"bucket": TEST_BUCKET, "key": TEST_KEY, "content": "Hello, world! 2"}
    resp = aws.diff(
        pylumi.URN("aws:s3/bucketObject:BucketObject"),
        "test-123-1",
        {"bucket": TEST_BUCKET, "key": "pulumi-test-1", "content": "Hello, world!"},
        new_props,
    )

    resp["ChangedKeys"].sort()

    assert resp == {
        "Changes": 2,
        "ReplaceKeys": ["key"],
        "StableKeys": ["bucket"],
        "ChangedKeys": ["content", "key"],
        "DetailedDiff": {
            "content": {"Kind": 4, "InputDiff": False},
            "key": {"Kind": 5, "InputDiff": False},
        },
        "DeleteBeforeReplace": False,
    }


def test_provider_diff_stable(aws):
    new_props = {"bucket": TEST_BUCKET, "key": TEST_KEY, "content": "Hello, world! 2"}
    resp = aws.diff(
        pylumi.URN("aws:s3/bucketObject:BucketObject"),
        "test-123-1",
        new_props,
        new_props,
    )

    resp["StableKeys"].sort()

    assert resp == {
        "Changes": 1,
        "ReplaceKeys": None,
        "StableKeys": ["bucket", "key"],
        "ChangedKeys": None,
        "DetailedDiff": {},
        "DeleteBeforeReplace": False,
    }


def test_provider_create_preview(aws, s3_client, s3_key):
    new_props = {
        "bucket": TEST_BUCKET,
        "key": s3_key,
        "content": "Hello, world! 2",
        "acl": "private",
        "forceDestroy": False,
        "id": "",
    }

    resp = aws.create(
        pylumi.URN("aws:s3/bucketObject:BucketObject"), new_props, preview=True
    )

    assert resp == {"ID": "", "Properties": new_props, "Status": 0}

    with pytest.raises(botocore.exceptions.ClientError):
        s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)


def test_provider_create(aws, s3_client, s3_key):
    new_props = {"bucket": TEST_BUCKET, "key": s3_key, "content": "Hello, world! 2"}

    resp = aws.create(pylumi.URN("aws:s3/bucketObject:BucketObject"), new_props)

    assert resp["Properties"].pop("__meta").startswith('{"')

    assert resp == {
        "ID": TEST_KEY,
        "Properties": {
            "acl": "private",
            "bucket": TEST_BUCKET,
            "bucketKeyEnabled": False,
            "cacheControl": "",
            "content": "Hello, world! 2",
            "contentDisposition": "",
            "contentEncoding": "",
            "contentLanguage": "",
            "contentType": "binary/octet-stream",
            "etag": "53554dd9d7d18fc279ff5546b714465f",
            "forceDestroy": False,
            "id": TEST_KEY,
            "key": TEST_KEY,
            "metadata": {},
            "objectLockLegalHoldStatus": "",
            "objectLockMode": "",
            "objectLockRetainUntilDate": "",
            "serverSideEncryption": "",
            "storageClass": "STANDARD",
            "tags": {},
            "tagsAll": {},
            "versionId": "",
            "websiteRedirect": "",
        },
        "Status": 0,
    }

    resp = s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)
    assert resp["Body"].read().decode() == new_props["content"]


def test_provider_read(aws, s3_client, s3_key):
    new_props = {"bucket": TEST_BUCKET, "key": s3_key, "content": "Hello, world! 2"}

    create_resp = aws.create(pylumi.URN("aws:s3/bucketObject:BucketObject"), new_props)

    resp = aws.read(
        pylumi.URN("aws:s3/bucketObject:BucketObject", create_resp["ID"]),
        create_resp["ID"],
        {},
        new_props,
    )

    assert resp == {
        "ID": TEST_KEY,
        "Inputs": {},
        "Outputs": {
            "acl": "private",
            "bucket": TEST_BUCKET,
            "bucketKeyEnabled": False,
            "cacheControl": "",
            "content": "Hello, world! 2",
            "contentDisposition": "",
            "contentEncoding": "",
            "contentLanguage": "",
            "contentType": "binary/octet-stream",
            "etag": "53554dd9d7d18fc279ff5546b714465f",
            "forceDestroy": False,
            "id": TEST_KEY,
            "key": TEST_KEY,
            "metadata": {},
            "objectLockLegalHoldStatus": "",
            "objectLockMode": "",
            "objectLockRetainUntilDate": "",
            "serverSideEncryption": "",
            "storageClass": "STANDARD",
            "tags": {},
            "tagsAll": {},
            "versionId": "",
            "websiteRedirect": "",
        },
        "Status": 0,
    }


def test_provider_update(aws, s3_client, s3_key):
    new_props = {"bucket": TEST_BUCKET, "key": s3_key, "content": "Hello, world! 2"}
    new_content = "Mr. Magoo"

    create_resp = aws.create(pylumi.URN("aws:s3/bucketObject:BucketObject"), new_props)

    resp = aws.update(
        pylumi.URN("aws:s3/bucketObject:BucketObject", create_resp["ID"]),
        create_resp["ID"],
        new_props,
        dict(new_props, content=new_content),
    )

    assert resp["Properties"].pop("__meta").startswith('{"')

    assert resp == {
        "ID": TEST_KEY,
        "Properties": {
            "acl": "private",
            "bucket": TEST_BUCKET,
            "bucketKeyEnabled": False,
            "cacheControl": "",
            "content": new_content,
            "contentDisposition": "",
            "contentEncoding": "",
            "contentLanguage": "",
            "contentType": "binary/octet-stream",
            "etag": "a96e6203ad76aa4969cc0e5e6c5ef9c7",
            "forceDestroy": False,
            "id": TEST_KEY,
            "key": TEST_KEY,
            "metadata": {},
            "objectLockLegalHoldStatus": "",
            "objectLockMode": "",
            "objectLockRetainUntilDate": "",
            "serverSideEncryption": "",
            "storageClass": "STANDARD",
            "tags": {},
            "tagsAll": {},
            "versionId": "",
            "websiteRedirect": "",
        },
        "Status": 0,
    }

    resp = s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)
    assert resp["Body"].read().decode() == new_content


def test_provider_delete(aws, s3_client, s3_key):
    new_props = {"bucket": TEST_BUCKET, "key": s3_key, "content": "Hello, world! 2"}

    create_resp = aws.create(pylumi.URN("aws:s3/bucketObject:BucketObject"), new_props)

    resp = aws.delete(
        pylumi.URN("aws:s3/bucketObject:BucketObject", create_resp["ID"]),
        create_resp["ID"],
        new_props,
    )

    assert resp == 0

    with pytest.raises(botocore.exceptions.ClientError):
        s3_client.get_object(Bucket=TEST_BUCKET, Key=s3_key)


def test_provider_invoke_validation_error(aws):
    with pytest.raises(pylumi.exc.InvocationValidationError):
        resp = aws.invoke("aws:s3/getBucket:getBucket", {})


def test_provider_invoke(aws):
    resp = aws.invoke("aws:s3/getBucket:getBucket", {"bucket": TEST_BUCKET})
    assert resp["bucket"] == TEST_BUCKET


def test_provider_invoke_fail(aws):
    with pytest.raises(pylumi.exc.ProviderError):
        resp = aws.invoke(
            "aws:s3/getBucket:getBucket", {"bucket": f"{TEST_BUCKET}-blah123"}
        )


# Doesn't really test anything other than that the function runs, can't figure out a better way right now
def test_provider_signal_cancellation(aws):
    aws.signal_cancellation()
