from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Новая запись', callback_data="new_service")
    ],
    [
        InlineKeyboardButton(text='Все сервисы', callback_data="all_services"),
    ]
])
