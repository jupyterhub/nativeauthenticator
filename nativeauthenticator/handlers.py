import base64
import io
import os
import socket
from datetime import date
from datetime import datetime
from datetime import timezone as tz

import qrcode
from jinja2 import ChoiceLoader
from jinja2 import FileSystemLoader
from jupyterhub.handlers import BaseHandler
from jupyterhub.handlers.login import LoginHandler

try:
    from jupyterhub.scopes import needs_scope

    admin_users_scope = needs_scope("admin:users")
except ImportError:
    from jupyterhub.utils import admin_only

    admin_users_scope = admin_only

from tornado import web
from tornado.escape import url_escape
from tornado.httputil import url_concat

import requests

from .orm import UserInfo

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def generate_otp_uri(username, secret):
    if secret:
        hostname = socket.gethostname()
        return f"otpauth://totp/{username}@{hostname}?secret={secret}&issuer={hostname}"
    else:
        return ""


def generate_otp_qrcode(username, secret):
    if secret:
        qrobj = qrcode.make(generate_otp_uri(username, secret))
        with io.BytesIO() as buffer:
            qrobj.save(buffer, "png")
            otp_qrcode = base64.b64encode(buffer.getvalue()).decode()
        return otp_qrcode
    else:
        return ""


class LocalBase(BaseHandler):
    """Base class that all handlers below extend."""

    _template_dir_registered = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not LocalBase._template_dir_registered:
            self.log.debug("Adding %s to template path", TEMPLATE_DIR)
            loader = FileSystemLoader([TEMPLATE_DIR])
            env = self.settings["jinja2_env"]
            previous_loader = env.loader
            env.loader = ChoiceLoader([previous_loader, loader])
            LocalBase._template_dir_registered = True


