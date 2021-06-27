from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import bot
import app.middlewares.helpers
from app.middlewares.checks import check_admin
from app.keyboards.inline import menu_buttons as kb
from app.keyboards.inline import callback_datas as cd
from app.middlewares.helpers import call_chat_and_message


async def user_menu(message: Message, state: FSMContext):
    await state.update_data(check="user", kind="none")
    await message.answer(text="Хай", reply_markup=kb.user_menu)


async def user_menu_call(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Хай",
        reply_markup=kb.user_menu,
    )


def register_handlers_user_menu(dp: Dispatcher):
    dp.register_message_handler(user_menu, commands=["menu", "user_menu"])
    dp.register_callback_query_handler(
        user_menu_call, cd.button_back_callback.filter(value="user_menu")
    )