# message.py

class Message:
    def __init__(self, message,previous_question,previous_answer,provider):
        self.message = message
        self.previous_question = previous_question
        self.previous_answer = previous_answer
        self.provider=provider
