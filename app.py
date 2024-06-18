from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.question_parser import question_chooser
from utils.team_log import team_log_get_answer
from utils.player_log import player_log_get_answer
from utils.playbyplay import play_by_play_get_answer
from utils.executor import execute_query, extract_sql_query
from utils.answer_parser import get_answer
from flask_socketio import SocketIO
from flask_socketio import send, emit
from utils.player_and_team import player_and_team_log_get_answer



app = Flask(__name__)
CORS(app) 

socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('billy')
def chat(data):
    if 'message' not in data:
        emit('billy', {'response': 'I am sorry, I do not have an answer for that question.',
             'type': 'query', 'status': 'done'})
        return

    message = data['message']

    
    while True:
        try:
            # Call the question_chooser function to get the bucket and question
            bucket, question = question_chooser('openai', message)

            print(f'Bucket: {bucket}')
            print(f'Question: {question}')

            if bucket == 'NoBucket':
                emit('billy', {
                        'response': "I am sorry, I do not have an answer for that question.", 'type': 'answer', 'status': 'done'})
                return

            raw_query = None

            if bucket == 'TeamGameLog':
                raw_query = team_log_get_answer('openai', question)
            elif bucket == 'PlayerGameLog':
                raw_query = player_log_get_answer('openai', question)
            elif bucket == 'PlayByPlay':
                raw_query = play_by_play_get_answer('openai', question)
            elif bucket == 'TeamAndPlayerLog':
                raw_query = player_and_team_log_get_answer('openai', question)

            # Extract the SQL query from the raw_query
            query = extract_sql_query(raw_query)

            emit('billy', {'response': query,
                    'type': 'query', 'status': 'generating'})

            # Execute the SQL query
            result = execute_query(query)

            # If execution reaches here, the query was successful, break the loop
            break

        except Exception as e:
            print(f'Error: {e}. Retrying...')

   

    answer = get_answer('openai', question, query, result)

    answerGenerating = True
    answer_string = ''

    while answerGenerating:
        try:
            next_answer = next(answer)
            answer_string += next_answer
            emit('billy', {'response': answer_string,
                 'type': 'answer', 'status': 'generating'})
        except Exception as e:
            answerGenerating = False
            emit('billy', {'response': answer_string,
                 'type': 'answer', 'status': 'done'})
    return answer_string



@app.route('/chat')
def chat_http(data):
    if 'message' not in data:
        emit('billy', {'response': 'I am sorry, I do not have an answer for that question.',
             'type': 'query', 'status': 'done'})
        return

    message = data['message']

    
    while True:
        try:
            # Call the question_chooser function to get the bucket and question
            bucket, question = question_chooser('openai', message)

            print(f'Bucket: {bucket}')
            print(f'Question: {question}')

            if bucket == 'NoBucket':
                emit('billy', {
                        'response': "I am sorry, I do not have an answer for that question.", 'type': 'answer', 'status': 'done'})
                return

            raw_query = None

            if bucket == 'TeamGameLog':
                raw_query = team_log_get_answer('openai', question)
            elif bucket == 'PlayerGameLog':
                raw_query = player_log_get_answer('openai', question)
            elif bucket == 'PlayByPlay':
                raw_query = play_by_play_get_answer('openai', question)
            elif bucket == 'TeamAndPlayerLog':
                raw_query = player_and_team_log_get_answer('openai', question)

            # Extract the SQL query from the raw_query
            query = extract_sql_query(raw_query)

            emit('billy', {'response': query,
                    'type': 'query', 'status': 'generating'})

            # Execute the SQL query
            result = execute_query(query)

            # If execution reaches here, the query was successful, break the loop
            break

        except Exception as e:
            print(f'Error: {e}. Retrying...')

   

    answer = get_answer('openai', question, query, result)

    answerGenerating = True
    answer_string = ''

    while answerGenerating:
        try:
            next_answer = next(answer)
            answer_string += next_answer
           
        except Exception as e:
            answerGenerating = False
            
    return answer_string



if __name__ == '__main__':
    app.run(port=8080, debug=True)
    socketio.run(app)
