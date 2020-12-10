from flask import Flask, jsonify, abort, request
from models import setup_db, db, Questions, Category
import sys
import math
import random


app = Flask(__name__)
setup_db(app)



@app.route('/categories')
def categories():
    response = {}
    categories = {}
    try:
        cat = Category.query.all()
    except Exception as e:
        abort(500)
    for a in cat:
        categories.update({a.id: a.type})
    response['categories'] = categories
    response['success'] = True
    response['total_categories'] = len(cat)
    return jsonify(response)


@app.route('/questions')
def questions():

    qpp = 5
    p = request.args.get('page')
    if p :
        page = int(p)
    else:
        page = 1

    response = {}

    category = Category.query.all()
    cat = [str(b.format()) for b in category]
    response['categories'] = cat

    questions = Questions.query.all()
    ques = [str(a.format()) for a in questions]
    response['questions'] = ques[(page-1)*qpp:qpp*page]

    response['total_questions'] = len(questions)
    response['total_pages'] = math.ceil(len(questions)/qpp)
    response['page'] = page
    response['qpp'] = qpp
    response['success'] = True
    return jsonify(response)


# POST QUESTIONS
@app.route('/questions', methods=['POST'])
def post_questions():
    error = False
    response = {}
    body = request.get_json()
    if body:
        quest=body.get('question')
        answer=body.get('answer')
        difficulty=body.get('difficulty')
        cat = body.get('cat')
        if quest and answer and difficulty:
            try:
                question = Questions(id=None, question=quest, answer=answer,
                                     difficulty=difficulty, cat=cat)
                question.insert()
                response['new question id'] = question.id
            except:
                error = True
                question.rollback()
                print(sys.exc_info())
                abort(500)
            finally:
                question.sesion_close()
        else:
            print(sys.exc_info())
            abort(400)
    else:
        print(sys.exc_info())
        abort(400)
    response['success']=True
    return jsonify(response)


@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    error = False
    response = {}
    question = Questions.query.get(id)
    if question:
        try:
            question.delete()
            response['success'] = True
        except:
            error = True
            question.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            question.sesion_close()
    else:
        abort(404)
    return jsonify(response)


@app.route('/categories/<int:id>/questions')
def ques_by_cat(id):
    response = {}
    if id:
        ques_by_cat = Questions.query.filter_by(cat=id).all()
        if ques_by_cat:
            response['questions'] = [a.format() for a in ques_by_cat]
            response['total_questions'] = len([a.format() for a in ques_by_cat])
            response['currentCategory'] = id
            response['success'] = True
        else:
            abort(404)
    else:
        abort(404)
    return jsonify(response)


@app.route('/quizzes', methods=['POST'])
def quizz():
    response = {}

    previous_question = int(request.json['previous_questions'])
    response['previous_questions'] = previous_question

    quiz_category = request.json['quiz_category']['id']
    if quiz_category:
        ques_by_cat = Questions.query.filter_by(cat=quiz_category).filter(Questions.id != previous_question).all()
    else:
        ques_by_cat = Questions.query.filter(Questions.id != previous_question).all()
    question = random.choice(ques_by_cat)
    response['question'] = question.format()
    response['quiz_cat'] = quiz_category
    response['success'] = True
    return jsonify(response)


@app.route('/questions/<int:id>', methods=['PATCH'])
def updateEDIT_questions(id):
    response = {}
    body = request.get_json()
    if body:
        quest=body.get('question')
        answer=body.get('answer')
        difficulty=body.get('difficulty')
        category=body.get('category')
        question = Questions.query.get(id)
        if question:
            if quest:
                question.question = quest
                response['updated'] = 'question have been updated'
            elif answer :
                question.answer = answer
                response['updated'] = 'answer have been updated'
            elif difficulty:
                question.difficulty = int(difficulty)
                response['updated'] = 'difficulty have been updated'
            else:
                abort(400)
            try:
                question.update()
                response['success'] = True
            except Exception as e:
                print(sys.exc_log())
                abort(500)
            finally:
                question.sesion_close()
        else:
            abort(405)
    else:
        abort(400)
    return jsonify(response)


@app.route('/categories/<int:id>', methods=['PATCH'])
def updateEDIT_categories(id):
    response = {}
    body = request.get_json()
    if body:
        category = Category.query.get(id)
        if category:
            type = body.get('type')
            question = body.get('question')
            if type:
                category.type = type
                response['updated'] = 'type have been updated'
            elif question :
                category.question = question
                response['updated'] = 'question have been updated'
            else:
                abort(400)
            try:
                category.update()
                response['success'] = True
            except Exception as e:
                print(sys.exc_log())
                abort(500)
            finally:
                category.sesion_close()
        else:
            abort(405)
    else:
        abort(400)
    return jsonify(response)


# POST CATEGORIES
@app.route('/categories', methods=['POST'])
def post_quizes():
    error = False
    response = {}
    body = request.get_json()
    if body:
        type = body.get('type')
        if type:
            try:
                cat = Category(id=None, type=type)
                cat.insert()
                response['success'] = True
                response['id'] = cat.id
                response['category'] = cat.type
            except :
                error = True
                print(sys.exc_info())
                cat.rollback()
                abort(500)
            finally:
                cat.sesion_close()
        else:
            print(sys.exc_info())
            abort(400)
    else:
        print(sys.exc_info())
        abort(400)
    return jsonify(response)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(401)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

@app.errorhandler(403)
def forbiden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbiden'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(405)
def method_now_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405


@app.errorhandler(422)
def unprocesable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocesable Entity'
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server Error'
    }), 500
