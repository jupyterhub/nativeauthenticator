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


class SignUpHandler(LocalBase):
    """Render the sign in page."""
    async def get(self):
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        self._register_template_path()
        html = self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            two_factor_auth=self.authenticator.allow_2fa,
        )
        self.finish(html)

    def get_result_message(self, user, username):
        alert = 'alert-info'
        message = 'Your information have been sent to the admin'

        if self.authenticator.open_signup:
            alert = 'alert-success'
            message = ('The signup was successful. You can now go to '
                       'home page and log in the system')
        if not user:
            alert = 'alert-danger'
            pw_len = self.authenticator.minimum_password_length
            taken = self.authenticator.user_exists(username)

            if pw_len:
                message = ("Something went wrong. Be sure your password has "
                           "at least {} characters, doesn't have spaces or "
                           "commas and is not too common.").format(pw_len)

            elif taken:
                message = ("Something went wrong. It appears that this "
                           "username is already in use. Please try again "
                           "with a different username.")

            else:
                message = ("Something went wrong. Be sure your password "
                           " doesn't have spaces or commas and is not too "
                           "common.")

        return alert, message

    async def post(self):
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        user_info = {
            'username': self.get_body_argument('username', strip=False),
            'pw': self.get_body_argument('pw', strip=False),
            'email': self.get_body_argument('email', '', strip=False),
            'has_2fa': bool(self.get_body_argument('2fa', '', strip=False)),
        }
        user = self.authenticator.create_user(**user_info)
        name = self.authenticator.user_exists(user_info['username'])

        alert, message = self.get_result_message(user, name)

        otp_secret, user_2fa = '', ''
        if user:
            otp_secret = user.otp_secret
            user_2fa = user.has_2fa

        html = self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            result_message=message,
            alert=alert,
            two_factor_auth=self.authenticator.allow_2fa,
            two_factor_auth_user=user_2fa,
            two_factor_auth_value=otp_secret,
        )
        self.finish(html)


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
        self.redirect(self.hub.base_url + 'authorize')


class ChangePasswordHandler(LocalBase):
    """Render the reset password page."""

    @web.authenticated
    async def get(self):
        self._register_template_path()
        html = self.render_template('change-password.html')
        self.finish(html)

    @web.authenticated
    async def post(self):
        user = await self.get_current_user()
        new_password = self.get_body_argument('password', strip=False)
        self.authenticator.change_password(user.name, new_password)

        html = self.render_template(
            'change-password.html',
            result_message='Your password has been changed successfully',
        )
        self.finish(html)


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
            enable_signup=self.authenticator.enable_signup,
            two_factor_auth=self.authenticator.allow_2fa,
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {'next': self.get_argument('next', '')},
            ),
        )
