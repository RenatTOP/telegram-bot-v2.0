from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import bot
from app.middlewares import helpers
from app.middlewares.checks import check_admin
from app.keyboards.inline import menu_buttons as kb
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message


@check_admin
async def admin_menu(message: Message, state: FSMContext):
    await state.update_data(check="admin", kind="none")
    await message.answer(text="Хай", reply_markup=kb.admin_menu)


@check_admin
async def admin_menu_call(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Хай",
        reply_markup=kb.admin_menu,
    )


def register_handlers_admin_menu(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands=["admin_menu"])
    dp.register_callback_query_handler(
        admin_menu_call, cd.button_back_callback.filter(value="admin_menu")
    )
