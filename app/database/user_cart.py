from app.database.database import users
from bson.objectid import ObjectId
from app.database.database import products


def add_product_to_cart(user_id: int, prod_id: str):
    return users.update_one({"userId": user_id}, {"$set": {"cart." + prod_id: +1}})


def del_product_in_cart(user_id: int, prod_id: str):
    return users.update_one({"userId": user_id}, {"$set": {"cart." + prod_id: -1}})


def get_products_from_cart(user_id: int):
    text = ""
    cart = users.find_one({"userId": user_id}, {"cart"})["cart"]
    for key in sorted(cart.keys()):
        products_in_cart = products.find_one({"_id": ObjectId(key)})
        amount = products_in_cart["amount"]
        label = products_in_cart["label"]
        number = cart[key]
        text += f"<i><b>{label}</b>\t {amount/100.0}\t x {number} шт\t <b>Усього:</b> {int(amount)*int(number)/100.0} грн.\n </i>"
    return text


def clear_cart(user_id: int):
    return users.update_one({"userId": user_id}, {"$set": {"cart": {}}})
