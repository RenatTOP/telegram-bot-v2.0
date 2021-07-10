from app.database.kinds import find_kinds


async def string_confirm(prod_data: dict) -> str:
    text = (
        f'Ви додаєте товар <b>{prod_data["label"]}</b>\n'
        f'Ціна: <b>{int(prod_data["amount"])/100.00} грн.</b>,\n'
        f'Вид: <b>{prod_data["kind"]}</b>,\n'
        f'Опис:<b>{prod_data["about"]}</b> \n'
        f'Картинка: <b>{prod_data["picture"]}</b>\n'
    )
    return text

async def string_kinds() -> str:
    kinds = await find_kinds()
    text = "\n"
    async for kind in kinds:
        text += f"\t\t<b>{kind['name']}</b>\n"
    return text