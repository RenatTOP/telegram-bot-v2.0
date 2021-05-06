import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import DATABASE
from bot import loop


client = AsyncIOMotorClient(DATABASE, io_loop=loop)

db = client.bot

users = db.users
kinds = db.kinds
products = db.products
departments = db.departments
applications = db.applications
