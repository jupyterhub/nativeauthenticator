import pytest
from unittest.mock import Mock


from nativeauthenticator import NativeAuthenticator


@pytest.fixture
def tmpcwd(tmpdir):
    tmpdir.chdir()


# use pytest-asyncio
pytestmark = pytest.mark.asyncio
# run each test in a temporary working directory
pytestmark = pytestmark(pytest.mark.usefixtures("tmpcwd"))


async def test_basic(tmpcwd):
    auth = NativeAuthenticator()
    response = await auth.authenticate(Mock(), {'username': 'name',
                                          'password': '123'})
    assert response == 'name'
