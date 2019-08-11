import base64
import bcrypt
import os
import re
from jupyterhub.orm import Base

import onetimepass
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import validates


class UserInfo(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    password = Column(LargeBinary, nullable=False)
    is_authorized = Column(Boolean, default=False)
    email = Column(String(128))
    has_2fa = Column(Boolean, default=False)
    otp_secret = Column(String(16))

    def __init__(self, **kwargs):
        super(UserInfo, self).__init__(**kwargs)
        if not self.otp_secret:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @classmethod
    def find(cls, db, username):
        """Find a user info record by name.
        Returns None if not found"""
        return db.query(cls).filter(cls.username == username).first()

    def is_valid_password(self, password):
        """Checks if a password passed matches the
        password stored"""
        encoded_pw = bcrypt.hashpw(password.encode(), self.password)
        return encoded_pw == self.password

    @classmethod
    def change_authorization(cls, db, username):
        user = db.query(cls).filter(cls.username == username).first()
        user.is_authorized = not user.is_authorized
        db.commit()
        return user

    @validates('email')
    def validate_email(self, key, address):
        if not address:
            return
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        address)
        return address

    def is_valid_token(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)
