import re
import uuid
from datetime import datetime
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.utils import callback_data
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import string
import random
from bot import dp
from bot import bot
from app.settings import qr_link
from app.database import users as user_db
from app.database import user_cart as cart_db
from app.states.checkout import IndicatedTime
from app.database import invoices as invoice_db
from app.database import departments as depart_db
from app.middlewares.state_check import state_check
from app.keyboards.inline import user_buttons as kb
from app.keyboards.inline.helper_buttons import back
from app.keyboards.inline import callback_datas as cd
from app.middlewares.checks import check_kind, check_cart
from app.middlewares.helpers import call_chat_and_message


async def choice_indicated_time(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    text = "Напишіть час до якого зробити замовлення, у форматі <b>ГГ:ХХ</b>"
    await IndicatedTime.first()
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=None
    )


async def get_indicated_time(message: Message, state: FSMContext):
    data = message.text
    data = data.strip()
    time = re.match(r"^(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", data) != None
    if not time:
        await message.answer("Введіть у форматі <b>ГГ:ХХ</b> Від 00:00 до 23:59 !")
        return
    await state_check(state)
    time_text = data.replace(":", "-")
    text = f"Бажаєте забрати замовлення о {time_text}?"
    kb_checkout = await kb.time_checkout(time_text)
    await message.answer(text=text, reply_markup=kb_checkout)


async def checkout(call: CallbackQuery):
    chat_id, message_id = await call_chat_and_message(call)
    user_id = call.from_user.id
    indicated_time = call.data
    indicated_time = indicated_time.replace("time_checkout_order:", "").replace(
        "-", ":"
    )
    await checkout_generator(user_id, indicated_time)
    checkout_kb = InlineKeyboardMarkup()
    checkout_kb.add(back("user_menu"))
    text = f"Ваше замовлення на {indicated_time} прийняте!"
    await bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=text, reply_markup=checkout_kb
    )


async def checkout_generator(user_id: int, indicated_time: str):
    order, data, cart_text = await user_db.get_user_data(user_id)
    depart_data = order["location"]
    depart_data = depart_data.split(", ")
    depart = depart_data[3]
    time = str(datetime.today())
    time = time.split(".", 1)[0]
    number = uuid.uuid4().int & (1 << 32) - 1
    qr = await qr_link(f"number={number}, time={time}")
    address = f"{depart_data[0]}, м.{depart_data[1]}, вул.{depart_data[2]}"
    text = (
        f"\t\t\t\t<b>ЗАМОВЛЕННЯ {number}</b>\n"
        f"{depart}\n{address}\nВИДАЧА:\n\t\t{cart_text}{hlink(' ', f'{qr}')}"
        f"\n\nНомер замовлення: <b>{number}</b>\nЧас замовлення: <b>{time}</b>\n"
        f"Час на який замовили: <b>{indicated_time}</b>"
    )
    depart_admin = await depart_db.find_department_by_location(
        depart_data[0], depart_data[1], depart_data[2], depart_data[3]
    )
    dp.loop.create_task(invoice_db.add_invoice(number, user_id, data, time, indicated_time))
    dp.loop.create_task(bot.send_message(depart_admin["admin"], text))
    dp.loop.create_task(cart_db.clear_cart(user_id))


def register_handlers_checkout(dp: Dispatcher):
    dp.register_callback_query_handler(checkout, cd.time_checkout_order.filter())
    dp.register_callback_query_handler(
        choice_indicated_time, cd.checkout_order.filter(data="confirm")
    )
    dp.register_message_handler(get_indicated_time, state=IndicatedTime.indicated_time)
