import os
from jinja2 import ChoiceLoader, FileSystemLoader
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import admin_only
from urllib import parse

from tornado import web

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
        )
        self.finish(html)

    def get_result_message(self, user):
        alert = 'alert-info'
        message = 'Your information have been sent to the admin'

        if self.authenticator.open_signup:
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
        body = self.request.body.decode('utf-8')
        body_arguments = dict(parse.parse_qsl(body))
        user = self.authenticator.get_or_create_user(**body_arguments)

        alert, message = self.get_result_message(user)

        html = self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            result_message=message,
            alert=alert
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
        user = self.get_current_user()
        new_password = self.get_body_argument('password', strip=False)
        self.authenticator.change_password(user.name, new_password)

        html = self.render_template(
            'change-password.html',
            result_message='Your password has been changed successfully',
        )
        self.finish(html)
