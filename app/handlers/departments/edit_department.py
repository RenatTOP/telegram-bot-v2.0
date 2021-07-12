import re
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.middlewares import checks
from app.database import departments as depart_db
from app.states.department import Edit_Department
from app.middlewares.state_check import state_check
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message
from app.keyboards.inline import department_buttons as kb
from app.handlers.departments.depart_helper import string_week



async def info_depart(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart_id = call["data"]
    depart_id = depart_id.replace("depart_info_edit:", "")
    depart_data = await depart_db.find_department(_id=depart_id)
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
    kb_info_depart = await kb.info_department(depart_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb_info_depart,
    )


async def edit_depart(call: CallbackQuery, state=FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    depart_id = depart.split("depart_edit:", 1)[1]
    await state_check(state)
    await state.update_data(_id=depart_id)
    text = "Оберіть що треба редагувати"
    edit_kb = await kb.edit_fields(depart_id)
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=edit_kb
    )


async def edit_field(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    depart = call["data"]
    if re.search(r"name", depart):
        await state.set_state(await Edit_Department.first())
        text = "Введіть нову назву закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"region", depart):
        await state.set_state(await Edit_Department.edit_region.set())
        text = "Введіть нову область закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"city", depart):
        await state.set_state(await Edit_Department.edit_city.set())
        text = "Введіть нове місто закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"address", depart):
        await state.set_state(await Edit_Department.edit_address.set())
        text = "Введіть нову адресу закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"phone", depart):
        await state.set_state(await Edit_Department.edit_phone.set())
        text = "Введіть новий телефон закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"admin", depart):
        await state.set_state(await Edit_Department.edit_admin.set())
        text = "Введіть новий ID адміністратора закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )

    elif re.search(r"timetable", depart):
        await state.set_state(await Edit_Department.edit_timetable.set())
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
    edit_depart = InlineKeyboardMarkup()
    edit_depart.add(back("depart_list"))
    if my_state == "Edit_Department:edit_name":
        dp.loop.create_task(depart_db.edit_depart(_id, "name", value))
        await message.answer(text=text, reply_markup=edit_depart)

    elif my_state == "Edit_Department:edit_region":
        dp.loop.create_task(depart_db.edit_depart(_id, "region", value))
        await message.answer(text=text, reply_markup=edit_depart)

    elif my_state == "Edit_Department:edit_city":
        dp.loop.create_task(depart_db.edit_depart(_id, "city", value))
        await message.answer(text=text, reply_markup=edit_depart)

    elif my_state == "Edit_Department:edit_address":
        dp.loop.create_task(depart_db.edit_depart(_id, "address", value))
        await message.answer(text=text, reply_markup=edit_depart)

    elif my_state == "Edit_Department:edit_admin":
        dp.loop.create_task(depart_db.edit_depart(_id, "admin", int(value)))
        await message.answer(text=text, reply_markup=edit_depart)

    elif my_state == "Edit_Department:edit_phone":
        dp.loop.create_task(depart_db.edit_depart(_id, "phone", value))
        await message.answer(text=text, reply_markup=edit_depart)
    try:
        if my_state == "Edit_Department:edit_timetable":
            (
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
            ) = value.split("|")
            monday = monday.strip()
            tuesday = tuesday.strip()
            wednesday = wednesday.strip()
            thursday = thursday.strip()
            friday = friday.strip()
            friday = friday.strip()
            saturday = saturday.strip()
            sunday = sunday.strip()
            value = {
                "Понеділок": monday,
                "Вівторок": tuesday,
                "Середа": wednesday,
                "Четвер": thursday,
                "Пятниця": friday,
                "Субота": saturday,
                "Неділя": sunday,
            }
            dp.loop.create_task(depart_db.edit_depart(_id, "timetable", value))
            await message.answer(text=text, reply_markup=edit_depart)
        await state_check(state)
    except:
        await message.answer(
            "Введіть розклад закладу у порядку\n"
            "від понеділка до неділі наприклад:\n"
            "8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|10:00-20:00|вихідний"
        )
        return


def register_handlers_edit_department(dp: Dispatcher):
    dp.register_callback_query_handler(info_depart, cd.depart_info_callback.filter())
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
            Edit_Department.edit_admin,
            Edit_Department.edit_timetable,
        ],
    )
