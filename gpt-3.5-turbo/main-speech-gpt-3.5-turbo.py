# installed python-telegram-bot, openai, flask
import openai as ai
import pyttsx3
import speech_recognition as rc
import time
import pyaudio

import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

ai.api_key = ""
recognizer = rc.Recognizer()
engine = pyttsx3.init()

def audio_to_text(filename):

    with rc.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")

def generate_response(user_text, print_output=False):
    print("debugg_generate_response_text")
    
    response = ai.ChatChatCompletion.creat(
        model="gpt-3.5-turbo",
        messages=user_text
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(response)

    # Return the first choice's text
    return response['choices'][0]['message']['content']

def speak_text(text):
    print("test_speak_text")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("test")
    while True:
        # Wait for user to say "genius"
        print("Say 'Genius' to start recording your question")
        with rc.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                r = recognizer.recognize_google(audio)
                if r.lower() == "genius":
                    
                    # Record audio
                    filename = "input.wav"
                    print("Say your question . . . ")
                    with rc.Microphone() as source:
                        recognizer = rc.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                        
                    # Transcribe audio to text
                    text = audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")
                        
                        # Read response using text-to-speech
                        speak_text(response)
                        
            except Exception as e:
                print("An error occurred: {}".format(e))





