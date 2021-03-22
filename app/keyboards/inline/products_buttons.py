import app.keyboards.inline.callback_datas as cd
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

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


async def products_list(products: list, pages: int):
    prod_list = InlineKeyboardMarkup()
    async for prod in products:
        _id = prod["_id"]
        label = prod["label"]
        amount = prod["amount"]
        text_button = f"{label}\t\t, {amount/100.00} грн."
        prod_list.add(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.prod_info_callback.new(_id=f"{_id}"),
            )
        )
    pages_back = pages - 6
    pages_next = pages + 6
    prod_list.add(
        InlineKeyboardButton(
            text="<== Попередня сторінка",
            callback_data=cd.prod_nav_list_callback.new(pages=f"{pages_back}"),
        )
    )
    prod_list.insert(
        InlineKeyboardButton(
            text="Наступна сторінка ==>",
            callback_data=cd.prod_nav_list_callback.new(pages=f"{pages_next}"),
        )
    )
    if 'admin' == "admin":
        prod_list.add(await help_kb.back("products"))
    else:
        prod_list.add(await help_kb.back("user_menu"))
    return prod_list


async def admin_info_product(prod_id: str):
    info_prod = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редагувати",
                    callback_data=cd.prod_button_edit_callback.new(_id=f"{prod_id}"),
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


async def user_info_product(prod_id: str):
    info_prod = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Додати до кошика",
                    callback_data=cd.add_to_cart_button.new(_id=f"{prod_id}"),
                ),
                InlineKeyboardButton(
                    text="Видалити із кошика",
                    callback_data=cd.del_from_cart_button.new(_id=f"{prod_id}"),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Оформити кошик",
                    callback_data=cd.checkout_order.new(data="cart"),
                ),
            ],
        ]
    )
    info_prod.add(await help_kb.back("user_prod_list"))
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