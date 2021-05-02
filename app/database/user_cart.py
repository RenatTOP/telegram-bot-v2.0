from app.database.database import users
from bson.objectid import ObjectId
from app.database.database import products


async def add_product_to_cart(user_id: int, prod_id: str) -> bool:
    try:
        number_prod = await users.find_one({"userId": user_id}, {f"cart.{prod_id}"})
        number_prod = number_prod["cart"][f"{prod_id}"]
        if number_prod < 5:
            number_prod += 1
            await users.update_one(
                {"userId": user_id}, {"$set": {f"cart.{prod_id}": number_prod}}
            )
            return True
        else:
            return False
    except:
        await users.update_one({"userId": user_id}, {"$set": {f"cart.{prod_id}": 1}})
        return True


async def del_product_from_cart(user_id: int, prod_id: str):
    number_prod_cart = await users.find_one({"userId": user_id}, {f"cart.{prod_id}"})
    number_prod = number_prod_cart["cart"][f"{prod_id}"]
    if number_prod == 1:
        await users.update_one({"userId": user_id}, {"$unset": {f"cart.{prod_id}": 1}})
    else:
        number_prod -= 1
        await users.update_one(
            {"userId": user_id}, {"$set": {f"cart.{prod_id}": number_prod}}
        )


async def get_products_from_cart(user_id: int) -> str:
    text = "Ваш кошик:\n"
    cart = await users.find_one({"userId": user_id}, {"cart"})
    cart = cart["cart"]
    suma = 0
    if cart:
        for key in sorted(cart.keys()):
            products_in_cart = await products.find_one({"_id": ObjectId(key)})
            _id = products_in_cart["_id"]
            amount = products_in_cart["amount"]
            label = products_in_cart["label"]
            number = cart[key]
            text += f"\t\t\t\t<i><b>{label}</b>\t <b>{amount/100.0}</b> ₴\t x <b>{number}</b> шт</i> --- <b>{amount/100*number}</b> ₴\n"
            suma += amount / 100 * number
        text += f"\nВсього: <b>{suma}</b> ₴"
    else:
        text += "\t\t\t\t*порожньо*"
    return text


async def clear_cart(user_id: int):
    await users.update_one({"userId": user_id}, {"$set": {"cart": {}}})
