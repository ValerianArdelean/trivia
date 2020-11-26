# models module for Trivia app
from flask_sqlalchemy import SQLAlchemy
import os


'''initiate SQLAlchemy to be used for clases declarations'''


db = SQLAlchemy()


'''app-db configurations need it to be in a function,
   so app parameter can be used as atribute in 'app' module'''


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)


'''declaring db scheema'''


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String())
    difficulty = db.Column(db.Integer)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # initialize in memory the table
    def __init__(self, id, question, answer, category, difficulty):
        self.id = id
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    # creating attributes for db objects
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def sesion_close(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    questions = db.relationship("Question", backref='categories')

    # initialize in memory the table
    def __init__(self, id, type, questions):
        self.id = id
        self.type = type
        self.questions = questions

    # creating attributes for db objects
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def sesion_close(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
