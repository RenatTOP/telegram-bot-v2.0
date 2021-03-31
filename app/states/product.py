from aiogram.dispatcher.filters.state import State, StatesGroup


class Product(StatesGroup):
    waiting_for_label = State()
    waiting_for_amount = State()
    waiting_for_kind = State()
    waiting_for_about = State()
    waiting_for_picture = State()
    waiting_for_confirm = State()
    waiting_for_edit = State()


class Edit_Product(StatesGroup):
    edit_label = State()
    edit_amount = State()
    edit_kind = State()
    edit_about = State()
    edit_picture = State()

class Kind(StatesGroup):
    waiting_for_name = State()
    waiting_for_name_prod = State()

class Edit_Kind(StatesGroup):
    edit_name = State()