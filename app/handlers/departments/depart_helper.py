async def string_week(timetable: dict) -> str:
    week = ""
    for day in timetable.keys():
        week += f'\t\t<b>{day}</b>: {timetable[f"{day}"]}\n'
    return week


async def string_confirm(depart_data: dict, week: str) -> str:
    text = (
        f'Ви додаєте заклад <b>{depart_data["name"]}</b>\n'
        f'за адресою: <b>{depart_data["region"]}</b>,'
        f'<b>{depart_data["city"]}</b>,'
        f'<b>{depart_data["address"]}</b> \n'
        f'Телефон: <b>{depart_data["phone"]}</b>\n'
        f"Розклад:\n"
        f"{week}"
    )
    return text