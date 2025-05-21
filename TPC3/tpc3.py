from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import random
import requests
import time
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = 'História de Portugal'
CORS(app)

def query_graphdb(endpoint_url, query):
    headers = {
        'Accept': 'application/json'
    }

    response = requests.get(endpoint_url, params={'query': query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Query failed. Returned code: {}. {}'.format(response.status_code, response.text))
    
endpoint = 'http://localhost:7200/repositories/historiaPT'

query = """ 
    PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    SELECT ?nome ?cognomes
    WHERE {
        ?rei a :Rei.
        ?rei :nome ?nome.
        ?rei :cognomes ?cognomes.
    }
"""


query_result = query_graphdb(endpoint, query)
list_k = []
for r in query_result['results']['bindings']:
    t = {
        'nome': r['nome']['value'].split('#')[-1], 
        'cognome': r['cognomes']['value'].split('#')[-1]
    }

    list_k.append(t)


@app.route('/')
def home():
    session['score'] = 0
    return redirect(url_for('question_type'))

@app.route('/question_type', methods=['GET', 'POST'])
def question_type():
    if request.method == 'POST':
        type = request.form.get('tipo')
        if type == 'quiz':
            return redirect(url_for('generate_question'))
        elif type == 'true_or_false':
            return redirect(url_for('generate_truefalse'))
    return render_template('question_type.html')

@app.route('/quiz', methods=['GET'])
def generate_question():
    king = random.choice(list_k)
    answer = king['cognome']

    options_list = list({r['cognome'] for r in list_k if r['cognome'] != answer})
    wrong_options = random.sample(options_list, min(3, len(options_list)))

    options = wrong_options + [answer]
    random.shuffle(options)

    question = {
        "question": f"Qual é o cognome do Rei {king['nome']}?",
        "options": options,
        "answer": answer
    }
    return render_template('quiz.html', question=question)

@app.route('/quiz', methods=['POST'])
def quiz():
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('answerCorrect')
        
    correct = True if user_answer == correct_answer else False
    session['score'] = session.get('score', 0) + (1 if correct else 0)
    return render_template('result.html', correct=correct, correct_answer=correct_answer, score=session['score']) 


@app.route('/true_or_false', methods=['GET'])
def generate_truefalse():
    king = random.choice(list_k)
    answer = king['cognome']

    # 50% de probabilidade de mostrar a resposta correta ou errada
    if random.choice([True, False]):
        question = f"O cognome do Rei {king['nome']} é '{answer}'."
        right_answer = "True"
    else:
        wrong_options = list({r['cognome'] for r in list_k if r['cognome'] != answer})
        wrong_answer = random.choice(wrong_options)
        question = f"O cognome do Rei {king['nome']} é '{wrong_answer}'."
        right_answer = "False"

    question = {
        "question": question,
        "answer": right_answer
    }

    return render_template('true_or_false.html', question=question)

@app.route('/true_or_false', methods=['POST'])
def truefalse_post():
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('answerCorrect')
    print(user_answer)
    print(correct_answer)   
    correct = True if user_answer == correct_answer else False
    session['score'] = session.get('score', 0) + (1 if correct else 0)
    return render_template('result.html', correct=correct, correct_answer=correct_answer, score=session['score'])

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)