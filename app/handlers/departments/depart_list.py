import re
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import bot
from app.middlewares import checks
from app.database import departments as depart_db
from app.states.department import Edit_Department
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb
from app.handlers.departments.depart_helper import string_week
from app.middlewares.checks import check_admin_or_user, check_sort_state


async def department_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    check = await check_admin_or_user(state)
    data = call["data"]
    text = "Перелік закладів"
    pages = 0
    sort = await check_sort_state(state)
    if "depart_sort" in data:
        sort = data.replace("depart_sort:", "")
        await state.update_data(sort=sort)
    elif "nav_depart" in data:
        pages = data.replace("nav_depart:", "")
        pages = int(pages)
    depart_count = await depart_db.get_count_departs(sort)
    if pages >= depart_count:
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
        kb_prod_list = await kb.departments_list(pages, check, sort)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb_prod_list,
        )


async def sort_depart_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    kb_departs = await kb.depart_sort("admin")
    text = "Оберіть область та місто"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_departs,
    )


def register_handlers_depart_list(dp: Dispatcher):
    dp.register_callback_query_handler(
        department_list, cd.depart_menu_callback.filter(value="list")
    )
    dp.register_callback_query_handler(department_list, cd.depart_button_sort.filter())
    dp.register_callback_query_handler(
        department_list, cd.depart_nav_list_callback.filter()
    )
    dp.register_callback_query_handler(
        department_list, cd.button_back_callback.filter(value="depart_list")
    )
    dp.register_callback_query_handler(
        sort_depart_list, cd.depart_menu_callback.filter(value="sort")
    )
