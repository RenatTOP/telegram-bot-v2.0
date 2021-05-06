import json
from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from app.database import user_cart as cart_db
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import user_buttons as kb
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline.helper_buttons import back
from app.middlewares.checks import check_kind, check_cart
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline.callback_datas import prod_info_callback
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def cart(message: Message):
    user_id = message.from_user.id
    text = await cart_db.get_products_from_cart(user_id)
    await message.answer(text)


async def cart_call(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    user_id = call.from_user.id
    text = await cart_db.get_products_from_cart(user_id)
    cart_kb = kb.cart_kb
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=cart_kb
    )


async def add_prod_to_cart(call: CallbackQuery):
    user_id = call.from_user.id
    prod = call["data"]
    prod_id = prod.replace("add_to_cart:", "")
    add = await cart_db.add_product_to_cart(user_id, prod_id)
    if add:
        text = "Одиниця товару додана до кошика"
    else:
        text = "У вашому кошику максимальна кількість цього товару (5)"
    await bot.answer_callback_query(
        callback_query_id=call.id, text=text, show_alert=False
    )


async def del_prod_from_cart(call: CallbackQuery):
    user_id = call.from_user.id
    try:
        prod = call["data"]
        prod_id = prod.replace("del_from_cart:", "")
        await cart_db.del_product_from_cart(user_id, prod_id)
        text = "Одиниця товару видалена із кошика"
    except:
        text = "Товару нема у кошику"
    await bot.answer_callback_query(
        callback_query_id=call.id, text=text, show_alert=False
    )


async def order_prod_in_cart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    user_id = call.from_user.id
    cart_text = await cart_db.get_products_from_cart(user_id)
    if "порожньо" in cart_text:
        text = "Ваш кошик порожній"
        await bot.answer_callback_query(
            callback_query_id=call.id, text=text, show_alert=False
        )
    else:
        data = call["data"]
        prod_id = data.replace("checkout_cart:", "")
        # cart = json.dumps(cart)
        # cart = cart.replace(":", "#")
        cart_kb = await kb.confirm_cart(prod_id)
        text = cart_text + "\n\n <b>Підтверджуєте це замовлення?</b>"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=cart_kb
        )


async def clear_cart(call: CallbackQuery):
    user_id = call.from_user.id
    if await check_cart(user_id):
        text = "Ваш кошик тепер порожній"
        await cart_db.clear_cart(user_id)
    else:
        text = "Ваш кошик порожній"
    await bot.answer_callback_query(
        callback_query_id=call.id, text=text, show_alert=False
    )


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart, commands=["cart"])
    dp.register_callback_query_handler(cart_call, cd.menu_callback.filter(value="Cart"))
    dp.register_callback_query_handler(add_prod_to_cart, cd.add_to_cart_button.filter())
    dp.register_callback_query_handler(
        del_prod_from_cart, cd.del_from_cart_button.filter()
    )
    dp.register_callback_query_handler(
        clear_cart, cd.button_back_callback.filter(value="clear")
    )
    dp.register_callback_query_handler(order_prod_in_cart, cd.checkout_cart.filter())
