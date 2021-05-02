from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.keyboards.inline.callback_datas as cd


admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Заклади",
                callback_data=cd.menu_callback.new(value="Departments"),
            ),
            InlineKeyboardButton(
                text="Товари",
                callback_data=cd.menu_callback.new(value="Products"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Рахунки",
                callback_data=cd.menu_callback.new(value="Invoices"),
            ),
            InlineKeyboardButton(
                text="Користувачі",
                callback_data=cd.menu_callback.new(value="Users"),
            ),
        ],
    ]
)


user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Товари",
                callback_data=cd.menu_callback.new(value="Products"),
            ),
            InlineKeyboardButton(
                text="Рахунки",
                callback_data=cd.menu_callback.new(value="Invoices"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Кошик",
                callback_data=cd.menu_callback.new(value="Cart"),
            ),
        ],
    ]
)