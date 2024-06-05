import streamlit as st
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder, speech_to_text
import tooling1
from process_images_from_array import *

# Initialize OpenAI client
client = OpenAI()

st.header("Convert patient's details to text")

# Option for users to either upload a file or record directly
option = st.radio("Choose an option:", ('Upload Audio File', 'Record Audio', 'Upload handwritten document'))

if 'text_output' not in st.session_state:
    st.session_state['text_output'] = ''

# Function to convert voice to text
def convert_voice_to_text(audio_file):
    transcript = client.audio.translations.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
    )
    return transcript


if option == 'Upload Audio File':
    audio_file = st.file_uploader("Upload an audio file", type=['m4a', 'wav', 'mp3', 'mp4'])
    if audio_file and st.button('Convert Audio to Text'):
        text_output = convert_voice_to_text(audio_file)  # Convert audio file to text
        st.session_state['text_output'] = text_output  # Store text output in session state for later use

        processed_output = tooling1.process_text_from_streamlit(st.session_state['text_output'])

        # Display the processed output in Streamlit
        st.text_area("Processed Output", value=processed_output, height=300)

elif option == 'Record Audio':
    st.write("Record your voice, and play the recorded audio:")
    audio = mic_recorder(start_prompt="Start Recording ⏺️", stop_prompt="Stop Recording ⏹️", key='recorder')
    if audio is not None and 'bytes' in audio:
        # Save the recorded audio to a file
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio['bytes'])  # Write the bytes to a file
        st.success("Audio recorded and saved successfully.")
        # Convert recorded audio to text
        if st.button('Convert Recorded Audio to Text'):
            with open("recorded_audio.wav", "rb") as f:
                text_output = convert_voice_to_text(f)  # Convert recorded audio file to text
                st.session_state['text_output'] = text_output  # Store text output in session state for later use

                processed_output = tooling1.process_text_from_streamlit(st.session_state['text_output'])
                
                # Display the processed output in Streamlit
                st.text_area("Processed Output", value=processed_output, height=300)

elif option == 'Upload handwritten document':
    img_file = st.file_uploader("Upload your document", type=['png', 'jpg', 'jpeg', 'pdf'])
    if img_file and st.button('Convert handwriting to Text'):
        base64_image = encode_image_file(img_file)
        raw_text_output = read_images(base64_image, text_prompt())  # Convert handwritten file to text
        st.session_state['text_output'] = raw_text_output  # Store raw text output in session state for later use
        print(raw_text_output)

        processed_output = tooling1.process_text_from_streamlit(st.session_state['text_output'])

        # Display the processed output in Streamlit
        st.text_area("Processed Output", value=processed_output, height=300)

