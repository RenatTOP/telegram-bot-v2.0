from aiogram import Dispatcher
from aiogram.types import Message
import app.database.users as user_db
from app.settings import SECRET_ADMIN
import app.middlewares.checks as checks
from app.database.users import db_check_admin
from aiogram.dispatcher.filters import RegexpCommandsFilter


async def initialization(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = (
        f"Вітаю {user_name}, ви зареєструвалися,"
        " передайте будь-ласка своє місцеположення /mygeo"
        " для визначення найближчих вдділень"
    )
    check = await checks.check_already_user(user_id)
    if check:
        text = "Ви вже зареєстровані"
        await message.answer(text)
    else:
        await user_db.add_user(user_id, user_name)
        await message.answer(text)


async def is_admin(message: Message):
    user_id = message.from_user.id
    check_message = message.text
    secret_admin = check_message.split()
    try:
        check_admin = await db_check_admin(user_id)
        if check_admin["isAdmin"]:
            await message.answer("Ви адмін")
        elif secret_admin[1].strip() == SECRET_ADMIN:
            await user_db.add_admin(user_id)
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
