import speech_recognition as sr
import pyaudio
import wave
import pprint

CHUNK = 1024 # определяет форму аудио сигнала
FRT = pyaudio.paInt16 # шестнадцатибитный формат задает значение амплитуды
CHAN = 1 # канал записи звука
RT = 44100 # частота 
REC_SEC = 5 #длина записи
OUTPUT = "output.wav"

pao = pyaudio.PyAudio()
my_recogniser = sr.Recognizer()

# ЗАПИСЬ АУДИО ФАЙЛА
# открываем поток для записи

def write_audio():
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

write_audio()

# # РАСПОЗНОВАНИЕ АУДИО ФАЙЛА
sample = sr.AudioFile('output.wav')
print(type(sample))

# with sample as audio:
#     content = r.record(audio)
#     r.adjust_for_ambient_noise(audio)

with sample as source:
    audiodata = my_recogniser.record(source)
    
print(type(audiodata))

try:
    text = my_recogniser.recognize_google(audio_data=audiodata, language="ru-RU")
    print(text)
except:
    print("sorry, could not recognise")


# r=sr.Recognizer()
# pprint.pprint(sr.Microphone.list_microphone_names())

# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source,duration=1)
#     # r.energy_threshold()
#     print("say anything : ")
#     audio = r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         print(text)
#     except:
#         print("sorry, could not recognise")