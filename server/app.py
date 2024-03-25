from flask import Flask, request, jsonify
from message import Message
from gen_ai import GenAI
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Enable JSON parsing as dictionaries
app.config['JSON_AS_DICT'] = True

@app.route('/bahmni/rest/v1/conversations', methods=["POST"])
def add_guide():
    print("Entered")
    message_data = request.json['message']
    message = Message(message_data)  # Convert JSON data to Message object
    print("Received message:", message.message)
    processed_message = GenAI.process_message(message)
    # Convert the processed message object to JSON
    response = jsonify(message=processed_message.message)
    return response

@app.route('/user')
def hello():
    print("Entered")
    return '<h1>Hello, World!</h1>'


