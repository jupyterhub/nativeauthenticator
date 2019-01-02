from jupyterhub import orm
from jupyterhub.auth import Authenticator

from tornado import gen

from .handlers import SignUpHandler


class NativeAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        return data['username']

    def get_or_create_user(self, username):
        user = orm.User.find(self.db, username)
        if not user:
            user = orm.User(name=username, admin=False)
            self.db.add(user)
        return user

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler)
        ]
        return super().get_handlers(app) + native_handlers
