from bson.objectid import ObjectId

from app.database.database import products
from app.keyboards.inline.department_buttons import edit_fields


async def add_product(label: str, amount: int, kind: str, about: str, picture: str):
    data = {
        "label": label,
        "amount": amount,
        "kind": kind,
        "about": about,
        "picture": picture,
    }
    return await products.insert_one(data)


async def get_count_products(kind):
    if kind == 'none' or not kind:
        all_products = await products.count_documents({})
    else:
        all_products = await products.count_documents({"kind": kind})
    return all_products


async def get_products(page_size: int, pages: int, kind: str):
    if kind == 'none' or not kind:
        all_products = products.find({}).sort("label").limit(page_size).skip(pages)
    else:
        all_products = products.find({"kind": kind}).sort("label").limit(page_size).skip(pages)
    return all_products


async def get_product_by_id(prod_id: str):
    return await products.find_one({"_id": ObjectId(prod_id)})


async def edit_product(_id: str, edit_field: str, edit_value):
    if edit_value.isdigit():
        edit_value = int(edit_value)
    else:
        edit_value = str(edit_value)
    return await products.update_one({"_id": ObjectId(_id)}, {"$set": {edit_field: edit_value}})


async def del_product(_id: str):
    return await products.delete_one({"_id": ObjectId(_id)})
