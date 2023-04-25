import os
import re
import shutil
import socket

import bcrypt
import pyotp
from jupyterhub.orm import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import validates


class UserInfo(Base):
    """
    This class represents the information that NativeAuthenticator persists in
    JupyterHub's database.
    """

    __tablename__ = "users_info"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # username should be a JupyterHub username, normalized by the Authenticator
    # class normalize_username function.
    username = Column(String(128), nullable=False)

    # password should be a bcrypt generated string that not only contains a
    # hashed password, but also the salt and cost that was used to hash the
    # password. Since bcrypt can extract the salt from this concatenation, this
    # can be used again during validation as salt.
    password = Column(LargeBinary, nullable=False)

    # is_authorized is a boolean to indicate if the user has been authorized,
    # either by an admin, or by validating via an email for example.
    is_authorized = Column(Boolean, default=False)

    # login_email_sent is boolean to indicate if a self approval email has been
    # sent out, as enabled by having a allow_self_approval_for configuration
    # set.
    login_email_sent = Column(Boolean, default=False)

    # email is a un-encrypted string representing the email
    email = Column(String(128))

    # has_2fa is a boolean that is being set to true if the user declares they
    # want to setup 2fa during sign-up.
    has_2fa = Column(Boolean, default=False)

    # otp_secret (one-time password secret) is given to a user during setup of
    # 2fa. With a shared secret like this, both the user and nativeauthenticator
    # are enabled to generate the same one-time password's, which enables them
    # to be matched against each other.
    otp_secret = Column(String(16))

    def __init__(self, use_google_libpam=False, **kwargs):
        super().__init__(**kwargs)
        self.otp_secret = self.get_otp_secret(use_google_libpam)

    @classmethod
    def find(cls, db, username):
        """
        Find a user info record by username.

        Returns None if no user was found.
        """
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def all_users(cls, db):
        """
        Returns all available user info records.
        """
        return db.query(cls).all()

    @classmethod
    def change_authorization(cls, db, username):
        """
        Toggles the authorization status of a user info record.

        Returns the user info record.
        """
        user = db.query(cls).filter(cls.username == username).first()
        user.is_authorized = not user.is_authorized
        db.commit()
        return user

    def get_otp_secret(self, use_google_libpam):
        """
        Return the existing OTP secret or create a new one if it does not exist.

        This does not modify self.otp_secret.
        """
        if self.has_2fa:
            if not self.otp_secret:
                google_libpam_installed = (
                    True if shutil.which("google-authenticator") else False
                )
                if use_google_libpam and google_libpam_installed:
                    google_auth_file = f"{os.path.expanduser(f'~{self.username}')}/.google_authenticator"
                    if not os.path.exists(google_auth_file):
                        os.system(
                            "google-authenticator"
                            + f" --secret={google_auth_file}"
                            + " --quiet --force --no-confirm"
                            + " --time-based --allow-reuse --window-size=3"
                            + " --rate-limit=3 --rate-time=30"
                        )
                    with open(google_auth_file) as f:
                        otp_secret = f.readline().strip("\n")
                else:
                    otp_secret = pyotp.random_base32()
            else:
                otp_secret = self.otp_secret
        else:
            otp_secret = ""
        return otp_secret

    def is_valid_password(self, password):
        """
        Checks if a provided password hashes to the hash we have stored in
        self.password.

        Note that self.password has been set to the return value of calling
        bcrypt.hashpw(...) before, that returns a concatenation of the random
        salt used and the hashed salt+password combination. So, when we are
        passing self.password back to bcrypt.hashpw(...) as a salt, it is smart
        enough to extract and use only the salt that was originally used.
        """
        return self.password == bcrypt.hashpw(password.encode(), self.password)

    @validates("email")
    def validate_email(self, key, address):
        """
        Validates any attempt to set the email field of a user info record.
        """
        if not address:
            return
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", address)
        return address

    def is_valid_token(self, token):
        """
        Validates a time-based one-time password (TOTP) as generated by a user's
        2fa application against the TOTP generated locally by the pyotp
        module. Assuming the user generated a TOTP with a common shared one-time
        password secret (otp_secret), these passwords should match.
        """
        if self.has_2fa:
            host = socket.gethostname()
            otp_uri = f"otpauth://totp/{self.username}@{host}?secret={self.otp_secret}&issuer={host}"
            totp = pyotp.parse_uri(otp_uri)
            return totp.verify(token)
        return True
