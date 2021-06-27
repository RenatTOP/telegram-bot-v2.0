from aiogram.dispatcher.filters.state import State, StatesGroup


class IndicatedTime(StatesGroup):
    indicated_time = State()
