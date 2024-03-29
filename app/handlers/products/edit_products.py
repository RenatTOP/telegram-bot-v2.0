import re
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import dp
from bot import bot
from app.middlewares import checks
from app.states.product import Edit_Product
from app.database import products as prod_db
from app.middlewares.checks import check_kind
from aiogram.types import Message, CallbackQuery
from app.middlewares.state_check import state_check
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.checks import check_admin_or_user
from app.keyboards.inline import products_buttons as kb
from app.middlewares.helpers import call_chat_and_message
from app.handlers.products.prod_helper import string_kinds, string_confirm


async def info_prod(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    check = await check_admin_or_user(state)
    prod_id = call["data"]
    prod_id = prod_id.replace("prod_info_edit:", "")
    prod_data = await prod_db.get_product_by_id(prod_id)
    picture = prod_data["picture"]
    text = (
        f"{hlink(' ', f'{picture}')}\n"
        f'<b>{prod_data["label"]}</b>\n'
        f'<b>{prod_data["kind"]}</b>,\n'
        f'<b>{int(prod_data["amount"])/100.00} грн.</b>,\n'
        f'<b>{prod_data["about"]}</b> \n'
    )
    kb_info_prod = await kb.info_product(prod_id, check)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_info_prod,
    )


async def edit_prod(call: CallbackQuery, state=FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    prod = call["data"]
    prod_id = prod.replace("prod_edit:", "")
    await state_check(state)
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
    edit_prod.add(back("prod_list"))
    if my_state == "Edit_Product:edit_label":
        dp.loop.create_task(prod_db.edit_product(_id, "label", value))
        await message.answer(text=text, reply_markup=edit_prod)
    elif my_state == "Edit_Product:edit_amount":
        if value.isdigit():
            dp.loop.create_task(prod_db.edit_product(_id, "amount", value))
            await message.answer(text=text, reply_markup=edit_prod)
        else:
            text = "Введіть ціну коректно"
            await message.answer(text=text, reply_markup=None)
            return
    elif my_state == "Edit_Product:edit_kind":
        if await check_kind(value):
            dp.loop.create_task(prod_db.edit_product(_id, "kind", value))
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
            text = (
                "Немає такого виду, введіть один із переліку або створять новий\n"
                + f"{kinds}"
            )
            await message.answer(text=text, reply_markup=edit_prod)
            return
    elif my_state == "Edit_Product:edit_about":
        dp.loop.create_task(prod_db.edit_product(_id, "about", value))
        await message.answer(text=text, reply_markup=edit_prod)
    elif my_state == "Edit_Product:edit_picture":
        dp.loop.create_task(prod_db.edit_product(_id, "picture", value))
        await message.answer(text=text, reply_markup=edit_prod)

    await state_check(state)


def register_handlers_edit_product(dp: Dispatcher):
    dp.register_callback_query_handler(info_prod, cd.prod_info_callback.filter())
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
