import bcrypt
from jupyterhub.auth import Authenticator

from sqlalchemy import inspect
from tornado import gen
from traitlets import Bool, Integer

from .common_credentials import COMMON_CREDENTIALS
from .handlers import (AuthorizationHandler, ChangeAuthorizationHandler,
                       SignUpHandler)
from .orm import UserInfo


class NativeAuthenticator(Authenticator):

    check_password_strength = Bool(
        config=True,
        default=False,
        help="""Creates a verification of password strength
        when a new user makes signup"""
    )
    password_length = Integer(
        config=True,
        default=8,
        help="""Check if the length of the password is at least this size on
        SignUp"""
    )

    def __init__(self, add_new_table=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if add_new_table:
            self.add_new_table()

    def add_new_table(self):
        inspector = inspect(self.db.bind)
        if 'users_info' not in inspector.get_table_names():
            UserInfo.__table__.create(self.db.bind)

    @gen.coroutine
    def authenticate(self, handler, data):
        user = UserInfo.find(self.db, data['username'])
        if not user:
            return
        if user.is_authorized and user.is_valid_password(data['password']):
            return data['username']

    def is_password_strong(self, password):
        checks = [
            len(password) >= self.password_length,
            password not in COMMON_CREDENTIALS
        ]
        return all(checks)

    def get_or_create_user(self, username, pw):
        user = UserInfo.find(self.db, username)
        if user:
            return user

        if self.check_password_strength and not self.is_password_strong(pw):
            return

        encoded_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        infos = {'username': username, 'password': encoded_pw}
        if username in self.admin_users:
            infos.update({'is_authorized': True})

        user_info = UserInfo(**infos)
        self.db.add(user_info)
        return user_info

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler),
            (r'/authorize', AuthorizationHandler),
            (r'/authorize/([^/]*)', ChangeAuthorizationHandler)
        ]
        return super().get_handlers(app) + native_handlers
