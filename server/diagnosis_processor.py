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





class DiagnosisProcessor:

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
    def process_message(input_message,refactored_message,llm,db):

        query_examples = [
        {
            "input": "Can u provide the diagnosis of Sharukh Khan",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, pd.age as patient_age,bpad.bed_number as patient_bed_number ,CONCAT(vd.coded_diagnosis, vd.non_coded_diagnosis) AS diagnosis
						from person_details_default pd
                        JOIN visit_diagnoses vd on vd.patient_id = pd.person_id
                        JOIN patient_visit_details_default pvdd on pvdd.visit_id=vd.visit_id
                        LEFT JOIN bed_patient_assignment_default bpad  on bpad.patient_id=pd.person_id 
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Sharukh Khan%' and bpad.date_stopped IS NULL and pvdd.visit_end_date IS NULL;
                """
        },
        {
            "input": "What are the diagnosis of Kishore Kumar ",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, pd.age as patient_age,bpad.bed_number as patient_bed_number ,CONCAT(vd.coded_diagnosis, vd.non_coded_diagnosis) AS diagnosis
						from person_details_default pd
                        JOIN visit_diagnoses vd on vd.patient_id = pd.person_id
                        JOIN patient_visit_details_default pvdd on pvdd.visit_id=vd.visit_id
                        LEFT JOIN bed_patient_assignment_default bpad  on bpad.patient_id=pd.person_id 
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Sharukh Khan%' and bpad.date_stopped IS NULL and pvdd.visit_end_date IS NULL;
                """
        },
        {
            "input": "Give me the diagnosis of patient in bed ICU2",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, pd.age as patient_age,bpad.bed_number as patient_bed_number ,CONCAT(vd.coded_diagnosis, vd.non_coded_diagnosis) AS diagnosis
						from person_details_default pd
                        JOIN visit_diagnoses vd on vd.patient_id = pd.person_id
                        JOIN patient_visit_details_default pvdd on pvdd.visit_id=vd.visit_id
                        LEFT JOIN bed_patient_assignment_default bpad  on bpad.patient_id=pd.person_id 
                        WHERE bpad.bed_number = 'ICU2'  and bpad.date_stopped IS NULL and pvdd.visit_end_date IS NULL;
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
        response = chain.invoke({"input":refactored_message ,"top_k":10,"table_info":"vitals,person_details_default"})
        #print(response)
        clean_query=response.content
        print(clean_query)
        result=db.run(clean_query)
        answer_prompt = PromptTemplate.from_template(
             """Given the following user question, corresponding SQL query, and SQL result, answer the user question . Carefully follow the below rules while framing your answer .
                 - If there are no rows in SQL Result , Feel free to say  'Oops !' & politely that there are No patient available for criteria of your question.
                 - If SQL result has either only 1 row or more than one row but patient name in all rows are same , Go ahead & provide diagnosis for the patient " 
                 - If there are more than 1 distinct patient name in SQL Result ,Say Aah ! & politely say that there are more than one patient for your ask & return all of their name , age & bednumber alone & ask for which patient they need diagnosis " 
            Question: {question}
            SQL Query: {clean_query}
            SQL Result: {result}
            Answer:"""
        )
        answer_chain = answer_prompt | llm 
        nlp_response = answer_chain.invoke({
            "question": refactored_message,
            "clean_query": response,
            "result": result
        })
        print(nlp_response)
        return ResponseMessage(nlp_response.content)