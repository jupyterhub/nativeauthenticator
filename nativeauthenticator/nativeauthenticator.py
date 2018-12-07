from jupyterhub.auth import Authenticator
from jupyterhub.handlers import BaseHandler

from tornado import gen


class SignInHandler(BaseHandler):

    async def get(self):
        pass


class NativeAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        return data['username']

    def get_handlers(self, app):
        native_handlers = [
            (r'/signin', SignInHandler)
        ]
        return super().get_handlers(app) + native_handlers
