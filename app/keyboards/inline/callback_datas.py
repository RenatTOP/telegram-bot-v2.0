from aiogram.utils.callback_data import CallbackData


menu_callback = CallbackData("admin_menu", "value")
button_back_callback = CallbackData("back", "value")
nav_list_callback = CallbackData("nav", "pages", "data")


choose_depart = CallbackData("choose", "value")

depart_button_sort = CallbackData("depart_sort", "sort")
depart_menu_callback = CallbackData("depart_menu", "value")
depart_confirm_callback = CallbackData("depart_confirm", "value")
depart_add_edit_callback = CallbackData("depart_add_edit", "field")
depart_nav_list_callback = CallbackData("nav_depart", "pages")
depart_info_callback = CallbackData("depart_info_edit", "_id")
depart_button_edit_callback = CallbackData("depart_edit", "_id")
depart_button_del_callback = CallbackData("depart_del", "_id")
depart_button_confirm_del_callback = CallbackData("depart_confirm_del", "_id")
depart_edit_edit_callback = CallbackData("depart_edit_edit", "field")


prod_button_sort = CallbackData("prod_sort", "kind")
kind_sort_callback = CallbackData("kind_sort", "sort")
prod_menu_callback = CallbackData("prod_menu", "value")
prod_nav_list_callback = CallbackData("nav_prod", "pages")
prod_confirm_callback = CallbackData("prod_confirm", "value")
prod_add_edit_callback = CallbackData("prod_add_edit", "field")
prod_info_callback = CallbackData("prod_info_edit", "_id")
prod_button_edit_callback = CallbackData("prod_edit", "_id")
prod_button_del_callback = CallbackData("prod_del", "_id")
prod_button_confirm_del_callback = CallbackData("prod_confirm_del", "_id")
prod_edit_edit_callback = CallbackData("prod_edit_edit", "field")


kind_menu_callback = CallbackData("kind_menu", "value")
kind_confirm_callback = CallbackData("kind_confirm", "value")
kind_add_callback = CallbackData("add_kind", "value")
kind_info_callback = CallbackData("kind_info_edit", "_id")
kind_button_edit_callback = CallbackData("kind_edit", "_id")
kind_button_del_callback = CallbackData("kind_del", "_id")
kind_button_confirm_del_callback = CallbackData("kind_confirm_del", "_id")


invoice_button_sort = CallbackData("invoice_sort", "kind")
invoice_sort_callback = CallbackData("invoice_sort", "sort")
invoice_menu_callback = CallbackData("invoice_menu", "value")
invoice_nav_list_callback = CallbackData("nav_invoice", "pages")
invoice_confirm_callback = CallbackData("invoice_confirm", "value")
invoice_add_edit_callback = CallbackData("invoice_add_edit", "field")
invoice_info_callback = CallbackData("invoice_info_edit", "_id")
invoice_button_edit_callback = CallbackData("invoice_edit", "_id")
invoice_button_del_callback = CallbackData("invoice_del", "_id")
invoice_button_confirm_del_callback = CallbackData("invoice_confirm_del", "_id")
invoice_edit_edit_callback = CallbackData("invoice_edit_edit", "field")


add_to_cart_button = CallbackData("add_to_cart", "_id")
del_from_cart_button = CallbackData("del_from_cart", "_id")
checkout_cart = CallbackData("checkout_cart", "_id")
checkout_order = CallbackData("checkout_order", "data")
time_checkout_order = CallbackData("time_checkout_order", "data")