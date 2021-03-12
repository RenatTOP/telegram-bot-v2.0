import app.database.kinds as kind_db
from app.database.database import users, kinds, products, departments


async def check_already_user(user_id: int):
    already_user = await users.find_one({'userId': user_id})
    return bool(already_user)

async def check_is_admin(user_id: int):
    is_admin = await users.find_one({'userId': user_id}, {'isAdmin': True})
    return bool(is_admin['isAdmin'])

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


def check_admin(function_to_decorate):
    async def is_admin(message):
        admin = await users.find_one({'userId': message.from_user.id}, {'isAdmin': True})
        if admin['isAdmin']:
            await function_to_decorate(message)
        else:
            message.answer("Ви не адмін!!!")
            return
    return is_admin