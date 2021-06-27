from aiogram import Dispatcher
from aiogram.types import Message

from app.database import kinds as kind_db
from app.middlewares import checks as checks
from app.middlewares.checks import check_is_admin
from aiogram.dispatcher.filters import RegexpCommandsFilter


async def add_prod_kind(message: Message):
    user_id = message.from_user.id
    kind = message.text
    try:
        kind = kind.split(" ", 1)[1]
        kind = kind.strip()
        check_kind = checks.check_kind(kind)
        if check_is_admin(user_id) and not check_kind:
            kind_db.add_kind(kind)
            await message.answer(f"Тип {kind} було додано")
        elif check_kind:
            await message.answer("Такий тип товару вже існує!")
        else:
            await message.answer("Ви не можете додавати види товару")
    except:
        await message.answer("Введіть команду у форматі\n/addkind Назва типу")


async def paste_kind_in_empty_products(message: Message):
    user_id = message.from_user.id
    kind = message.text
    try:
        kind = kind.split(" ", 1)[1]
        kind = kind.strip()
        check_kind = checks.check_kind(kind)
        if check_is_admin(user_id) and check_kind and checks.check_empty_kind:
            # kind_db.paste_kind(kind)
            await message.answer(f"Тип {kind} було додано до товарів без типу")
        elif not check_kind:
            await message.answer("Такий тип товару не існує!")
        elif not checks.check_empty_kind:
            await message.answer("Товарів без типу немає")
        else:
            await message.answer("Ви не можете додавати види товару")
    except:
        await message.answer("Введіть команду у форматі\n/paste_kind Назва типу")


async def del_prod_kind(message: Message):
    user_id = message.from_user.id
    kind = message.text
    try:
        kind = kind.split(" ", 1)[1]
        kind = kind.strip()
        check_kind = checks.check_kind(kind)
        if check_is_admin(user_id) and check_kind:
            kind_db.del_kind(kind)
            await message.answer(
                f"Тип {kind} було видалено, але майте на увазі,"
                " що товару цього типу залишилися без типу"
            )
        elif not check_kind:
            await message.answer("Такий тип товару не існує!")
        else:
            await message.answer("Ви не можете додавати види товару")
    except:
        await message.answer("Введіть команду у форматі\n/delkind Назва типу")


def register_handlers_CRUD_kinds(dp: Dispatcher):
    dp.register_message_handler(
        add_prod_kind, RegexpCommandsFilter(regexp_commands=["addkind .", "addkind"])
    )
    dp.register_message_handler(
        del_prod_kind, RegexpCommandsFilter(regexp_commands=["delkind .", "delkind"])
    )
    dp.register_message_handler(
        paste_kind_in_empty_products,
        RegexpCommandsFilter(regexp_commands=["paste_kind .", "paste_kind"]),
    )
