from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import goog
import asyncio

bot = Bot(token='token')
dp = Dispatcher()


def set_button(num):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='Смотреть дальше 👍',
        callback_data=num)]])


async def set_curse_video(num, chat):
    await bot.copy_message(from_chat_id=0, message_id=num, chat_id=chat)


@dp.message(Command(commands=['start']))
async def video_command(message: Message):
    await bot.copy_message(from_chat_id=0, message_id=8, chat_id=message.from_user.id)


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    data = await goog.get(1)
    await message.answer(text=data[2])
    await set_curse_video(int(data[3]), message.from_user.id)
    await asyncio.sleep(int(data[4]))
    temp = await goog.get(2)
    await message.answer(text=temp[1], reply_markup=set_button(temp[0]))


@dp.callback_query(lambda callback: callback.data == 'pass')
async def page(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query(lambda callback: int(callback.data) in range(100))
async def page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=callback.message.text, reply_markup=set_button('pass'))
    data = await goog.get(int(callback.data))
    await callback.message.answer(text=data[2])
    await set_curse_video(int(data[3]), callback.from_user.id)
    await asyncio.sleep(int(data[4]))
    temp = await goog.get(int(callback.data) + 1)
    if not temp:
        await callback.message.answer(text='Конец курса')
        return
    await callback.message.answer(text=temp[1], reply_markup=set_button(temp[0]))


@dp.channel_post(lambda message: message.video)
async def post(message: Message):
    await message.reply(text=f'ID Видео: {message.message_id}\n'
                             f'Время (с): {message.video.duration // 2}')


if __name__ == '__main__':
    dp.run_polling(bot)
