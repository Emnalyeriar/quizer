import os, csv, random


def get_questions(session):
    with open('data/quiz.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        session['questions'] = list(reader)
        
        session['questions'] = [
            [string.decode('utf-8') for string in question]
            for question in session['questions']
        ]
