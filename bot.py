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
    from app.handlers import usergeo, info, kinds1
    from app.handlers.users.users_handler import register_handlers_users
    from app.handlers.departments.departments_handlers import register_handlers_department
    from app.handlers.menus.menus_handlers import register_handlers_menus
    from app.handlers.products.products_handler import register_handlers_products
    from app.handlers.kinds.kinds_handler import register_handlers_kinds

    register_handlers_users(dp)
    usergeo.register_handlers_user_geo(dp)

    register_handlers_menus(dp)

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
