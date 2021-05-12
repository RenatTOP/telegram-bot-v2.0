import os
from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN') #? token bot
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME') #? app name Heroku
SECRET_ADMIN = os.getenv('SECRET_ADMIN') #? Admin secret key 
DATABASE = os.getenv('DATABASE') #? database link


WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com' #? Heroku host
WEBHOOK_PATH = f'/webhook/bot' #? Heroku path in host
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}' #? Heroku full URL


WEBAPP_HOST = '0.0.0.0' #? app host
WEBAPP_PORT = os.getenv('PORT') #? app port


QR_COLOR = "000000" #? color for QR code
QR_BG_COLOR = "FFFFFF" #? background color for QR code

#? generate qr code link
async def qr_link(data) -> str:
    link = (
        f"https://api.qrserver.com/v1/create-qr-code/?color={QR_COLOR}"
        f"&bgcolor={QR_BG_COLOR}&data={data}&qzone=1&margin=0&size=200x200&ecc=L"
    )
    return link