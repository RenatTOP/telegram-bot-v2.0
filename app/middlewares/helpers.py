from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards import inline
from app.middlewares.checks import check_admin_or_user
from app.database import products, departments, invoices


async def call_chat_and_message(call) -> list:
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    ids = [chat_id, message_id]
    return ids


async def message_chat_and_message(message) -> list:
    chat_id = message.chat.id
    message_id = message.message_id
    ids = [chat_id, message_id]
    return ids


async def create_list(
    bot,
    call: CallbackQuery,
    state: FSMContext,
    text: str,
    sort: str,
    type_sort: str,
    call_1: str,
    call_2: str
):
    chat_id, message_id = await call_chat_and_message(call)
    check = await check_admin_or_user(state)
    data = call["data"]
    pages = 0
    if call_1 in data:
        sort = data.replace(call_1+":", "")
        if type_sort == "kind":
            await state.update_data(kind=sort)
        elif type_sort == "sort":
            await state.update_data(sort=sort)
        elif type_sort == "invoice_sort":
            await state.update_data(invoice_sort=sort)
    elif call_2 in data:
        pages = data.replace("nav:", "").replace(":"+call_2, "")
        pages = int(pages)
    if call_2 == "product":
        pages_count = await products.get_count_products(sort)
    elif call_2 == "department":
        pages_count = await departments.get_count_departs(sort)
    elif call_2 == "invoice":
        pages_count = await invoices.get_count_invoices(sort)
    if pages >= pages_count:
        text = "Це остання сторінка"
        await bot.answer_callback_query(
            callback_query_id=call.id, text=text, show_alert=False
        )
    elif pages < 0:
        text = "Це перша сторінка"
        await bot.answer_callback_query(
            callback_query_id=call.id, text=text, show_alert=False
        )
    else:
        if call_2 == "product":
            keyboard = await inline.products_buttons.products_list(pages, check, sort)
        elif call_2 == "invoice":
            keyboard = await inline.invoices_buttons.invoices_list(pages, check, sort)
        elif call_2 == "department":
            keyboard = await inline.department_buttons.departments_list(pages, check, sort)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard,
        )
