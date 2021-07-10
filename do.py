
# def set_hook():
#     import asyncio
#     from aiogram import Bot
#     from app.settings import HEROKU_APP_NAME, WEBHOOK_URL, BOT_TOKEN
#     bot = Bot(token=BOT_TOKEN)

#     async def hook_set():
#         if not HEROKU_APP_NAME:
#             print('You have forgot to set HEROKU_APP_NAME')
#             quit()
#         await bot.set_webhook(WEBHOOK_URL)
#     asyncio.run(hook_set())
#     bot.close()


def start():
    from bot import main
    main()
