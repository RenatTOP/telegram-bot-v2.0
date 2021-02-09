from dotenv import load_dotenv
load_dotenv()
from bson.objectid import ObjectId
import os
import re


# class DBHandler:
#     def __init__(self, dialect, user, password, host, dbname, port='5432'):
#         try:
#             connection_string = dialect + "://" + user + ":" + password \
#                 + "@" + host + ":" + port + "/" + dbname
#             print(connection_string)
#             self.__conn = sa.create_engine(connection_string)
#             self.__meta = sa.MetaData()
#             # create internal tables here sql
#         except Exception as e:
#             print(e)

#     def create_internal_tables(self):
#         try:
#             sa.Table(config.tables_names['USERS_TABLE'], self.__meta,
#                      sa.Column('id', sa.Integer, primary_key=True),
#                      sa.Column('first_name', sa.String(30)))

#             sa.Table(config.tables_names['PRODUCTS_TABLE'], self.__meta,
#                      sa.Column('product_id', sa.String(35), primary_key=True),
#                      sa.Column('label', sa.String(50)),
#                      sa.Column('amount', sa.Integer),
#                      sa.Column('about', sa.String(1024)),
#                      sa.Column('picture_url', sa.String(1024)))
#             self.__meta.create_all(self.__conn)
#         except Exception as ex:
#             print(ex)

#     def add_user(self, chat_id, first_name):
#         try:
#             sa.Table('cart_renat_{}'.format(chat_id), self.__meta,
#                      sa.Column('product_id', sa.String(35), primary_key=True),
#                      sa.Column('number', sa.Integer))
#             self.__meta.create_all(self.__conn)
#             table = self.__meta.tables[config.tables_names['USERS_TABLE']]
#             self.__conn.execute(table.insert((chat_id, first_name)))
#         except Exception as ex:
#             print(ex)

#     def add_product(self, product_id, label, amount, about, picture):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
#         stmt = table.insert((product_id, label, amount, about, picture))
#         self.__conn.execute(stmt)

#     def del_product(self, product_id):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
#         stmt = table.delete().where(table.c.product_id == product_id)
#         self.__conn.execute(stmt)

#     def get_products(self, page_size, offset):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
#         res = self.__conn.execute(sa.select([table.c.product_id, table.c.label, table.c.amount]).limit(
#             page_size).offset(offset)).fetchall()
#         return res

#     def get_product_by_id(self, product_id):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
#         res = self.__conn.execute(
#             sa.select([table.c.label, table.c.amount, table.c.about, table.c.picture_url]).where(
#                 table.c.product_id == product_id)
#         ).fetchall()
#         return res

#     def add_products_to_cart(self, chat_id, product_id):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
#         stmt = sa.select(
#             [sa.text("1")]
#         ).where(table.c.product_id == product_id)

#         result = self.__conn.execute(stmt).fetchall()

#         if len(result) == 0:
#             self.__conn.execute(table.insert((product_id, 1)))
#         else:
#             stmt = table.update().where(table.c.product_id ==
#                                         product_id).values(number=table.c.number+1)
#             self.__conn.execute(stmt)

#     def get_products_from_cart(self, chat_id):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
#         return self.__conn.execute(sa.select([table])).fetchall()

#     def clear_the_cart(self, chat_id):
#         self.__meta.reflect(bind=self.__conn)
#         table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
#         return self.__conn.execute(table.delete())

from pymongo import MongoClient


client = MongoClient(os.environ['DATABASE'])

db = client.bot

users = db.users
products = db.products
applications = db.applications


def add_user(user_id):
    data = {
        "userId": user_id,
        "cart": {},
        "isAdmin": False
    }
    return users.insert_one(data).inserted_id

def add_admin(user_id):
    return users.update_one({"userId": user_id}, {"$set": {"isAdmin": True}})

def add_application(user_id, firstname, order_prod, indicated_time, order_time, username='', lastname=''):
    data = {
        "userId": user_id,
        "firstname": firstname,
        "lasname": lastname,
        "username": username,
        "cart": { order_prod },
        "indicatedTime": indicated_time,
        "orderTime": order_time
    }
    return applications.insert_one(data).inserted_id


def add_product(label, amount, about, picture):
    data = {
        "label": label,
        "amount": amount,
        "about": about,
        "picture": picture
    }
    return products.insert_one(data).inserted_id

def get_products(page_size, offset):
    return products.find({}).limit(page_size).skip(offset).sort("label")

def get_product_by_id(prod_id):
    return products.find_one({"_id": ObjectId(prod_id)})

def del_product(prod_id):
    products.delete_one({"_id": ObjectId(prod_id)})


def add_product_to_cart(user_id, prod_id):
    return users.update_one({ "userId": user_id }, { "$set": {"cart."+prod_id: +1}})

def del_product_in_cart(user_id, prod_id):
    return users.update_one({"userId": user_id}, { "$set": {"cart."+prod_id: -1}})

# def get_products_from_cart(user_id):
#     return users.find_one({"userId": user_id}, {"cart"})

def get_products_from_cart(user_id):
    text = ''
    get_cart = users.find_one({"userId": user_id}, {'cart'})
    # len_cart = len(get_cart)
    for i, number in db.get_products_from_cart(user_id):
        prod_and_amount_by_cart = get_cart['cart'][i]
        prod_and_amount_by_cart_str = re.findall(r'\w+', str(prod_and_amount_by_cart))
        prod_id = prod_and_amount_by_cart_str[0]
        amount = prod_and_amount_by_cart_str[1]
        get_label = products.find_one({'_id': ObjectId(prod_id)}, {'label'})
        label = get_label['label']
        text += '_{}\t{}\t x {}_\n'.format(label, amount/100.0, number)
    return text

def clear_cart(user_id):
    return users.update_one({"userId": user_id}, {"$set": {"cart": []}})
