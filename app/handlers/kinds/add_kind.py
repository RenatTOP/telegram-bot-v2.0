from aiogram import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.states.product import Kind
from app.database import kinds as kind_db
from app.middlewares.checks import check_kind
from app.middlewares.state_check import state_check
from app.keyboards.inline import kind_buttons as kb
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message, message_chat_and_message
from app.keyboards.inline.helper_buttons import back


async def add_kind(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Введіть назву виду"
    kb_kind_back = InlineKeyboardMarkup()
    kb_kind_back.add(back("kinds"))
    await state.set_state(Kind.first())
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_kind_back,
    )


async def kind_name(message: Message, state: FSMContext):
    name = message.text
    name = name.strip()
    if await check_kind(name):
        text = "Такий вид вже існує!"
    else:
        dp.loop.create_task(kind_db.add_kind(name))
        text = f'Ви додали вид "{name}"'
    kb_kind_back = InlineKeyboardMarkup()
    kb_kind_back.add(back("kinds"))
    await state_check(state)
    await message.answer(text, reply_markup=kb_kind_back)


def register_handlers_add_kind(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_kind, cd.kind_menu_callback.filter(value=["add"]), state="*"
    )
    dp.register_message_handler(kind_name, state=Kind.waiting_for_name)
