from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd


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
                    text="Так, обрати час",
                    callback_data=cd.checkout_order.new(data="confirm"),
                ),
                InlineKeyboardButton(
                    text="Ні",
                    callback_data=cd.button_back_callback.new(value="cart")
                    if prod_id == "cart"
                    else cd.prod_info_callback.new(_id=f"{prod_id}"),
                ),
            ]
        ]
    )
    return cart


async def time_checkout(indicated_time: str):
    checkout = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.time_checkout_order.new(data=f"{indicated_time}"),
                ),
            ]
        ]
    )
    checkout.add(back("cart"))
    return checkout
