import bcrypt
import dbm
import os
from datetime import datetime
from jupyterhub.auth import Authenticator
from pathlib import Path

from sqlalchemy import inspect
from tornado import gen
from traitlets import Bool, Integer, Unicode

from .handlers import (
    AuthorizationHandler, ChangeAuthorizationHandler, ChangePasswordHandler,
    ChangePasswordAdminHandler, LoginHandler, SignUpHandler,
)
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
    enable_signup = Bool(
        config=True,
        default_value=True,
        help=("Allows every user to registry a new account")
    )
    open_signup = Bool(
        config=True,
        default_value=False,
        help=("Allows every user that made sign up to automatically log in "
              "the system without needing admin authorization")
    )
    ask_email_on_signup = Bool(
        False,
        config=True,
        help="Asks for email on signup"
    )
    import_from_firstuse = Bool(
        False,
        config=True,
        help="Import users from FirstUse Authenticator database"
    )
    firstuse_db_path = Unicode(
        'passwords.dbm',
        config=True,
        help="""
        Path to store the db file of FirstUse with username / pwd hash in
        """
    )
    delete_firstuse_db_after_import = Bool(
        config=True,
        default_value=False,
        help="Deletes FirstUse Authenticator database after the import"
    )
    allow_2fa = Bool(
        False,
        config=True,
        help=""
    )

    def __init__(self, add_new_table=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.login_attempts = dict()
        if add_new_table:
            self.add_new_table()

        if self.import_from_firstuse:
            self.add_data_from_firstuse()

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
        username = self.normalize_username(data['username'])
        password = data['password']

        user = self.get_user(username)
        if not user:
            return

        if self.allowed_failed_logins:
            if self.is_blocked(username):
                return

        validations = [
            user.is_authorized,
            user.is_valid_password(password)
        ]
        if user.has_2fa:
            validations.append(user.is_valid_token(data.get('2fa')))

        if all(validations):
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
                self.COMMON_PASSWORDS = set(f.read().splitlines())
        return password in self.COMMON_PASSWORDS

    def is_password_strong(self, password):
        checks = [len(password) >= self.minimum_password_length]

        if self.check_common_password:
            checks.append(not self.is_password_common(password))

        return all(checks)

    def get_user(self, username):
        return UserInfo.find(self.db, self.normalize_username(username))

    def user_exists(self, username):
        return self.get_user(username) is not None

    def create_user(self, username, pw, **kwargs):
        username = self.normalize_username(username)

        if self.user_exists(username):
            return

        if not self.is_password_strong(pw) or \
           not self.validate_username(username):
            return

        if not self.enable_signup:
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
        user = self.get_user(username)
        user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        self.db.commit()

    def validate_username(self, username):
        invalid_chars = [',', ' ']
        if any((char in username) for char in invalid_chars):
            return False
        return super().validate_username(username)

    def get_handlers(self, app):
        native_handlers = [
            (r'/login', LoginHandler),
            (r'/signup', SignUpHandler),
            (r'/authorize', AuthorizationHandler),
            (r'/authorize/([^/]*)', ChangeAuthorizationHandler),
            (r'/change-password', ChangePasswordHandler),
            (r'/change-password/([^/]+)', ChangePasswordAdminHandler),
        ]
        return native_handlers

    def delete_user(self, user):
        user_info = self.get_user(user.name)
        if user_info is not None:
            self.db.delete(user_info)
            self.db.commit()
        return super().delete_user(user)

    def delete_dbm_db(self):
        db_path = Path(self.firstuse_db_path)
        db_dir = db_path.cwd()
        db_name = db_path.name
        db_complete_path = str(db_path.absolute())

        # necessary for BSD implementation of dbm lib
        if os.path.exists(os.path.join(db_dir, db_name + '.db')):
            os.remove(db_complete_path + '.db')
        else:
            os.remove(db_complete_path)

    def add_data_from_firstuse(self):
        with dbm.open(self.firstuse_db_path, 'c', 0o600) as db:
            for user in db.keys():
                password = db[user].decode()
                new_user = self.create_user(user.decode(), password)
                if not new_user:
                    error = '''User {} was not created. Check password
                               restrictions or username problems before trying
                               again'''.format(user)
                    raise ValueError(error)

        if self.delete_firstuse_db_after_import:
            self.delete_dbm_db()
