import app.keyboards.inline.callback_datas as cd
from app.keyboards.inline.helper_buttons import back
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


checkout = ""

async def confirm_cart(prod_id: str, data: str):
    cart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.checkout_order.new(
                        data=f"{data}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Ні",
                    callback_data=cd.prod_info_callback.new(_id=f"{prod_id}"),
                ),
            ],
        ]
    )
    return cart