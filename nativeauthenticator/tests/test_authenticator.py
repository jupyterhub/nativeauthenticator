import pytest
from jupyterhub.tests.mocking import MockHub

from nativeauthenticator import NativeAuthenticator
from ..orm import UserInfo


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


async def test_create_user(tmpcwd, app):
    '''Test if method get_or_create_user creates a new user'''
    auth = NativeAuthenticator(db=app.db)
    auth.get_or_create_user('John Snow', 'password')
    user_info = UserInfo.find(app.db, 'John Snow')
    assert user_info.username == 'John Snow'


@pytest.mark.parametrize("password,min_len,expected", [
    ("qwerty", 1, False),
    ("agameofthrones", 1, True),
    ("agameofthrones", 15, False),
    ("averyveryverylongpassword", 15, True),
])
async def test_create_user_with_strong_passwords(password, min_len, expected,
                                                 tmpcwd, app):
    '''Test if method get_or_create_user and strong passwords'''
    auth = NativeAuthenticator(db=app.db)
    auth.check_common_password = True
    auth.minimum_password_length = min_len
    user = auth.get_or_create_user('John Snow', password)
    assert bool(user) == expected


@pytest.mark.parametrize("username,password,authorized,expected", [
    ("name", '123', False, False),
    ("John Snow", '123', True, False),
    ("Snow", 'password', True, False),
    ("John Snow", 'password', False, False),
    ("John Snow", 'password', True, True),
])
async def test_authentication(username, password, authorized, expected,
                              tmpcwd, app):
    '''Test if authentication fails with a unexistent user'''
    auth = NativeAuthenticator(db=app.db)
    auth.get_or_create_user('John Snow', 'password')
    if authorized:
        UserInfo.change_authorization(app.db, 'John Snow')
    response = await auth.authenticate(app, {'username': username,
                                             'password': password})
    assert bool(response) == expected


async def test_handlers(app):
    '''Test if all handlers are available on the Authenticator'''
    auth = NativeAuthenticator(db=app.db)
    handlers = auth.get_handlers(app)
    assert handlers[1][0] == '/signup'
    assert handlers[2][0] == '/authorize'
