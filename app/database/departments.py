from app.database.database import departments
from bson.objectid import ObjectId


async def add_department(
    name: str,
    region: str,
    city: str,
    address: str,
    phone: str,
    timetable: dict,
    admin: int,
):
    data = {
        "name": name,
        "region": region,
        "city": city,
        "address": address,
        "phone": phone,
        "timetable": timetable,
        "admin": admin,
    }
    return await departments.insert_one(data)


async def get_count_departs(sort):
    if sort == "none" or not sort:
        all_departments = await departments.count_documents({})
    else:
        region, city = sort.split("#", 1)
        all_departments = await departments.count_documents(
            {"region": region, "city": city}
        )
    return all_departments


async def edit_depart(_id: str, edit_field: str, edit_value):
    return await departments.update_one(
        {"_id": ObjectId(_id)}, {"$set": {edit_field: edit_value}}
    )


async def del_department(_id: str):
    return await departments.delete_one({"_id": ObjectId(_id)})


async def find_departments():
    departments_list = departments.find({}, {"_id", "name", "region", "city"}).sort(
        "region"
    )
    return departments_list


async def departments_list(page_size: int, pages: int, sort: str):
    if sort == "none" or not sort:
        all_departments = departments.find({}).limit(page_size).skip(pages).sort("name")
    else:
        region, city = sort.split("#", 1)
        all_departments = (
            departments.find(
                {"region": region, "city": city}, {"_id", "name", "region", "city"}
            )
            .limit(page_size)
            .skip(pages)
            .sort("name")
        )
    return all_departments


async def find_department(_id: str):
    return await departments.find_one({"_id": ObjectId(_id)})


async def find_department_by_location(region: str, city: str, address: str, name: str):
    admin = await departments.find_one(
        {"region": region, "city": city, "address": address, "name": name}, {"admin"}
    )
    return admin
