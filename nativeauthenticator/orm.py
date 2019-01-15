import bcrypt
from jupyterhub.orm import Base

from sqlalchemy import (
    Boolean, Column, Integer, String
)


class UserInfo(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_authorized = Column(Boolean, default=False)

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
