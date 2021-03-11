from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.types import Message, CallbackQuery
from app.database import departments as depart_db
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
    await depart_db.del_department(depart_id)
    text = "Ви видалили цей заклад"
    edit_depart = InlineKeyboardMarkup()
    edit_depart.add(await help_kb.back("depart_list"))
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