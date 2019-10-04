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
        self._register_template_path()
        html = self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            two_factor_auth=self.authenticator.allow_2fa,
        )
        self.finish(html)

    def get_result_message(self, user):
        alert = 'alert-success'
        message = ('The signup was successful. You can now go to '
                   'home page and log in the system')
        if not user:
            alert = 'alert-danger'
            pw_len = self.authenticator.minimum_password_length

            if pw_len:
                message = ("Something went wrong. Be sure your password has "
                           "at least {} characters, doesn't have spaces or "
                           "commas and is not too common.").format(pw_len)

            else:
                message = ("Something went wrong. Be sure your password "
                           " doesn't have spaces or commas and is not too "
                           "common.")

        return alert, message

    async def post(self):
        api_token = self.get_body_argument('api_token', '', strip=False)
        user_info = {
            'username': self.get_body_argument('username', strip=False),
            'pw': self.get_body_argument('pw', strip=False),
            'is_authorized': True,
            'email': self.get_body_argument('email', '', strip=False),
            'has_2fa': bool(self.get_body_argument('2fa', '', strip=False)),
        }
        alert, message = '', ''
        otp_secret, user_2fa = '', ''
        if api_token == os.environ.get('ADMIN_API_TOKEN', 'SHOULD_BE_CHANGED'):
            user = self.authenticator.get_or_create_user(**user_info)
            alert, message = self.get_result_message(user)
            if user:
                otp_secret = user.otp_secret
                user_2fa = user.has_2fa
        else:
            alert = 'alert-danger'
            message = ('Signup not allowed.'
                       ' Ask an Cashstory Admin to get access')

        self._register_template_path()
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
        self.redirect('/authorize')


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
        message = ''
        if self.authenticator.open_change_password:
            message = 'Your password has been changed successfully'
            self.authenticator.change_password(user.name, new_password)
        else:
            message = 'You can\'t change your password, ask an Admin'
        html = self.render_template(
            'change-password.html',
            result_message=message,
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
            two_factor_auth=self.authenticator.allow_2fa,
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {'next': self.get_argument('next', '')},
            ),
        )
