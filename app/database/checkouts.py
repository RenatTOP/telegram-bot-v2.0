from app.database.database import checkouts


async def add_checkout(number: int, user: int, order: dict, time: str):
    data = {
        "number": number,
        "user": user,
        "order": order,
        "time": time,
        "confirm": False
    }
    return await checkouts.insert_one(data)


async def get_count():
    return await checkouts.count_documents({})