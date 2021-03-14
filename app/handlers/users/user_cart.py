from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from app.database import user_cart as cart_db
from app.middlewares.checks import check_kind, check_cart
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message


async def cart(message: Message):
    user_id = message.from_user.id
    user_cart = await cart_db.get_products_from_cart(user_id)
    await message.answer(user_cart)


async def add_prod_to_cart(call: CallbackQuery):
    user_id = call.from_user.id
    prod = call["data"]
    prod_id = prod.split("add_to_cart:", 1)[1]
    await cart_db.add_product_to_cart(user_id, prod_id)
    text = "Товар доданий до кошика"
    await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )


async def del_prod_from_cart(call: CallbackQuery):
    user_id = call.from_user.id
    prod = call["data"]
    prod_id = prod.split("del_from_cart:", 1)[1]
    await cart_db.del_product_from_cart(user_id, prod_id)
    text = "Товар доданий до кошика"
    await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )


async def order_prod_in_cart():
    pass


async def clear_cart(call: CallbackQuery):
    user_id = call.from_user.id
    if check_cart(user_id):
        text = "Ваш кошик тепер порожній"
        await cart_db.clear_cart(user_id)
    else:
        text = "Ваш кошик порожній"
    await bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=False
    )


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart, commands=["cart"])
