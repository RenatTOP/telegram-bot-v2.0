from app.database.database import users


async def add_user(user_id: int, user_name: str):
    data = {
        "userId": user_id,
        "username": user_name,
        "cart": {},
        "isAdmin": False,
        "location": "",
    }
    await users.insert_one(data)


async def add_admin(user_id: int):
    await users.update_one({"userId": user_id}, {"$set": {"isAdmin": True}})


async def set_user(user_id: int, key: str, field: str):
    await users.update_one({"userId": user_id}, {"$set": {key: field}})


async def db_check_admin(user_id: int):
    return await users.find_one({'userId': user_id}, {'isAdmin': True})


