import os
from jinja2 import ChoiceLoader, FileSystemLoader
from jupyterhub.handlers import BaseHandler
from jupyterhub.handlers.login import LoginHandler
from jupyterhub.utils import admin_only

from tornado import web
from tornado.escape import url_escape
from tornado.httputil import url_concat

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

class AuthorizationHandler(LocalBase):
    """Render the sign in page."""
    @admin_only
    async def get(self):
        self._register_template_path()
        html = self.render_template(
            'autorization-area.html',
            ask_email=self.authenticator.ask_email_on_signup,
            users=self.db.query(UserInfo).all(),
        )
        self.finish(html)


class ChangeAuthorizationHandler(LocalBase):
    @admin_only
    async def get(self, slug):
        UserInfo.change_authorization(self.db, slug)
        self.redirect('/authorize')

class LoginHandler(LoginHandler, LocalBase):

    def _render(self, login_error=None, username=None):
        self._register_template_path()
        return self.render_template(
            'native-login.html',
            next=url_escape(self.get_argument('next', default='')),
            username=username,
            login_error=login_error,
            custom_html=self.authenticator.custom_html,
            login_url=self.settings['login_url'],
            two_factor_auth=self.authenticator.allow_2fa,
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {'next': self.get_argument('next', '')},
            ),
        )
