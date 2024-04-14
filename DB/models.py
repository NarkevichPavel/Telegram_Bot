from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    func,
    DateTime
)

from DB.db_engine import url_engine
from DB.db_conn import DBConnection

Base = declarative_base()


class Photos(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=True)


class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True, unique=True)
    date_joined = Column(DateTime, default=func.now())


if __name__ == '__main__':
    db_connector = DBConnection(db_url=url_engine)
    db_connector.create_tables(Base)
