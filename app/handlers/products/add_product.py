from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.database import kinds as kind_db
from app.database import products as prod_db
from app.states.product import Kind, Product
from app.middlewares.checks import check_kind
from app.middlewares.state_check import state_check
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.checks import check_admin_or_user
from app.keyboards.inline import products_buttons as kb
from app.middlewares.helpers import call_chat_and_message
from app.handlers.products.prod_helper import string_kinds, string_confirm


async def add_product(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    await state_check(state)
    await state.set_state(await Product.first())
    text = f"Введіть назву товару"
    kb_prod_back = InlineKeyboardMarkup()
    kb_prod_back.add(back("products"))
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_prod_back,
    )


async def prod_label(message: Message, state: FSMContext):
    label = message.text
    label = label.strip()
    prod_data = await state.get_data()
    if "label" in prod_data:
        await state.update_data(label=label)
        prod_data = await state.get_data()
        await state.set_state(await Product.waiting_for_confirm.set())
        text = await string_confirm(prod_data)
        await message.answer(text, reply_markup=kb.confinm_prod)
    else:
        await state.update_data(label=label)
        await state.set_state(await Product.next())
        text = f"Введіть ціну товару у копійках"
        await message.answer(text)


async def prod_amount(message: Message, state: FSMContext):
    amount = message.text
    amount = amount.strip()
    prod_data = await state.get_data()
    if amount.isdigit():
        if "amount" in prod_data:
            await state.update_data(amount=amount)
            prod_data = await state.get_data()
            await state.set_state(await Product.waiting_for_confirm.set())
            text = await string_confirm(prod_data)
            await message.answer(text, reply_markup=kb.confinm_prod)
        else:
            await state.update_data(amount=amount)
            await state.set_state(await Product.next())
            text = f"Введіть вид товару"
            await message.answer(text)
    else:
        text = "Введіть ціну коректно"
        await message.answer(text=text, reply_markup=None)
        return


async def prod_kind(message: Message, state: FSMContext):
    kind = message.text
    kind = kind.strip()
    prod_data = await state.get_data()
    if await check_kind(kind):
        if "prod_kind" in prod_data:
            await state.update_data(prod_kind=kind)
            prod_data = await state.get_data()
            await state.set_state(await Product.waiting_for_confirm.set())
            text = await string_confirm(prod_data)
            await message.answer(text, reply_markup=kb.confinm_prod)
        else:
            await state.update_data(prod_kind=kind)
            await state.set_state(await Product.next())
            text = "Введіть опис товару"
            await message.answer(text)
    else:
        await state.update_data(add_kind=kind)
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
            "Немає такого виду, введіть один"
            + "із переліку або створять новий\n"
            + f"{kinds}"
        )
        await message.answer(text=text, reply_markup=edit_prod)
        return


