from app.database.departments import edit_depart
import app.keyboards.inline.callback_datas as cd
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ?menu Department buttons

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
                text="⬅ Повернутися",
                callback_data=cd.depart_menu_callback.new(value="back"),
            )
        ],
    ]
)

# ?add Department buttons

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

# ?edit Department buttons

async def departments_list(departments: list):
    depart_list = InlineKeyboardMarkup(row_width=1)
    async for depart in departments:
        _id = depart["_id"]
        name = depart["name"]
        city = depart["city"]
        text_button = f"{name}\t\t м. {city}"
        depart_list.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.depart_info_callback.new(_id=f"{_id}"),
            )
        )
    depart_list.insert(await back("departments"))
    return depart_list


async def info_department(depart_id: str):
    info_depart = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редагувати",
                    callback_data=cd.depart_button_edit_callback.new(
                        _id=f"{depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Видалити",
                    callback_data=cd.depart_button_del_callback.new(_id=f"{depart_id}"),
                ),
            ]
        ]
    )
    info_depart.insert(await back("depart_list"))
    return info_depart


async def del_department(depart_id: str):
    del_depart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.depart_button_confirm_del_callback.new(
                        _id=f"{depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Ні",
                    callback_data=cd.depart_info_callback.new(_id=f"{depart_id}"),
                ),
            ],
        ]
    )
    return del_depart


edit_fields = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назва",
                callback_data=cd.depart_edit_edit_callback.new(field="name"),
            ),
            InlineKeyboardButton(
                text="Область",
                callback_data=cd.depart_edit_edit_callback.new(field="region"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Телефон",
                callback_data=cd.depart_edit_edit_callback.new(field="phone"),
            ),
            InlineKeyboardButton(
                text="Місто",
                callback_data=cd.depart_edit_edit_callback.new(field="city"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Розклад",
                callback_data=cd.depart_edit_edit_callback.new(field="timetable"),
            ),
            InlineKeyboardButton(
                text="Адреса",
                callback_data=cd.depart_edit_edit_callback.new(field="address"),
            ),
        ],
    ]
)

# ?other Department buttons


async def back(value: str):
    back = InlineKeyboardButton(
        text="⬅ Повернутися",
        callback_data=cd.depart_button_back_callback.new(value=f"{value}"),
    )
    return back