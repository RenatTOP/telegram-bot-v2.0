from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.keyboards.inline.callback_datas as cd


menu_depart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перелік закладів",
                callback_data=cd.depart_menu_callback.new(value="list"),
            ),
            InlineKeyboardButton(
                text="Додати заклад",
                callback_data=cd.depart_menu_callback.new(value="add"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data=cd.depart_menu_callback.new(value="back"),
            )
        ],
    ]
)

cancel_add_depart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Скасувати",
                callback_data=cd.depart_confirm_callback.new(value="Cancel"),
            )
        ]
    ]
)

confirm_or_fail_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так",
                callback_data=cd.admin_menu_callback.new(value="Departments"),
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.depart_confirm_callback.new(value="Not")
            ),
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data=cd.admin_menu_callback.new(value="Departments"),
            )
        ]
    ]
)

confinm_depart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так", callback_data=cd.depart_confirm_callback.new(value="Yes")
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.depart_confirm_callback.new(value="No")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Скасувати",
                callback_data=cd.depart_confirm_callback.new(value="Cancel"),
            )
        ],
    ]
)

add_edit_depart = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назва",
                callback_data=cd.depart_add_edit_callback.new(field="name"),
            ),
            InlineKeyboardButton(
                text="Область",
                callback_data=cd.depart_add_edit_callback.new(field="region"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Телефон",
                callback_data=cd.depart_add_edit_callback.new(field="phone"),
            ),
            InlineKeyboardButton(
                text="Місто",
                callback_data=cd.depart_add_edit_callback.new(field="city"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Розклад",
                callback_data=cd.depart_add_edit_callback.new(field="timetable"),
            ),
            InlineKeyboardButton(
                text="Адреса",
                callback_data=cd.depart_add_edit_callback.new(field="address"),
            ),
        ],
    ]
)
