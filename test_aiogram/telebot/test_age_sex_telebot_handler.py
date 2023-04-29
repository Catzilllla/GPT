import telebot
from telebot import types

API_TOKEN = '5306488432:AAHSUp-jzHTOGqbv9NOlsJfLfelCY8dbrdE'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Хендлер команд '/start' и '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привет, твое имя?
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Сколько тебе лет?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'Упс!')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Возвраст должен быть числом. Сколько тебе лет?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Мужчина', 'Женщина')
        msg = bot.reply_to(message, 'Твой пол?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'Упс!')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Мужчина') or (sex == u'Женщина'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(chat_id, 'Приятно познакомиться ' + user.name + '\n Возвраст:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'Упс!')


# Включить сохранение обработчиков следующего шага в файл "./.handlers-saves/step.save".
# Delay=2 означает, что после любого изменения в обработчиках следующего шага будет задержка 2сек (например calling register_next_step_handler())
# сохранение произойдет через 2 секунды задержки
bot.enable_save_next_step_handlers(delay=2)

# Загрузить next_step_handlers из файла (default "./.handlers-saves/step.save")
# ВНИМАНИЕ работает только если enable_save_next_step_handlers был вызван!
bot.load_next_step_handlers()

bot.polling()