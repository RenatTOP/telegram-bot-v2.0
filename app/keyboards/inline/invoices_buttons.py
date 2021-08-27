from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from app.keyboards.inline.helper_buttons import back
from app.database import invoices as invoice_db
from app.keyboards.inline import callback_datas as cd


admin_menu_invoices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перелік рахунків",
                callback_data=cd.invoice_menu_callback.new(value="list"),
            ),
            InlineKeyboardButton(
                text="Рахунки за видом",
                callback_data=cd.invoice_menu_callback.new(value="sort"),
            ),
        ],
    ]
)
admin_menu_invoices.add(back("admin_menu"))


sort_invoices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Відкриті",
                callback_data=cd.invoice_sort_callback.new(sort="opened"),
            ),
            InlineKeyboardButton(
                text="Скасовані",
                callback_data=cd.invoice_sort_callback.new(sort="canceled"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Підтверджені",
                callback_data=cd.invoice_sort_callback.new(sort="confirmed"),
            ),
            InlineKeyboardButton(
                text="Закриті",
                callback_data=cd.invoice_sort_callback.new(sort="closed"),
            ),
        ],
    ]
)

async def invoices_list(pages: int, check: str, kind: str) -> InlineKeyboardMarkup:
    invoice_list_kb = InlineKeyboardMarkup()
    invoices = await invoice_db.get_invoices(6, pages, kind)
    async for invoice in invoices:
        _id = invoice["_id"]
        label = invoice["number"]
        amount = invoice["time"]
        text_button = f"№ {number}\t\t, T {time}"
        invoice_list_kb.add(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.invoice_info_callback.new(_id=f"{_id}"),
            )
        )
    pages_back = pages - 6
    pages_next = pages + 6
    invoice_list_kb.add(
        InlineKeyboardButton(
            text="<== Попередня сторінка",
            callback_data=cd.nav_list_callback.new(
                pages=f"{pages_back}", data="invoice"
            ),
        )
    )
    invoice_list_kb.insert(
        InlineKeyboardButton(
            text="Наступна сторінка ==>",
            callback_data=cd.nav_list_callback.new(
                pages=f"{pages_next}", data="invoice"
            ),
        )
    )
    invoice_list_kb.add(back("invoices"))
    return invoice_list_kb
