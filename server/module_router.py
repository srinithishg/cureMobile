from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field


class ModuleRouter:
    @staticmethod
    def find_module(input_message,refactored_message,llm):
        few_shot_examples = [
        {
            "question": "Give me the vital's of kennedy ?",
            "module_key": "vitals"
        }, 
        {
            "question": "Get me the temperature of kumar ?",
            "module_key": "vitals"
        }, 
        {
            "question": "Blood pressure of vishnu ?",
            "module_key": "vitals"
        },
        {
            "question": "what are the vitals patient in bed ICU2 ?",
            "module_key": "vitals"
        },
        {
            "question": "Give me my appointment's today?",
            "module_key": "appointments"
        },
        {
            "question": "Get me my appointment's ?",
            "module_key": "appointments"
        },
        {
            "question": "How does my day look like ?",
            "module_key": "appointments"
        },
        {
            "question": "How does my week look like ?",
            "module_key": "appointments"
        },
        {
            "question": "What are my free time today ?",
            "module_key": "appointments"
        },
        {
            "question": "diagnosis of karthick ?",
            "module_key": "diagnosis"
        },
        {
            "question": "Get me the details of karna ?",
            "module_key": "personal"
        },
        {
            "question": "Get me the details of patient in bed B-1 ?",
            "module_key": "personal"
        },
        {
            "question": "what are some latest advancements in oncology treatment ?",
            "module_key": "global"
        },
        {
            "question":"get me some latest research papers in medical field",
            "module_key":"global"
        },
        {
            "question":"tell me a joke ",
            "module_key":"global"
        }
    ]
        example_prompt = PromptTemplate(
            input_variables=["question", "module_key"], template="Question: {question}\n{module_key}"
        )
        prompt = FewShotPromptTemplate(
        examples=few_shot_examples,
        example_prompt=example_prompt,
        prefix="You are a Module expert . Based on the examples , Given an input question,return either either of these keys 'vitals' , 'appointments' , 'diagnosis' ,'personal' , 'global'",
        suffix="Question: {input}",
        input_variables=["input"],
        )
        chain = prompt | llm
        print("Input Message in find module "+refactored_message)
        response = chain.invoke({"input":refactored_message})
        print("Module Info ")
        print(response)
        return response.content
    
    @staticmethod
    def process_question(input_message,llm):
        few_shot_examples=[
        {
            "previous_question": "Give me the temperature of Jhon Peter ?",
            "previous_answer": "The Temperature vital of Jhon Peter are as follows : Temparature : 37 degree celcius",
            "current_question": "Can u give his complete vitals",
            "rephrased_question":"Give me the complete vital's of Jhon Peter"
        },
        {
            "previous_question": "Get me the vitals of Sindu Reddy",
            "previous_answer": "Sindu Reddy is the only patient available for the criteria of your question.\nPatient Name: Kennedy King\nPatient Age: 89\nPatient Bed Number: 49792\n\nVitals:\n- Temperature: 98\n- Heart Rate: 97\n- Respiratory Rate: 21\n- Systolic BP: 110\n- Diastolic BP: 90\n- Oxygen Saturation: 35\n- Position: Standing",
            "current_question": "Give me today's appointments",
            "rephrased_question":"Give me today's appointments"
        },
        {
            "previous_question": "Get me the vitals of Sindu Reddy",
            "previous_answer": "Sindu Reddy is the only patient available for the criteria of your question.\nPatient Name: Kennedy King\nPatient Age: 89\nPatient Bed Number: 49792\n\nVitals:\n- Temperature: 98\n- Heart Rate: 97\n- Respiratory Rate: 21\n- Systolic BP: 110\n- Diastolic BP: 90\n- Oxygen Saturation: 35\n- Position: Standing",
            "current_question": "Can u you get her appointments ",
            "rephrased_question":"Give me the appointments of patient Sindu Reddy"
        },
        {
            "previous_question": "Get me the diagnosis of Sindu Reddy",
            "previous_answer": "Sindu Reddy is the only patient available for the criteria of your question.\nPatient Name: Kennedy King\nPatient Age: 89\nPatient Bed Number: 49792\n\nVitals:\n- Temperature: 98\n- Heart Rate: 97\n- Respiratory Rate: 21\n- Systolic BP: 110\n- Diastolic BP: 90\n- Oxygen Saturation: 35\n- Position: Standing",
            "current_question": "How does my day look like ?",
            "rephrased_question":"How does my day look like ?"
        },
        {
            "previous_question": "Get my appointments for today ",
            "previous_answer": "- Appointment Details:\n   1. Patient ID: 49790\n      Patient Name: 52508\n      Provider: Test Doctor\n      Start Time: 2024-03-29 11:30\n      End Time: 2024-03-29 12:00\n      Department: Orthopaedics\n      Type: Surgery - Orthopaedics\n      Status: Scheduled\n      Location: CURE Ethiopia\n      Additional Notes: Scheduled\n\n(Note: This is today's appointment for Test Doctor)",
            "current_question": "Get me vital of patient in bed number ICU1",
            "rephrased_question":"Get me vital of patient in bed number ICU1"
        },
        {
            "previous_question": "Get me the vitals of Devaraj Durairaj",
            "previous_answer": "Devaraj Durairaj is the only patient available for the criteria of your question.\nPatient Name: Kennedy King\nPatient Age: 89\nPatient Bed Number: 49792\n\nVitals:\n- Temperature: 98\n- Heart Rate: 97\n- Respiratory Rate: 21\n- Systolic BP: 110\n- Diastolic BP: 90\n- Oxygen Saturation: 35\n- Position: Standing",
            "current_question": "Can u you get his latest diagnosis ",
            "rephrased_question":"Give me the latest diagnosis details of patient Devaraj Durairaj"
        },
        {
            "previous_question": "vital of Sharma ",
            "previous_answer": "Aah! There are more than one patient for your inquiry. \nHere are the details of the patients with name, age, and bed number:\n1. Name: Vishal Sharma, Age: 78, Bed Number: 49592\n2. Name: Anushka Sigh Sharma, Age: 89, Bed Number: 49792\n3. Name: Rohit Sharma, Age: 34, Bed Number: ICU1\n\nPlease specify which patient's vitals you would like to know.",
            "current_question": "Rohit Sharma",
            "rephrased_question":"What are the vitals of Rohit Sharma"
        },
        {
            "previous_question": "Get me the vital's of haasan ",
            "previous_answer": "Aah! There are more than one patient for your inquiry. \nHere are the details of the patients with name, age, and bed number:\n1. Name: Kamal haasan, Age: 78, Bed Number: Not available \n2. Name: Vaani haasan , Age: 34, Bed Number: ICU1\n\nPlease specify which patient's vitals you would like to know.",
            "current_question": "Kamal Haasan",
            "rephrased_question":"What are the vitals of Kamal Haasan"
        },
        {
            "previous_question": "Get me the diagnosis of Karthick",
            "previous_answer": "Aah! There are more than one patient for your ask. \nPatient 1 - Name: Murali Karthick, Age: 31, Bed Number: ICU5\nPatient 2 - Name: Dinesh Karthick, Age: 34, Bed Number: B-1\n\nPlease specify for which patient you need the diagnosis.",
            "current_question": "The one in ICU5 ",
            "rephrased_question":"Give me the diagnosis of patient in bed ICU5"
        }
        ]
        if input_message.previous_question is not None and input_message.previous_answer is not None:
            example_prompt = PromptTemplate.from_template(
                """
                Previous Question: {previous_question}
                Previous Answer: {previous_answer}
                Current Question: {current_question}
                Rephrased Question: {rephrased_question}
                """
            )
            prompt = FewShotPromptTemplate(
                example_prompt=example_prompt,
                examples=few_shot_examples,
                prefix="Your a world class chat bot . Based on Context of Previous Question asked by human & corresponding Previous Answer given by you , Check the Current Question and rephrase or elaborate the Current Question based on Previous Question & Answer . If u feel Current Question is unrelated to Previous Question & Answer ,Just return Current Question itself no prefix or suffix.",
                suffix= 
                """
                Previous Question: {previous_question}
                Previous Answer: {previous_answer}
                Current Question: {current_question}
                Rephrased Question:
                """,
                input_variables=["previous_question", "previous_answer", "current_question"],
            )
            chain = prompt | llm
            question=input_message.message
            question_response = chain.invoke({"previous_question":input_message.previous_question,"previous_answer":input_message.previous_answer,"current_question":question})
            print("Refactored Message \n "+question_response.content)
            return question_response.content
        else:
            return input_message.message
    
