from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.keyboards.inline.callback_datas as cd

menu_prod = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перелік товарів",
                callback_data=cd.prod_menu_callback.new(value="list"),
            ),
            InlineKeyboardButton(
                text="Додати товар",
                callback_data=cd.prod_menu_callback.new(value="add"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data=cd.prod_menu_callback.new(value="back"),
            )
        ],
    ]
)
