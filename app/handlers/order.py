from aiogram import Dispatcher, types
import app.middlewares.keyboards as kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Order(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()


async def order_start(message: types.Message):
    text = 'Меню'
    await message.answer(text, reply_markup=kb.order_buttons)

async def tovars(call: types.CallbackQuery):
    await call.answer(cache_time=60,text="⏳")
    await call.message.edit_text('Це товар 1', reply_markup=kb.buy_tovar1)


def register_handlers_order(dp):
    dp.register_message_handler(order_start, commands=['order'])
    dp.register_callback_query_handler(tovars, text="Tovar1")
    















# @bot.message_handler(commands=['order'])
# def order(message):
#     user_id = message.chat.id
#     cart_text = db.get_products_from_cart(user_id)
#     text = "Ваш кошик: \n"
#     if len(cart_text) != 0:
#         text += cart_text
#     markup = make_order_keyboard(3, 0)
#     bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')
# def swipe_presed(query):
#     data = json.loads(query.data)
#     return data.get('offset') is not None \
#         and data.get('pid') is None \
#         and data.get('inf') is None \
#         and data.get('abt') is None2


# @bot.callback_query_handler(func=swipe_presed)
# def swipe_page(query):
#     try:
#         data = json.loads(query.data)
#         user_id = query.message.chat.id
#         message_id = query.message.message_id
#         print(data)
#         offset = data.get('offset')
#         print(offset is not None)
#         if offset is not None:
#             if offset == 'first_page':
#                 bot.answer_callback_query(
#                     callback_query_id=query.id, text='Це перша сторінка')
#                 return
#             elif offset == 'last_page':
#                 bot.answer_callback_query(
#                     callback_query_id=query.id, text='Це остання сторінка')
#                 return
#             else:
#                 keyboard = make_order_keyboard(3, offset)
#                 cart_text = db.get_products_from_cart(user_id)
#                 text = "Ваш кошик: \n"
#                 if len(cart_text) != 0:
#                     text += cart_text
#                 try:
#                     bot.edit_message_text(
#                         text=text, chat_id=user_id, parse_mode='Markdown', reply_markup=keyboard, message_id=message_id)
#                 except:
#                     bot.delete_message(
#                         chat_id=user_id, message_id=message_id)
#                     bot.send_message(
#                         text=text, chat_id=user_id, parse_mode='Markdown', reply_markup=keyboard)
#     except:
#         pass
# def make_order_keyboard(page_size, offset):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     for product in db.get_products(page_size, offset):
#         prod_id, label, amount = product
#         prod_data = json.dumps({'pid': prod_id, 'offset': offset})
#         about_data = json.dumps({'abt': prod_id, 'offset': offset})
#         prod_row = []
#         prod_row.append(types.InlineKeyboardButton(
#             text=label+' '+str(amount/100), callback_data=prod_data))
#         prod_row.append(types.InlineKeyboardButton(
#             text='Детальніше', callback_data=about_data))
#         markup.add(*prod_row)    markup.add(types.InlineKeyboardButton(  text='Видалити зміст кошика',
#                                             callback_data=json.dumps({'inf': 'clear', 'offset': offset})))
#     markup.add(types.InlineKeyboardButton(  text='Купити',
#                                             callback_data=json.dumps({'inf': 'buy'})))
#     if offset == 0:
#         markup.add(types.InlineKeyboardButton(
#             text='<==', callback_data=json.dumps({'offset': 'first_page'})))
#     else:
#         markup.add(types.InlineKeyboardButton(
#             text='<==', callback_data=json.dumps({'offset': offset-3})))
#     if len(db.get_products(page_size, offset + 3)) == 0:
#         markup.add(types.InlineKeyboardButton(
#             text='==>', callback_data=json.dumps({'offset': 'last_page'})))
#     else:
#         markup.add(types.InlineKeyboardButton(
#             text='==>', callback_data=json.dumps({'offset': offset+3})))
#     return markup


# def clear_pressed(query):
#     data = json.loads(query.data)
#     return data.get('inf') == 'clear'


# def order_pressed(query):
#     data = json.loads(query.data)
#     return data.get('pid') is not None


# def about_pressed(query):
#     data = json.loads(query.data)
#     return data.get('abt') is not None


# def buy_pressed(query):
#     data = json.loads(query.data)
#     return data.get('inf') == 'buy'


# @bot.callback_query_handler(func=about_pressed)
# def send_info_about(query):
#     try:
#         data = json.loads(query.data)
#         user_id = query.message.chat.id
#         message_id = query.message.message_id
#         prod_id = data.get('abt')
#         offset = data.get('offset')
#         label, amount, about, url = db.get_product_by_id(prod_id)[0]
#         caption = "*{} - {}*\n_{}_".format(label, amount / 100.0, about)
#         markup = types.InlineKeyboardMarkup()
#         markup.add(types.InlineKeyboardButton(text='Повернутися',
#                                               callback_data=json.dumps({'offset': offset})))
#         bot.delete_message(chat_id=user_id, message_id=message_id)
#         bot.send_photo(chat_id=user_id, photo=url, caption=caption,
#                        parse_mode='Markdown', reply_markup=markup)
#     except:
#         bot.answer_callback_query(query.id, text='Повідомлення застаріле')
