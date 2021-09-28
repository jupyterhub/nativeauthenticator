import os
from datetime import datetime, date
from datetime import timezone as tz
from jinja2 import ChoiceLoader, FileSystemLoader
from jupyterhub.handlers import BaseHandler
from jupyterhub.handlers.login import LoginHandler
from jupyterhub.utils import admin_only

from tornado import web
from tornado.escape import url_escape
from tornado.httputil import url_concat

import requests

from .orm import UserInfo

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


class LocalBase(BaseHandler):
    _template_dir_registered = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not LocalBase._template_dir_registered:
            self.log.debug('Adding %s to template path', TEMPLATE_DIR)
            loader = FileSystemLoader([TEMPLATE_DIR])
            env = self.settings['jinja2_env']
            previous_loader = env.loader
            env.loader = ChoiceLoader([previous_loader, loader])
            LocalBase._template_dir_registered = True


class SignUpHandler(LocalBase):
    """Render the sign in page."""
    async def get(self):
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        html = await self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            two_factor_auth=self.authenticator.allow_2fa,
            recaptcha_key=self.authenticator.recaptcha_key,
            tos=self.authenticator.tos,
        )
        self.finish(html)

    def get_result_message(self, user, taken, human=True):
        alert = 'alert-info'
        message = 'Your information has been sent to the admin'
        if user and user.login_email_sent:
            message = 'Check your email to authorize your access'

        # Always error if username is taken.
        if taken:
            alert = 'alert-danger'
            message = ("Something went wrong. It appears that this "
                       "username is already in use. Please try again "
                       "with a different username.")
        else:
            # Error if user creation was not successful.
            if not user:
                alert = 'alert-danger'
                pw_len = self.authenticator.minimum_password_length
                if pw_len:
                    message = ("Something went wrong. Be sure your "
                               "password has at least {} characters, doesn't "
                               "have spaces or commas and is not too "
                               "common.").format(pw_len)
                else:
                    message = ("Something went wrong. Be sure your password "
                               "doesn't have spaces or commas and is not too "
                               "common.")

            # If user creation went through & open-signup is enabled, success.
            elif self.authenticator.open_signup:
                alert = 'alert-success'
                message = ('The signup was successful. You can now go to '
                           'home page and log in the system')

        if not human:
            alert = 'alert-danger'
            message = ("You failed the reCAPTCHA. Please try again")

        return alert, message

    async def post(self):
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        assume_human = True
        url = "https://www.google.com/recaptcha/api/siteverify"

        if self.authenticator.recaptcha_key:
            recaptcha_response = \
                self.get_body_argument('g-recaptcha-response', strip=True)
            if recaptcha_response == "":
                assume_human = False
            else:
                data = {
                    'secret': self.authenticator.recaptcha_secret,
                    'response': recaptcha_response
                }
                validation_status = requests.post(url, data=data)
                assume_human = validation_status.json().get("success")
                if assume_human:
                    self.authenticator.log.info("Passed reCaptcha")
                else:
                    self.authenticator.log.error("Failed reCaptcha")

        if assume_human:
            user_info = {
                'username': self.get_body_argument('username', strip=False),
                'pw': self.get_body_argument('pw', strip=False),
                'email': self.get_body_argument('email', '', strip=False),
                'has_2fa': bool(self.get_body_argument('2fa', '', strip=False))
            }
            taken = self.authenticator.user_exists(user_info['username'])
            user = self.authenticator.create_user(**user_info)
        else:
            user = False
            taken = False

        alert, message = self.get_result_message(user, taken, assume_human)

        otp_secret, user_2fa = '', ''
        if user:
            otp_secret = user.otp_secret
            user_2fa = user.has_2fa

        html = await self.render_template(
            'signup.html',
            ask_email=self.authenticator.ask_email_on_signup,
            result_message=message,
            alert=alert,
            two_factor_auth=self.authenticator.allow_2fa,
            two_factor_auth_user=user_2fa,
            two_factor_auth_value=otp_secret,
            recaptcha_key=self.authenticator.recaptcha_key,
            tos=self.authenticator.tos,
        )
        self.finish(html)


class AuthorizationHandler(LocalBase):
    """Render the sign in page."""
    @admin_only
    async def get(self):
        html = await self.render_template(
            'autorization-area.html',
            ask_email=self.authenticator.ask_email_on_signup,
            users=self.db.query(UserInfo).all(),
        )
        self.finish(html)


class ChangeAuthorizationHandler(LocalBase):
    @admin_only
    async def get(self, slug):
        UserInfo.change_authorization(self.db, slug)
        self.redirect(self.hub.base_url + 'authorize#' + slug)


