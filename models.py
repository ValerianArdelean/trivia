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


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String())
    difficulty = db.Column(db.Integer)
    cat = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f'{self.id} {self.question} {self.answer} {self.difficulty} {self.cat}'

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

    def rollback():
        db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty,
            'category': self.cat
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    question = db.relationship("Questions", backref='category', lazy='dynamic')

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

    def rollback():
        db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            #'question': self.question
        }
