from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import bot
from app.keyboards.inline import callback_datas as cb
from app.keyboards.inline import invoices_buttons as kb
from app.keyboards.inline import helper_buttons as help_kb


async def invoices(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await state.update_data(sort="none")
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Це меню рахунків",
        reply_markup=kb.admin_menu_invoices,
    )


def register_handlers_menu_invoices(dp: Dispatcher):
    dp.register_callback_query_handler(
        invoices, cb.menu_callback.filter(value=["Departments"]), state="*"
    )
    dp.register_callback_query_handler(
        invoices, cb.button_back_callback.filter(value=["departments"]), state="*"
    )
