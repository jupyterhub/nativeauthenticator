import datetime
import dbm
import os
import time
from datetime import timezone as tz

import pytest
from jupyterhub.tests.mocking import MockHub

from ..handlers import EmailAuthorizationHandler
from ..orm import UserInfo
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


@pytest.mark.parametrize(
    "is_admin,open_signup,expected_authorization",
    [
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
async def test_create_user(is_admin, open_signup, expected_authorization, tmpcwd, app):
    """Test method create_user for new user and authorization"""
    auth = NativeAuthenticator(db=app.db)

    if is_admin:
        auth.admin_users = {"johnsnow"}
    if open_signup:
        auth.open_signup = True

    auth.create_user("johnsnow", "password")
    user_info = UserInfo.find(app.db, "johnsnow")
    assert user_info.username == "johnsnow"
    assert user_info.is_authorized == expected_authorization


async def test_create_user_bad_characters(tmpcwd, app):
    """Test method create_user with bad characters on username"""
    auth = NativeAuthenticator(db=app.db)
    assert not auth.create_user("john snow", "password")
    assert not auth.create_user("john,snow", "password")


async def test_create_user_twice(tmpcwd, app):
    """Test if creating users with an existing handle errors."""
    auth = NativeAuthenticator(db=app.db)

    # First creation should succeed.
    assert auth.create_user("johnsnow", "password")

    # Creating the same account again should fail.
    assert not auth.create_user("johnsnow", "password")

    # Creating a user with same handle but different pw should also fail.
    assert not auth.create_user("johnsnow", "adifferentpassword")


async def test_get_authed_users(tmpcwd, app):
    """Test if get_authed_users returns the proper set of users."""
    auth = NativeAuthenticator(db=app.db)

    auth.admin_users = set()
    assert auth.get_authed_users() == set()

    auth.create_user("johnsnow", "password")
    assert auth.get_authed_users() == set()

    UserInfo.change_authorization(app.db, "johnsnow")
    assert auth.get_authed_users() == set({"johnsnow"})

    auth.create_user("daenerystargaryen", "anotherpassword")
    assert auth.get_authed_users() == set({"johnsnow"})

    auth.admin_users = set({"daenerystargaryen"})
    assert "johnsnow" in auth.get_authed_users()
    assert "daenerystargaryen" in auth.get_authed_users()


async def test_get_unauthed_amount(tmpcwd, app):
    """Test if get_unauthed_amount returns the proper amount."""
    auth = NativeAuthenticator(db=app.db)

    auth.admin_users = set()
    assert auth.get_unauthed_amount() == 0

    auth.create_user("johnsnow", "password")
    assert auth.get_unauthed_amount() == 1

    UserInfo.change_authorization(app.db, "johnsnow")
    assert auth.get_unauthed_amount() == 0

    auth.create_user("daenerystargaryen", "anotherpassword")
    assert auth.get_unauthed_amount() == 1

    auth.create_user("tyrionlannister", "yetanotherpassword")
    assert auth.get_unauthed_amount() == 2

    auth.admin_users = set({"daenerystargaryen"})
    assert auth.get_unauthed_amount() == 1


@pytest.mark.parametrize(
    "password,min_len,expected",
    [
        ("qwerty", 1, False),
        ("agameofthrones", 1, True),
        ("agameofthrones", 15, False),
        ("averyveryverylongpassword", 15, True),
    ],
)
async def test_create_user_with_strong_passwords(
    password, min_len, expected, tmpcwd, app
):
    """Test if method create_user and strong passwords mesh"""
    auth = NativeAuthenticator(db=app.db)
    auth.check_common_password = True
    auth.minimum_password_length = min_len
    user = auth.create_user("johnsnow", password)
    assert bool(user) == expected


async def test_change_password(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    user = auth.create_user("johnsnow", "password")
    assert user.is_valid_password("password")
    auth.change_password("johnsnow", "newpassword")
    assert not user.is_valid_password("password")
    assert user.is_valid_password("newpassword")


async def test_no_change_to_bad_password(tmpcwd, app):
    """Test that changing password doesn't bypass password requirements"""
    auth = NativeAuthenticator(db=app.db)
    auth.check_common_password = True
    auth.minimum_password_length = 8

    auth.create_user("johnsnow", "ironwood")

    # Can't change password of nonexistent users.
    assert auth.change_password("samwelltarly", "palanquin") is None
    assert auth.get_user("johnsnow").is_valid_password("ironwood")

    # Can't change password to something too short.
    assert auth.change_password("johnsnow", "mummer") is None
    assert auth.get_user("johnsnow").is_valid_password("ironwood")

    # Can't change password to something too common.
    assert auth.change_password("johnsnow", "dragon") is None
    assert auth.get_user("johnsnow").is_valid_password("ironwood")

    # CAN change password to something fulfilling criteria.
    assert auth.change_password("johnsnow", "Daenerys") is not None
    assert not auth.get_user("johnsnow").is_valid_password("ironwood")
    assert auth.get_user("johnsnow").is_valid_password("Daenerys")


@pytest.mark.parametrize(
    "enable_signup,expected_success",
    [
        (True, True),
        (False, False),
    ],
)
async def test_create_user_disable(enable_signup, expected_success, tmpcwd, app):
    """Test method get_or_create_user not create user if signup is disabled"""
    auth = NativeAuthenticator(db=app.db)
    auth.enable_signup = enable_signup

    user = auth.create_user("johnsnow", "password")

    if expected_success:
        assert user.username == "johnsnow"
    else:
        assert not user


@pytest.mark.parametrize(
    "username,password,authorized,expected",
    [
        ("name", "123", False, False),
        ("johnsnow", "123", True, False),
        ("Snow", "password", True, False),
        ("johnsnow", "password", False, False),
        ("johnsnow", "password", True, True),
    ],
)
async def test_authentication(username, password, authorized, expected, tmpcwd, app):
    """Test if authentication fails with a unexistent user"""
    auth = NativeAuthenticator(db=app.db)
    auth.create_user("johnsnow", "password")
    if authorized:
        UserInfo.change_authorization(app.db, "johnsnow")
    response = await auth.authenticate(
        app, {"username": username, "password": password}
    )
    assert bool(response) == expected


async def test_handlers(app):
    """Test if all handlers are available on the Authenticator"""
    auth = NativeAuthenticator(db=app.db)
    handlers = auth.get_handlers(app)
    assert handlers[0][0] == r"/login"
    assert handlers[1][0] == r"/signup(/[^/]+)?"
    assert handlers[2][0] == r"/discard/([^/]+)"
    assert handlers[3][0] == r"/authorize"
    assert handlers[4][0] == r"/authorize/([^/]+)"
    assert handlers[5][0] == r"/confirm/([^/]+)"
    assert handlers[6][0] == r"/change-password"
    assert handlers[7][0] == r"/change-password/([^/]+)"


async def test_add_new_attempt_of_login(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)

    assert not auth.login_attempts
    auth.add_login_attempt("username")
    assert auth.login_attempts["username"]["count"] == 1
    auth.add_login_attempt("username")
    assert auth.login_attempts["username"]["count"] == 2


async def test_authentication_login_count(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    infos = {"username": "johnsnow", "password": "password"}
    wrong_infos = {"username": "johnsnow", "password": "wrong_password"}
    auth.create_user(infos["username"], infos["password"])
    UserInfo.change_authorization(app.db, "johnsnow")

    assert not auth.login_attempts

    await auth.authenticate(app, wrong_infos)
    assert auth.login_attempts["johnsnow"]["count"] == 1

    await auth.authenticate(app, wrong_infos)
    assert auth.login_attempts["johnsnow"]["count"] == 2

    await auth.authenticate(app, infos)
    assert not auth.login_attempts.get("johnsnow")


async def test_authentication_with_exceed_atempts_of_login(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    auth.allowed_failed_logins = 3
    auth.secs_before_next_try = 10

    infos = {"username": "johnsnow", "password": "wrongpassword"}
    auth.create_user(infos["username"], "password")
    UserInfo.change_authorization(app.db, "johnsnow")

    for i in range(3):
        response = await auth.authenticate(app, infos)
        assert not response

    infos["password"] = "password"
    response = await auth.authenticate(app, infos)
    assert not response

    time.sleep(12)
    response = await auth.authenticate(app, infos)
    assert response


async def test_get_user(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    auth.create_user("johnsnow", "password")

    # Getting existing user is successful.
    assert auth.get_user("johnsnow") is not None

    # Getting non-existing user fails.
    assert auth.get_user("samwelltarly") is None


async def test_delete_user(tmpcwd, app):
    auth = NativeAuthenticator(db=app.db)
    auth.create_user("johnsnow", "password")

    user = type("User", (), {"name": "johnsnow"})
    auth.delete_user(user)

    user_info = UserInfo.find(app.db, "johnsnow")
    assert not user_info


async def test_import_from_firstuse_dont_delete_db_after(tmpcwd, app):
    with dbm.open("passwords.dbm", "c", 0o600) as db:
        db["user1"] = "password"

    auth = NativeAuthenticator(db=app.db)
    auth.add_data_from_firstuse()

    files = os.listdir()
    assert UserInfo.find(app.db, "user1")
    assert ("passwords.dbm" in files) or ("passwords.dbm.db" in files)


async def test_import_from_firstuse_delete_db_after(tmpcwd, app):
    with dbm.open("passwords.dbm", "c", 0o600) as db:
        db["user1"] = "password"

    auth = NativeAuthenticator(db=app.db)
    auth.delete_firstuse_db_after_import = True

    auth.add_data_from_firstuse()
    files = os.listdir()
    assert UserInfo.find(app.db, "user1")
    assert ("passwords.dbm" not in files) and ("passwords.dbm.db" not in files)


@pytest.mark.parametrize(
    "user,pwd",
    [
        ("user1", "password"),
        ("user 1", "somethingelsereallysecure"),
    ],
)
async def test_import_from_firstuse_invalid_password(user, pwd, tmpcwd, app):
    with dbm.open("passwords.dbm", "c", 0o600) as db:
        db[user] = pwd

    auth = NativeAuthenticator(db=app.db)
    auth.check_common_password = True
    with pytest.raises(ValueError):
        auth.add_data_from_firstuse()


async def test_secret_key(app):
    auth = NativeAuthenticator(db=app.db)
    auth.ask_email_on_signup = False
    auth.allow_self_approval_for = ".*@example.com$"
    auth.secret_key = "short"

    with pytest.raises(ValueError):
        auth.setup_self_approval()

    auth.secret_key = "very long and kind-of random asdgaisgfjbafksdgasg"

    auth.setup_self_approval()
    assert auth.ask_email_on_signup is True


async def test_approval_token(app):
    auth = NativeAuthenticator(db=app.db)
    auth.allow_self_approval_for = ".*@example.com$"
    auth.secret_key = "very long and kind-of random asdgaisgfjbafksdgasg"
    auth.setup_self_approval()

    # confirm that a forged slug cannot be used
    with pytest.raises(ValueError):
        EmailAuthorizationHandler.validate_slug("foo", auth.secret_key)

    # confirm that an expired URL cannot be used
    expiration = datetime.datetime.now(tz.utc) - datetime.timedelta(days=2)
    token = auth.generate_approval_token("somebody", when=expiration)
    with pytest.raises(ValueError):
        EmailAuthorizationHandler.validate_slug(token, auth.secret_key)

    # confirm that a non-expired, correctly signed URL can be used
    expiration = datetime.datetime.now(tz.utc) + datetime.timedelta(days=2)
    token = auth.generate_approval_token("somebody", when=expiration)
    out = EmailAuthorizationHandler.validate_slug(token, auth.secret_key)
    assert out["username"] == "somebody"
    assert out["expire"] == expiration
