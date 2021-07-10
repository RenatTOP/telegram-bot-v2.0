from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.database import kinds as kind_db
from app.keyboards.inline import kind_buttons as kb
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message


async def del_kind(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    kind = call["data"]
    kind_id = kind.split("kind_del:", 1)[1]
    text = "Видалити цей вид?"
    kb_del_kind = await kb.del_kind(kind_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_del_kind,
    )


async def kind_confirm_del(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    kind = call["data"]
    kind_id = kind.split("kind_confirm_del:", 1)[1]
    dp.loop.create_task(kind_db.del_kind(kind_id))
    text = "Ви видалили цей вид, а також видалили вид у товарів з цим видом"
    edit_kind = InlineKeyboardMarkup()
    edit_kind.add(back("kind_list"))
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_kind
    )


def register_handlers_del_kind(dp: Dispatcher):
    dp.register_callback_query_handler(del_kind, cd.kind_button_del_callback.filter())
    dp.register_callback_query_handler(
        kind_confirm_del, cd.kind_button_confirm_del_callback.filter()
    )
