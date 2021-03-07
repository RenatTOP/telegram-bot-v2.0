from app.database.database import departments
from bson.objectid import ObjectId


async def add_department(
    name: str, region: str, city: str, address: str, phone: str, timetable: dict
):
    data = {
        "name": name,
        "region": region,
        "city": city,
        "address": address,
        "phone": phone,
        "timetable": timetable,
    }
    return await departments.insert_one(data)


async def edit_depart(_id: str, edit_field: str, edit_value):
    return await departments.update_one(
        {"_id": ObjectId(_id)}, {"$set": {edit_field: edit_value}}
    )


async def del_department(_id: str):
    return await departments.delete_one({"_id": ObjectId(_id)})


async def departments_list():
    departments_list = departments.find({}, {"_id", "name", "city"}).sort("name").sort("city")
    return departments_list


async def find_department(_id: str):
    return await departments.find_one({"_id": ObjectId(_id)})
