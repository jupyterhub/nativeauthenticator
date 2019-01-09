import bcrypt
from jupyterhub.orm import User
from jupyterhub.auth import Authenticator

from sqlalchemy import inspect
from tornado import gen

from .handlers import SignUpHandler
from .orm import UserInfo


class NativeAuthenticator(Authenticator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        inspector = inspect(self.db.bind)
        if 'users_info' not in inspector.get_table_names():
            UserInfo.__table__.create(self.db.bind)

    @gen.coroutine
    def authenticate(self, handler, data):
        user = UserInfo.find(self.db, data['username'])
        if user.is_valid_password(data['password']):
            return data['username']

    def get_or_create_user(self, username, password):
        user = User.find(self.db, username)
        if not user:
            user = User(name=username, admin=False)
            self.db.add(user)

        encoded_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_info = UserInfo(username=username, password=encoded_pw)
        self.db.add(user_info)
        return user

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler)
        ]
        return super().get_handlers(app) + native_handlers
