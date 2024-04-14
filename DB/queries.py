from DB.db_conn import DBConnection
from DB.db_engine import url_engine

from DB.models import (
    Users,
    Photos
)


class UserActivity:
    def __init__(self):
        self.manager = DBConnection(db_url=url_engine)

    def create_user(self, request):
        with self.manager as session:
            session.add(Users(**request))

            session.commit()

    def count_users(self):
        with self.manager as session:
            data = session.query(Users).count()
            return data


class PhotoActivity:

    def __init__(self):
        self.manager = DBConnection(db_url=url_engine)

    def create_photo(self, request):
        with self.manager as session:
            session.add(Photos(**request))

            session.commit()

    def get_photos(self):
        with self.manager as session:
            data = session.query(Photos).all()
            return data
