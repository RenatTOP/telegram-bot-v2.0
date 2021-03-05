from app.database.database import departments
from bson.objectid import ObjectId


def add_department(
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
    return departments.insert_one(data).inserted_id


def edit_depart(_id: str, edit_field: str, edit_value):
    return departments.update_one({"_id": ObjectId(_id)}, {"$set": {edit_field: edit_value}})


def del_department(_id: str):
    return departments.delete_one({"_id": ObjectId(_id)})


def departments_list():
    departments_list = list(
        departments.find({}, {"_id", "name", "city"}).sort("name").sort("city")
    )
    return departments_list


def find_department(_id: str):
    return departments.find_one({"_id": ObjectId(_id)})
