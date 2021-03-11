from bot import bot
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import products_buttons as kb


async def products(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Це меню продуктів",
        reply_markup=kb.menu_prod,
    )


def register_handlers_menu_products(dp: Dispatcher):
    dp.register_callback_query_handler(
        products, cd.admin_menu_callback.filter(value=["Products"]), state="*"
    )
    dp.register_callback_query_handler(
        products, cd.button_back_callback.filter(value=["products"]), state="*"
    )