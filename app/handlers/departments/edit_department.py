from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.dispatcher import FSMContext
import app.middlewares.checks
from app.keyboards.inline import department_buttons as kb
import logging
from app.keyboards.inline import callback_datas as cd
from bot import bot
from app.database import departments as depart_db
from app.handlers.departments.depart_helper import string_week
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.middlewares.helpers import call_chat_and_message
import re
from app.states.department import Edit_Department
from do import start


async def department_list(message: Message):
    # chat_id, message_id = await call_chat_and_message(call)
    departments = depart_db.departments_list()
    depart_list = InlineKeyboardMarkup(row_width=2)
    text_button = ""
    for depart in departments:
        _id = depart["_id"]
        name = depart["name"]
        city = depart["city"]
        text_button = f"{name}\t\t м.{city}"
        depart_list.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=cd.depart_info_callback.new(_id=f"{_id}"),
            )
        )
    text = "Перелік закладів"
    await message.answer(text=text, reply_markup=depart_list)


async def info_depart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart_id = call["data"]
    depart_id = depart_id.split("depart_info_edit:", 1)[1]
    depart_data = depart_db.find_department(_id=depart_id)
    week = await string_week(depart_data["timetable"])
    text = (
        f'Назва закладу: <b>{depart_data["name"]}</b>\n'
        f'Адреса: <b>{depart_data["region"]}</b>,'
        f'<b>{depart_data["city"]}</b>,'
        f'<b>{depart_data["address"]}</b> \n'
        f'Телефон: <b>{depart_data["phone"]}</b>\n'
        f"Розклад:\n"
        f"{week}"
    )
    edit_depart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редагувати",
                    callback_data=cd.depart_button_edit_callback.new(
                        _id=f"{depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Видалити",
                    callback_data=cd.depart_button_del_callback.new(_id=f"{depart_id}"),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Повернутися",
                    callback_data=cd.depart_button_back_callback.new(q="True"),
                )
            ],
        ]
    )
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_depart
    )


async def del_depart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_del:", 1)[1]
    depart_db.del_department(depart_id)
    text = "Ви видалили заклад"
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )


async def edit_depart(call: CallbackQuery, state=FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_edit:", 1)[1]
    await state.finish()
    await state.update_data(_id=depart_id)
    text = "Оберіть що треба редагувати"
    edit_depart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назва",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="name"
                    ),
                ),
                InlineKeyboardButton(
                    text="Область",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="region"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Телефон",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="phone"
                    ),
                ),
                InlineKeyboardButton(
                    text="Місто",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="city"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Розклад",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="timetable"
                    ),
                ),
                InlineKeyboardButton(
                    text="Адреса",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="address"
                    ),
                ),
            ],
        ]
    )
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_depart
    )


async def edit_field(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    if re.search(r"name", depart):
        await Edit_Department.first()
        text = "Введіть нову назву закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )

    elif re.search(r"region", depart):
        await Edit_Department.edit_region.set()
        text = "Введіть нову область закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )

    elif re.search(r"city", depart):
        await Edit_Department.edit_city.set()
        text = "Введіть нове місто закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )

    elif re.search(r"address", depart):
        await Edit_Department.edit_address.set()
        text = "Введіть нову адресу закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )

    elif re.search(r"phone", depart):
        await Edit_Department.edit_phone.set()
        text = "Введіть новий телефон закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )

    elif re.search(r"timetable", depart):
        await Edit_Department.edit_timetable.set()
        text = "Введіть новий графік робіт закладу"
        await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )


async def confirm_change(message: Message, state: FSMContext):
    my_state = await state.get_state()
    data = await state.get_data()
    _id = data["_id"]
    value = message.text
    text = "Зміни прийняті"
    if my_state == "Edit_Department:edit_name":
        await state.finish()
        await message.answer(text=text)

    elif my_state == "Edit_Department:edit_region":
        depart_db.edit_depart(_id, 'region', value)
        await state.finish()
        await message.answer(text=text)

    elif my_state == "Edit_Department:edit_city":
        depart_db.edit_depart(_id, 'city', value)
        await state.finish()
        await message.answer(text=text)

    elif my_state == "Edit_Department:edit_address":
        depart_db.edit_depart(_id, 'address', value)
        await state.finish()
        await message.answer(text=text)

    elif my_state == "Edit_Department:edit_phone":
        depart_db.edit_depart(_id, 'phone', value)
        await state.finish()
        await message.answer(text=text)

    elif my_state == "Edit_Department:edit_timetable":
        depart_db.edit_depart(_id, 'timetable', value)
        await state.finish()
        await message.answer(text=text)


def register_handlers_edit_department(dp: Dispatcher):
    dp.register_message_handler(department_list, commands=["edit"])
    dp.register_callback_query_handler(info_depart, cd.depart_info_callback.filter())
    dp.register_callback_query_handler(
        del_depart, cd.depart_button_del_callback.filter()
    )
    dp.register_callback_query_handler(
        edit_depart, cd.depart_button_edit_callback.filter()
    )
    dp.register_callback_query_handler(
        edit_field, cd.depart_edit_edit_callback.filter()
    )
    dp.register_message_handler(
        confirm_change,
        state=[
            Edit_Department.edit_name,
            Edit_Department.edit_region,
            Edit_Department.edit_city,
            Edit_Department.edit_address,
            Edit_Department.edit_phone,
            Edit_Department.edit_timetable,
        ],
    )
