"""
This is a echo bot.
It echoes any incoming text messages.
"""
import logging
from decimal import Decimal
import requests
from yandex_geocoder import Client
from aiogram_config import API_TOKEN
from aiogram_config import API_YA_DECORER
from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=False)
st_but_1 = KeyboardButton(text='/help')
st_but_2 = KeyboardButton(text='/start')
st_but_3 = KeyboardButton(text='/img')
st_but_4 = KeyboardButton(text='/location')

start_keyboard.add(st_but_1, st_but_2, st_but_3).add(st_but_4)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# yandex API geocoder
client = Client(API_YA_DECORER)

# help commands
HELP_COMMANDS = """
<b>/help</b> = <em>список команд</em>
<b>/start</b> = <em>старт бота</em>
<b>/img</b> = <em>картинка</em>
"""

# URL's
URL_CAT = 'https://api.thecatapi.com/v1/images/search'


hello_list = [
    'Здравствуйте,',
    'Буду очень рада вас видеть, запишитесь пожалуйста и приходите в гости!',
    'А это вам котёнка для поднятия настроения!',
    ]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text=f'{hello_list[0]} {message.chat.first_name}! {hello_list[1]} {hello_list[2]}',
                         reply_markup=start_keyboard)
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer(text=HELP_COMMANDS, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['img'])
async def img_send_api(message: types.Message):
    # api cats
    response = requests.get(URL_CAT).json()
    random_cat = response[0].get('url')

    await bot.send_photo(chat_id=message.chat.id, photo=random_cat)
    await message.delete()


@dp.message_handler(commands=['location'])
async def send_location(message: types.Message):
    coordinates = client.coordinates("Москва Скандинавский бульвар 3к2")
    #assert coordinates == (Decimal("37.587093"), Decimal("55.733969"))
    address = client.address(Decimal("37.498644"), Decimal("55.567657"))
    #assert address == "Россия, Москва, улица Льва Толстого, 16"

    # await bot.send_location(chat_id=message.from_user.id, latitude=coord, longitude=coord_list[1])
    await bot.send_message(message.chat.id, text=str(coordinates))
    await bot.send_message(message.chat.id, text=str(address))
    await message.delete()


# @dp.message_handler()
# async def count_symb(message: types.Message):

#     # check count symbols in user message
#     await message.reply(message.text.count('👍'))

#     # send private message
#     await bot.send_message(message.from_user.id, text="<em>Любое сообщение в приватный чат!</em>", parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
