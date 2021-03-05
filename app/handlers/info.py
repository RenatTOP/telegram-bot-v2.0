from aiogram import Dispatcher


async def description(message):
    text = "Бот для онлайн кафе \nПосилання на відео"
    await message.answer(text)


async def about(message):
    text = "Робота Олійника Рената"
    await message.answer(text)


def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(description, commands=["description"])
    dp.register_message_handler(about, commands=["about"])
