from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_1 = InlineKeyboardButton("Первая кнопка!", callback_data="button1")
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

order_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(1)

tovar1 = InlineKeyboardButton(text="Tovar1", callback_data="Tovar1")
order_buttons.insert(tovar1)

buy_tovar1 = InlineKeyboardMarkup(1)
one = InlineKeyboardButton(text="Купити", callback_data="Купив1")
buy_tovar1.insert(one)
