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
from langchain.memory import ChatMessageHistory




class GenAI:

    @staticmethod
    def process_question(input_message,llm):
        if input_message.previous_question is not None and input_message.previous_answer is not None:
            question_prompt = PromptTemplate.from_template(
                """Carefully study following Previous Question,& corresponding Previous Answer given by you , relate the Current Question to Previous Question & Previous Answer context. If u feel Previous Question & Previous Answer is unrelated to  Current Question just Current Question itself. In case u return Current Question ,  Omit any prefix or suffix.

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
            print(nlp_response)
            return nlp_response.content
        else:
            return input_message.message


    @staticmethod
    def process_message(input_message):
        llm = ChatOpenAI(openai_api_key="")
        #db = SQLDatabase.from_uri("mysql+mysqlconnector://openmrs-user:password@localhost:3306/openmrs",include_tables=["person","person_name","concept","concept_name","obs"])
        # print(db.dialect)
        # query_examples = [
        # {
        #     "input": "Give me the vitals of patient Jhon ",
        #     "query": """SELECT p.person_id, concat(pn.given_name,' ',pn.family_name) as patient_name,
        #                 MAX(CASE WHEN cn.name = 'Diastolic Blood Pressure' THEN o.value_numeric END) AS diastolic_bp,
        #                 MAX(CASE WHEN cn.name = 'Systolic Blood Pressure' THEN o.value_numeric END) AS systolic_bp,
        #                 MAX(CASE WHEN cn.name = 'Arterial Blood Oxygen Saturation (Pulse Oximeter)' THEN o.value_numeric END) AS spo2,
        #                 MAX(CASE WHEN cn.name = 'Body Position' THEN cn2.name END) AS body_position,
        #                 MAX(CASE WHEN cn.name = 'Temperature' THEN o.value_numeric END) AS temperature,
        #                 MAX(CASE WHEN cn.name = 'Respiratory Rate' THEN o.value_numeric END) AS resp_rate
        #                 FROM person p
        #                 JOIN person_name pn ON p.person_id = pn.person_id
        #                 JOIN obs o ON p.person_id = o.person_id
        #                 JOIN concept_name cn ON o.concept_id = cn.concept_id AND cn.locale = 'en'
        #                 LEFT JOIN concept_name cn2 ON o.value_coded = cn2.concept_id AND cn2.locale = 'en'
        #                 WHERE CONCAT(pn.given_name,' ',pn.family_name) like '%Jhon%' AND o.voided = 0
        #                 GROUP by person_id,patient_name;
        #         """
        # }
        # ]
        # example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
        # prompt = FewShotPromptTemplate(
        # example_prompt=example_prompt,
        # examples=query_examples,
        # prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
        # suffix="User input: {input}\nSQL query: ",
        # input_variables=["input", "top_k", "table_info"],
        # )
        # print(prompt.format(input=input_message.message, top_k=10, table_info="person,person_name,concept,concept_name,obs"))
        # chain = prompt | llm 
        # response=chain.invoke({"input":input_message.message,"top_k":10,"table_info":"person,person_name,concept,concept_name,obs"})

        db = SQLDatabase.from_uri("postgresql+psycopg2://bahmni-mart:password@localhost:5432/martdb",include_tables=["vitals","person_details_default","patient_appointment_default"])
        print(db.dialect)
        print(db.get_usable_table_names())
        refactored_message=GenAI.process_question(input_message,llm)
        query_examples = [
        {
            "input": "Give me the appointments of Jhon - Logged-In Provider=Test Doctor ",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, pad.*
                        FROM person_details_default pd
						JOIN patient_appointment_default pad ON pad.patient_id = pd.person_id
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Jhon%' ;
                """
        },
        {
            "input": "Get my appointments on 28 Feb - Logged-In Provider=Test Doctor",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'Test Doctor'
                            AND DATE(appointment_start_time) = '2024-02-28';
                """
        },
                {
            "input": "Get my appointments  - Logged-In Provider=Test Doctor",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'Test Doctor'
                            AND DATE(appointment_start_time) BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '2 day';
                """
        },
        {
            "input": "Give me today's appointments  - Logged-In Provider=Test Doctor",
            "query": """SELECT *
                            FROM patient_appointment_default
                            WHERE appointment_provider = 'Test Doctor'
                            AND DATE(appointment_start_time) = CURRENT_DATE;
                """
        },
        {
            "input": "I want the vitals of patient Julius Ceaser - Logged-In Provider=Test Doctor",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, latest_v.*
                        FROM person_details_default pd
                        JOIN (
                            SELECT v1.*
                            FROM vitals v1
                            JOIN (
                                SELECT patient_id, MAX(obs_datetime) AS latest_timestamp
                                FROM vitals
                                GROUP BY patient_id
                            ) v2 ON v1.patient_id = v2.patient_id AND v1.obs_datetime = v2.latest_timestamp
                        ) AS latest_v ON pd.person_id = latest_v.patient_id
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Julius Ceaser%' ;
                """
        },
        {
            "input": "Vishal Kumar Sharma's Vital's please - Logged-In Provider=Test Doctor",
            "query": """SELECT REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') AS patient_name, latest_v.*
                        FROM person_details_default pd
                        JOIN (
                            SELECT v1.*
                            FROM vitals v1
                            JOIN (
                                SELECT patient_id, MAX(obs_datetime) AS latest_timestamp
                                FROM vitals
                                GROUP BY patient_id
                            ) v2 ON v1.patient_id = v2.patient_id AND v1.obs_datetime = v2.latest_timestamp
                        ) AS latest_v ON pd.person_id = latest_v.patient_id
                        WHERE REPLACE(TRIM(CONCAT(pd.given_name, ' ', pd.middle_name, ' ', pd.family_name)), '  ', ' ') ILIKE '%Vishal Kumar Sharma%' ;
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

        system = """Double check the user's {dialect} query for common mistakes, including:
        - Whenever you identify a name in question , check if name exists in alteast one of  given_name,middle_name & family_name columns or combination of these columns in person_details_default.
        - Whenver possible add names in your queries.
        - Always Strictly return SQL query alone . no prefix or suffix.
        If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

        Output the final SQL query only."""
        validation_prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", "{query}")]
        ).partial(dialect=db.dialect)
        validation_chain = validation_prompt | llm | StrOutputParser()

        full_chain = {"query": chain} | validation_chain
        response = chain.invoke({"input":refactored_message + " - Logged-In Provider=" + input_message.provider ,"top_k":10,"table_info":"vitals,person_details_default,patient_appointment_default"})
        print(response)
        clean_query=response.content
        print(clean_query)
        result=db.run(clean_query)
        answer_prompt = PromptTemplate.from_template(
             """Given the following user question, corresponding SQL query, and SQL result, Provide an answer  . If there are more than one row in SQL Result with different names , Instead of returning an answer , clarify for which name they need an answer. 

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
        demo_ephemeral_chat_history = ChatMessageHistory()
        demo_ephemeral_chat_history.add_user_message(input_message.message)
        demo_ephemeral_chat_history.add_ai_message(nlp_response)
        print(demo_ephemeral_chat_history.messages)
        return ResponseMessage(nlp_response.content)
        

#print(db.get_table_info())




# class Table(BaseModel):
#     """Table in SQL database."""

#     name: str = Field(description="Name of table in SQL database.")
#     table_names = "\n".join(db.get_usable_table_names())
#     system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
# The tables are: {table_names}
# Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
    
# table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
# table_chain.invoke({"input": "How many patients total patients are there"})


# def get_tables() -> List[str]:
#     tables = []
#     tables.extend(["patient"])
#     return tables


# query_chain = create_sql_query_chain(llm, db)
# # Convert "question" key to the "input" key expected by current table_chain.
# table_chain = {"input": itemgetter("question")} | get_tables
# # Set table_names_to_use using table_chain.
# full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain

# query = full_chain.invoke(
#     {"question": "What is the total count of patients "}
# )
# print(query)

# template = """ Based on schema below , give query ,. 
# {schema}

# Question : {question}
# SQL Query : 
# """

# prompt = ChatPromptTemplate.from_template(template)

# def get_schema(_):
#     return db.get_table_info()

# sql_chain= (
#     RunnablePassthrough.assign(schema=get_schema)
#     | prompt
#     | llm
#     | StrOutputParser
# )

# print(sql_chain.invoke ({"question":"How many patients are there ?"}))






# response = chain.invoke({"question": "How many patients are there , which can be got from patient table"})
# print(response)

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are World class Medical Assistant Bot who can answer everything on medical field not more 50 words"),
#     ("user", "{input}")
# ])

# chain = prompt | llm 

# print(chain.invoke({"input": "what are the risk factors for hypertension"}))


# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are world class Medical Assistant ChatBot."),
#     ("user", "{input}")
# ])
# chain = prompt | llm 

# print(chain.invoke({"input": "what are the risk of hypertension"}))
    


