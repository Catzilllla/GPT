from aiogram import executor, types, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import sqlite3 as sqdb



TOKEN_API = '6059784930:AAFaon_GMywQYkdUwkT_-wyTQb7VKOyeW4s'
init_bot = Bot(token=TOKEN_API)
disp_bot = Dispatcher(init_bot)
HELP_COMMANDS = """
/help
/start
/createprofile
"""

# СТАРТ И МЕНЮ
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
st_kb_1 = KeyboardButton(text='/help')
st_kb_2 = KeyboardButton(text='/start')
st_kb_3 = KeyboardButton(text='/createprofile', callback_data='createprofile')
start_keyboard.add(st_kb_1, st_kb_2, st_kb_3)

inlkeyb = InlineKeyboardMarkup(row_width=2)
inlb_1 = InlineKeyboardButton(text='Просмотр всех продуктов', callback_data='getallproduct')
inlb_2 = InlineKeyboardButton(text='Добавить новый продукт', callback_data='addnewproduct')
inlkeyb.add(inlb_1, inlb_2)


async def sqlite_db_connector():
    global database, cursor
    database = sqdb.connect('test_bd.db')
    cursor = database.cursor()
    cursor.execute("CREATE  TABLE IF NOT EXISTS products(name TEXT, photo TEXT)")
    database.commit()


async def select_product_in_db():
    products = cursor.execute("SELECT * FROM product").fetchall()
    return products

async def fun_startup(_):
    print("Telegram bot activated . . . ")
    await sqlite_db_connector()
    print("Connection to DB Sqlite3 successful!")

@disp_bot.message_handler(commands=['help'])
async def help_mess(message: types.Message) -> None:
    await message.answer(text=HELP_COMMANDS,
                         parse_mode='HTML')
    await message.delete()


@disp_bot.message_handler(commands=['start'])
async def start_mess(message: types.Message) -> None:
    await message.answer(text="Привет! я тестовый бот по БД SQLITE!!! Давай уже работать!",
                         reply_markup=start_keyboard, parse_mode='HTML')
    await message.delete()


@disp_bot.callback_query_handler(text='createprofile')
async def create_profile_func(callback: types.CallbackQuery) -> None:
    if callback.data == 'createprofile':
        callback.message(
            "Вы зашли в кабинет добавления продуктов!"
            "Пожалуйста введите название продукта!", reply_markup=inlkeyb
            )

@disp_bot.callback_query_handler(text='getallproduct')
async def create_profile_func(callback: types.CallbackQuery) -> None:
    products = await select_product_in_db()
    if not products:
        callback.message.answer("Ничего нету в базе данных!!!")


if __name__ == "__main__":
    executor.start_polling(dispatcher=disp_bot,
                           skip_updates=True,
                           on_startup=fun_startup)
