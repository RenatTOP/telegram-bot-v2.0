# def add_to_cart(query):
#     data = json.loads(query.data)
#     prod_id = data.get('pid')
#     user_id = query.message.chat.id
#     if prod_id is not None:
#         db.add_product_to_cart(user_id, prod_id)
#         return prod_id


# @bot.callback_query_handler(func=order_pressed)
# def add_order_callback(query):
#     try:
#         message_id = query.message.message_id
#         prod_id = add_to_cart(query)
#         offset = json.loads(query.data).get('offset')
#         text = 'Ваш кошик: \n' + db.get_products_from_cart(query.message.chat.id)
#         bot.edit_message_text(  message_id=message_id, text=text, chat_id=query.message.chat.id,
#                                 reply_markup=make_order_keyboard(3, offset), parse_mode='Markdown')
#         label, amount, about, url = db.get_product_by_id(prod_id)
#         bot.answer_callback_query(
#             callback_query_id=query.id, text='Ви додали товар {} до кошика'.format(label))
#     except:
#         pass


# @bot.callback_query_handler(func=clear_pressed)
# def clear_callback(query):
#     try:
#         message_id = query.message.message_id
#         chat_id = query.message.chat.id
#         offset = json.loads(query.data).get('offset')
#         db.clear_cart(chat_id)
#         text = 'Ваш кошик: \n' + db.get_products_from_cart(chat_id)
#         bot.edit_message_text(  message_id=message_id, text=text, chat_id=chat_id,
#                                 parse_mode='Markdown', reply_markup=make_order_keyboard(3, offset)
#         )
#         bot.answer_callback_query(
#             callback_query_id=query.id, text='Ви видалили кошик'
#         )
#     except:
#         bot.answer_callback_query(
#             callback_query_id=query.id, text='Ваш кошик порожній'
#         )
#         return
# @bot.pre_checkout_query_handler(func=lambda query: True)
# def check_out(pcq):
#     bot.answer_pre_checkout_query(
#         pre_checkout_query_id=pcq.id, ok=True, error_message='Сталася помилка')


import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
import aiogram.utils.markdown as fmt
from aiogram.dispatcher.filters import Text, RegexpCommandsFilter
from random import randint
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.utils.callback_data import CallbackData
from aiogram.types import BotCommand
from app.settings import BOT_TOKEN
import app.middlewares.keyboards as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage


loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
logging.basicConfig(level=logging.INFO)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Початок роботи"),
        BotCommand(command="/about", description="Хто створив бота"),
        BotCommand(command="/description", description="Про що бот"),
    ]
    await bot.set_my_commands(commands)


@dp.message_handler(Text(equals="С пюрешкой"))
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.answer(
        f"{fmt.hide_link('https://telegram.org/blog/video-calls/ru')}Кто бы мог подумать, что "
        "в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
        "возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
        "когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
        "коронавируса, команда Павла Дурова не растерялась и сделала качественные "
        "видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)"
    )


async def cmd_test2(message: types.Message):
    user_id = message.from_user.id
    url = "https://static9.depositphotos.com/1594308/1110/i/600/depositphotos_11107478-stock-photo-fantasy.jpg"
    await bot.send_photo(chat_id=user_id, photo=url, parse_mode="Markdown")


dp.register_message_handler(cmd_test2, commands="test2")


@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await message.reply("Вы заблокированы")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard
    )


@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer()

    # Здесь хранятся пользовательские данные.


# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}

# fabnum - префикс, action - название аргумента, которым будем передавать значение
callback_numbers = CallbackData("fabnum", "action")


def get_keyboard_fab():
    buttons = [
        types.InlineKeyboardButton(
            text="-1", callback_data=callback_numbers.new(action="decr")
        ),
        types.InlineKeyboardButton(
            text="+1", callback_data=callback_numbers.new(action="incr")
        ),
        types.InlineKeyboardButton(
            text="Подтвердить", callback_data=callback_numbers.new(action="finish")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(MessageNotModified):
        await message.edit_text(
            f"Укажите число: {new_value}", reply_markup=get_keyboard_fab()
        )


@dp.message_handler(commands="numbers_fab")
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


@dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]))
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    user_value = user_data.get(call.from_user.id, 0)
    action = callback_data["action"]
    if action == "incr":
        user_data[call.from_user.id] = user_value + 1
        await update_num_text_fab(call.message, user_value + 1)
    elif action == "decr":
        user_data[call.from_user.id] = user_value - 1
        await update_num_text_fab(call.message, user_value - 1)
    await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()


if __name__ == "__main__":
    from app.handlers import user, usergeo, info, kinds, products, user_cart, order
    from app.handlers.departments import departments_handlers as dh
    from app.handlers.menus import menus_handlers as mh
    from app.handlers.products import add_product

    user.register_handlers_users(dp)
    usergeo.register_handlers_user_geo(dp)

    mh.register_handlers_admin_menu(dp)

    dh.register_handlers_department(dp)

    info.register_handlers_info(dp)
    user_cart.register_handlers_cart(dp)
    order.register_handlers_order(dp)
    add_product.register_handlers_CRUD_products(dp)
    kinds.register_handlers_CRUD_kinds(dp)
    set_commands(bot)

    import locale
    import gettext

    domain = "helloworld"
    current_locale = "nb_NO"
    print("Current locale: {}".format(current_locale))
    locale_path = "locale/"
    gnu_translations = gettext.translation(
        domain="helloworld", localedir=locale_path, languages=[current_locale]
    )
    gnu_translations.install()
    print(_("helloworld"))

    executor.start_polling(dp, skip_updates=True)
