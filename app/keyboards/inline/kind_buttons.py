from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline.helper_buttons import back


async def kinds_list(kinds: list) -> InlineKeyboardMarkup:
    kind_list = InlineKeyboardMarkup(row_width=4)
    async for kind in kinds:
        _id = kind["_id"]
        name = kind["name"]
        text_button = f"{name}"
        kind_list.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.kind_info_callback.new(_id=f"{_id}"),
            )
        )
    kind_list.add(back("kinds"))
    return kind_list


async def info_kind(kind_id: str) -> InlineKeyboardMarkup:
    info_kind = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редагувати",
                    callback_data=cd.kind_button_edit_callback.new(
                        _id=f"{kind_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Видалити",
                    callback_data=cd.kind_button_del_callback.new(_id=f"{kind_id}"),
                ),
            ]
        ]
    )
    info_kind.add(back("kind_list"))
    return info_kind


confinm_kind = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так", callback_data=cd.kind_confirm_callback.new(value="Yes")
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.kind_confirm_callback.new(value="No")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Скасувати",
                callback_data=cd.kind_confirm_callback.new(value="Cancel"),
            )
        ],
    ]
)


confirm_or_fail_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Так",
                callback_data=cd.prod_menu_callback.new(value=["Kinds"]),
            ),
            InlineKeyboardButton(
                text="Ні", callback_data=cd.kind_confirm_callback.new(value="Not")
            ),
        ]
    ]
)


async def del_kind(kind_id: str) -> InlineKeyboardMarkup:
    del_kind = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=cd.kind_button_confirm_del_callback.new(
                        _id=f"{kind_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Ні",
                    callback_data=cd.kind_info_callback.new(_id=f"{kind_id}"),
                ),
            ],
        ]
    )
    return del_kind