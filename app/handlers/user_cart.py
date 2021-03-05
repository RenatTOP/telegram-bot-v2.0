from aiogram import Dispatcher
from aiogram.types import Message
import app.database.user_cart as cart_db


async def cart(message: Message):
    user_id = message.from_user.id
    user_cart = cart_db.get_products_from_cart(user_id)
    await message.answer(user_cart)


def register_handlers_cart(dp: Dispatcher):
    dp.register_message_handler(cart, commands=["cart"])
