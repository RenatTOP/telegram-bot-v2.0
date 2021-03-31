from bot import bot
from aiogram import Dispatcher
import app.database.kinds as kind_db
from aiogram.dispatcher import FSMContext
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import kind_buttons as kb
from app.middlewares.helpers import call_chat_and_message, message_chat_and_message
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.states.product import Kind


async def add_kind(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Введіть назву виду"
    kb_kind_back = InlineKeyboardMarkup()
    kb_kind_back.add(await help_kb.back("kinds"))
    await Kind.waiting_for_name.set()
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
        text = 'Такий вид вже існує!'
    else:
        await kind_db.add_kind(name)
        text = f'Ви додали вид "{name}"'
    kb_kind_back = InlineKeyboardMarkup()
    kb_kind_back.add(await help_kb.back("kinds"))
    await state.finish()
    await message.answer(text, reply_markup=kb_kind_back)


def register_handlers_add_kind(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_kind, cd.kind_menu_callback.filter(value=["add"]), state="*"
    )
    dp.register_message_handler(kind_name, state=Kind.waiting_for_name)
