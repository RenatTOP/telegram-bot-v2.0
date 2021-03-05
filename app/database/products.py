from app.database.database import products
from bson.objectid import ObjectId


def add_product(label: str, amount: int, kind: str, about: str, picture: str):
    data = {
        "label": label,
        "amount": amount,
        "kind": kind,
        "about": about,
        "picture": picture,
    }
    return products.insert_one(data).inserted_id


def get_products(page_size: int, offset: int):
    all_products = list(products.find({}).limit(page_size).skip(offset).sort("label"))
    return all_products


def get_product_by_id(prod_id: str):
    return products.find_one({"_id": ObjectId(prod_id)})


def edit_product(label: str, edit_field: str, edit_value):
    if edit_value.isdigit():
        edit_value = int(edit_value)
    else:
        edit_value = str(edit_value)
    return products.update_one({"label": label}, {"$set": {edit_field: edit_value}})


def del_product(label: str):
    return products.delete_one({"label": label})
