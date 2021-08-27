import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.settings import DATABASE


loop = asyncio.get_event_loop()
client = AsyncIOMotorClient(DATABASE, io_loop=loop)

db = client.bot

users = db.users
kinds = db.kinds
products = db.products
departments = db.departments
invoices = db.invoices

