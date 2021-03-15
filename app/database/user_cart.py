from app.database.database import users
from bson.objectid import ObjectId
from app.database.database import products


async def add_product_to_cart(user_id: int, prod_id: str):
    number_prod = await users.find_one({"userId": user_id}, {f"cart.{prod_id}"})
    number_prod = number_prod["cart"][f"{prod_id}"]
    number_prod += 1
    await users.update_one({"userId": user_id}, {"$set": {f"cart.{prod_id}": number_prod}})


async def del_product_from_cart(user_id: int, prod_id: str):
    number_prod = await users.find_one({"userId": user_id}, {f"cart.{prod_id}"})
    number_prod = number_prod["cart"][f"{prod_id}"]
    number_prod -= 1
    await users.update_one({"userId": user_id}, {"$set": {f"cart.{prod_id}": number_prod}})


async def get_products_from_cart(user_id: int):
    text = "Ваш кошик:\n"
    cart = await users.find_one({"userId": user_id}, {"cart"})
    cart = cart["cart"]
    if cart:
        for key in sorted(cart.keys()):
            products_in_cart = await products.find_one({"_id": ObjectId(key)})
            amount = products_in_cart["amount"]
            label = products_in_cart["label"]
            number = cart[key]
            text += (f"\t\t\t\t<i><b>{label}</b>\t {amount/100.0} ₴\t x {number} шт</i>\n"
            )
    else:
        text += "\t\t\t\t*порожньо*"
    return text


async def clear_cart(user_id: int):
    await users.update_one({"userId": user_id}, {"$set": {"cart": {}}})["cart"]
