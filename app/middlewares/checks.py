from functools import wraps
import app.database.kinds as kind_db
from app.database.users import db_check_admin
from app.database.database import users, kinds, products, departments


async def check_already_user(user_id: int):
    already_user = await users.find_one({'userId': user_id})
    return bool(already_user)


async def check_is_admin(user_id: int):
    return await db_check_admin(user_id)


async def find_product(label: str):
    find_product = await products.find_one({'label': label})
    return bool(find_product)


async def check_empty_kind():
    is_empty = await products.find({'kind': ''})
    return bool(is_empty)


async def check_kind(name: str):
    find_kind = await kinds.find_one({'name': name})
    return bool(find_kind)


async def check_department(name: str):
    department = await departments.find_one({'name': name})
    return bool(department)


def check_admin(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        user_id = args[0].from_user.id
        admin = await db_check_admin(user_id)
        if admin['isAdmin']:
            await func(*args, **kwargs)
        else:
            if 'message_id' in args[0]:
                await args[0].answer("Ви не адмін!!!")
            else:
                await args[0].message.answer("Ви не адмін!!!")
            return
    return wrap


def check_admin_or_user(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        user_id = args[0].from_user.id
        admin = await db_check_admin(user_id)
        if admin['isAdmin']:
            await func(*args, **kwargs, keyboard='admin')
        else:
            await func(*args, **kwargs, keyboard='user')
    return wrap