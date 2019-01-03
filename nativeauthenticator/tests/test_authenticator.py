import pytest
from unittest.mock import Mock
from jupyterhub.tests.mocking import MockHub

from nativeauthenticator import NativeAuthenticator


@pytest.fixture
def tmpcwd(tmpdir):
    tmpdir.chdir()


@pytest.fixture
def app():
    hub = MockHub()
    hub.init_db()
    return hub


# use pytest-asyncio
pytestmark = pytest.mark.asyncio
# run each test in a temporary working directory
pytestmark = pytestmark(pytest.mark.usefixtures("tmpcwd"))


async def test_basic(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    response = await auth.authenticate(Mock(), {'username': 'name',
                                                'password': '123'})
    assert response == 'name'
