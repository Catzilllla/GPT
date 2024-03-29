import openai as ai
from config import HELP_COMMANDS, hello_list, OPEN_AI_KEY
from config import fun_startup
from config import disp_bot, init_bot
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, File
from bot_keyboard import start_keyboard
from pathlib import Path
import speech_recognition as rc
import pyglet


recognizer = rc.Recognizer()
ai.api_key = OPEN_AI_KEY
messages  = [
    {"role": "system", "content": "You are a programming assistant at Proghunter.ru, helping users with Python and JavaScript programming with popular frameworks."},
]


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


@disp_bot.message_handler(commands=['help'])
async def help_mess(message: types.Message) -> None:
    await message.answer(text=HELP_COMMANDS,
                         parse_mode='HTML')
    await message.delete()


@disp_bot.message_handler(commands=['start'])
async def start_mess(message: types.Message) -> None:
    await message.answer(text=str(
                         f'{hello_list[0]}\n'
                         f'<b>{message.chat.first_name}!</b>\n'
                         f'{hello_list[1]} {hello_list[2]}\n'
                         ),
                         reply_markup=start_keyboard, parse_mode='HTML')
    await message.delete()


# РАСПОЗНАВАНИЕ АУДИО
def audio_to_text(filename):
    with rc.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")


# ПРИЁМ АУДИО
async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    audio_file = await init_bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
    return audio_file

# не понятно пока что как открывать файл в папке - нужно распознать текст в audio_to_text
# !!!!!!!!!!!!!!!!!!!
@disp_bot.message_handler(content_types=[ContentType.VOICE])
async def any_message_from_user(message: types.Message) -> None:
    voice = await message.voice.get_file()
    path = "files/voices/"
    audio_file = await handle_file(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    
    song = pyglet.media.load(audio_file)
    audio_text = audio_to_text(audio_file)
    content = any_message_from_user(audio_text)
    any_message_from_user(content)


    # задумка, чтобы писать какую-либо фразу перед ответом о том, что как будето АИ размышляет
    # phrasa_response = generate_response("короткое высказываение мыслителя, в стиле - я думаю, что это будет примерно так")
    # нужно считать сколько символом ответ и если больше 100 символов, то спрашивать выводить ответ или нет
@disp_bot.message_handler()
async def any_message_from_user(message: types.Message) -> None:
    update(messages, "user", message.text)
    print("generate_response_text")    
    response = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Новая модель с контекстом
        messages=messages,   # База данных на основе словаря
    )
    resolutipn_response = response['choices'][0]['message']['content'] + "\n" + str(len(response))
    await message.answer(resolutipn_response, parse_mode="markdown")


if __name__ == "__main__":
    executor.start_polling(disp_bot,
                           skip_updates=True,
                           on_startup=fun_startup)
