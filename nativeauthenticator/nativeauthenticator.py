import bcrypt
import os
from datetime import datetime
from jupyterhub.auth import Authenticator

from sqlalchemy import inspect
from tornado import gen
from traitlets import Bool, Integer

from .handlers import (AuthorizationHandler, ChangeAuthorizationHandler,
                       ChangePasswordHandler, SignUpHandler)
from .orm import UserInfo


class NativeAuthenticator(Authenticator):

    COMMON_PASSWORDS = None
    check_common_password = Bool(
        config=True,
        default=False,
        help=("Creates a verification of password strength "
              "when a new user makes signup")
    )
    minimum_password_length = Integer(
        config=True,
        default=1,
        help=("Check if the length of the password is at least this size on "
              "signup")
    )
    allowed_failed_logins = Integer(
        config=True,
        default=0,
        help=("Configures the number of failed attempts a user can have "
              "before being blocked.")
    )
    seconds_before_next_try = Integer(
        config=True,
        default=600,
        help=("Configures the number of seconds a user has to wait "
              "after being blocked. Default is 600.")
    )
    open_signup = Bool(
        config=True,
        default=False,
        help=("Allows every user that made sign up to automatically log in "
              "the system without needing admin authorization")
    )
    ask_email_on_signup = Bool(
        config=True,
        default=False,
        help="Asks for email on signup"
    )

    def __init__(self, add_new_table=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.login_attempts = dict()
        if add_new_table:
            self.add_new_table()

    def add_new_table(self):
        inspector = inspect(self.db.bind)
        if 'users_info' not in inspector.get_table_names():
            UserInfo.__table__.create(self.db.bind)

    def add_login_attempt(self, username):
        if not self.login_attempts.get(username):
            self.login_attempts[username] = {'count': 1,
                                             'time': datetime.now()}
        else:
            self.login_attempts[username]['count'] += 1
            self.login_attempts[username]['time'] = datetime.now()

    def can_try_to_login_again(self, username):
        login_attempts = self.login_attempts.get(username)
        if not login_attempts:
            return True

        time_last_attempt = datetime.now() - login_attempts['time']
        if time_last_attempt.seconds > self.seconds_before_next_try:
            return True

        return False

    def is_blocked(self, username):
        logins = self.login_attempts.get(username)

        if not logins or logins['count'] < self.allowed_failed_logins:
            return False

        if self.can_try_to_login_again(username):
            return False
        return True

    def successful_login(self, username):
        if self.login_attempts.get(username):
            self.login_attempts.pop(username)

    @gen.coroutine
    def authenticate(self, handler, data):
        username = data['username']
        password = data['password']

        user = UserInfo.find(self.db, username)
        if not user:
            return

        if self.allowed_failed_logins:
            if self.is_blocked(username):
                return

        if user.is_authorized and user.is_valid_password(password):
            self.successful_login(username)
            return username

        self.add_login_attempt(username)

    def is_password_common(self, password):
        common_credentials_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'common-credentials.txt'
        )
        if not self.COMMON_PASSWORDS:
            with open(common_credentials_file) as f:
                self.COMMON_PASSWORDS = f.read().splitlines()
        return password in self.COMMON_PASSWORDS

    def is_password_strong(self, password):
        checks = [len(password) > self.minimum_password_length]

        if self.check_common_password:
            checks.append(not self.is_password_common(password))

        return all(checks)

    def get_or_create_user(self, username, pw, **kwargs):
        user = UserInfo.find(self.db, username)
        if user:
            return user

        if not self.is_password_strong(pw) or \
           not self.validate_username(username):
            return

        encoded_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        infos = {'username': username, 'password': encoded_pw}
        infos.update(kwargs)
        if username in self.admin_users or self.open_signup:
            infos.update({'is_authorized': True})

        try:
            user_info = UserInfo(**infos)
        except AssertionError:
            return

        self.db.add(user_info)
        self.db.commit()
        return user_info

    def change_password(self, username, new_password):
        user = UserInfo.find(self.db, username)
        user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.db.commit()

    def validate_username(self, username):
        invalid_chars = [',', ' ']
        if any((char in username) for char in invalid_chars):
            return False
        return super().validate_username(username)

    def get_handlers(self, app):
        native_handlers = [
            (r'/signup', SignUpHandler),
            (r'/authorize', AuthorizationHandler),
            (r'/authorize/([^/]*)', ChangeAuthorizationHandler),
            (r'/change-password', ChangePasswordHandler),
        ]
        return super().get_handlers(app) + native_handlers

    def delete_user(self, user):
        user_info = UserInfo.find(self.db, user.name)
        self.db.delete(user_info)
        self.db.commit()
        return super().delete_user(user)