class SignUpHandler(LocalBase):
    """Responsible for rendering the /hub/signup page, validating input to that
    page, account creation and giving accurate feedback to users."""

    async def get(self):
        """Rendering on GET requests ("normal" visits)."""

        # 404 if signup is not currently open.
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        # Render page with relevant settings from the authenticator.
        html = await self.render_template(
            "signup.html",
            ask_email=self.authenticator.ask_email_on_signup,
            two_factor_auth_allow=self.authenticator.allow_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            recaptcha_key=self.authenticator.recaptcha_key,
            tos=self.authenticator.tos,
        )
        self.finish(html)

    def get_result_message(
        self,
        user,
        assume_user_is_human,
        username_already_taken,
        confirmation_matches,
        user_is_admin,
    ):
        """Helper function to discern exactly what message and alert level are
        appropriate to display as a response. Called from post() below."""

        # Error if failed captcha.
        if not assume_user_is_human:
            alert = "alert-danger"
            message = "You failed the reCAPTCHA. Please try again"
        # Error if username is taken.
        elif username_already_taken:
            alert = "alert-danger"
            message = (
                "Something went wrong!\nIt appears that this "
                "username is already in use. Please try again "
                "with a different username."
            )
        # Error if confirmation didn't match password.
        elif not confirmation_matches:
            alert = "alert-danger"
            message = "Your password did not match the confirmation. Please try again."
        # Error if user creation was not successful.
        elif not user:
            alert = "alert-danger"
            minimum_password_length = self.authenticator.minimum_password_length
            # Error if minimum password length is > 0.
            if minimum_password_length > 0:
                message = (
                    "Something went wrong!\nBe sure your username "
                    "does not contain spaces, commas or slashes, your "
                    f"password has at least {minimum_password_length} "
                    "characters and is not too common."
                )
            # Error if minimum password length is 0.
            else:
                message = (
                    "Something went wrong!\nBe sure your username "
                    "does not contain spaces, commas or slashes and your "
                    "password is not too common."
                )
        # If user creation went through & open-signup is enabled, success.
        # If user creation went through & the user is an admin, also success.
        elif (user is not None) and (self.authenticator.open_signup or user_is_admin):
            alert = "alert-success"
            message = (
                "The signup was successful! You can now go to "
                "the home page and log in to the system."
            )
        else:
            # Default response if nothing goes wrong.
            alert = "alert-info"
            message = "Your information has been sent to the admin."

            if (user is not None) and user.login_email_sent:
                message = (
                    "The signup was successful! Check your email "
                    "to authorize your access."
                )

        return alert, message

    async def post(self):
        """Rendering on POST requests (signup visits with data attached)."""

        # 404 if users aren't allowed to sign up.
        if not self.authenticator.enable_signup:
            raise web.HTTPError(404)

        if not self.authenticator.recaptcha_key:
            # If this option is not enabled, we proceed under
            # the assumption that the user is human.
            assume_user_is_human = True
        else:
            # If this option _is_ enabled, we assume the user
            # is _not_ human until we know otherwise.
            assume_user_is_human = False

            recaptcha_response = self.get_body_argument(
                "g-recaptcha-response", strip=True
            )
            if recaptcha_response != "":
                data = {
                    "secret": self.authenticator.recaptcha_secret,
                    "response": recaptcha_response,
                }
                siteverify_url = "https://www.google.com/recaptcha/api/siteverify"
                validation_status = requests.post(siteverify_url, data=data)

                assume_user_is_human = validation_status.json().get("success")

                # Logging result
                if assume_user_is_human:
                    self.authenticator.log.info("Passed reCaptcha")
                else:
                    self.authenticator.log.error("Failed reCaptcha")

        if assume_user_is_human:
            user_info = {
                "username": self.get_body_argument("username", strip=False),
                "password": self.get_body_argument("signup_password", strip=False),
                "email": self.get_body_argument("email", "", strip=False),
                "has_2fa": bool(self.get_body_argument("2fa", "", strip=False))
                or self.authenticator.require_2fa,
            }
            username_already_taken = self.authenticator.user_exists(
                user_info["username"]
            )
            user = self.authenticator.create_user(**user_info)
        else:
            username_already_taken = False
            user = None

        # Collect various information for precise (error) messages.
        password = self.get_body_argument("signup_password", strip=False)
        confirmation = self.get_body_argument(
            "signup_password_confirmation", strip=False
        )
        confirmation_matches = password == confirmation
        user_is_admin = user_info["username"] in self.authenticator.admin_users

        # Call helper function from above for precise alert-level and message.
        alert, message = self.get_result_message(
            user,
            assume_user_is_human,
            username_already_taken,
            confirmation_matches,
            user_is_admin,
        )

        otp_secret, user_2fa = "", ""
        if user:
            otp_secret = user.otp_secret
            user_2fa = user.has_2fa

        html = await self.render_template(
            "signup.html",
            ask_email=self.authenticator.ask_email_on_signup,
            result_message=message,
            alert=alert,
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_google=self.authenticator.use_google_libpam,
            two_factor_auth_user=user_2fa,
            two_factor_auth_value=otp_secret,
            two_factor_auth_uri=generate_otp_uri(user.username, otp_secret),
            two_factor_auth_qrcode=generate_otp_qrcode(user.username, otp_secret),
            recaptcha_key=self.authenticator.recaptcha_key,
            tos=self.authenticator.tos,
        )
        self.finish(html)


class AuthorizationAreaHandler(LocalBase):
    """Responsible for rendering the /hub/authorize page."""

    @admin_users_scope
    async def get(self):
        html = await self.render_template(
            "authorization-area.html",
            ask_email=self.authenticator.ask_email_on_signup,
            users=self.db.query(UserInfo).all(),
        )
        self.finish(html)


class ToggleAuthorizationHandler(LocalBase):
    """Responsible for the authorize/[someusername] page,
    which immediately redirects after toggling the
    respective user's authorization status."""

    @admin_users_scope
    async def get(self, slug):
        UserInfo.change_authorization(self.db, slug)
        self.redirect(self.hub.base_url + "authorize#" + slug)