async def kind_list(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Введіть назву нового виду товарів"
    await state.set_state(await Kind.waiting_for_name_prod.set())
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


async def kind_name(message: Message, state: FSMContext):
    name = message.text
    name = name.strip()
    kind = await state.get_data()
    kind = kind["add_kind"]
    if kind != name:
        text = "Введений раніше вид та створений " + "не співпадають, введіть коректно"
    elif not await check_kind(name):
        await state.update_data(prod_kind=name)
        text = "Новий вид створено\nТепер введіть опис товару"
        await state.set_state(await Product.waiting_for_about.set())
        await kind_db.add_kind(name)
    else:
        text = "Такий вид вже є!"
    await message.answer(text)


async def prod_about(message: Message, state: FSMContext):
    about = message.text
    about = about.strip()
    prod_data = await state.get_data()
    if "about" in prod_data:
        await state.update_data(about=about)
        prod_data = await state.get_data()
        await state.set_state(await Product.waiting_for_confirm.set())
        text = await string_confirm(prod_data)
        await message.answer(text, reply_markup=kb.confinm_prod)
    else:
        await state.update_data(about=about)
        await state.set_state(await Product.next())
        text = "Введіть посилання на картинку товару"
        await message.answer(text)


async def prod_picture(message: Message, state: FSMContext):
    picture = message.text
    picture = picture.strip()
    prod_data = await state.get_data()
    if "picture" in prod_data:
        await state.update_data(picture=picture)
        prod_data = await state.get_data()
        await state.set_state(await Product.waiting_for_confirm.set())
    else:
        await state.update_data(picture=picture)
        await state.set_state(await Product.next())
    prod_data = await state.get_data()
    text = await string_confirm(prod_data)
    await message.answer(text, reply_markup=kb.confinm_prod)


async def confirm_product(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    if call["data"] == "prod_confirm:Yes":
        prod_data = await state.get_data()
        label = prod_data["label"]
        amount = int(prod_data["amount"])
        kind = prod_data["prod_kind"]
        about = prod_data["about"]
        picture = prod_data["picture"]
        dp.loop.create_task(prod_db.add_product(label, amount, kind, about, picture))
        edit_prod = InlineKeyboardMarkup()
        edit_prod.add(back("products"))
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(
            f'Товар "{label}" було додано', reply_markup=edit_prod
        )
        await state_check(state)
    elif call["data"] == "prod_confirm:No":
        text = "Оберіть що треба редагувати:"
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb.add_edit_prod,
        )
    elif call["data"] == "prod_add_edit:label":
        await state.set_state(await Product.waiting_for_label.set())
        text = "Введіть нову назву товару"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
    elif call["data"] == "prod_add_edit:amount":
        await state.set_state(await Product.waiting_for_amount.set())
        text = "Введіть нову ціну товару у копійках"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
    elif call["data"] == "prod_add_edit:prod_kind":
        await state.set_state( await Product.waiting_for_kind.set())
        text = "Введіть новий вид товару"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
    elif call["data"] == "prod_add_edit:about":
        await state.set_state(await Product.waiting_for_about.set())
        text = "Введіть новий опис товару"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
    elif call["data"] == "prod_add_edit:picture":
        await state.set_state(await Product.waiting_for_picture.set())
        text = "Введіть новие посилання на картинку товару"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


async def cancel(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Відкинути всі зміни?"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb.confirm_or_fail_cancel,
    )


async def fail_cancel(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    my_state = await state.get_state()
    if my_state == "Product:waiting_for_label":
        text = "Введіть назву товару"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )
    elif my_state == "Product:waiting_for_confirm":
        prod_data = await state.get_data()
        text = await string_confirm(prod_data)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb.confinm_prod,
        )


def register_handlers_add_product(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_product, cd.prod_menu_callback.filter(value=["add"]), state="*"
    )
    dp.register_message_handler(prod_label, state=Product.waiting_for_label)
    dp.register_message_handler(prod_amount, state=Product.waiting_for_amount)
    dp.register_message_handler(prod_kind, state=Product.waiting_for_kind)
    dp.register_message_handler(prod_about, state=Product.waiting_for_about)
    dp.register_message_handler(prod_picture, state=Product.waiting_for_picture)
    dp.register_callback_query_handler(
        kind_list, cd.kind_add_callback.filter(value="add"), state="*"
    )
    dp.register_message_handler(kind_name, state=Kind.waiting_for_name_prod)
    dp.register_callback_query_handler(
        confirm_product,
        cd.prod_confirm_callback.filter(value=["Yes", "No"]),
        state=Product.waiting_for_confirm,
    )
    dp.register_callback_query_handler(
        confirm_product,
        cd.prod_add_edit_callback.filter(
            field=["label", "amount", "prod_kind", "about", "picture"]
        ),
        state=Product.waiting_for_confirm,
    )
    dp.register_callback_query_handler(
        cancel, cd.prod_confirm_callback.filter(value=["Cancel"]), state="*"
    )
    dp.register_callback_query_handler(
        fail_cancel, cd.prod_confirm_callback.filter(value=["Not"]), state="*"
    )
