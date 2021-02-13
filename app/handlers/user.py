from aiogram import types
import app.database.database as db
import os
from app.middlewares.checks import check_is_admin
from app.settings import SECRET_ADMIN

async def initialization(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = 'Вітаю {}, ви зареєструвалися, можете перейти до товарів командою /order'.format(
        user_name)
    check = db.check_already_user(user_id)
    if (check):
        text = 'Ви вже зареєстровані'
        await message.answer(text)
    else:
        db.add_user(user_id, user_name)
        await message.answer(text)

async def is_admin(message: types.Message):
    user_id = message.from_user.id
    check_message = message.text
    check_secret_admin = check_message.split()
    if (check_is_admin(user_id)):
        text = 'Ви вже адмін'
        await message.answer(text)
    elif (check_secret_admin[1] == SECRET_ADMIN):
        text = 'Вітаю, ви тепер адмін'
        db.add_admin(user_id)
        await message.answer(text)
    else:
        text = 'Невірний секретний ключ'
        await message.answer(text)