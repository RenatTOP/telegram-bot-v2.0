import aiogram.types
from aiogram.utils.callback_data import CallbackData


admin_menu_callback = CallbackData("admin_menu", "value")


depart_menu_callback = CallbackData("depart_menu", "value")
depart_confirm_callback = CallbackData("depart_confirm", "value")
depart_add_edit_callback = CallbackData("depart_add_edit", "field")
depart_info_callback = CallbackData("depart_info_edit", "_id")
depart_button_edit_callback = CallbackData("depart_edit", "_id")
depart_button_del_callback = CallbackData("depart_del", "_id")
depart_button_confirm_del_callback = CallbackData("depart_confirm_del", "_id")
depart_edit_edit_callback = CallbackData("deprt_edit_edit", "field")
depart_button_back_callback = CallbackData("back", "value")

prod_menu_callback = CallbackData("prod_menu", "value")
prod_confirm_callback = CallbackData("depart_confirm", "value")
prod_edit_callback = CallbackData("depart_edit", "value")
