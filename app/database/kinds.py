from app.database.database import kinds
from app.database.database import products


def add_kind(name: str):
    data = {"name": name}
    return kinds.insert_one(data).inserted_id


def paste_kind(name: str):
    return products.update_many({"kind": ""}, {"$set": {"kind": name}})


def del_kind(name: str):
    products.update_many({"kind": name}, {"$set": {"kind": ""}})
    kinds.delete_one({"name": name})
    return