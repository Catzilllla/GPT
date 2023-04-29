import telebot
from telebot import types

API_TOKEN = '5306488432:AAHSUp-jzHTOGqbv9NOlsJfLfelCY8dbrdE'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

def f(message):
    return message.text == '1'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, message.chat.type)

bot.polling()
