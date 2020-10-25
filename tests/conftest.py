import boto3
import botocore
import pytest
import pylumi


TEST_BUCKET = 'clf-misc'

TEST_REGION = 'us-east-2'

TEST_KEY = 'pulumi-test-2'


@pytest.fixture(scope='session')
def ctx():
    with pylumi.Context() as ctx:
        yield ctx


@pytest.fixture(scope='session')
def aws(ctx):
    with ctx.provider('aws', {'region': TEST_REGION}) as prov:
        yield prov


@pytest.fixture
def s3_client():
    return boto3.client('s3', region_name=TEST_REGION)


@pytest.fixture(scope='function')
def s3_key(s3_client):
    try:
        s3_client.delete_object(Bucket=TEST_BUCKET, Key=TEST_KEY)
    except botocore.exceptions.ClientError:
        pass
    yield TEST_KEY
    try:
        s3_client.delete_object(Bucket=TEST_BUCKET, Key=TEST_KEY)
    except botocore.exceptions.ClientError:
        pass
