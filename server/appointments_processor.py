from langchain_openai import ChatOpenAI
from response_message import ResponseMessage
# from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from operator import itemgetter
from typing import List
from message import Message
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate




class AppointmentsProcessor:
    @staticmethod
    def process_message(input_message,refactored_message,llm,db):
        query_examples = [
        {
            "input": "I am a Provider Chatting with you and my name is John Smith. Give me the appointments of Manikandan",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, pad.*
                        FROM person_details_default pd
						JOIN patient_appointment_default pad ON pad.patient_id = pd.person_id
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Manikandan%' limit 5 ;
                """
        },
        {
            "input": "I am a Provider Chatting with you and my name is John Smith. Get my appointments on 28 Feb",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'John Smith'
                            AND DATE(appointment_start_time) = '2024-02-28' limit 5;
                """
        },
                {
            "input": "I am a Provider Chatting with you and my name is John Smith. Get my appointments",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'John Smith'
                            AND DATE(appointment_start_time) BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '2 day' limit 5;
                """
        },
        {
            "input": "I am a Provider Chatting with you and my name is John Smith. Give me my today's appointments",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'John Smith'
                            AND DATE(appointment_start_time) = CURRENT_DATE limit 5;
                """
        }
        ]

        example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
        prompt = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=query_examples,
        prefix="You are a Postgres SQL expert. Based on the examples , Given an input question, create a syntactically correct Postgres SQL query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
        suffix="User input: {input}\nSQL query: ",
        input_variables=["input", "top_k", "table_info"],
        )
        #print(prompt.format(input=input_message.message, top_k=10, table_info="person,person_name,concept,concept_name,obs"))
        chain = prompt | llm
        default_message = "I am a Provider and my name is "+ input_message.provider
        final_input=default_message + ". "+ refactored_message
        print("Final Input\n"+ final_input)
        response = chain.invoke({"input":final_input ,"top_k":5,"table_info":"person_details_default,patient_appointment_default"})
        print(response)
        clean_query=response.content
        print(clean_query)
        result=db.run(clean_query)
        answer_prompt = PromptTemplate.from_template(
             """Given the following user question, corresponding SQL query, and SQL result, answer the user question  . Carefully follow the below rules while framing your answer ." 
                - If there are rows in SQL result ,then give the appointment details .
                - If there are no rows in SQL Result , Feel free to say  oh ! & politely say that there no appointments .
                - The column appointment_provider is the doctor assigned for the appointment .
            Question: {question}
            SQL Query: {clean_query}
            SQL Result: {result}
            Answer:"""
        )
        answer_chain = answer_prompt | llm 
        nlp_response = answer_chain.invoke({
            "question": final_input,
            "clean_query": response,
            "result": result
        })
        print(nlp_response)
        return ResponseMessage(nlp_response.content)







