import os

from bot import HEROKU_APP_NAME


if not HEROKU_APP_NAME:
    from bot import web

    from bot import app


    web.run_app(app, port="8080", host="127.0.0.1")