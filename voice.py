import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3

# Configure Google's Generative AI
GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Function to record audio and convert to text
def record_and_convert():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now:")
        audio = r.listen(source, timeout=5)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Function to generate AI response
def generate_ai_response(input_text):
    response = model.generate_content(input_text)
    return response.text

# Function to perform text-to-speech
def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Set the first voice
    engine.setProperty('rate', 150)  # Adjust speaking rate
    engine.say(text)
    engine.runAndWait()

st.title("Speech Recognition and AI Response with TTS")

if st.button("Record and Process"):
    st.write("Recording...")
    input_text = record_and_convert()
    st.write(f"Recognized Text: {input_text}")

    if input_text and input_text != "Could not understand the audio" and not input_text.startswith("Could not request results"):
        response_text = generate_ai_response(input_text)
        st.write(f"AI Response: {response_text}")
        text_to_speech(response_text)  # Automatically play AI response
    else:
        st.error(input_text)
