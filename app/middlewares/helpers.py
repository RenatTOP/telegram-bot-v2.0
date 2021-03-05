import asyncio


async def call_chat_and_message(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    ids = [chat_id, message_id]
    return ids
