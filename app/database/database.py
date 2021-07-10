import os
from motor.motor_asyncio import AsyncIOMotorClient

from bot import loop
from app.settings import DATABASE, DATABASE_PROD


client = AsyncIOMotorClient(DATABASE_PROD, io_loop=loop)

db = client.bot

users = db.users
kinds = db.kinds
products = db.products
departments = db.departments
applications = db.applications
invoices = db.invoices

