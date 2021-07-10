from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.database import departments as depart_db
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb


async def del_depart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_del:", 1)[1]
    text = "Видалити цей заклад?"
    kb_del_depart = await kb.del_department(depart_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_del_depart,
    )


async def depart_confirm_del(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_confirm_del:", 1)[1]
    dp.loop.create_task(depart_db.del_department(depart_id))
    text = "Ви видалили цей заклад"
    edit_depart = InlineKeyboardMarkup()
    edit_depart.add(back("depart_list"))
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_depart
    )


def register_handlers_del_department(dp: Dispatcher):
    dp.register_callback_query_handler(
        del_depart, cd.depart_button_del_callback.filter()
    )
    dp.register_callback_query_handler(
        depart_confirm_del, cd.depart_button_confirm_del_callback.filter()
    )
