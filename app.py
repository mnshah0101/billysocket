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

app = Flask(__name__)
CORS(app) 

socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('billy')
def chat(data):
    if 'message' not in data:
        return jsonify({'error': 'Invalid message'}), 400
    message = data['message']
    # Call the question_chooser function to get the bucket and question
    bucket, question = question_chooser('openai', message)

    if bucket == 'NoBucket':
        response = {
            'response': f"I'm sorry, I don't have an answer for that question."
        }
        return jsonify(response), 200

    raw_query = None
    
    if bucket == 'TeamGameLog':
        raw_query = team_log_get_answer('openai', question)
    elif bucket =='PlayerGameLog':
        raw_query = player_log_get_answer('openai', question)
    elif bucket == 'PlayByPlay':
        raw_query = play_by_play_get_answer('openai', question)

    # Extract the SQL query from the raw_query
    query = extract_sql_query(raw_query)

    emit('billy', {'response': query, 'type': 'query', 'status': 'generating'})

    # Execute the SQL query
    result = execute_query(query)



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
            emit('billy', {'response': answer_string, 'type': 'answer', 'status': 'done'})
    return
        


    
   

if __name__ == '__main__':
    app.run(port=8080, debug=True)
    socketio.run(app)
