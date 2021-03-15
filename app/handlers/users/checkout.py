from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from app.database import user_cart as cart_db
from app.middlewares.checks import check_kind, check_cart
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message


async def checkout(call: CallbackQuery):
    chat_id, message_id = call_chat_and_message(call)
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id,text=text, reply_markup=kb.edit_fields
    )