import pytest

import pylumi


@pytest.fixture(scope='session')
def ctx():
    with pylumi.Context() as ctx:
        yield ctx


@pytest.fixture(scope='function')
def aws(ctx):
    with ctx.Provider('aws', {'region': 'us-east-2'}) as prov:
        yield prov
