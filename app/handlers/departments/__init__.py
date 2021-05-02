from aiogram import Dispatcher
from aiogram import Dispatcher
from app.handlers.departments.add_department import register_handlers_add_department
from app.handlers.departments.edit_department import register_handlers_edit_department
from app.handlers.departments.menu import register_handlers_menu_departments
from app.handlers.departments.del_department import register_handlers_del_department


def register_handlers_department(dp: Dispatcher):
    register_handlers_add_department(dp)
    register_handlers_edit_department(dp)
    register_handlers_del_department(dp)
    register_handlers_menu_departments(dp)