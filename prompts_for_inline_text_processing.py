def text_in_image_processing_prompt():
    prompt ="""
You are an expert extracting text form the images using OCR.
You will be provided with the image, which contains text in it. 
You are required to provide for each encountered text to provide:
- text itself
- left x coordinate of the block text is located in
- left y coordinate of the block text is located in
- height of the block text is located in
- width of the block text is located in
- background colour in RGB format of the block text is located in
- font size of the text in the block
Return the data in a form of an array:
[[text,x,y,w,h,bg_colour,font_size]]
Return only data, dont put any explanation
""" 
    return prompt
def single_text_to_sentence(image_summaries, text_found):
    prompt = f"""
You have just parsed the image and returned this data {image_summaries}.
This is great output but the coordinates are not correct. 
I have run through the same image and recieved this array {text_found}.
I need you to adjust your data based on the array and return new array in the format of the array I provided.
New array should have your texts, but the coordinates should from the array I got.
For example: you have ['one man',23,23,100,20,E2EAF1,12]
Array has: ['one', 50, 37, 84, 29]['man', 144, 37, 93, 29]
You should merge two array elements together in this case and return ['one man',50,37,121,29,E2EAF1,12]
Where the entry from the array contain single word or part of single word, match it with your data and return your text with array coordinates
Text size and colour should taken from your data.
Return the new array in this format:
[[text,x,y,w,h,bg_colour,font_size]]
Return only data, dont put any explanation
"""