# audio and handwriting convertor. Hospitals case
audio convertor to different languages, also returns structured data from voice

The way it works
- you can either upload your audio file or record it or upload your handwriting
- then the system converts the file into text
- based on this you can get a structured output, for example in this example you are getting json contianing some predifined fields
- input can be in any language, output is fixed to english but can be changed to any

Apps and modules:
- app.py: main streamlit app
- process_images: module to process video image from handwritten file
- tooling1: module to process text and give structured output using tools descsribed there
