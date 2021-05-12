import app.keyboards.inline.callback_datas as cd
from app.keyboards.inline.helper_buttons import back
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cart_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оформити кошик",
                callback_data=cd.checkout_cart.new(_id="cart"),
            ),
        ],
    ]
)
cart_kb.add(back("user_menu"))

async def confirm_cart(prod_id: str):
    cart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.checkout_order.new(data="confirm"),
                ),
            ],
        ]
    )
    cart.insert(
        InlineKeyboardButton(
            text="Ні",
            callback_data=cd.button_back_callback.new(value="cart") if prod_id == "cart" \
                else cd.prod_info_callback.new(_id=f"{prod_id}"),
        ),
    )
    return cart
