from telebot import TeleBot
from telebot import types
import requests

bot = TeleBot("5306488432:AAHSUp-jzHTOGqbv9NOlsJfLfelCY8dbrdE")
current_shown_dates = {}

URL_CAT = 'https://api.thecatapi.com/v1/images/search'

hello_list = [
    'Здравствуйте!',
    'Буду очень рада вас видеть, запишитесь пожалуйста и приходите в гости!',
    'Можно заранее оплатить приём. Кнопка для оплаты будет доступна после резерва по времени.',
    'А это вам котёнка для поднятия настроения!'
    ]

def get_cat_image():
    response = requests.get(URL_CAT).json()
    random_cat = response[0].get('url')
    return random_cat


# @bot.message_handler(content_types=['text'])
# def chatting(message):
#     markup = types.InlineKeyboardMarkup()
#     btn_0 = types.InlineKeyboardButton(text='ПОНЕДЕЛЬНИК', callback_data='btn_2')
#     btn_1 = types.InlineKeyboardButton(text='ВТОРНИК', callback_data='btn_2')
#     btn_2 = types.InlineKeyboardButton(text='СРЕДА', callback_data='btn_2')
#     btn_3 = types.InlineKeyboardButton(text='ЧЕТВЕРГ', callback_data='btn_2')
#     btn_4 = types.InlineKeyboardButton(text='ПЯТНИЦА', callback_data='btn_2')
#     btn_5 = types.InlineKeyboardButton(text='СУББОТА', callback_data='btn_2')
#     btn_6 = types.InlineKeyboardButton(text='ВОСКРЕСЕНЬЕ', callback_data='btn_2')
#     btn_7 = types.InlineKeyboardButton(text='ЕЩЕ КОТЭ', callback_data='btn_2')
#     markup.add(btn_0, btn_1, btn_2, btn_3)
#     markup.add(btn_4, btn_5, btn_6)
#     markup.add(btn_7)
    
#     bot.delete_message(message.chat.id, message.message_id)


# @bot.message_handler(content_types=['photo'])
@bot.message_handler(commands=['start'])
def main_prog(message):
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard_1 = types.KeyboardButton(text='ХОЧУ НОВОГО КОТЭ')
    keyboard_2 = types.KeyboardButton(text='ЗАПИСЬ НА ПРИЁМ')
    keyboard.add(keyboard_1, keyboard_2)

    bot.send_photo(message.chat.id, get_cat_image())
    bot.send_message(message.chat.id, f'{hello_list[0]} {message.chat.first_name} {hello_list[1]} {hello_list[2]} {hello_list[3]}', reply_markup=keyboard)
    
    bot.send_message(message.chat.id, message)
    # bot.delete_message(message.chat.id, chatting(tex_odt))
    # bot.delete_chat_photo(message.chat.photo, img)
    
    # bot.send_message(message.chat.id, message.photo)


bot.polling()
