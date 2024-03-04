from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Optional
from langchain.chains.openai_functions import (
    create_openai_fn_chain, create_structured_output_chain)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.tools import StructuredTool

class ClientDetails(BaseModel):
    """
    Pydantic arguments schema for person details
    """
    name: str = Field(description="Name of the person")
    age: str = Field(description="Age of the person")
    location: str = Field(description="Place where the person is located")

class CarDetails(BaseModel):
    """
    Pydantic arguments for car details
    """
    oem: str = Field(description="car manufacturer name e.g. BMW, Mercedes")
    model: str = Field(description="model details e.g. BMW 523")
    year: str = Field(description="Year when the car was manufactured")

def get_client_details(name: str, age: str, location: str) -> str:
    response = ClientDetails(name=name, age=age, location=location)
    
    return response.json()

def get_car_details(oem: str, model: str, year: str) -> str:
    response = CarDetails(oem=oem, model=model, year=year)
    
    return response.json()

# Define a main function to process text from Streamlit
def process_text_from_streamlit(text_output: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4-0125-preview",
        response_format={"type": "json_object"}
    )

    tools = [
        StructuredTool.from_function(func=get_client_details, args_schema=ClientDetails, description="Function to get person details"),
        StructuredTool.from_function(func=get_car_details, args_schema=CarDetails, description="Function to get car details")
    ]
    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    system_init_prompt = "You are an expert in getting information about people"
    user_init_prompt = f"Find all details about the person and their car and return the output in json this is the detailed text description: {text_output}"

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
