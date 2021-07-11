from aiohttp import web

from bot import app


web.run_app(app, port="8080", host="127.0.0.1")