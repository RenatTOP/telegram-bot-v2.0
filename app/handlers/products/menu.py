from bot import bot
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.middlewares.checks import check_admin_or_user
from app.keyboards.inline import products_buttons as kb


async def menu_products(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    check = await check_admin_or_user(state)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    keyboard = kb.admin_menu_prod if check == "admin" else kb.user_menu_prod
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Це меню товарів",
        reply_markup=keyboard,
    )


def register_handlers_menu_products(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_products, cd.menu_callback.filter(value=["Products"]), state="*"
    )
    dp.register_callback_query_handler(
        menu_products, cd.button_back_callback.filter(value=["products"]), state="*"
    )