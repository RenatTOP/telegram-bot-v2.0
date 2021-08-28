from app.database.database import applications


def add_application(
    user_id: int,
    firstname: str,
    lastname: str,
    order_prod: dict,
    indicated_time,
    order_time,
):
    data = {
        "userId": user_id,
        "firstname": firstname,
        "lasname": lastname,
        "cart": order_prod,
        "indicatedTime": indicated_time,
        "orderTime": order_time,
    }
    return applications.insert_one(data).inserted_id