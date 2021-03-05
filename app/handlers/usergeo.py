from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.database.database import users
from dadata import Dadata


async def geo(message: Message):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    await message.answer(
        "Привіт! Натисни на кнопку та передай мені своє місцеположення",
        reply_markup=keyboard,
    )


async def location(message: Message):
    if message.location is not None:
        user_id = message.from_user.id
        latitude = message.location.latitude
        longitude = message.location.longitude
        users.update_one(
            {"userId": user_id},
            {"$set": {"location.latitude": latitude, "location.longitude": longitude}},
        )
        await message.answer("Координати прийняті")
    else:
        await message.answer("Спробуте ще раз")


async def send_geo(message: Message):
    reverse_geocode_result = (48.863939, 38.084605)
    await message.answer(reverse_geocode_result)


def register_handlers_user_geo(dp: Dispatcher):
    dp.register_message_handler(geo, commands=["mygeo"])
    dp.register_message_handler(location, content_types=["location"])
