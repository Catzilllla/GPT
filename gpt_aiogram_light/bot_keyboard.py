from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# СТАРТ И МЕНЮ
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
st_kb_1 = KeyboardButton(text='/help')
st_kb_2 = KeyboardButton(text='/start')
st_kb_3 = KeyboardButton(text='/settings')
st_kb_4 = KeyboardButton(text='/help')
start_keyboard.add(st_kb_1, st_kb_2)


# МЕНЮ ЗАПИСИ
menu_keyb = ReplyKeyboardMarkup(resize_keyboard=False)
menu_kb_1 = KeyboardButton(text='Выбрать время', callback_data='Set_time')
menu_kb_2 = KeyboardButton(text=' 🔙 Назад к котятам', callback_data='back_cat')
menu_keyb.add(menu_kb_1, menu_kb_2)
