from aiogram import Dispatcher
from aiogram.types import Message
import app.database.users as user_db
from app.settings import SECRET_ADMIN
import app.middlewares.checks as checks
from app.middlewares.checks import check_is_admin
from aiogram.dispatcher.filters import RegexpCommandsFilter


async def initialization(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = (
        f"Вітаю {user_name}, ви зареєструвалися,"
        " передайте будь-ласка своє місцеположення /mygeo"
        " для визначення найближчих вдділень"
    )
    check = checks.check_already_user(user_id)
    if check:
        text = "Ви вже зареєстровані"
        await message.answer(text)
    else:
        user_db.add_user(user_id, user_name)
        await message.answer(text)


async def is_admin(message: Message):
    user_id = message.from_user.id
    check_message = message.text
    check_secret_admin = check_message.split()
    try:
        if check_is_admin(user_id):
            await message.answer("Ви адмін")
        elif check_secret_admin[1] == SECRET_ADMIN:
            user_db.add_admin(user_id)
            await message.answer("Вітаю, ви тепер адмін")
        else:
            await message.answer("Невірний таємний ключ")
    except:
        await message.answer(
            "<i>Ви <b>не</b> адмін</i> \n"
            "<i>Введіть таємний ключ у форматі </i>\n"
            "'<b>/is_admin таємний ключ'</b>"
        )


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(initialization, commands=["start"])
    dp.register_message_handler(
        is_admin, RegexpCommandsFilter(regexp_commands=["is_admin .", "is_admin"])
    )
