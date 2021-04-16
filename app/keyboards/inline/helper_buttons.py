import app.keyboards.inline.callback_datas as cd
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def back(value: str):
    back = InlineKeyboardButton(
        text="⬅ Повернутися",
        callback_data=cd.button_back_callback.new(value=f"{value}"),
    )
    return back

async def check_back(value: str, check: str):
    back = InlineKeyboardButton(
        text="⬅ Повернутися",
        callback_data=cd.button_back2_callback.new(value=f"{value}", check=f"{check}"),
    )
    return back