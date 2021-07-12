from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import dp
from bot import bot
from app.middlewares import helpers
from app.states.department import Department
from app.database import departments as depart_db
from app.middlewares.checks import check_is_admin
from app.middlewares.state_check import state_check
from app.handlers.departments.depart_helper import *
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import department_buttons as kb
from app.middlewares.helpers import call_chat_and_message


async def add_department(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    await state_check(state)
    Department.first()
    text = f"Введіть назву закладу"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb.cancel_add_depart,
    )


async def depart_name(message: Message, state: FSMContext):
    name = message.text
    name = name.strip()
    depart_data = await state.get_data()
    if "name" in depart_data:
        await state.update_data(name=name)
        depart_data = await state.get_data()
        await Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(name=name)
        await Department.next()
        text = f"Введіть область в якій знаходиться заклад"
        await message.answer(text)


async def depart_region(message: Message, state: FSMContext):
    region = message.text
    region = region.strip()
    depart_data = await state.get_data()
    if "region" in depart_data:
        await state.update_data(region=region)
        depart_data = await state.get_data()
        Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(region=region)
        Department.next()
        text = f"Введіть місто у якому знаходиться заклад"
        await message.answer(text)


async def depart_city(message: Message, state: FSMContext):
    city = message.text
    city = city.strip()
    depart_data = await state.get_data()
    if "city" in depart_data:
        await state.update_data(city=city)
        depart_data = await state.get_data()
        Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(city=city)
        Department.next()
        text = "Тепер введіть адресу закладу"
        await message.answer(text)


async def depart_address(message: Message, state: FSMContext):
    address = message.text
    address = address.strip()
    depart_data = await state.get_data()
    if "address" in depart_data:
        await state.update_data(address=address)
        depart_data = await state.get_data()
        Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(address=address)
        Department.next()
        text = "Тепер введіть телефон/и закладу"
        await message.answer(text)


async def depart_phone(message: Message, state: FSMContext):
    phone = message.text
    phone = phone.strip()
    depart_data = await state.get_data()
    if "phone" in depart_data:
        await state.update_data(phone=phone)
        depart_data = await state.get_data()
        Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(phone=phone)
        Department.next()
        text = "Тепер введіть ID адміністратора закладу"
        await message.answer(text)


async def depart_admin(message: Message, state: FSMContext):
    admin = message.text
    admin = int(admin)
    depart_data = await state.get_data()
    if "admin" in depart_data:
        await state.update_data(admin=admin)
        depart_data = await state.get_data()
        Department.waiting_for_confirm.set()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    else:
        await state.update_data(admin=admin)
        Department.next()
        text = (
            "Тепер введіть розклад закладу у порядку\n"
            "від понеділка до неділі наприклад:\n"
            "8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|10:00-20:00|вихідний"
        )
        await message.answer(text)


async def depart_timetable(message: Message, state: FSMContext):
    try:
        timetable = message.text
        (
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
        ) = timetable.split("|")
        monday = monday.strip()
        tuesday = tuesday.strip()
        wednesday = wednesday.strip()
        thursday = thursday.strip()
        friday = friday.strip()
        friday = friday.strip()
        saturday = saturday.strip()
        sunday = sunday.strip()
        timetable = {
            "Понеділок": monday,
            "Вівторок": tuesday,
            "Середа": wednesday,
            "Четвер": thursday,
            "Пятниця": friday,
            "Субота": saturday,
            "Неділя": sunday,
        }
        depart_data = await state.get_data()
        if "timetable" in depart_data:
            await state.update_data(timetable=timetable)
            depart_data = await state.get_data()
            Department.waiting_for_confirm.set()
        else:
            await state.update_data(timetable=timetable)
            depart_data = await state.get_data()
            Department.next()
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await message.answer(text, reply_markup=kb.confinm_depart)
    except:
        await message.answer(
            "Введіть розклад закладу у порядку\n"
            "від понеділка до неділі наприклад:\n"
            "8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|8:00-22:00|10:00-20:00|вихідний"
        )
        return


async def confirm_department(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    if call["data"] == "depart_confirm:Yes":
        depart_data = await state.get_data()
        name = depart_data["name"]
        region = depart_data["region"]
        city = depart_data["city"]
        address = depart_data["address"]
        phone = depart_data["phone"]
        admin = depart_data["admin"]
        timetable = depart_data["timetable"]
        dp.loop.create_task(depart_db.add_department(
            name, region, city, address, phone, timetable, admin
        ))
        edit_depart = InlineKeyboardMarkup()
        edit_depart.add(back("depart_list"))
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(
            f'Заклад "{name}" було додано', reply_markup=edit_depart
        )
        await state_check(state)

    elif call["data"] == "depart_confirm:No":
        text = "Оберіть що треба редагувати:"
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb.add_edit_depart,
        )

    elif call["data"] == "depart_add_edit:name":
        Department.waiting_for_name.set()
        text = "Введіть нову назву закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

    elif call["data"] == "depart_add_edit:region":
        Department.waiting_for_region.set()
        text = "Введіть нову область закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

    elif call["data"] == "depart_add_edit:city":
        Department.waiting_for_city.set()
        text = "Введіть нове місто закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

    elif call["data"] == "depart_add_edit:address":
        Department.waiting_for_address.set()
        text = "Введіть новий адрес закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

    elif call["data"] == "depart_add_edit:phone":
        Department.waiting_for_phone.set()
        text = "Введіть новий телефон закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

    elif call["data"] == "depart_add_edit:timetable":
        Department.waiting_for_timetable.set()
        text = "Введіть новий розклад закладу"
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


async def cancel(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Відкинути всі зміни?"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=kb.confirm_or_fail_cancel,
    )


async def fail_cancel(call: CallbackQuery, state: FSMContext):
    chat_id, message_id = await call_chat_and_message(call)
    my_state = await state.get_state()
    if my_state == "Department:waiting_for_name":
        text = "Введіть назву закладу"
        await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
        )
    elif my_state == "Department:waiting_for_confirm":
        depart_data = await state.get_data()
        timetable = depart_data["timetable"]
        week = await string_week(timetable)
        text = await string_confirm(depart_data, week)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=kb.confinm_depart,
        )


def register_handlers_add_department(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_department, cd.depart_menu_callback.filter(value=["add"]), state="*"
    )
    dp.register_message_handler(depart_name, state=Department.waiting_for_name)
    dp.register_message_handler(depart_region, state=Department.waiting_for_region)
    dp.register_message_handler(depart_city, state=Department.waiting_for_city)
    dp.register_message_handler(depart_address, state=Department.waiting_for_address)
    dp.register_message_handler(depart_phone, state=Department.waiting_for_phone)
    dp.register_message_handler(depart_admin, state=Department.waiting_for_admin)
    dp.register_message_handler(
        depart_timetable, state=Department.waiting_for_timetable
    )
    dp.register_callback_query_handler(
        confirm_department,
        cd.depart_confirm_callback.filter(value=["Yes", "No"]),
        state=Department.waiting_for_confirm,
    )
    dp.register_callback_query_handler(
        confirm_department,
        cd.depart_add_edit_callback.filter(
            field=["name", "region", "city", "address", "phone", "timetable"]
        ),
        state=Department.waiting_for_confirm,
    )
    dp.register_callback_query_handler(
        cancel, cd.depart_confirm_callback.filter(value=["Cancel"]), state="*"
    )
    dp.register_callback_query_handler(
        fail_cancel, cd.depart_confirm_callback.filter(value=["Not"]), state="*"
    )
