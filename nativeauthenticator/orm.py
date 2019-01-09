from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @classmethod
    def find(cls, db, username):
        """Find a user info record by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.username == username).first()
