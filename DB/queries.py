from sqlalchemy.orm import selectinload

from DB.db_conn import DBConnection
from DB.db_engine import url_engine

from DB.models import (
    Users,
    Photos,
    Answers,
    Questions,
    question_answer_association_table
)


class UserActivity:
    def __init__(self):
        self.manager = DBConnection(db_url=url_engine)

    def create_user(self, request):
        with self.manager as session:
            user = session.query(Users).filter(Users.username == request.get('username')).first()

            if user:
                return

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


with DBConnection(db_url=url_engine) as session:
    photos = [
        'e34.png',
        'e36.png',
        'e90.png',
    ]

    # question = session.query(Questions).one()
    #
    # data = question.answers
    #
    # for i in data:
    #     print(i.name)

    # answer = session.query(Answers).first()
    #
    # data = answer.questions
    #
    # print(data[0].id)
