from sqlalchemy.orm import (
    declarative_base,
    relationship,
    mapped_column,
    Mapped
)

from sqlalchemy import (
    Column,
    UniqueConstraint,
    func,
    DateTime,
    Table,
    ForeignKey,
)

from DB.db_engine import url_engine
from DB.db_conn import DBConnection

Base = declarative_base()

question_answer_association_table = Table(
    "question_answer_association_table",
    Base.metadata,
    Column("question_id", ForeignKey("question.id"), primary_key=True, nullable=False),
    Column("answers_id", ForeignKey("answers.id"), primary_key=True,  nullable=False),
    UniqueConstraint("question_id", "answers_id", name="question_answer_association_unique"),
)


class Answers(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    questions: Mapped[list['Questions']] = relationship(
        secondary=question_answer_association_table,
        back_populates="answers"
    )


class Photos(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Questions(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey('photo.id'))
    correct_answer_id: Mapped[int] = mapped_column(ForeignKey('answers.id'))
    answers: Mapped[list['Answers']] = relationship(
        secondary=question_answer_association_table,
        back_populates='questions'
    )


class Users(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    date_joined: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


if __name__ == '__main__':
    db_connector = DBConnection(db_url=url_engine)
    db_connector.create_tables(Base)
