from dotenv import load_dotenv
load_dotenv()
import os
from telebot import TeleBot, types
import json
import re
import database as db
from flask import Flask, request, make_response

app = Flask(__name__)

bot = TeleBot(os.environ['TOKEN'])


@bot.message_handler(commands=['start'])
def initialization(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    text = 'Вітаю {}, ви зареєструвалися, можете перейти до покупок командою /order'.format(
        user_name)
    bot.send_message(user_id, text)
    db.add_user(user_id)

@bot.message_handler(commands=['isAdmin{}'.format(os.environ['SECRET_ADMIN'])])
def upd_admin(message):
    user_id = message.chat.id
    text = 'Вітаю, ви адмін'
    bot.send_message(user_id, text)
    db.add_admin(user_id)


@bot.message_handler(commands=['setdescription'])
def set_description(message):
    user_id = message.chat.id
    text = 'Бот для онлайн кафе'
    bot.send_message(user_id, text)


@bot.message_handler(commands=['setabout'])
def set_about(message):
    user_id = message.chat.id
    text = 'Робота Олійника Рената'
    bot.send_message(user_id, text)


@bot.message_handler(commands=['order'])
def order(message):
    user_id = message.chat.id
    cart_text = db.get_products_from_cart(user_id)
    text = "Ваш кошик: \n"
    if len(cart_text) != 0:
        text += cart_text
    markup = make_order_keyboard(3, 0)
    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')


# def make_cart_text(user_id):
#     text = ""
#     for id, number in db.get_products_from_cart(user_id):
#         prod_inf = db.get_product_by_id(id)
#         label, amount, about, url = prod_inf[0]
#         text += '_{}\t{}\t x {}_\n'.format(label, amount/100.0, number)
#     return text


def swipe_presed(query):
    data = json.loads(query.data)
    return data.get('offset') is not None \
        and data.get('pid') is None \
        and data.get('inf') is None \
        and data.get('abt') is None


@bot.callback_query_handler(func=swipe_presed)
def swipe_page(query):
    try:
        data = json.loads(query.data)
        user_id = query.message.chat.id
        message_id = query.message.message_id
        print(data)
        offset = data.get('offset')
        print(offset is not None)
        if offset is not None:
            if offset == 'first_page':
                bot.answer_callback_query(
                    callback_query_id=query.id, text='Це перша сторінка')
                return
            elif offset == 'last_page':
                bot.answer_callback_query(
                    callback_query_id=query.id, text='Це остання сторінка')
                return
            else:
                keyboard = make_order_keyboard(3, offset)
                cart_text = make_cart_text(user_id)
                text = "Ваш кошик: \n"
                if len(cart_text) != 0:
                    text += cart_text
                try:
                    bot.edit_message_text(
                        text=text, chat_id=user_id, parse_mode='Markdown', reply_markup=keyboard, message_id=message_id)
                except:
                    bot.delete_message(
                        chat_id=user_id, message_id=message_id)
                    bot.send_message(
                        text=text, chat_id=user_id, parse_mode='Markdown', reply_markup=keyboard)
    except:
        pass


def make_order_keyboard(page_size, offset):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for product in db.get_products(page_size, offset):
        prod_id, label, amount = product
        prod_data = json.dumps({'pid': prod_id, 'offset': offset})
        about_data = json.dumps({'abt': prod_id, 'offset': offset})
        prod_row = []
        prod_row.append(types.InlineKeyboardButton(
            text=label+' '+str(amount/100), callback_data=prod_data))
        prod_row.append(types.InlineKeyboardButton(
            text='Детальніше', callback_data=about_data))
        markup.add(*prod_row)

    markup.add(types.InlineKeyboardButton(  text='Видалити зміст кошика',
                                            callback_data=json.dumps({'inf': 'clear', 'offset': offset})))
    markup.add(types.InlineKeyboardButton(  text='Купити',
                                            callback_data=json.dumps({'inf': 'buy'})))
    if offset == 0:
        markup.add(types.InlineKeyboardButton(
            text='<==', callback_data=json.dumps({'offset': 'first_page'})))
    else:
        markup.add(types.InlineKeyboardButton(
            text='<==', callback_data=json.dumps({'offset': offset-3})))
    if len(db.get_products(page_size, offset + 3)) == 0:
        markup.add(types.InlineKeyboardButton(
            text='==>', callback_data=json.dumps({'offset': 'last_page'})))
    else:
        markup.add(types.InlineKeyboardButton(
            text='==>', callback_data=json.dumps({'offset': offset+3})))
    return markup


@bot.message_handler(regexp='addproduct '+r". \w+")
def add_new_product(message):
    new_prod = message.text
    user_id = message.chat.id
    product = re.split(r"\. |\.\.\. ", new_prod),
    label = product[0][1]
    amount = int(product[0][2])
    about = product[0][3]
    picture = product[0][4]
    db.add_product(label, amount, about, picture)
    text = "Товар {} додано у магазин".format(label)
    bot.send_message(user_id, text)

@bot.message_handler(regexp='delproduct'+r". \w+")
def del_product(message):
    prod = message.text
    user_id = message.chat.id
    product = re.split(r"\. |\.\.\. ", prod),
    product_id = product[0][1]
    db.del_product(product_id)
    text = "Товар {} видалено із магазину".format(product_id)
    bot.send_message(user_id, text)

def clear_pressed(query):
    data = json.loads(query.data)
    return data.get('inf') == 'clear'


def order_pressed(query):
    data = json.loads(query.data)
    return data.get('pid') is not None


def about_pressed(query):
    data = json.loads(query.data)
    return data.get('abt') is not None


def buy_pressed(query):
    data = json.loads(query.data)
    return data.get('inf') == 'buy'


@bot.callback_query_handler(func=about_pressed)
def send_info_about(query):
    try:
        data = json.loads(query.data)
        user_id = query.message.chat.id
        message_id = query.message.message_id
        prod_id = data.get('abt')
        offset = data.get('offset')
        label, amount, about, url = db.get_product_by_id(prod_id)[0]
        caption = "*{} - {}*\n_{}_".format(label, amount / 100.0, about)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Повернутися',
                                              callback_data=json.dumps({'offset': offset})))
        bot.delete_message(chat_id=user_id, message_id=message_id)
        bot.send_photo(chat_id=user_id, photo=url, caption=caption,
                       parse_mode='Markdown', reply_markup=markup)
    except:
        bot.answer_callback_query(query.id, text='Повідомлення застаріле')


