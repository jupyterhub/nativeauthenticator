import os
from jinja2 import ChoiceLoader, FileSystemLoader
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import admin_only

from .orm import UserInfo

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


class LocalBase(BaseHandler):
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


class SignUpHandler(LocalBase):
    """Render the sign in page."""
    async def get(self):
        self._register_template_path()
        html = self.render_template('signup.html')
        self.finish(html)

    async def post(self):
        username = self.get_body_argument('username', strip=False)
        password = self.get_body_argument('password', strip=False)
        user = self.authenticator.get_or_create_user(username, password)

        result_message = 'Your information have been sent to the admin'
        if not user:
            result_message = """Something went wrong. Be sure your password
                                have a upper case letter, a lower case
                                and a number."""

        html = self.render_template(
            'signup.html',
            result=bool(user),
            result_message=result_message,
        )
        self.finish(html)


class AuthorizationHandler(LocalBase):
    """Render the sign in page."""
    @admin_only
    async def get(self):
        self._register_template_path()
        html = self.render_template('autorization-area.html',
                                    users=self.db.query(UserInfo).all())
        self.finish(html)


class ChangeAuthorizationHandler(LocalBase):
    @admin_only
    async def get(self, slug):
        UserInfo.change_authorization(self.db, slug)
        self.redirect('/authorize')
