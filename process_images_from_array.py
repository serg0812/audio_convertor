import base64
import matplotlib as plt 
from base64 import b64decode
import numpy as np
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage


def encode_image_file(image_file):
    ''' Encode uploaded image file '''
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_captioning(img_base64,prompt):
    ''' Image summary '''
    chat = ChatOpenAI(model="gpt-4o",
                      max_tokens=4000)

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text":prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        },
                    },
                ]
            )
        ]
    )
    return msg.content

# Read images, encode to base64 strings, and get image summaries
def read_images(base64_images, prompt):
    image_summaries = []

    # Check if base64_images is a single image or a list of images
    if isinstance(base64_images, str):
        # If it's a single image, process it directly
        img_capt = image_captioning(base64_images, prompt)
        image_summaries.append(img_capt)
    else:
        # If it's a list of images, process each image
        for base64_image in base64_images:
            img_capt = image_captioning(base64_image, prompt)
            image_summaries.append(img_capt)
    
    return image_summaries

def text_prompt():
    prompt ="""
You are given a page, which is handwritten.
You should provide clear text output based on what is written.
Don not hallucinate, provide only the text output.
""" 
    return prompt

