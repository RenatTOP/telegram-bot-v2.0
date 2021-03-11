import app.keyboards.inline.callback_datas as cd
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ?menu Product buttons

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
                text="Види товарів",
                callback_data=cd.prod_menu_callback.new(value="Kinds"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅ Повернутися",
                callback_data=cd.button_back_callback.new(value="admin_menu"),
            )
        ],
    ]
)

# ?add Product buttons

cancel_add_prod = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Скасувати",
                callback_data=cd.prod_confirm_callback.new(value="Cancel"),
            )
        ]
    ]
)

confirm_or_fail_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так",
                callback_data=cd.admin_menu_callback.new(value="Products"),
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.prod_confirm_callback.new(value="Not")
            ),
        ]
    ]
)


confinm_prod = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так", callback_data=cd.prod_confirm_callback.new(value="Yes")
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.prod_confirm_callback.new(value="No")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Скасувати",
                callback_data=cd.prod_confirm_callback.new(value="Cancel"),
            )
        ],
    ]
)

add_edit_prod = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назва",
                callback_data=cd.prod_add_edit_callback.new(field="label"),
            ),
            InlineKeyboardButton(
                text="Ціна",
                callback_data=cd.prod_add_edit_callback.new(field="amount"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Вид",
                callback_data=cd.prod_add_edit_callback.new(field="kind"),
            ),
            InlineKeyboardButton(
                text="Опис",
                callback_data=cd.prod_add_edit_callback.new(field="about"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Посилання на картинку",
                callback_data=cd.prod_add_edit_callback.new(field="picture"),
            )
        ],
    ]
)

# ?edit Product buttons

async def products_list(products: list):
    prod_list = InlineKeyboardMarkup(row_width=2)
    async for prod in products:
        _id = prod["_id"]
        label = prod["label"]
        amount = prod["amount"]
        text_button = f"{label}\t\t, ціна {amount/100.00} грн."
        prod_list.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.prod_info_callback.new(_id=f"{_id}"),
            )
        )
    prod_list.add(await help_kb.back("products"))
    return prod_list


async def info_product(prod_id: str):
    info_prod = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редагувати",
                    callback_data=cd.prod_button_edit_callback.new(
                        _id=f"{prod_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Видалити",
                    callback_data=cd.prod_button_del_callback.new(_id=f"{prod_id}"),
                ),
            ]
        ]
    )
    info_prod.add(await help_kb.back("prod_list"))
    return info_prod


async def del_product(prod_id: str):
    del_prod = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.prod_button_confirm_del_callback.new(
                        _id=f"{prod_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Ні",
                    callback_data=cd.prod_info_callback.new(_id=f"{prod_id}"),
                ),
            ],
        ]
    )
    return del_prod


edit_fields = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назва",
                callback_data=cd.prod_edit_edit_callback.new(field="label"),
            ),
            InlineKeyboardButton(
                text="Ціна",
                callback_data=cd.prod_edit_edit_callback.new(field="amount"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Вид",
                callback_data=cd.prod_edit_edit_callback.new(field="kind"),
            ),
            InlineKeyboardButton(
                text="Опис",
                callback_data=cd.prod_edit_edit_callback.new(field="about"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Посилання на зображення",
                callback_data=cd.prod_edit_edit_callback.new(field="picture"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅ Повернутися",
                callback_data=cd.button_back_callback.new(value="prod_list"),
            )
        ],
    ]
)