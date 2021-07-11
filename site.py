if not "HEROKU" in list(os.environ.keys()):
    from aiohttp import web

    from bot import app


    web.run_app(app, port="8080", host="127.0.0.1")