def add_to_cart(query):
    data = json.loads(query.data)
    prod_id = data.get('pid')
    user_id = query.message.chat.id
    if prod_id is not None:
        db.add_product_to_cart(user_id, prod_id)
        return prod_id


@bot.callback_query_handler(func=order_pressed)
def add_order_callback(query):
    try:
        message_id = query.message.message_id
        prod_id = add_to_cart(query)
        offset = json.loads(query.data).get('offset')
        text = 'Ваш кошик: \n' + db.get_products_from_cart(query.message.chat.id)
        bot.edit_message_text(  message_id=message_id, text=text, chat_id=query.message.chat.id,
                                reply_markup=make_order_keyboard(3, offset), parse_mode='Markdown')
        label, amount, about, url = db.get_product_by_id(prod_id)
        bot.answer_callback_query(
            callback_query_id=query.id, text='Ви додали товар {} до кошика'.format(label))
    except:
        pass


@bot.callback_query_handler(func=clear_pressed)
def clear_callback(query):
    try:
        message_id = query.message.message_id
        chat_id = query.message.chat.id
        offset = json.loads(query.data).get('offset')
        db.clear_cart(chat_id)
        text = 'Ваш кошик: \n' + db.get_products_from_cart(chat_id)
        bot.edit_message_text(  message_id=message_id, text=text, chat_id=chat_id,
                                parse_mode='Markdown', reply_markup=make_order_keyboard(3, offset)
        )
        bot.answer_callback_query(
            callback_query_id=query.id, text='Ви видалили кошик'
        )
    except:
        bot.answer_callback_query(
            callback_query_id=query.id, text='Ваш кошик порожній'
        )
        return


@bot.callback_query_handler(func=buy_pressed)
def send_buy(query):
    order_list = []
    for prod_id, number in db.get_products_from_cart(query.message.chat.id):
        label, amount, about, url = db.get_product_by_id(prod_id)[0]
        for i in range(0, number):
            order_list.append(types.LabeledPrice(label=label, amount=amount))
    if len(order_list) == 0:
        bot.answer_callback_query(
            callback_query_id=query.id, text='У вас порожній кошик')
        return
    if len(order_list) > 10:
        bot.answer_callback_query(
            callback_query_id=query.id, text='У вас не має бути більше 10 товарів'
        )
        return
    bot.send_invoice(   chat_id=query.message.chat.id, title="Чек покупок",
                        description='Ваш чек',
                        provider_token=os.environ['PAYMENT_TOKEN'],
                        start_parameter='params',
                        currency='UAH',
                        prices=order_list,
                        invoice_payload='Good'
    )
    bot.delete_message( chat_id=query.message.chat.id,
                        message_id=query.message.message_id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def check_out(pcq):
    bot.answer_pre_checkout_query(
        pre_checkout_query_id=pcq.id, ok=True, error_message='Сталася помилка')


# @bot.message_handler(content_types=['successful_payment'])
# def payment_ok(message):
#     # если проект реализуется в реальной жизни, то в этом месте  оплаченый заказ добавляется
#     # в систему обработки заказов и выполняется оператором кассы
#     chat_id = message.chat.id
#     amount = message.successful_payment.total_amount / 100.0
#     currency = message.successful_payment.currency
#     bot.send_message(
#         chat_id=chat_id, text='Дякуємо за покупку. Ваша сума {} {}'.format(amount, currency))


# @app.route('/webhook', methods=['POST'])
# def hadle_messages():
#     bot.process_new_updates(
#         [types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return 'ok', 200


# @app.route('/setwh')
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://renattopbot.herokuapp.com/webhook')
#     return 'ok', 200


# @app.route('/')
# def index():
#     return "Renat APP"


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    bot.infinity_polling()