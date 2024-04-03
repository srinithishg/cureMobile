from flask import Flask,request,jsonify
from message import Message
from gen_ai import GenAI
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/bahmni/rest/v1/conversations', methods=["POST"])
def add_guide():
    print("Entered")
    print(request)
    message_data = request.json['message']
    previous_question = request.json.get('previous_question', None)
    previous_answer = request.json.get('previous_answer', None)
    provider = request.json.get('provider', None)
    request_object = Message(message_data,previous_question,previous_answer,provider)  # Convert JSON data to Message object
    print("Received message:", request_object.message)
    processed_message = GenAI.process_message(request_object)
    # Convert the processed message object to JSON
    response = jsonify(message=processed_message.message)
    return response

@app.route('/home')
def hello():
    print("Entered")
    return '<h1>Hello, World!</h1>'


