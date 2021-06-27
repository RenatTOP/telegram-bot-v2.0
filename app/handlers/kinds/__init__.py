from aiogram import Dispatcher

from app.handlers.kinds.add_kind import register_handlers_add_kind
from app.handlers.kinds.edit_kind import register_handlers_edit_kind
from app.handlers.kinds.del_kind import register_handlers_del_kind
from app.handlers.kinds.menu import register_handlers_menu_kinds


def register_handlers_kinds(dp: Dispatcher):
    register_handlers_menu_kinds(dp)
    register_handlers_add_kind(dp)
    register_handlers_edit_kind(dp)
    register_handlers_del_kind(dp)