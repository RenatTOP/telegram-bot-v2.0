async def state_check(state):
    data = await state.get_data()
    check, kind = data["check"], data["kind"]
    await state.finish()
    await state.update_data(check=check, kind=kind)