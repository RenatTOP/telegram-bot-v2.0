from aiogram import Dispatcher

from app.handlers.menus.user_menu import register_handlers_user_menu
from app.handlers.menus.admin_menu import register_handlers_admin_menu


def register_handlers_menus(dp: Dispatcher):
    register_handlers_admin_menu(dp)
    register_handlers_user_menu(dp)