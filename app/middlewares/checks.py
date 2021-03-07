import app.database.kinds as kind_db
from app.database.database import users
from app.database.database import kinds
from app.database.database import products
from app.database.database import departments


def check_already_user(user_id: int):
    already_user = users.find_one({'userId': user_id})
    return bool(already_user)

async def check_is_admin(user_id: int):
    is_admin = await users.find_one({'userId': user_id}, {'isAdmin': True})
    return bool(is_admin['isAdmin'])

def find_product(label: str):
    find_product = products.find_one({'label': label})
    return bool(find_product)

def check_empty_kind():
    is_empty = list(products.find({'kind': ''}))
    return bool(is_empty)

def check_kind(name: str):
    find_kind = kinds.find_one({'name': name})
    return bool(find_kind)

def check_department(name: str):
    department = departments.find_one({'name': name})
    return bool(department)