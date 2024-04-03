from langchain_core.prompts import ChatPromptTemplate
from response_message import ResponseMessage


class GlobalProcessor:
    @staticmethod
    def process_message(input_message,refactored_message,llm):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class medical chat bot . Give answer not more than 50 words "),
            ("user", "{input}")
        ])
        chain = prompt | llm 
        response=chain.invoke({"input": refactored_message})
        print("Global Processor Response ")
        print(response)
        return ResponseMessage(response.content)