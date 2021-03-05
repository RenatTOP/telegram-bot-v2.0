import aiogram.types
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import admin_menu_buttons as kb
from bot import bot
from app.middlewares.checks import check_is_admin


async def admin_menu(message: Message):
    user_id = message.from_user.id
    is_admin = check_is_admin(user_id)
    if is_admin:
        await message.answer(text="Хай", reply_markup=kb.admin_menu)
    else:
        await message.answer("Ви не адмін")


def register_handlers_admin_menu(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands=["admin_menu"])
