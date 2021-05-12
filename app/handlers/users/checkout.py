import aiogram.utils.callback_data
from bot import bot
from aiogram import Dispatcher
import aiogram.dispatcher.filters
from aiogram.utils.markdown import hlink
from app.database import user_cart as cart_db
from app.database import checkouts as checkout_db
from app.database import users as user_db
from app.keyboards.inline.helper_buttons import back
from app.middlewares.checks import check_kind, check_cart
from aiogram.types import Message, CallbackQuery
from app.keyboards.inline import callback_datas as cd
from app.keyboards.inline import user_buttons as kb
from app.middlewares.helpers import call_chat_and_message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.settings import qr_link
from datetime import datetime

async def checkout(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    user_id = call.from_user.id
    order = await checkout_generator(user_id)
    text = "Ваше замовлення прийняте!"
    await bot.send_message(735981984, "order")
    checkout_kb = InlineKeyboardMarkup()
    checkout_kb.add(back("user_menu"))
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=checkout_kb
    )


async def create_order(data: dict):
    order = ""


async def qr(message: Message):
    text = await checkout_generator(message.from_user.id)
    await message.answer(text)


async def checkout_generator(user_id: int):
    order, data, cart_text = await user_db.get_user_data(user_id)
    depart_data = order["location"]
    depart_data = depart_data.split(", ")
    depart = depart_data[3]
    time = str(datetime.today())
    time = time.split(".", 1)[0]
    number = await checkout_db.get_count() + 1
    await checkout_db.add_checkout(number, user_id, data, time)
    qr = await qr_link(f"number={number}, time={time}")
    address = f"{depart_data[0]}, м.{depart_data[1]}, вул.{depart_data[2]}"
    text = f"{depart}\n{address}\nВИДАЧА:\n\t\t{cart_text}{hlink(' ', f'{qr}')}"
    return text


def register_handlers_checkout(dp: Dispatcher):
    dp.register_message_handler(qr, commands=["test"])
