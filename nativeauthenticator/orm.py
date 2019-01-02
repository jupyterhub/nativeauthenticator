from sqlalchemy import (
    Column, ForeignKey, Integer,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False),

    @classmethod
    def find(cls, db, name):
        """Find a user info record by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()
