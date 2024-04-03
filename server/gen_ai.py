from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from module_router import ModuleRouter
from vitals_processor import VitalsProcessor
from appointments_processor import AppointmentsProcessor
from diagnosis_processor import DiagnosisProcessor
from global_processor import GlobalProcessor
from personal_details_processor import PersonalDetailsProcessor




class GenAI:

    @staticmethod
    def process_question(input_message,llm):
        if input_message.previous_question is not None and input_message.previous_answer is not None:
            question_prompt = PromptTemplate.from_template(
                """Your a world class chat bot . Based on Context of Previous Question asked by human & corresponding Previous Answer given by you , Check the Current Question and rephrase or elaborate the Current Question based on Previous Question & Answer . If u feel Current Question is unrelated to Previous Question & Answer ,Just return Current Question itself no prefix or suffix.

                Previous Question: {previous_question}
                Previous Answer: {previous_answer}
                Current Question: {current_question}
                New Framed Question:"""
            )
            question_chain = question_prompt | llm 
            nlp_response = question_chain.invoke({
                "previous_question": input_message.previous_question,
                "previous_answer": input_message.previous_answer,
                "current_question": input_message.message
            })
            print("Refactored Message\n"+nlp_response.content)
            return nlp_response.content
        else:
            return input_message.message


    @staticmethod
    def process_message(input_message):
        llm = ChatOpenAI(openai_api_key="")
        db = SQLDatabase.from_uri("postgresql+psycopg2://bahmni-mart:password@localhost:5432/martdb",include_tables=["vitals","person_details_default","patient_appointment_default"])
        print(db.dialect)
        print(db.get_usable_table_names())
        refactored_message=ModuleRouter.process_question(input_message,llm)
        module = ModuleRouter.find_module(input_message,refactored_message,llm)
        if module == "vitals":
            return VitalsProcessor.process_message(input_message,refactored_message,llm,db)
        elif module == "appointments":
            return AppointmentsProcessor.process_message(input_message,refactored_message,llm,db)
        elif module == "diagnosis":
            return DiagnosisProcessor.process_message(input_message,refactored_message,llm,db)
        elif module == "personal":
            return PersonalDetailsProcessor.process_message(input_message,refactored_message,llm,db)
        else:
            return GlobalProcessor.process_message(input_message,refactored_message,llm)
    


