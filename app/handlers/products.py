from aiogram import types
import re
import app.database.database as db
from app.middlewares.checks import check_is_admin

async def add_product(message: types.Message):
    try:
        user_id = message.from_user.id
        if (check_is_admin(user_id)):
            new_prod = message.text
            product = re.split(r"\|", new_prod),
            label = product[0][1]
            label = label.strip()
            amount = int(product[0][2])
            about = product[0][3]
            about = about.strip()
            picture = product[0][4]
            picture = picture.strip()
            db.add_product(label, amount, about, picture)
            text = f"Товар \"{label}\" додано у магазин"
            await message.answer(text)
        else:
            text = 'Ви не можете додавати товари'
            await message.answer(text)
    except:
        await message.answer('Введіть команду вірно!')