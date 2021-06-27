from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.database import departments as depart_db
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd


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
                text="Заклади за областю та містом",
                callback_data=cd.depart_menu_callback.new(value="sort"),
            ),
        ]
    ]
)
menu_depart.add(back("admin_menu"))

# ?list Department buttons

async def departments_list(pages: int, check, sort):
    depart_list_kb = InlineKeyboardMarkup()
    departs = await depart_db.departments_list(6, pages, sort)
    async for depart in departs:
        _id = depart["_id"]
        name = depart["name"]
        region = depart["region"]
        city = depart["city"]
        text_button = f"{name},\t {region},\t {city}"
        if check == "admin":
            depart_list_kb.add(
                InlineKeyboardButton(
                    text=text_button,
                    callback_data=cd.depart_info_callback.new(_id=f"{_id}"),
                )
            )
        elif check == "user":
            depart_list_kb.add(
                InlineKeyboardButton(
                    text=text_button,
                    callback_data=cd.choose_depart.new(value=f"{_id}"),
                )
            )
    pages_back = pages - 6
    pages_next = pages + 6
    depart_list_kb.add(
        InlineKeyboardButton(
            text="<== Попередня сторінка",
            callback_data=cd.depart_nav_list_callback.new(
                pages=f"{pages_back}"
            ),
        )
    )
    depart_list_kb.insert(
        InlineKeyboardButton(
            text="Наступна сторінка ==>",
            callback_data=cd.depart_nav_list_callback.new(
                pages=f"{pages_next}"
            ),
        )
    )
    if check == "admin":
        depart_list_kb.add(back("departments"))
    return depart_list_kb

async def depart_sort(check):
    depart_list = await depart_db.find_departments()
    depart_list_kb = InlineKeyboardMarkup()
    depart_set = set()
    async for depart in depart_list:
        depart = f"{depart['region']}#{depart['city']}"
        depart_set.add(depart)
    for depart in depart_set:
        text = depart.replace("#", ", ")
        depart_list_kb.add(
            InlineKeyboardButton(
                text=text,
                callback_data=cd.depart_button_sort.new(sort=f"{depart}"),
            )
        )
    if check == "admin":
        depart_list_kb.add(back("departments"))
    return depart_list_kb

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
                callback_data=cd.menu_callback.new(value="Departments"),
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

async def info_department(depart_id: str):
    info_depart = InlineKeyboardMarkup(
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
    info_depart.add(back("depart_list"))
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


async def edit_fields(depart_id: str):
    edit_kb = InlineKeyboardMarkup(
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
            [
                InlineKeyboardButton(
                    text="Адміністратор",
                    callback_data=cd.depart_edit_edit_callback.new(field="admin"),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Повернутися",
                    callback_data=cd.depart_info_callback.new(_id=f"{depart_id}"),
                ),
            ],
        ]
    )
    return edit_kb