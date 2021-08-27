from functools import wraps

from app.database import kinds as kind_db
from app.database.users import db_check_admin
from app.database.database import users, kinds, products, departments


async def check_already_user(user_id: int) -> bool:
    already_user = await users.find_one({'userId': user_id})
    return bool(already_user)


async def check_is_admin(user_id: int):
    return await db_check_admin(user_id)


async def find_product(label: str) -> bool:
    find_product = await products.find_one({'label': label})
    return bool(find_product)


async def check_empty_kind() -> bool:
    is_empty = await products.find({'kind': ''})
    return bool(is_empty)


async def check_kind(name: str) -> bool:
    find_kind = await kinds.find_one({'name': name})
    return bool(find_kind)


async def check_department(name: str) -> bool:
    department = await departments.find_one({'name': name})
    return bool(department)


async def check_cart(user_id: int) -> bool:
    cart = await users.find_one({"userId": user_id}, {"cart"})
    cart = cart["cart"]
    return bool(cart)


async def check_prod_in_cart(user_id: int, prod_id: str) -> str:
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


async def check_admin_or_user(state) -> str:
    check = await state.get_data()
    if "check" in check:
        return check['check']
    return "none"


async def check_kind_state(state) -> str:
    kind = await state.get_data()
    if "kind" in kind:
        return kind["kind"]
    return "none"


async def check_sort_state(state) -> str:
    sort = await state.get_data()
    if "sort" in sort:
        return sort['sort']
    return "none"


async def check_sort_invoice_state(state) -> str:
    sort = await state.get_data()
    if "invoice_sort" in sort:
        return sort['invoice_sort']
    return "none"
