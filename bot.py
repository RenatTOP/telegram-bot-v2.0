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
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from random import randint
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.types import BotCommand
from app.settings import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.database.database import users


loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
logging.basicConfig(level=logging.INFO)



if __name__ == "__main__":
    from app.handlers import usergeo, info, kinds1, order
    from app.handlers.users.users_handler import register_handlers_users
    from app.handlers.departments.departments_handlers import register_handlers_department
    from app.handlers.menus.menus_handlers import register_handlers_admin_menu
    from app.handlers.products.products_handler import register_handlers_products
    from app.handlers.kinds.kinds_handler import register_handlers_kinds

    register_handlers_users(dp)
    usergeo.register_handlers_user_geo(dp)

    register_handlers_admin_menu(dp)

    register_handlers_department(dp)
    register_handlers_kinds(dp)
    info.register_handlers_info(dp)
    order.register_handlers_order(dp)
    register_handlers_products(dp)
    kinds1.register_handlers_CRUD_kinds(dp)

    import locale
    import gettext

    domain = "helloworld"
    current_locale = "uk_UA"
    print("Current locale: {}".format(current_locale))
    locale_path = "locale/"
    gnu_translations = gettext.translation(
        domain="helloworld", localedir=locale_path, languages=[current_locale]
    )
    gnu_translations.install()
    print(_("helloworld")) # pylint:disable=undefined-variable

    executor.start_polling(dp, skip_updates=True)
