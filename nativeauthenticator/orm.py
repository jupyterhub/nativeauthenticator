import bcrypt
from jupyterhub.orm import Base, User

from sqlalchemy import (
    Column, ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship


class UserInfo(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @classmethod
    def find(cls, db, username):
        """Find a user info record by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.username == username).first()

    def is_valid_password(self, password):
        encoded_pw = bcrypt.hashpw(password.encode(), self.password)
        return encoded_pw == self.password
