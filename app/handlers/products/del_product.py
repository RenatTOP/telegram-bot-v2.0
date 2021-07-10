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
from app.database import products as prod_db
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import products_buttons as kb
from app.middlewares.helpers import call_chat_and_message


async def del_product(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    prod_id = prod.replace("prod_del:", "")
    text = "Видалити цей товар?"
    kb_del_prod = await kb.del_product(prod_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_del_prod,
    )


async def prod_confirm_del(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    prod_id = prod.split("prod_confirm_del:", 1)[1]
    text = "Ви видалили цей товар"
    edit_prod = InlineKeyboardMarkup()
    edit_prod.add(back("kinds"))
    dp.loop.create_task(prod_db.del_product(prod_id))
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_prod
    )


def register_handlers_del_product(dp: Dispatcher):
    dp.register_callback_query_handler(
        del_product, cd.prod_button_del_callback.filter()
    )
    dp.register_callback_query_handler(
        prod_confirm_del, cd.prod_button_confirm_del_callback.filter()
    )
