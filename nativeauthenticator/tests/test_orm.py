import pytest
from sqlalchemy.exc import StatementError

from ..orm import UserInfo


@pytest.mark.parametrize("email", ["john", "john@john"])
def test_validate_method_wrong_email(email, tmpcwd, app):
    with pytest.raises(AssertionError):
        UserInfo(username="john", password=b"pwd", email=email)


def test_validate_method_correct_email(tmpcwd, app):
    user = UserInfo(username="john", password=b"pwd", email="john@john.com")
    app.db.add(user)
    app.db.commit()
    assert UserInfo.find(app.db, "john")


def test_all_users(tmpcwd, app):
    assert len(UserInfo.all_users(app.db)) == 0
    user = UserInfo(
        username="daenerystargaryen",
        password=b"yesispeakvalyrian",
        email="khaleesi@valyria.com",
    )
    app.db.add(user)
    app.db.commit()

    assert len(UserInfo.all_users(app.db)) == 1


def test_wrong_pwd_type(tmpcwd, app):
    with pytest.raises(StatementError):
        user = UserInfo(username="john", password="pwd", email="john@john.com")
        app.db.add(user)
        UserInfo.find(app.db, "john")
