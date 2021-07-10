from bson.objectid import ObjectId

from app.database.database import users
from app.database.database import products


async def add_user(user_id: int, user_name: str):
    data = {
        "userId": user_id,
        "username": user_name,
        "cart": {},
        "isAdmin": False,
        "location": "",
    }
    await users.insert_one(data)


async def add_admin(user_id: int):
    await users.update_one({"userId": user_id}, {"$set": {"isAdmin": True}})


async def set_user(user_id: int, key: str, field: str):
    await users.update_one({"userId": user_id}, {"$set": {key: field}})


async def check_location(user_id: int):
    user = await users.find_one({"userId": user_id}, {"location"})
    return bool(user["location"])


async def get_user_data(user_id: int):
    text = ""
    user = await users.find_one({"userId": user_id}, {"_id": 0})
    cart = user["cart"]
    data = ""
    all_suma = 0
    for key in sorted(cart.keys()):
        products_in_cart = await products.find_one({"_id": ObjectId(key)})
        _id = products_in_cart["_id"]
        amount = products_in_cart["amount"]
        label = products_in_cart["label"]
        number = cart[key]
        amount_grn = amount / 100.0
        suma = amount / 100 * number
        text += (
            f"\t\t\t\t<i><b>{label}</b>\t <b>{round(amount_grn, 2)}</b> ₴"
            f"\t x <b>{number}</b> шт</i> --- <b>{round(suma, 2)}</b> ₴\n"
        )
        all_suma += suma
    text += f"\nВсього: <b>{round(all_suma, 2)}</b> ₴"
    return user, cart, text


async def db_check_admin(user_id: int):
    return await users.find_one({"userId": user_id}, {"isAdmin": True})
