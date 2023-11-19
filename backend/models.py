from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """ Creates the base class that inherit DeclarativeBase which
    which allows for ORM and our database structure to be created.
    
    Returns: None
    """

class User(Base):
    __tablename__ = "user"

    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)