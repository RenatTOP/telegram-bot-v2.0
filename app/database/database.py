import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import DATABASE


client = AsyncIOMotorClient(DATABASE)

db = client.bot

users = db.users
kinds = db.kinds
products = db.products
departments = db.departments
applications = db.applications