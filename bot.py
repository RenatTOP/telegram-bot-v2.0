import os
import logging
import asyncio
from aiohttp import web
from random import randint
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.settings import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=False)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
logging.basicConfig(level=logging.INFO)



async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
    

async def on_startup(app: web.Application) -> web.Response:
    Bot.set_current(bot)
    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(WEBHOOK_URL)
    return web.Response(status=200)


async def on_shutdown(request: web.Request) -> web.Response:
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.close_bot()
    return web.Response(status=200)


async def execute(request: web.Request) -> web.Response:
    request_body_dict = await request.json()
    update = types.Update(**(request_body_dict))
    await dp.process_updates([update])
    return web.Response(status=200)


async def main(dp):
    from app.handlers import info, kinds1
    from app.handlers.users import register_handlers_users
    from app.handlers.menus import register_handlers_menus
    from app.handlers.kinds import register_handlers_kinds
    from app.handlers.products import register_handlers_products
    from app.handlers.departments import register_handlers_department

    register_handlers_users(dp)
    register_handlers_menus(dp)
    register_handlers_department(dp)
    register_handlers_kinds(dp)
    info.register_handlers_info(dp)
    register_handlers_products(dp)
    kinds1.register_handlers_CRUD_kinds(dp)


    # import locale
    # import gettext

    # domain = "helloworld"
    # current_locale = "uk_UA"
    # print("Current locale: {}".format(current_locale))
    # locale_path = "locale/"
    # gnu_translations = gettext.translation(
    #     domain="helloworld", localedir=locale_path, languages=[current_locale]
    # )
    # gnu_translations.install()
    # print(_("helloworld")) #pylint:disable=undefined-variable


app = web.Application()
app.router.add_get("/", handle)
app.router.add_post(f"/disable_bot/{BOT_TOKEN}", on_shutdown)


if __name__ == "__main__":
    from app.handlers import info, kinds1
    from app.handlers.users import register_handlers_users
    from app.handlers.menus import register_handlers_menus
    from app.handlers.kinds import register_handlers_kinds
    from app.handlers.products import register_handlers_products
    from app.handlers.departments import register_handlers_department

    register_handlers_users(dp)
    register_handlers_menus(dp)
    register_handlers_department(dp)
    register_handlers_kinds(dp)
    info.register_handlers_info(dp)
    register_handlers_products(dp)
    kinds1.register_handlers_CRUD_kinds(dp)
    

    if "HEROKU" in list(os.environ.keys()):
        app.on_startup.append(on_startup)
        app.router.add_post(f"/webhook/{BOT_TOKEN}", execute)
        web.run_app(app, port=WEBAPP_PORT, host=WEBAPP_HOST)
    else:
        executor.start_polling(dp, skip_updates=True)