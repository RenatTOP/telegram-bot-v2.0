from bson.objectid import ObjectId
from app.database.database import kinds
from app.database.database import products


async def add_kind(name: str):
    data = {"name": name}
    return await kinds.insert_one(data)


async def edit_kind(_id: str, name: str):
    await products.update_many({"kind": ""}, {"$set": {"kind": name}})
    await kinds.update_one({"_id": _id}, {"$set": {"name": name}})
    return


async def del_kind(_id: str):
    name = await kinds.find_one({"_id": ObjectId(_id)}, {"name"})
    await products.update_many({"kind": name['name']}, {"$set": {"kind": ""}})
    return await kinds.delete_one({"_id": ObjectId(_id)})


async def get_kind_by_id(_id: str):
    return await kinds.find_one({"_id": ObjectId(_id)})


async def find_kinds():
    return kinds.find({}, {"name"}).sort("name")