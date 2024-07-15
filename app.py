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
from utils.perplexity import ask_expert
from flask import request
import dotenv
import os
from pymongo import MongoClient

dotenv.load_dotenv()




app = Flask(__name__)
CORS(app) 

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
try:
    client = MongoClient(MONGO_DB_URL)
    db = client['chatbot']
    print("Connected to MongoDB")
except Exception as e:
    print("Could not connect to MongoDB", e)


socketio = SocketIO(app, cors_allowed_origins='*')




@socketio.on('billy')
def chat(data):
    if 'message' not in data:
        emit('billy', {'response': 'I am sorry, I do not have an answer for that question.',
             'type': 'query', 'status': 'done'})
        print('No message or ip or session')
        return
    print("Message:")
    print(data['message'])

    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


    message = data['message']['message']

    session = data['message']['session']

    print(f'IP: {ip}')
    print(f'Session: {session}')

    
    while True:
        try:
            # Call the question_chooser function to get the bucket and question
            bucket, question = question_chooser('anthropic', message)

            print(f'Bucket: {bucket}')
            print(f'Question: {question}')
            
            if bucket =='Conversation':
                emit('billy', {'response':question, 'type': 'answer', 'status': 'done'})
                return

            if bucket == 'NoBucket':
                if question == '':
                    emit('billy', {
                        'response': "I am sorry, I do not have an answer for that question.", 'type': 'answer', 'status': 'done'})
                    return

                emit('billy', {
                        'response':question, 'type': 'answer', 'status': 'done'})
                return
            
            if bucket == 'ExpertAnalysis':
                emit('billy', {'response': '',
                               'type': 'query', 'status': 'generating'})
                generator = ask_expert(question)
                answer = ''
                generating_answer = True
                while generating_answer:
                    try:
                        next_answer = next(generator)
                        answer += next_answer
                        emit('billy', {'response': next_answer,
                             'type': 'answer', 'status': 'generating'})
                    except Exception as e:
                        generating_answer = False
                        emit('billy', {'response': next_answer,
                             'type': 'answer', 'status': 'done'})
                        
                return answer

            raw_query = None

            if bucket == 'TeamGameLog':
                raw_query = team_log_get_answer('anthropic', question)
            elif bucket == 'PlayerGameLog':
                raw_query = player_log_get_answer('anthropic', question)
            elif bucket == 'PlayByPlay':
                raw_query = play_by_play_get_answer('anthropic', question)
            elif bucket == 'TeamAndPlayerLog':
                raw_query = player_and_team_log_get_answer(
                    'anthropic', question)
            
            print(f'Raw Query: {raw_query}')
                
            if 'error' and 'cannot' in raw_query.lower():
                emit('billy', {'response': '',
                               'type': 'query', 'status': 'generating'})
                generator = ask_expert(question)
                answer = ''
                generating_answer = True
                while generating_answer:
                    try:
                        next_answer = next(generator)
                        answer += next_answer
                        emit('billy', {'response': next_answer,
                             'type': 'answer', 'status': 'generating'})
                    except Exception as e:
                        generating_answer = False
                        emit('billy', {'response': next_answer,
                             'type': 'answer', 'status': 'done'})

                return answer


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

            try:

                print('Inserting into MongoDB')

                collection = db['correct']
                collection.insert_one(
                    {"question": question, "query": query, "answer": answer_string, "ip": ip, "session": session})
                print("Inserted into MongoDB")
            except Exception as e:
                print("Could not insert into MongoDB", e)



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
                raw_query = team_log_get_answer('anthropic', question)
            elif bucket == 'PlayerGameLog':
                raw_query = player_log_get_answer('anthropic', question)
            elif bucket == 'PlayByPlay':
                raw_query = play_by_play_get_answer('anthropic', question)
            elif bucket == 'TeamAndPlayerLog':
                raw_query = player_and_team_log_get_answer(
                    'anthropic', question)

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

    app.run(port=33507, debug=True)


    socketio.run(app)
