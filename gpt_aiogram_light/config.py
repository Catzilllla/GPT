from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher


OPEN_AI_KEY = ""
API_TOKEN = ''
API_YA_DECORER = ''
HELP_COMMANDS = """
<b>/help</b> = <em>список команд</em>
<b>/start</b> = <em>старт бота</em>
<b>/img</b> = <em>картинка</em>
<b>/register</b> = <em>регистрация</em>
"""

hello_list = [
    'Здравствуйте,',
    'Я простой, но умный GPT робот 🤖! Спасибо, что зашли в гости!',
    'Опишите, что вас интересует больше всего или задайте ❓ 🙈',
    ]

init_bot = Bot(token=API_TOKEN)
disp_bot = Dispatcher(bot=init_bot)


async def fun_startup(_):
    print("Telegram бот запущен!")
