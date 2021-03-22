import re
from bot import bot
import app.middlewares.checks
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from app.states.product import Edit_Product
from app.middlewares.checks import check_admin_or_user
from app.database import products as prod_db
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import products_buttons as kb
from app.keyboards.inline import helper_buttons as help_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.handlers.products.prod_helper import string_kinds, string_confirm


async def product_list(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    data = call["data"]
    print(data)
    text = "Перелік товарів"
    pages = 0
    if 'nav_prod' in data:
        pages = data.split("nav_prod:", 1)[1]
        pages = int(pages)
    prod_count = await prod_db.get_count_products()
    if pages > prod_count:
        text = "Це остання сторінка"
        await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )
    elif pages < 0:
        text = "Це перша сторінка"
        await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )
    else:
        products = await prod_db.get_products(6, pages)
        kb_prod_list = await kb.products_list(products, pages)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb_prod_list,
        )


async def info_prod(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod_id = call["data"]
    prod_id = prod_id.split("prod_info_edit:", 1)[1]
    prod_data = await prod_db.get_product_by_id(prod_id)
    picture = prod_data["picture"]
    text = (
        f"{hlink(' ', f'{picture}')}\n"
        f'Назва товару: <b>{prod_data["label"]}</b>\n'
        f'Вид: <b>{prod_data["kind"]}</b>,\n'
        f'Ціна:<b>{prod_data["amount"]/100.00} грн.</b>,\n'
        f'Опис:<b>{prod_data["about"]}</b> \n'
    )
    kb_info_prod = await kb.admin_info_product(prod_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_info_prod,
    )


async def user_info_prod(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod_id = call["data"]
    prod_id = prod_id.split("prod_info_edit:", 1)[1]
    prod_data = await prod_db.get_product_by_id(prod_id)
    picture = prod_data["picture"]
    text = (
        f"{hlink(' ', f'{picture}')}\n"
        f'<b>{prod_data["label"]}</b>\n'
        f'<b>{prod_data["kind"]}</b>,\n'
        f'<b>{prod_data["amount"]/100.00} грн.</b>,\n'
        f'<b>{prod_data["about"]}</b> \n'
    )
    kb_info_prod = await kb.user_info_product(prod_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_info_prod,
    )



async def edit_prod(call: CallbackQuery, state=FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    prod_id = prod.split("prod_edit:", 1)[1]
    await state.finish()
    await state.update_data(_id=prod_id)
    text = "Оберіть що треба редагувати"
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=kb.edit_fields
    )


async def edit_field(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    if re.search(r"label", prod):
        await Edit_Product.first()
        text = "Введіть нову назву товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"amount", prod):
        await Edit_Product.edit_amount.set()
        text = "Введіть нову ціну товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"kind", prod):
        await Edit_Product.edit_kind.set()
        text = "Введіть новий вид товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"about", prod):
        await Edit_Product.edit_about.set()
        text = "Введіть новий опис товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"picture", prod):
        await Edit_Product.edit_picture.set()
        text = "Введіть новие посилання на картинку товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )


async def confirm_change(message: Message, state: FSMContext):
    my_state = await state.get_state()
    data = await state.get_data()
    _id = data["_id"]
    value = message.text
    value = value.strip()
    text = "Зміни прийняті"
    edit_prod = InlineKeyboardMarkup()
    edit_prod.add(await help_kb.back("prod_list"))
    if my_state == "Edit_Product:edit_label":
        await prod_db.edit_product(_id, "label", value)
        await message.answer(text=text, reply_markup=edit_prod)

    elif my_state == "Edit_Product:edit_amount":
        if value.isdigit():
            await prod_db.edit_product(_id, "amount", value)
            await message.answer(text=text, reply_markup=edit_prod)
        else:
            text = 'Введіть ціну коректно'
            await message.answer(text=text, reply_markup=None)
            return

    elif my_state == "Edit_Product:edit_kind":
        if await check_kind(value):
            await prod_db.edit_product(_id, "kind", value)
            await message.answer(text=text, reply_markup=edit_prod)
        else:
            await state.update_data(kind=value)
            kinds = await string_kinds()
            edit_prod = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Додати вид",
                            callback_data=cd.kind_add_callback.new(value="add"),
                        ),
                    ],
                ]
            )
            text = "Немає такого виду, введіть один"+\
                    "із переліку або створять новий\n"+\
                    f"{kinds}"
            await message.answer(text=text, reply_markup=edit_prod)
            return

    elif my_state == "Edit_Product:edit_about":
        await prod_db.edit_product(_id, "about", value)
        await message.answer(text=text, reply_markup=edit_prod)

    elif my_state == "Edit_Product:edit_picture":
        await prod_db.edit_product(_id, "picture", value)
        await message.answer(text=text, reply_markup=edit_prod)

    await state.finish()


def register_handlers_edit_product(dp: Dispatcher):
    dp.register_callback_query_handler(
        product_list, cd.prod_menu_callback.filter(value=["list"])
    )
    dp.register_callback_query_handler(
        product_list, cd.prod_nav_list_callback.filter()
    )
    dp.register_callback_query_handler(
        product_list, cd.button_back_callback.filter(value=["prod_list"])
    )
    dp.register_callback_query_handler(info_prod, cd.prod_info_callback.filter())
    dp.register_callback_query_handler(user_info_prod, cd.prod_user_info_callback.filter())
    dp.register_callback_query_handler(edit_prod, cd.prod_button_edit_callback.filter())
    dp.register_callback_query_handler(edit_field, cd.prod_edit_edit_callback.filter())
    dp.register_message_handler(
        confirm_change,
        state=[
            Edit_Product.edit_label,
            Edit_Product.edit_amount,
            Edit_Product.edit_kind,
            Edit_Product.edit_about,
            Edit_Product.edit_picture,
        ],
    )