import pytest
from jupyterhub.tests.mocking import MockHub


@pytest.fixture
def tmpcwd(tmpdir):
    tmpdir.chdir()


@pytest.fixture
def app():
    hub = MockHub()
    hub.init_db()
    return hub
