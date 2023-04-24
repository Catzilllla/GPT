#installed python-telegram-bot, openai, flask
import openai as ai
import pyttsx3
import speech_recognition as rc
import time
import pyaudio


# устанавливаем API-ключ OpenAI
ai.api_key = "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"

engine = pyttsx3.init()

def audio_to_text(filename):
    recognizer = rc.Recognizer()
    with rc.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skiping unknown error')

def generate_response(user_text, print_output=False):
    print("generate_response_text")
    completions = ai.Completion.create(
        engine="text-davinci-003",
        prompt=user_text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text

def speak_text(text):
    print("test_speak_text")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("test")
    while True:
        #Wait for user to say "genius"
        print("Say 'Genius' to start recording your question")
        with rc.Microphone() as source:
            recognizer = rc.Recognizer()
            audio = recognizer.listen(source)
            try:
                trancription = recognizer.recognize_google(audio)
                if trancription.lower() == "genius":
                    
                    #Record audio
                    filename = "input.wav"
                    print("Say your question . . . ")
                    with rc.Microphone() as source:
                        recognizer = rc.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                        
                    #Transcribe audio to text
                    text = audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        #Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")
                        
                        #Read response using text-to-speech
                        speak_text(response)
                        
            except Exception as e:
                print("An error occured: {}".format(e))





