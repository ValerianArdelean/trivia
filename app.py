from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALACHEMY_DATABASE_URI'] = 'postgresql://valerian@localhost:5432/trivia'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return jsonify({'message':'maaa'})
