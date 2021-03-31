from bot import bot
import app.middlewares.checks
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from app.states.product import Edit_Product
from app.middlewares.checks import check_admin_or_user
from app.database import products as prod_db
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import products_buttons as kb
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def product_list(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    data = call["data"]
    text = "Перелік товарів"
    pages = 0
    if 'nav_prod' in data:
        pages = data.replace("nav_prod:", "")
        pages = pages.replace(":none", "")
        pages = int(pages)
    prod_count = await prod_db.get_count_products()
    if pages > prod_count:
        text = "Це остання сторінка"
        await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )
    elif pages < 0:
        text = "Це перша сторінка"
        await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )
    else:
        products = await prod_db.get_products(6, pages)
        kb_prod_list = await kb.products_list(products, pages)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb_prod_list,
        )


async def sort_prod_list(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    data = call['data']
    data = data.split("prod_sort:", 1)[1]
    kb_sort = await kb.sorted_kb(data)
    text = 'Оберіть за яким видом сортувати'
    await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb_sort,
        )

def register_handlers_product_list(dp: Dispatcher):
    dp.register_callback_query_handler(
        product_list, cd.prod_menu_callback.filter(value=["list"])
    )
    dp.register_callback_query_handler(
        product_list, cd.prod_nav_list_callback.filter(sort=["none"])
    )
    dp.register_callback_query_handler(
        product_list, cd.button_back_callback.filter(value=["prod_list"])
    )