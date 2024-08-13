import streamlit as st
import googletrans
import speech_recognition as sr
from gtts import gTTS
import pickle
import pygame
import os

# Initialize the recognizer
r = sr.Recognizer()
languages = pickle.load(open('languages.pkl','rb'))
languages=languages.values()
language = st.selectbox(
    "Type or select a Language from the dropdown",
    languages
)
st.empty()

def record_text():
    try:
        # Use the microphone as source for input
        with sr.Microphone() as source:
            # Prepare recognizer to receive input
            r.adjust_for_ambient_noise(source=source, duration=0.2)

            st.write("Listening...")
            # Listens for the user's input
            audio = r.listen(source)

            st.write("Recognizing...")
            # Using Google to recognize audio
            MyText = r.recognize_google(audio)

            return MyText.capitalize()

    except sr.RequestError as e:
        st.write(f"Could not request results; {e}")
        st.write("--------------------------")

    except sr.UnknownValueError:
        st.write("Unknown error occurred")
        st.write("--------------------------")


def translator(text):
    # Create a Translator object for translation
    translator = googletrans.Translator()

    languages=googletrans.LANGUAGES
    for lang_code, lang_name in languages.items():
        if language in lang_name:
            code = lang_code

    # Translate the given text to Hindi (dest="hi")
    translated_text = translator.translate(text, dest=code)

    # Return the translated text
    return translated_text.text



def text_to_speech(text):
    filename = "audio1.mp3"

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Stop the mixer if it's playing any music
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Remove the existing file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    # Convert the text to speech and save the new audio file
    sound = gTTS(text, lang="hi")
    sound.save(filename)

    # Initialize the pygame mixer again
    pygame.mixer.init()

    # Load and play the saved audio file
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        continue


# Streamlit UI
st.title("Voice Translator")
st.write(f"Say something and I'll translate it to {language.capitalize()}!")

if st.button("Start Listening"):

    st.write("--------------------------")
    st.write("Say 'Stop' to stop.")
    st.write("--------------------------")
    while True:
        text = record_text()
        if text:
            st.write("You:", text)

            if text == 'Stop':
                st.write("Stopping...")
                text_to_speech("Stopping...")
                st.write("--------------------------")
                break
            else:
                translated_text = translator(text)
                st.write(f"{language.capitalize()} Translation:", translated_text)
                text_to_speech(translated_text)
                st.write("--------------------------")

