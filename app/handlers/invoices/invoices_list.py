import re
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot import bot
from app.middlewares import checks, helpers
from app.middlewares.checks import check_admin_or_user, check_sort_invoice_state
from app.database import invoices as invoice_db
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import invoices_buttons as kb


async def invoices_list(call: CallbackQuery, state: FSMContext):
    text = "Перелік чеків"
    sort = await check_kind_state(state)
    call_1 = "invoice_sort"
    call_2 = type_sort = "invoice"
    await helpers.create_list(bot, call, state, text, sort, type_sort, call_1, call_2)


async def sort_invoices_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    kb_kinds = await kb.kinds_kb()
    text = "Оберіть за яким станом обробки сортувати"
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
    dp.register_callback_query_handler(invoices_list, cd.nav_list_callback.filter(data="invoice"))
    dp.register_callback_query_handler(
        product_list, cd.button_back_callback.filter(value="prod_list")
    )
    dp.register_callback_query_handler(
        sort_kind_list, cd.prod_menu_callback.filter(value=["sort"])
    )