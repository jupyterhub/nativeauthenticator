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
        self.redirect('/')

    def get_result_message(self, user):
        alert = 'alert-success'
        message = ('The signup was successful. You can now go to '
                   'home page and log in the system')
        if not user:
            alert = 'alert-danger'
            password_len = self.authenticator.minimum_password_length

            if password_len:
                message = ("Something went wrong. Be sure your password has "
                           "at least {} characters, doesn't have spaces or "
                           "commas and is not too common.").format(password_len)

            else:
                message = ("Something went wrong. Be sure your password "
                           " doesn't have spaces or commas and is not too "
                           "common.")

        return alert, message

    async def post(self):
        api_token = self.request.headers.get('Authorization', None)
        user_info = {
            'username': self.get_body_argument('username', strip=False),
            'password': self.get_body_argument('password', strip=False),
            'is_authorized': True,
            'email': self.get_body_argument('email', '', strip=False),
            'admin': self.get_body_argument('admin', False, strip=False),
        }
        alert, message = '', ''
        userExist = self.authenticator.get_user(**user_info)
        if userExist:
            alert = 'alert-danger'
            message = ('User already exist'
                       ' Ask an Cashstory Admin to get access')
        elif api_token and api_token == os.environ.get('ADMIN_API_TOKEN', 'SHOULD_BE_CHANGED'):
            user = self.authenticator.create_user(**user_info)
            alert, message = self.get_result_message(user)
        else:
            alert = 'alert-danger'
            message = ('Signup not allowed.'
                       ' Ask an Cashstory Admin to get access')
         
        response = {
            'name': user_info.get('username'),
            'message': message,
        }
        if alert == 'alert-danger':
            response['error'] = True

        self.finish(response)
        return response


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


class DeleteHandler(LocalBase):
    @admin_only
    async def get(self, slug):
        UserInfo.delete_user(self.db, slug)
        self.redirect('/authorize')


class ChangePasswordHandler(LocalBase):
    """Render the reset password page."""

    @web.authenticated
    async def get(self):
       self.redirect('/')

    @web.authenticated
    async def post(self):
        api_token = self.request.headers.get('Authorization', None)
        username = self.get_body_argument('username', strip=False)
        user = self.authenticator.get_user(username)
        message = ''
        alert = 'alert-success'
        if api_token and api_token == os.environ.get('ADMIN_API_TOKEN', 'SHOULD_BE_CHANGED'):
            new_password = self.get_body_argument('password', strip=False)
            message = 'Your password has been changed successfully'
            self.authenticator.change_password(user.name, new_password)
        else:
            message = 'You can\'t change your password, ask an Admin'
            alert = 'alert-danger'

        response = {
            'name': username,
            'message': message,
        }
        if alert == 'alert-danger':
            response['error'] = True

        self.finish(response)
        return response

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
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {'next': self.get_argument('next', '')},
            ),
        )
