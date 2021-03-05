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


async def edit_depart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_edit:", 1)[1]
    text = "Оберіть що треба редагувати"
    edit_depart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назва",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="name", _id=f"({depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Область",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="region", _id=f"({depart_id}"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Телефон",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="phone", _id=f"({depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Місто",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="city", _id=f"({depart_id}"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Розклад",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="timetable", _id=f"({depart_id}"
                    ),
                ),
                InlineKeyboardButton(
                    text="Адреса",
                    callback_data=cd.depart_edit_edit_callback.new(
                        field="address", _id=f"({depart_id}"
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
    depart_id = depart.split("(", 1)[1]
    if re.search(r"name", depart):
        text = "Введіть нову назву закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)

    elif re.search(r"region", depart):
        text = "Введіть нову область закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)

    elif re.search(r"city", depart):
        text = "Введіть нове місто закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)

    elif re.search(r"address", depart):
        text = "Введіть нову адресу закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)

    elif re.search(r"phone", depart):
        text = "Введіть новий телефон закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)

    elif re.search(r"timetable", depart):
        text = "Введіть новий графік робіт закладу"
        await bot.answer_callback_query(call.id, text="Зміни прийняті")
        await call.message.answer(text)


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
