from bot import bot
from aiogram import Dispatcher
import app.database.kinds as kind_db
from aiogram.dispatcher import FSMContext
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import kind_buttons as kb
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def kind_list(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    kinds = await kind_db.find_kinds()
    text = "Перелік видів"
    kb_kind_list = await kb.kinds_list(kinds)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_kind_list,
    )


async def info_kind(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    kind_id = call["data"]
    kind_id = kind_id.split("kind_info_edit:", 1)[1]
    kind_data = await kind_db.get_kind_by_id(kind_id)
    text = (
        f'Вид: <b>{kind_data["name"]}</b>\n'
    )
    kb_info_kind = await kb.info_kind(kind_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_info_kind,
    )


async def edit_name(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    kind_id = call["data"]
    kind_id = kind_id.split("kind_edit:", 1)[1]
    text = "Введіть нову назву"
    edit_kind = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Повернутися",
                    callback_data=cd.kind_info_callback.new(
                        _id=f"{kind_id}"
                    ),
                ),
            ]
        ]
    )
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=edit_kind,
    )


def register_handlers_edit_kind(dp: Dispatcher):
    dp.register_callback_query_handler(
        kind_list, cd.kind_menu_callback.filter(value=["list"])
    )
    dp.register_callback_query_handler(
        kind_list, cd.button_back_callback.filter(value=["kind_list"])
    )
    dp.register_callback_query_handler(info_kind, cd.kind_info_callback.filter())
    dp.register_callback_query_handler(edit_name, cd.kind_button_edit_callback.filter())