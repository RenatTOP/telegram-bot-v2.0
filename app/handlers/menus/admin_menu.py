from bot import bot
from aiogram import Dispatcher
import app.middlewares.helpers
from aiogram.types import Message, CallbackQuery
from app.middlewares.checks import check_is_admin
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import admin_menu_buttons as kb


async def admin_menu(message: Message):
    user_id = message.from_user.id
    is_admin = await check_is_admin(user_id)
    if is_admin:
        await message.answer(text="Хай", reply_markup=kb.admin_menu)
    else:
        await message.answer("Ви не адмін")


async def admin_menu_call(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Хай",
        reply_markup=kb.admin_menu,
    )


def register_handlers_admin_menu(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands=["admin_menu"])
    dp.register_callback_query_handler(
        admin_menu_call, cd.button_back_callback.filter(value="admin_menu")
    )
