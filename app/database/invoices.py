from app.database.database import invoices


async def add_invoice(number: int, user: int, order: dict, time: str, indicated_time: str):
    data = {
        "number": number,
        "user": user,
        "order": order,
        "time": time,
        "indicated_time": indicated_time,
        "status": "opened"
    }
    return await invoices.insert_one(data)


async def get_invoices(page_size: int, pages: int, sort: str):
    if sort == 'none' or not sort:
        all_invoices = invoices.find({}).sort("time").limit(page_size).skip(pages)
    else:
        all_invoices = invoices.find({"status": sort}).sort("time").limit(page_size).skip(pages)
    return all_invoices


async def get_count_invoices(sort):
    if sort == 'none' or not sort:
        all_invoices = await invoices.count_documents({})
    else:
        all_invoices = await invoices.count_documents({"status": sort})
    return all_invoices