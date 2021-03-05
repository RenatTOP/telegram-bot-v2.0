from app.database.database import users


def add_user(user_id: int, user_name: str):
    data = {
        "userId": user_id,
        "username": user_name,
        "cart": {},
        "isAdmin": False,
        "location": {"latitude": 0, "longitude": 0},
    }
    return users.insert_one(data).inserted_id


def add_admin(user_id: int):
    return users.update_one({"userId": user_id}, {"$set": {"isAdmin": True}})
