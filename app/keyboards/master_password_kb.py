from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


set_master_password_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Задать пароль', callback_data='set_master_password')
    ]
])

# эта клавиатура выводится, когда просят ввести мастер-пароль ещё раз
change_first_password = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Изменить первый пароль', callback_data='set_master_password')
    ]
])
