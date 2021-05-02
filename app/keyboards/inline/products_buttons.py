import app.keyboards.inline.callback_datas as cd
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.inline.helper_buttons import back
from app.database.kinds import find_kinds
from app.database import products as prod_db

# ?menu Product buttons

admin_menu_prod = InlineKeyboardMarkup(
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
                text="Товари за видом",
                callback_data=cd.prod_menu_callback.new(value="sort"),
            ),
            InlineKeyboardButton(
                text="Види товарів",
                callback_data=cd.prod_menu_callback.new(value="Kinds"),
            ),
        ],
    ]
)
admin_menu_prod.add(back("admin_menu"))

user_menu_prod = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Усі товари",
                callback_data=cd.prod_menu_callback.new(value="list"),
            ),
            InlineKeyboardButton(
                text="Товари за видом",
                callback_data=cd.prod_menu_callback.new(value="sort"),
            ),
        ],
    ]
)
user_menu_prod.add(back("user_menu"))


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
                callback_data=cd.menu_callback.new(value="Products"),
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


async def products_list(pages: int, check, kind):
    prod_list_kb = InlineKeyboardMarkup()
    products = await prod_db.get_products(6, pages, kind)
    async for prod in products:
        _id = prod["_id"]
        label = prod["label"]
        amount = prod["amount"]
        text_button = f"{label}\t\t, {amount/100.00} грн."
        if check == "admin":
            prod_list_kb.add(
                InlineKeyboardButton(
                    text=text_button,
                    callback_data=cd.prod_info_callback.new(_id=f"{_id}"),
                )
            )
        elif check == "user":
            prod_list_kb.add(
                InlineKeyboardButton(
                    text=text_button,
                    callback_data=cd.prod_info_callback.new(_id=f"{_id}"),
                )
            )
    pages_back = pages - 6
    pages_next = pages + 6
    prod_list_kb.add(
        InlineKeyboardButton(
            text="<== Попередня сторінка",
            callback_data=cd.prod_nav_list_callback.new(
                pages=f"{pages_back}"
            ),
        )
    )
    prod_list_kb.insert(
        InlineKeyboardButton(
            text="Наступна сторінка ==>",
            callback_data=cd.prod_nav_list_callback.new(
                pages=f"{pages_next}"
            ),
        )
    )
    prod_list_kb.add(back("products"))
    return prod_list_kb


async def kinds_kb(check):
    kind_list = await find_kinds()
    kind_list_kb = InlineKeyboardMarkup(row_width=2)
    async for kind in kind_list:
        kind = kind['name']
        kind_list_kb.insert(
            InlineKeyboardButton(
                text=kind,
                callback_data=cd.prod_button_sort.new(kind=f"{kind}"),
            )
        )
    kind_list_kb.add(back("products"))
    return kind_list_kb


async def info_product(prod_id: str, check: str):
    if check == "admin":
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
    else:
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
                    callback_data=cd.checkout_cart.new(_id=f"{prod_id}"),
                ),
            ],
        ]
    )
    info_prod.add(back("prod_list"))
    return info_prod


async def del_product(prod_id: str):
    del_prod = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.checkout_order.new(
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
    ]
)
edit_fields.add(back("prod_list"))
