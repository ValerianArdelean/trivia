from flask import Flask, jsonify
from models import setup_db, Questions


app = Flask(__name__)
setup_db(app)


@app.route('/')
def index():
    questions = str(Questions.query.all())
    return jsonify({'questions': questions})