class AuthorizeHandler(LocalBase):
    async def get(self, slug):
        must_stop = True
        msg = "Invalid URL"
        if self.authenticator.allow_self_approval_for:
            try:
                data = AuthorizeHandler.validate_slug(
                        slug, self.authenticator.secret_key)
                must_stop = False
            except ValueError:
                pass

        if not must_stop:
            username = data["username"]
            msg = "{} was already authorized".format(username)
            usr = UserInfo.find(self.db, username)
            if not usr.is_authorized:
                UserInfo.change_authorization(self.db, username)
                msg = "{} has been authorized".format(username)

            # add POSIX user!!

        html = await self.render_template(
            'my_message.html',
            message=msg,
        )
        self.finish(html)

    # static method so it can be easily tested without initializate the class
    @staticmethod
    def validate_slug(slug, key):
        from .crypto.signing import Signer, BadSignature
        s = Signer(key)
        try:
            obj = s.unsign_object(slug)
        except BadSignature as e:
            raise ValueError(e)

        # the following it is not supported in earlier versions of python
        # obj["expire"] = datetime.fromisoformat(obj["expire"])

        # format="%Y-%m-%dT%H:%M:%S.%f"
        datestr, timestr = obj["expire"].split("T")

        # before the T
        year_month_day = datestr.split("-")
        dateobj = date(int(year_month_day[0]),
                       int(year_month_day[1]),
                       int(year_month_day[2]))

        # after the T
        # manually parsing iso-8601 times with a colon in the timezone
        # since the strptime does not support it
        if timestr[-3] == ":":
            timestr = timestr[:-3] + timestr[-2:]
        timeobj = datetime.strptime(timestr, "%H:%M:%S.%f%z").timetz()

        obj["expire"] = datetime.combine(dateobj, timeobj)

        if datetime.now(tz.utc) > obj["expire"]:
            raise ValueError("The URL has expired")

        return obj


class ChangePasswordHandler(LocalBase):
    """Render the reset password page."""

    @web.authenticated
    async def get(self):
        user = await self.get_current_user()
        html = await self.render_template(
            'change-password.html',
            user_name=user.name,
        )
        self.finish(html)

    @web.authenticated
    async def post(self):
        user = await self.get_current_user()
        new_password = self.get_body_argument('password', strip=False)
        self.authenticator.change_password(user.name, new_password)

        html = await self.render_template(
            'change-password.html',
            user_name=user.name,
            result_message='Your password has been changed successfully',
        )
        self.finish(html)


class ChangePasswordAdminHandler(LocalBase):
    """Render the reset password page."""

    @admin_only
    async def get(self, user_name):
        if not self.authenticator.user_exists(user_name):
            raise web.HTTPError(404)
        html = await self.render_template(
            'change-password.html',
            user_name=user_name,
        )
        self.finish(html)

    @admin_only
    async def post(self, user_name):
        new_password = self.get_body_argument('password', strip=False)
        self.authenticator.change_password(user_name, new_password)

        message_template = 'The password for {} has been changed successfully'
        html = await self.render_template(
            'change-password.html',
            user_name=user_name,
            result_message=message_template.format(user_name),
        )
        self.finish(html)


class LoginHandler(LoginHandler, LocalBase):

    def _render(self, login_error=None, username=None):
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

    async def post(self):
        # parse the arguments dict
        data = {}
        for arg in self.request.arguments:
            data[arg] = self.get_argument(arg, strip=False)

        auth_timer = self.statsd.timer('login.authenticate').start()
        user = await self.login_user(data)
        auth_timer.stop(send=False)

        if user:
            # register current user for subsequent requests to user
            # (e.g. logging the request)
            self._jupyterhub_user = user
            self.redirect(self.get_next_url(user))
        else:
            # default error mesage on unsuccessful login
            error = 'Invalid username or password'

            # check is user exists and has correct password,
            # and is just not authorised
            nuser = self.authenticator.get_user(data['username'])
            if nuser is not None:
                if (nuser.is_valid_password(data['password'])
                        and not nuser.is_authorized):
                    error = 'User has not been authorized by administrator yet'

            html = await self._render(
                login_error=error, username=data['username']
            )
            self.finish(html)


class DiscardHandler(LocalBase):
    """Discard a user from database"""

    @admin_only
    async def get(self, user_name):
        user = self.authenticator.get_user(user_name)
        if user is not None:
            if not user.is_authorized:
                # Delete user from NativeAuthenticator db table (users_info)
                user = type('User', (), {'name': user_name})
                self.authenticator.delete_user(user)

                # Also delete user from jupyterhub registry, if present
                if self.users.get(user_name) is not None:
                    self.users.delete(user_name)

        self.redirect(self.hub.base_url + 'authorize')
