import speech_recognition as sr
import pyaudio
import wave
import pprint
import openai as ai
import pyttsx3
from gtts import gTTS
from playsound import playsound

ai.api_key = "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"

language = 'ru'

CHUNK = 1024 # определяет форму аудио сигнала
FRT = pyaudio.paInt16 # шестнадцатибитный формат задает значение амплитуды
CHAN = 1 # канал записи звука
RT = 44100 # частота 
REC_SEC = 5 #длина записи
OUTPUT = "output.wav"

pao = pyaudio.PyAudio()
my_recogniser = sr.Recognizer()
# engine = pyttsx3.init()


def speech_audio():
    # ЗАПИСЬ АУДИО ФАЙЛА
    # открываем поток для записи
    
    stream = pao.open(format=FRT,channels=CHAN,rate=RT,input=True,frames_per_buffer=CHUNK)
    print("rec")

    # формируем выборку данных фреймов
    frames = []
    for i in range(0, int(RT / CHUNK * REC_SEC)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("done")

    # останавливаем и закрываем поток 
    stream.stop_stream()
    stream.close()
    pao.terminate()

    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(pao.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
    w.close()
    
    # # РАСПОЗНОВАНИЕ АУДИО ФАЙЛА
    sample = sr.AudioFile('output.wav')
    print(type(sample))
    
    with sample as source:
        audiodata = my_recogniser.record(source)
    
    print(type(audiodata))

    try:
        text = my_recogniser.recognize_google(audio_data=audiodata, language="ru-RU")
        print(text)
        return text
    except:
        print("sorry, could not recognise")


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


def text_to_audio(text_val):
    obj = gTTS(text=text_val, lang=language, slow=False)
    obj.save("exam.mp3")
    playsound("exam.mp3")


if __name__ == "__main__":
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful IT specialist."
            },
    ]

    # while True:
    #     # Wait for user to say "genius"
    #     print("Скажешь что-нибудь для AI?")
    #     try:
    #         with sr.Microphone() as source:
    #             audio = my_recogniser.listen(source)
    #             user_input = speech_audio()
    #             messages = gpt_Update(messages, "system", user_input)
    #             model_response = generate_response(messages)
    #             messages = gpt_Update(messages, "assistant", model_response)
            
    #             # ЗДЕСЬ ВОСПРОИЗВЕДЕНИЕ ГОЛОСА
    #             text_to_audio(model_response)
    #             print(model_response)
    #             print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
                    
    #     except Exception as e:
    #             print("An error occurred: {}".format(e))
                    
                    
    pprint.pprint(messages)
        
    # ЗДЕСЬ ЗАПИСЬ ГОЛОСА
    user_input = speech_audio()
    messages = gpt_Update(messages, "system", user_input)
    model_response = generate_response(messages)
    messages = gpt_Update(messages, "assistant", model_response)
       
    # ЗДЕСЬ ВОСПРОИЗВЕДЕНИЕ ГОЛОСА
    text_to_audio(model_response)
        
    print(model_response)
    print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    
    