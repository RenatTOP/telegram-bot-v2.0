from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.types import Message, CallbackQuery
from app.database import products as prod_db
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import products_buttons as kb
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def del_product(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    prod_id = prod.split("prod_del:", 1)[1]
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
    edit_prod.add(await help_kb.back("kinds"))
    await prod_db.del_product(prod_id)
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