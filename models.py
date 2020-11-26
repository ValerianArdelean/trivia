from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://valerian@localhost:5432/trivia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(),nullable=False)
    difficulty = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.id} {self.question} {self.difficulty}'
