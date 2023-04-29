from config import HELP_COMMANDS, hello_list
from config import fun_startup
from config import disp_bot
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from bot_keyboard import start_keyboard


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



if __name__ == "__main__":
    executor.start_polling(disp_bot,
                           skip_updates=True,
                           on_startup=fun_startup)
