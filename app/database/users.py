from app.database.database import users
from app.database.database import products
from bson.objectid import ObjectId


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
    user = await users.find_one({'userId': user_id}, {"location"})
    return bool(user["location"])


async def get_user_data(user_id: int):
    text = ""
    user = await users.find_one({"userId": user_id}, {"_id": 0})
    cart = user["cart"]
    data = ""
    suma = 0
    for key in sorted(cart.keys()):
        products_in_cart = await products.find_one({"_id": ObjectId(key)})
        _id = products_in_cart["_id"]
        amount = products_in_cart["amount"]
        label = products_in_cart["label"]
        number = cart[key]
        text += f"\t\t\t\t<i><b>{label}</b>\t <b>{amount/100.0}</b> ₴\t x <b>{number}</b> шт</i> --- <b>{amount/100*number}</b> ₴\n"
        suma += amount / 100 * number
    text += f"\nВсього: <b>{suma}</b> ₴"
    return user, cart, text


async def db_check_admin(user_id: int):
    return await users.find_one({'userId': user_id}, {'isAdmin': True})


