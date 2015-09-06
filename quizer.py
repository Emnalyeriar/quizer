# -*- coding: utf-8 -*-
"""
Quizer - a quiz application created with Flask.
"""

import os, csv, random, string, time
from flask import Flask, session, request, render_template, redirect, url_for
import helpers

# create app and initialize config
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('QUIZER_SETTINGS', silent=True)


ANSWER_IDS = {str(i): l for i, l in enumerate('ABCDE')}


@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    """
    Welcome page - quiz info and username form.
    """
    username = session.get('username')

    if request.method == 'POST':
        if not username:
            username = session['username'] = request.form['username']
        if username:
            return redirect(url_for('question_page'))

    return render_template('welcome.html', username=username)


@app.route('/pytanie', methods=['GET', 'POST'])
def question_page():
    """
    Quiz question page - show question, handle answer.
    """
    if not session.get('questions'):
        helpers.get_questions(session)
        session['points'] = 0;

    if len(session['questions']) <= 3:
        del session['questions']
        return redirect(url_for('result_page'))

    if session.get('right_answer') and 'answer' in request.form:
        delta = time.time() - session['time']
        if ANSWER_IDS.get(request.form['answer']) == session['right_answer']:
            if delta > 30:
                session['points'] += 1
            elif 10 <= delta <= 30:
                session['points'] += 2
            elif delta < 10:
                session['points'] += 3

    questions = session['questions']
    answers = questions.pop(questions.index(random.choice(questions)))
    question = answers.pop(0)
    session['right_answer'] = answers.pop(len(answers)-1)
    session['time'] = time.time()

    return render_template('question.html',
        answers=answers,
        question=question,
    )


@app.route('/wynik')
def result_page():
    """
    Last page - show results.
    """
    return render_template('result.html',
        result=session['points'],
    )


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080'))
    )
