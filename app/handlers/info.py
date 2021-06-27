from aiogram import Dispatcher
from aiogram.types import Message



async def description(message: Message):
    text = "Бот для швидких онлайн замовлень у закладах фастфуду"
    await message.answer(text)


async def about(message: Message):
    text = "Робота Олійника Рената"
    await message.answer(text)


def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(description, commands=["description"])
    dp.register_message_handler(about, commands=["about"])
