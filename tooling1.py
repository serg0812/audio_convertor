from openai  import OpenAI # for calling the OpenAI API
import json
def get_client_details(text):
    client = OpenAI()
    system_prompt = f"""
    You are a doctor, processsing patient's records recorded ealier
    Return only the data relevant to tools, skip the rest.
    You record only these details:
    name: str = Field(description="Name of the person")
    age: str = Field(description="Age of the person")
    birthplace: str = Field(description="Place where the person was born")
    gender: str = Field(description="Describes patient's gender")
    history: str = Field(description="Describes previous conditions") 
    issue: str = Field(description="Describes the issue") 
    condition: str = Field(description="Describes the current patients condition") 
    The format the data should be returned in is the following, example
    [
    Name: John Doe,
    age: 43,
    birthplace: London,
    gender: male,
    history: had COVID 2 years ago,
    issue: Has a headeachke, 
    condition: 38 degrres temperature, cough
    ]
    As you are returning json, you have to change square brackets to curly brackets
    Return only the data relevant to the above, skip the rest.
    If there is no data for the keys you MUST not invent anything and return the fields empty
    You MUST provide the output in english, if the input is in another language - translate it into English
    Do not hallucinate, provide only the output which is related to what is provided
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"Thats your records to go through: {text}"}
        ]
        )
    temp_text=completion.choices[0].message.content.strip()
    obj= temp_text.strip("```json").strip("```").strip()
    rating=json.loads(obj)

    return rating

