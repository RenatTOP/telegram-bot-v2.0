import os
import jinja2
import logging
import asyncio
import aiohttp_jinja2
from aiohttp import web
from random import randint
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import get_new_configured_app

from app.routes import routes
from app.settings import (
    BOT_TOKEN,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT,
    HEROKU_APP_NAME,
)


loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=False)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
logging.basicConfig(level=logging.INFO)


async def on_startup(app):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


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

    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    app.router.add_static("/static/", path="app/static/", name="static")
    aiohttp_jinja2.setup(
        app, enable_async=True, loader=jinja2.FileSystemLoader("app/templates")
    )
    app["static_root_url"] = "static"
    routes(app)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)