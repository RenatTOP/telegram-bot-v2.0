from aiogram import Dispatcher
from aiogram import Dispatcher
from app.handlers.menus.admin_menu import register_handlers_admin_menu


def register_handlers_menus(dp: Dispatcher):
    register_handlers_admin_menu(dp)