import os
from jinja2 import ChoiceLoader, FileSystemLoader
from jupyterhub.auth import Authenticator
from jupyterhub.handlers import BaseHandler

from tornado import gen


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


class SignUpHandler(BaseHandler):
    """Render the sign in page."""

    def __init__(self, *args, **kwargs):
        self._loaded = False
        super().__init__(*args, **kwargs)

    def _register_template_path(self):
        if self._loaded:
            return
        self.log.debug('Adding %s to template path', TEMPLATE_DIR)
        loader = FileSystemLoader([TEMPLATE_DIR])
        env = self.settings['jinja2_env']
        previous_loader = env.loader
        env.loader = ChoiceLoader([previous_loader, loader])
        self._loaded = True

    async def get(self):
        self._register_template_path()
        html = self.render_template('signup.html')
        self.finish(html)


class NativeAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        return data['username']

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler)
        ]
        return super().get_handlers(app) + native_handlers
