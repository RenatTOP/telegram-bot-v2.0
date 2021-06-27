from aiogram.dispatcher.filters.state import State, StatesGroup


class Department(StatesGroup):
    waiting_for_name = State()
    waiting_for_region = State()
    waiting_for_city = State()
    waiting_for_address = State()
    waiting_for_phone = State()
    waiting_for_admin = State()
    waiting_for_timetable = State()
    waiting_for_confirm = State()
    waiting_for_edit = State()


class Edit_Department(StatesGroup):
    edit_name = State()
    edit_region = State()
    edit_city = State()
    edit_address = State()
    edit_phone = State()
    edit_admin = State()
    edit_timetable = State()