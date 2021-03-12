import os
from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
SECRET_ADMIN = os.getenv('SECRET_ADMIN')
DATABASE = os.getenv('DATABASE')


WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/bot'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')
