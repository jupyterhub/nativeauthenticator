import pytest
from jupyterhub.tests.mocking import MockHub
from sqlalchemy.exc import StatementError

from ..orm import UserInfo


@pytest.fixture
def tmpcwd(tmpdir):
    tmpdir.chdir()


@pytest.fixture
def app():
    hub = MockHub()
    hub.init_db()
    return hub


@pytest.mark.parametrize('email', ['john', 'john@john'])
def test_validate_method_wrong_email(email, tmpdir, app):
    with pytest.raises(AssertionError):
        UserInfo(username='john', password=b'pwd', email=email)


def test_validate_method_correct_email(tmpdir, app):
    user = UserInfo(username='john', password=b'pwd', email='john@john.com')
    app.db.add(user)
    assert UserInfo.find(app.db, 'john')


def test_wrong_pwd_type(tmpdir, app):
    with pytest.raises(StatementError):
        user = UserInfo(username='john', password='pwd', email='john@john.com')
        app.db.add(user)
        UserInfo.find(app.db, 'john')
