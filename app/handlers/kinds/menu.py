import aiogram.dispatcher
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import bot
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import products_buttons as kb
from app.middlewares.helpers import call_chat_and_message


async def kinds(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Меню видів"
    kb_kind_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перелік видів",
                    callback_data=cd.kind_menu_callback.new(value="list"),
                ),
                InlineKeyboardButton(
                    text="Додати вид",
                    callback_data=cd.kind_menu_callback.new(value="add"),
                ),
            ]
        ]
    )
    kb_kind_back.add(back("products"))
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_kind_back,
    )


def register_handlers_menu_kinds(dp: Dispatcher):
    dp.register_callback_query_handler(
        kinds, cd.prod_menu_callback.filter(value=["Kinds"])
    )
    dp.register_callback_query_handler(
        kinds, cd.button_back_callback.filter(value=["kinds"]), state="*"
    )