class EmailAuthorizationHandler(LocalBase):
    """Responsible for the confirm/[someusername] validation of
    cryptographic URLs for the self-serve-approval feature."""

    async def get(self, slug):
        """Called on GET requests. The slug is given in the URL after /confirm/.
        It's a long-ish string of letters encoding which user this authorization
        link is for and until when it is valid, cryptographically signed by the
        secret key given in the configuration file. This is done to make the
        approval URL not-reverse-engineer-able."""

        slug_validation_successful = False
        message = "Invalid URL"

        if self.authenticator.allow_self_approval_for:
            try:
                data = EmailAuthorizationHandler.validate_slug(
                    slug, self.authenticator.secret_key
                )
                slug_validation_successful = True
            except ValueError:
                pass

        if slug_validation_successful:
            username = data["username"]
            usr = UserInfo.find(self.db, username)

            if not usr.is_authorized:
                UserInfo.change_authorization(self.db, username)
                message = f"{username} has been authorized!"
            else:
                message = f"{username} was already authorized."

        html = await self.render_template(
            "my_message.html",
            message=message,
        )
        self.finish(html)

    # static method so it can be easily tested without initializate the class
    @staticmethod
    def validate_slug(slug, key):
        """This function makes sure the given slug is
        not expired and has a valid signature."""
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
        dateobj = date(
            int(year_month_day[0]), int(year_month_day[1]), int(year_month_day[2])
        )

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


class Change2FAHandler(LocalBase):
    """Responsible for rendering the /hub/change-otp page where users can add or modify
    2FA for their account. Both on GET requests, when simply navigating to the site,
    and on POST requests, with the data to change the 2FA setting."""

    @web.authenticated
    async def get(self):
        """Rendering on GET requests ("normal" visits)."""

        user = await self.get_current_user()
        userinfo = self.authenticator.get_user(user.name)
        html = await self.render_template(
            "change-2fa.html",
            user_name=userinfo.username,
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_google=self.authenticator.use_google_libpam,
            two_factor_auth_user=userinfo.has_2fa,
            two_factor_auth_value=userinfo.otp_secret,
            two_factor_auth_uri=generate_otp_uri(
                userinfo.username, userinfo.otp_secret
            ),
            two_factor_auth_qrcode=generate_otp_qrcode(
                userinfo.username, userinfo.otp_secret
            ),
        )
        self.finish(html)

    @web.authenticated
    async def post(self):
        """Rendering on POST requests (requests with data attached)."""

        user = await self.get_current_user()
        userinfo = self.authenticator.get_user(user.name)
        password = self.get_body_argument("password", strip=False)
        token = self.get_body_argument("2fa", "", strip=False)

        correct_password = userinfo.is_valid_password(password)
        correct_token = userinfo.is_valid_token(token)

        if not correct_password:
            alert = "alert-danger"
            message = "Your current password was incorrect. Please try again."
        elif not correct_token:
            alert = "alert-danger"
            message = "Your 2FA token was invalid. Please try again."
        else:
            success = self.authenticator.change_2fa(user.name)
            userinfo = self.authenticator.get_user(user.name)
            if success:
                alert = "alert-success"
                action = "ENABLED" if userinfo.has_2fa else "DISABLED"
                message = (
                    "You have successfully " + action + " two factor authentication!"
                )
            else:
                alert = "alert-danger"
                message = "Something went wrong! Please try again."

        html = await self.render_template(
            "change-2fa.html",
            user_name=userinfo.username,
            result_message=message,
            alert=alert,
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_google=self.authenticator.use_google_libpam,
            two_factor_auth_user=userinfo.has_2fa,
            two_factor_auth_value=userinfo.otp_secret,
            two_factor_auth_uri=generate_otp_uri(
                userinfo.username, userinfo.otp_secret
            ),
            two_factor_auth_qrcode=generate_otp_qrcode(
                userinfo.username, userinfo.otp_secret
            ),
        )
        self.finish(html)


