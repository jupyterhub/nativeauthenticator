import bcrypt
from jupyterhub.orm import User
from jupyterhub.auth import Authenticator

from sqlalchemy import inspect
from sqlalchemy.orm import relationship
from tornado import gen

from .handlers import SignUpHandler
from .orm import UserInfo


class NativeAuthenticator(Authenticator):

    def __init__(self, add_new_table=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if add_new_table:
            self.add_new_table()

    def add_new_table(self):
        inspector = inspect(self.db.bind)
        if 'users_info' not in inspector.get_table_names():
            User.info = relationship(UserInfo, backref='users')
            UserInfo.__table__.create(self.db.bind)

    @gen.coroutine
    def authenticate(self, handler, data):
        user = UserInfo.find(self.db, data['username'])
        if user and user.is_valid_password(data['password']):
            return data['username']

    def get_or_create_user(self, username, password):
        user = User.find(self.db, username)
        if not user:
            user = User(name=username, admin=False)
            self.db.add(user)

        encoded_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_info = UserInfo(user=user, username=username, password=encoded_pw)
        self.db.add(user_info)
        return user

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler)
        ]
        return super().get_handlers(app) + native_handlers
