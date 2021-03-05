from aiogram import Dispatcher
from aiogram.types import Message
import app.database.kinds as kind_db
import app.database.products as prod_db
import app.middlewares.checks as checks
from app.middlewares.checks import check_is_admin
from aiogram.dispatcher.filters import RegexpCommandsFilter


async def all_products(message: Message):
    products = prod_db.get_products(5,0)
    text = ''
    for product in products:
        text += f"{product['label']} \n"
    await message.answer(text)

async def add_product(message: Message):
    user_id = message.from_user.id
    try:
        if (check_is_admin(user_id)):
            new_prod = message.text
            new_prod = new_prod.split(' ', 1)[1]
            label, amount, kind, about, picture = new_prod.split("|")
            label = label.strip()
            amount = int(amount)
            kind = kind.strip()
            about = about.strip()
            picture = picture.strip()
            is_kind = checks.check_kind(kind)
            if (is_kind):
                prod_db.add_product(label, amount, kind, about, picture)
                text = f'Товар \'{label}\' додано у магазин'
                await message.answer(text)
            else:
                await message.answer('Немає такого типу товару, виправте помилку або створіть новий тип')
        else:
            text = 'Ви не можете додавати товари'
            await message.answer(text)
    except:
        await message.answer(   'Введіть команду у форматі \n\''
                                '/addproduct Назва товару | Ціна  у копійках |'
                                'Тип товару | Опис товару | Лінк на зображення\'')

async def edit_product(message: Message):
    user_id = message.from_user.id
    edit_prod = message.text
    try:
        edit_prod = edit_prod.split(' ', 1)[1]
        label, edit_field, edit_value = edit_prod.split('|')
        label = label.strip()
        edit_field = edit_field.strip()
        edit_value = edit_value.strip()
        check_product = checks.find_product(label)
        if (check_is_admin(user_id) and check_product):
            prod_db.edit_product(label, edit_field, edit_value)
            await message.answer(f'Товар \'{label}\' був змінений')
        elif (check_product == False):
            await message.answer('Такого товару нема')
        else:
            text = 'Ви не можете видаляти товари'
            await message.answer(text)
    except:
        await message.answer(   'Введіть команду у форматі \n\''
                                '/editproduct Назва товару'
                                '| Поле редагування (label, amount, about, picture)'
                                '| Нове значення\'')


async def del_product(message: Message):
    user_id = message.from_user.id
    label = message.text
    try:
        label = label.split(' ', 1)[1]
        label = label.strip()
        check_product = checks.find_product(label)
        if (check_is_admin(user_id) and check_product):
            prod_db.del_product(label)
            await message.answer(f'Товар \'{label}\' було видалено')
        elif (check_product == False):
            await message.answer('Такого товару нема')
        else:
            text = 'Ви не можете видаляти товари'
            await message.answer(text)
    except:
        await message.answer('Введіть команду у форматі\n/delproduct Назва товару')


def register_handlers_CRUD_products(dp: Dispatcher):
    dp.register_message_handler(all_products, commands=['allproducts'])
    dp.register_message_handler(add_product, RegexpCommandsFilter(regexp_commands=['addproduct .', 'addproduct']))
    dp.register_message_handler(del_product, RegexpCommandsFilter(regexp_commands=['delproduct .', 'delproduct']))
    dp.register_message_handler(edit_product, RegexpCommandsFilter(regexp_commands=['editproduct .', 'editproduct']))