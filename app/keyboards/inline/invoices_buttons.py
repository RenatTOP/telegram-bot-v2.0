from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from app.keyboards.inline.helper_buttons import back
from app.database import invoices as invoice_db
from app.keyboards.inline import callback_datas as cd


sort_invoices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Відкриті",
                callback_data=cd.invoices_sort_callback.new(value="opened"),
            ),
            InlineKeyboardButton(
                text="Скасовані",
                callback_data=cd.invoices_sort_callback.new(value="canceled"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Підтверджені",
                callback_data=cd.invoices_sort_callback.new(value="confirmed"),
            ),
            InlineKeyboardButton(
                text="Закриті",
                callback_data=cd.invoices_sort_callback.new(value="closed"),
            ),
        ],
    ]
)

admin_menu_prod.add(back("admin_menu"))


async def invoices_list(pages: int, check: str, sort: str) -> InlineKeyboardMarkup:
    invoice_list_kb = InlineKeyboardMarkup()
    invoices = await invoice_db.get_invoices(6, pages, sort)
    async for invoice in invoices:
        _id = invoice["_id"]
        number = invoice["number"]
        status = invoice["status"]
        text_button = f"{number}\t\t, {status}"

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


async def invoices_list(pages: int, check: str, sort: str) -> InlineKeyboardMarkup:
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
            callback_data=cd.prod_nav_list_callback.new(pages=f"{pages_back}"),
        )
    )
    prod_list_kb.insert(
        InlineKeyboardButton(
            text="Наступна сторінка ==>",
            callback_data=cd.prod_nav_list_callback.new(pages=f"{pages_next}"),
        )
    )
    prod_list_kb.add(back("products"))
    return prod_list_kb