class Change2FAAdminHandler(LocalBase):
    """Responsible for rendering the /hub/change-otp/[someusername] page where
    uadmins can modify any user's 2FA setting. Both on GET requests, when simply
    navigating to the site, and on POST requests, with the data to change the
    2FA setting."""

    @admin_users_scope
    async def get(self, user_name):
        """Rendering on GET requests ("normal" visits)."""

        if not self.authenticator.user_exists(user_name):
            raise web.HTTPError(404)

        userinfo = self.authenticator.get_user(user_name)
        html = await self.render_template(
            "change-2fa-admin.html",
            user_name=user_name,
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_user=userinfo.has_2fa,
        )
        self.finish(html)

    @admin_users_scope
    async def post(self, user_name):
        """Rendering on POST requests (requests with data attached)."""
        success = self.authenticator.change_2fa(user_name)
        userinfo = self.authenticator.get_user(user_name)
        if success:
            alert = "alert-success"
            action = "ENABLED" if userinfo.has_2fa else "DISABLED"
            message = (
                f"You have successfully "
                + action
                + " two factor authentication for "
                + user_name
                + "!"
            )
        else:
            alert = "action-danger"
            message = "Something went wrong! Please try again."

        html = await self.render_template(
            "change-2fa-admin.html",
            user_name=user_name,
            result_message=message,
            alert=alert,
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_google=self.authenticator.use_google_libpam,
            two_factor_auth_user=userinfo.has_2fa,
            two_factor_auth_secret=userinfo.otp_secret,
            two_factor_auth_uri=generate_otp_uri(user_name, userinfo.otp_secret),
            two_factor_auth_qrcode=generate_otp_qrcode(user_name, userinfo.otp_secret),
        )
        self.finish(html)


class ChangePasswordHandler(LocalBase):
    """Responsible for rendering the /hub/change-password page where users can change
    their own password. Both on GET requests, when simply navigating to the site,
    and on POST requests, with the data to change the password attached."""

    @web.authenticated
    async def get(self):
        """Rendering on GET requests ("normal" visits)."""

        user = await self.get_current_user()
        userinfo = self.authenticator.get_user(user.name)
        html = await self.render_template(
            "change-password.html",
            user_name=user.name,
            two_factor_auth_user=userinfo.has_2fa,
        )
        self.finish(html)

    @web.authenticated
    async def post(self):
        """Rendering on POST requests (requests with data attached)."""

        user = await self.get_current_user()
        userinfo = self.authenticator.get_user(user.name)
        old_password = self.get_body_argument("old_password", strip=False)
        new_password = self.get_body_argument("new_password", strip=False)
        confirmation = self.get_body_argument("new_password_confirmation", strip=False)
        token = self.get_body_argument("2fa", "", strip=False)

        correct_password = userinfo.is_valid_password(old_password)
        correct_token = userinfo.is_valid_token(token)

        new_password_matches_confirmation = new_password == confirmation

        if not correct_password and correct_token:
            alert = "alert-danger"
            message = "Your current password was incorrect. Please try again."
        elif correct_password and not correct_token:
            alert = "alert-danger"
            message = "Your 2FA code is invalid. Please try again."
        elif not new_password_matches_confirmation:
            alert = "alert-danger"
            message = (
                "Your new password didn't match the confirmation. Please try again."
            )
        else:
            success = self.authenticator.change_password(user.name, new_password)
            if success:
                alert = "alert-success"
                message = "Your password has been changed successfully!"
            else:
                alert = "alert-danger"
                minimum_password_length = self.authenticator.minimum_password_length
                # Error if minimum password length is > 0.
                if minimum_password_length > 0:
                    message = (
                        "Something went wrong!\n"
                        "Be sure your new password has at least"
                        f" {minimum_password_length} characters "
                        "and is not too common."
                    )
                # Error if minimum password length is 0.
                else:
                    message = (
                        "Something went wrong!\n"
                        "Be sure your new password is not too common."
                    )

        html = await self.render_template(
            "change-password.html",
            user_name=user.name,
            result_message=message,
            alert=alert,
            two_factor_auth_user=userinfo.has_2fa,
        )
        self.finish(html)


