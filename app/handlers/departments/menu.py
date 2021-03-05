import aiogram.types
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import department_buttons as kb
from app.handlers.departments.add_department import register_handlers_add_department
from app.keyboards.inline import callback_datas as cb
from bot import bot
from aiogram.dispatcher import FSMContext


async def departments(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Це меню', reply_markup=kb.menu_depart)


async def products(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Це меню', reply_markup=kb.menu_depart)


async def ivoices(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Це меню', reply_markup=kb.menu_depart)


async def users(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Це меню', reply_markup=kb.menu_depart)


def register_handlers_menu_departments(dp: Dispatcher):
    dp.register_callback_query_handler(departments, cb.admin_menu_callback.filter(value=['Departments']), state='*')
    dp.register_callback_query_handler(products, cb.admin_menu_callback.filter(value=['Products']), state='*')
    dp.register_callback_query_handler(ivoices, cb.admin_menu_callback.filter(value=['Invoices']), state='*')
    dp.register_callback_query_handler(users, cb.admin_menu_callback.filter(value=['Users']), state='*')
