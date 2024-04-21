from DB.db_conn import DBConnection
from DB.db_engine import url_engine

from DB.models import (
    Users,
    Photos,
    Answers,
    Questions,
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


class QuestionActivity:

    def __init__(self):
        self.manager = DBConnection(db_url=url_engine)

    def create_photo(self, data: str):
        with self.manager as session:
            session.add(Photos(name=data))
            session.commit()

            photo = session.query(Photos).filter(Photos.name == data).first()
            return photo.id

    def get_photos(self):
        with self.manager as session:
            data = session.query(Photos).all()
            return data

    def create_answer(self, data: list):
        with self.manager as session:
            for obj in data:
                answer = session.query(Answers).filter(Answers.name == obj).first()

                if answer:
                    continue

                session.add(Answers(name=obj))
                session.commit()

    def search_answer(self, data: list):
        with self.manager as session:
            answers = []

            for obj in data:
                answer = session.query(Answers).filter(Answers.name == obj).first()
                answers.append(answer)

            return answers

    def create_question(self, data: dict):
        with self.manager as session:
            self.create_answer(data=data.get('answer'))

            answers = self.search_answer(data.get('answer'))
            correct_answer = self.search_answer(data.get('correct_answer'))
            photo = self.create_photo(data.get('photo'))

            session.add(Questions(
                photo_id=photo,
                correct_answer_id=correct_answer[0].id,
            ))
            session.commit()

            question = session.query(Questions).filter(Questions.photo_id == photo).first()

            for answer in answers:
                question.answers.append(answer)
                session.commit()

    def get_answers_question(self, photo_name):
        with self.manager as session:
            photo = session.query(Photos).filter(Photos.name == photo_name).first()
            question = session.query(Questions).filter(Questions.photo_id == photo.id).first()

            answers = []

            for answer in question.answers:
                answers.append(answer.name)

            return answers

    def get_correct_answer(self, photo_id, user_answer):
        with self.manager as session:
            question = session.query(Questions).filter(Questions.photo_id == photo_id).first()
            correct_answer_id = question.correct_answer_id

            correct_answer = session.query(Answers).filter(Answers.id == correct_answer_id).first()

            if user_answer == correct_answer.name:
                return correct_answer.name

            return




