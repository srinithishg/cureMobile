# from langchain_openai import ChatOpenAI
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



class GenAI:


    @staticmethod
    def process_message(input_message):
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2, max_tokens=1024,anthropic_api_key="")
        db = SQLDatabase.from_uri("mysql+mysqlconnector://openmrs-user:password@localhost:3306/openmrs",include_tables=["person","person_name","concept","concept_name","obs"])
        print(db.dialect)

        chain = create_sql_query_chain(llm, db)
        response = chain.invoke({"question": input_message.message + "Assume You are World class SQL Generator . Return SQL Query alone provided  concept names are Diastolic Blood Pressure, Systolic Blood Pressure , Arterial Blood Oxygen Saturation (Pulse Oximeter) , Body Position , Temperature , Respiratory Rate . you can ignore voided data and locale other than en . Patient name are stored in person_name table"})
        clean_query=response.replace("SQLQuery:\n", "")
        print(clean_query)
        result=db.run(clean_query)
        answer_prompt = PromptTemplate.from_template(
             """Given the following user question, corresponding SQL query, and SQL result,  .

            Question: {question}
            SQL Query: {clean_query}
            SQL Result: {result}
            Answer:"""
        )
        answer_chain = answer_prompt | llm 
        nlp_response = answer_chain.invoke({
            "question": input_message.message,
            "clean_query": clean_query,
            "result": result
        })
        print(nlp_response)
        return Message(nlp_response.content)
        

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