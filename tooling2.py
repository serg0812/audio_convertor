from langchain.agents import AgentExecutor
from langchain.tools import StructuredTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function 
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import json

class ClientDetails(BaseModel):
    """
    Pydantic arguments schema for person details
    """
    name: str = Field(description="Name of the person")
    age: str = Field(description="Age of the person")
    birthplace: str = Field(description="Place where the person was born")
    sex: str = Field(description="Describes patient's gender")
    history: str = Field(description="Describes previous conditions") 
    issue: str = Field(description="Describes the issue") 
    condition: str = Field(description="Describes the current patients condition") 

def get_client_details(name: str, age: str, birthplace: str, sex: str, history: str, issue: str, condition: str) -> str:
    response = ClientDetails(name=name, age=age, birthplace=birthplace, sex=sex, history=history, issue=issue, condition=condition)
    
    return response.json()

# Define a main function to process text from Streamlit
def process_text_from_streamlit(text_output: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o",
        response_format={"type": "json_object"} #odd bug, resolves below via prompt
    )

    tools = [
        StructuredTool.from_function(func=get_client_details, args_schema=ClientDetails, description="Function to get person details")
    ]
#    llm_with_tools = llm.bind(functions=[function_calling.convert_to_openai_function(t) for t in tools])
    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])
# in any of the prompt you have to specify that response should be in json!!! otherwise you will get an error
    system_init_prompt = "You are a doctor handling the records of your patient"
    user_init_prompt = f"""
    Return only the data relevant to tools, skip the rest.
    Return in a json format.
    If there is no data you MUST not invent anything and leave the fields empty
    Do not hallucinate, provide only the output which is related to what is provided
    You should run each function just once
    Here is your data: {text_output}""" 

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_init_prompt),
        ("user", user_init_prompt),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = (
        {"input": lambda x: x["input"],
         "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke({"input": text_output})
    return response.get("output")
