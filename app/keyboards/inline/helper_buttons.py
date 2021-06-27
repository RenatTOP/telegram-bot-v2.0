from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import callback_datas as cd


def back(value: str):
    back = InlineKeyboardButton(
        text="⬅ Повернутися",
        callback_data=cd.button_back_callback.new(value=f"{value}"),
    )
    return back