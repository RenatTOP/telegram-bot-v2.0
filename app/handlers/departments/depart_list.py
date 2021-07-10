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
from app.middlewares import checks, helpers
from app.database import departments as depart_db
from app.states.department import Edit_Department
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb
from app.handlers.departments.depart_helper import string_week
from app.middlewares.checks import check_admin_or_user, check_sort_state


async def department_list(call: CallbackQuery, state: FSMContext):
    text = "Перелік закладів"
    sort = await check_sort_state(state)
    type_sort = "sort"
    call_1 = "depart_sort"
    call_2 = "department"
    await helpers.create_list(bot, call, state, text, sort, type_sort, call_1, call_2)


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
        department_list, cd.nav_list_callback.filter(data="department")
    )
    dp.register_callback_query_handler(
        department_list, cd.button_back_callback.filter(value="depart_list")
    )
    dp.register_callback_query_handler(
        sort_depart_list, cd.depart_menu_callback.filter(value="sort")
    )