class ChangePasswordAdminHandler(LocalBase):
    """Responsible for rendering the /hub/change-password/[someusername] page where
    admins can change any user's password. Both on GET requests, when simply
    navigating to the site, and on POST requests, with the data to change the
    password attached."""

    @admin_users_scope
    async def get(self, user_name):
        """Rendering on GET requests ("normal" visits)."""

        if not self.authenticator.user_exists(user_name):
            raise web.HTTPError(404)

        html = await self.render_template(
            "change-password-admin.html",
            user_name=user_name,
        )
        self.finish(html)

    @admin_users_scope
    async def post(self, user_name):
        """Rendering on POST requests (requests with data attached)."""

        new_password = self.get_body_argument("new_password", strip=False)
        confirmation = self.get_body_argument("new_password_confirmation", strip=False)

        new_password_matches_confirmation = new_password == confirmation

        if not new_password_matches_confirmation:
            alert = "alert-danger"
            message = (
                "The new password didn't match the confirmation. Please try again."
            )
        else:
            success = self.authenticator.change_password(user_name, new_password)
            if success:
                alert = "alert-success"
                message = f"The password for {user_name} has been changed successfully"
            else:
                alert = "alert-danger"
                minimum_password_length = self.authenticator.minimum_password_length
                # Error if minimum password length is > 0.
                if minimum_password_length > 0:
                    message = (
                        "Something went wrong!\nBe sure the new password "
                        f"for {user_name} has at least {minimum_password_length} "
                        "characters and is not too common."
                    )
                # Error if minimum password length is 0.
                else:
                    message = (
                        "Something went wrong!\nBe sure the new password "
                        f"for {user_name} is not too common."
                    )

        html = await self.render_template(
            "change-password-admin.html",
            user_name=user_name,
            result_message=message,
            alert=alert,
        )
        self.finish(html)


class LoginHandler(LoginHandler, LocalBase):
    """Responsible for rendering the /hub/login page."""

    def _render(self, login_error=None, username=None, otp_secret=""):
        """For 'normal' rendering."""

        return self.render_template(
            "native-login.html",
            next=url_escape(self.get_argument("next", default="")),
            username=username,
            login_error=login_error,
            custom_html=self.authenticator.custom_html,
            login_url=self.settings["login_url"],
            enable_signup=self.authenticator.enable_signup,
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {"next": self.get_argument("next", "")},
            ),
            two_factor_auth_allow=self.authenticator.allow_2fa
            or self.authenticator.require_2fa,
            two_factor_auth_require=self.authenticator.require_2fa,
            two_factor_auth_google=self.authenticator.use_google_libpam,
            two_factor_auth_value=otp_secret,
            two_factor_auth_uri=generate_otp_uri(username, otp_secret),
            two_factor_auth_qrcode=generate_otp_qrcode(username, otp_secret),
        )

    async def post(self):
        """Rendering on POST requests (requests with data attached)."""

        # parse the arguments dict
        data = {}
        for arg in self.request.arguments:
            data[arg] = self.get_argument(arg, strip=False)

        auth_timer = self.statsd.timer("login.authenticate").start()
        user = await self.login_user(data)
        auth_timer.stop(send=False)

        if user:
            # register current user for subsequent requests to user
            # (e.g. logging the request)
            self._jupyterhub_user = user
            self.redirect(self.get_next_url(user))
        else:
            # identify specific reason for authentication failure
            username = data["username"]
            user = self.authenticator.get_user(username)
            otp_secret = user.otp_secret
            if user is not None:
                if user.is_valid_password(data["password"]):
                    if not user.is_authorized:
                        error = (
                            f"User {username} has not been authorized "
                            "by an administrator yet."
                        )
                    elif self.authenticator.require_2fa and not user.has_2fa:
                        success = self.authenticator.change_2fa(username)
                        user = self.authenticator.get_user(username)
                        otp_secret = user.otp_secret if success else ""
                        error = "This server requires two factor authentication."
                    else:
                        error = "Invalid 2FA token. Please try again."
                else:
                    error = "Invalid password. Please try again."
            else:
                error = f"User {username} does not exist. Please try again."

            html = await self._render(
                login_error=error, username=username, otp_secret=otp_secret
            )
            self.finish(html)


class DiscardHandler(LocalBase):
    """Responsible for the /hub/discard/[someusername] page
    that immediately redirects after discarding a user
    from the database."""

    @admin_users_scope
    async def get(self, user_name):
        user = self.authenticator.get_user(user_name)
        if user is not None:
            if not user.is_authorized:
                # Delete user from NativeAuthenticator db table (users_info)
                user = type("User", (), {"name": user_name})
                self.authenticator.delete_user(user)

                # Also delete user from jupyterhub registry, if present
                if self.users.get(user_name) is not None:
                    self.users.delete(user_name)

        self.redirect(self.hub.base_url + "authorize")
