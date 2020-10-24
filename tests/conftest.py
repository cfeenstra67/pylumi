import boto3
import botocore
import pytest
import pylumi


TEST_BUCKET = 'clf-misc'

TEST_REGION = 'us-east-2'


@pytest.fixture(scope='session')
def ctx():
    with pylumi.Context() as ctx:
        yield ctx


@pytest.fixture(scope='session')
def aws(ctx):
    with ctx.Provider('aws', {'region': TEST_REGION}) as prov:
        yield prov


@pytest.fixture
def s3_client():
    return boto3.client('s3', region_name=TEST_REGION)


@pytest.fixture(scope='function')
def s3_key(s3_client):
    key = 'pulumi-test-2'
    try:
        s3_client.delete_object(Bucket=TEST_BUCKET, Key=key)
    except botocore.exceptions.ClientError:
        pass
    yield key
    try:
        s3_client.delete_object(Bucket=TEST_BUCKET, Key=key)
    except botocore.exceptions.ClientError:
        pass
