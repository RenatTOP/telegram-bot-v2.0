from functools import wraps

from app.database import kinds as kind_db
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


async def check_cart(user_id: int):
    cart = await users.find_one({"userId": user_id}, {"cart"})
    cart = cart["cart"]
    return bool(cart)


async def check_prod_in_cart(user_id: int, prod_id: str):
    cart = await users.find_one({"userId": user_id}, {"cart"})
    cart = cart["cart"]
    if cart[f"{prod_id}"] == 0:
        return "Кошик порожній"
    elif cart[f"{prod_id}"] == 5:
        return "У кошика забагато цього товару"


def check_admin(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        user_id = args[0].from_user.id
        admin = await db_check_admin(user_id)
        if admin['isAdmin']:
            await func(*args, **kwargs)
        else:
            text = "Ви не адмін!!!"
            if 'message_id' in args[0]:
                await args[0].answer(text)
            else:
                await args[0].message.answer(text)
            return
    return wrap


async def check_admin_or_user(state):
    check = await state.get_data()
    try:
        check = check['check']
    except:
        check = "user"
    return check


async def check_kind_state(state):
    kind = await state.get_data()
    try:
        kind = kind['kind']
    except:
        kind = "none"
    return kind


async def check_sort_state(state):
    sort = await state.get_data()
    try:
        sort = sort['sort']
    except:
        sort = "none"
    return sort


# def check_admin_or_user(func):
#     @wraps(func)
#     async def wrap(call_or_message, state):
#         check = await state.get_data()
#         print(check)
#         check = check['check']
#         if check == "admin":
#             await func(call_or_message, state, check='admin')
#         else:
#             await func(call_or_message, state, check='user')
#     return wrap