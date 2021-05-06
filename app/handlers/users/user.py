from bot import bot
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
import app.database.users as user_db
import app.database.departments as depart_db
from app.settings import SECRET_ADMIN
import app.middlewares.checks as checks
from app.database.users import db_check_admin
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb
from aiogram.dispatcher.filters import RegexpCommandsFilter


async def initialization(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    check = await checks.check_already_user(user_id)
    if check:
        text = "Ви вже зареєстровані"
    else:
        text = (
            f"Вітаю {user_name}, ви зареєструвалися, "
            "введіть команду /choose щоб обрати заклад"
        )
        await user_db.add_user(user_id, user_name)
    await message.answer(text)


async def choose_depart(message: Message):
    kb_departs = await kb.depart_sort("user")
    text = "Оберіть область та місто"
    await message.answer(text, reply_markup=kb_departs)


async def confirm_choose(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    user_id = call.from_user.id
    depart_id = call["data"]
    depart_id = depart_id.replace("choose:", "")
    depart = await depart_db.find_department(_id=depart_id)
    await user_db.set_user(
        user_id,
        "location",
        f"{depart['region']}, {depart['city']}, {depart['address']}, {depart['name']}",
    )
    text = (
        f"Ви обрали заклад {depart['name']}, за адресою:\n "
        f"{depart['region']} обл., м.{depart['city']} вул.{depart['address']}\n "
        "введіть /menu щоб перейти до покупок"
    )
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=None,
    )


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
            await message.answer(
                "Вітаю, ви тепер адмін\n"
                "Видаліть будь-ласка попереднє повідомлення із таємним ключем"
            )
        else:
            await message.answer("Невірний таємний ключ")
    except:
        await message.answer(
            "<i>Ви <b>не</b> адмін</i> \n"
            "<i>Введіть таємний ключ у форматі </i>\n"
            "'<b>/is_admin таємний ключ'</b>"
        )


def register_handlers_init_users(dp: Dispatcher):
    dp.register_message_handler(initialization, commands=["start"])
    dp.register_message_handler(choose_depart, commands=["choose"])
    dp.register_message_handler(
        is_admin, RegexpCommandsFilter(regexp_commands=["is_admin .", "is_admin"])
    )
    dp.register_callback_query_handler(confirm_choose, cd.choose_depart.filter())
