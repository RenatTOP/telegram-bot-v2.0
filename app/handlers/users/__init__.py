from aiogram import Dispatcher

from app.handlers.users.user_cart import register_handlers_cart
from app.handlers.users.user import register_handlers_init_users
from app.handlers.users.checkout import register_handlers_checkout


def register_handlers_users(dp: Dispatcher):
    register_handlers_init_users(dp)
    register_handlers_cart(dp)
    register_handlers_checkout(dp)