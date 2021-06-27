from aiogram import Dispatcher

from app.handlers.products.menu import register_handlers_menu_products
from app.handlers.products.prod_list import register_handlers_product_list
from app.handlers.products.del_product import register_handlers_del_product
from app.handlers.products.add_product import register_handlers_add_product
from app.handlers.products.edit_products import register_handlers_edit_product


def register_handlers_products(dp: Dispatcher):
    register_handlers_add_product(dp)
    register_handlers_product_list(dp)
    register_handlers_edit_product(dp)
    register_handlers_del_product(dp)
    register_handlers_menu_products(dp)