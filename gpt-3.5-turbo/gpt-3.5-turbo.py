# installed python-telegram-bot, openai, flask
import openai as ai
import pprint
import pyttsx3
import speech_recognition as rc
import time
import pyaudio
# from test_speech_rec import write_audio

# recognizer = rc.Recognizer()
# engine = pyttsx3.init()
ai.api_key = ""

# def audio_to_text(filename):
    
#     with rc.AudioFile(filename) as source:
#         audio = recognizer.record(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except:
#         print("Skipping unknown error")
        
# def speak_text(text):
#     print("test_speak_text")
#     engine.say(text)
#     engine.runAndWait()


def gpt_Update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
    

def generate_response(user_text, print_output=False):
    print("debugg_generate_response_text")
    
    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_text
    )

    # # Displaying the output can be helpful if things go wrong
    if print_output:
        print(response)

    # Return the first choice's text
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful IT specialist."
            },
        # {
        #     "role": "system", 
        #     "content": "You are a helpful IT specialist."
        #     },
        # {
        #     "role": "user", 
        #     "content": "My name is Catzilla. I am a software developer."
        #     },
        # {
        #     "role": "assistant", 
        #     "content": "Hey Catzilla"
        #     },
    ]
    
    while True:
        pprint.pprint(messages)
        user_input = input()
        messages = gpt_Update(messages, "system", user_input)
        model_response = generate_response(messages)
        messages = gpt_Update(messages, "assistant", model_response)
        print(model_response)
        print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
