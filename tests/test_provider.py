import pylumi


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
        {'bucket': 'clf-misc', 'key': 'pulumi-test-1', 'content': 'Hello, world!'},
        new_props
    )

    assert props == {
        '__defaults': ['acl', 'forceDestroy'],
        'acl': 'private',
        'forceDestroy': False,
        **new_props
    }

    assert errs == [{'Property': '', 'Reason': "Missing required property 'bucket'"}]


def test_provider_check_valid(aws):
    new_props = {'bucket': 'clf-misc', 'key': 'pulumi-test-2', 'content': 'Hello, world! 2'}
    props, errs = aws.check(
        pylumi.URN('aws:s3/bucketObject:BucketObject'),
        {'bucket': 'clf-misc', 'key': 'pulumi-test-1', 'content': 'Hello, world!'},
        new_props
    )

    assert props == {
        '__defaults': ['acl', 'forceDestroy'],
        'acl': 'private',
        'forceDestroy': False,
        **new_props
    }

    assert errs is None

