from bot import bot
import app.middlewares.checks
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from app.states.product import Edit_Product
from app.middlewares.checks import check_admin_or_user, check_kind_state
from app.database import products as prod_db
from app.database import kinds as kind_db
from aiogram.dispatcher import FSMContext
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import products_buttons as kb
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re


async def product_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    check = await check_admin_or_user(state)
    data = call["data"]
    text = "Перелік товарів"
    pages = 0
    kind = await check_kind_state(state)
    if "prod_sort" in data:
        kind = data.replace("prod_sort:", "")
        await state.update_data(kind=kind)
    elif "nav_prod" in data:
        pages = data.replace("nav_prod:", "")
        pages = int(pages)
    prod_count = await prod_db.get_count_products(kind)
    if pages >= prod_count:
        text = "Це остання сторінка, або товарів цього виду намає"
        await bot.answer_callback_query(
            callback_query_id=call.id, text=text, show_alert=False
        )
    elif pages < 0:
        text = "Це перша сторінка"
        await bot.answer_callback_query(
            callback_query_id=call.id, text=text, show_alert=False
        )
    else:
        kb_prod_list = await kb.products_list(pages, check, kind)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb_prod_list,
        )


async def sort_kind_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    kb_kinds = await kb.kinds_kb()
    text = "Оберіть за яким видом сортувати"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_kinds,
    )


def register_handlers_product_list(dp: Dispatcher):
    dp.register_callback_query_handler(
        product_list, cd.prod_menu_callback.filter(value=["list"])
    )
    dp.register_callback_query_handler(product_list, cd.prod_button_sort.filter())
    dp.register_callback_query_handler(product_list, cd.prod_nav_list_callback.filter())
    dp.register_callback_query_handler(product_list, cd.button_back_callback.filter(value="prod_list"))
    dp.register_callback_query_handler(
        sort_kind_list, cd.prod_menu_callback.filter(value=["sort"])
    )