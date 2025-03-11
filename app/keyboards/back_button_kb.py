from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_back_button(callback_data: str = 'main_menu') -> InlineKeyboardButton:
    """Создание кнопки 'Назад' с переданной callback_data. Если ничего не передается,
    кнопка будет вести в главное меню"""
    return InlineKeyboardButton(text='🔙Назад', callback_data=callback_data)


async def create_back_kb(callback_data: str = 'main_menu') -> InlineKeyboardMarkup:
    """Создание клавиатуры с одной кнопкой 'Назад' с переданной необязательной callback_data. Если ничего не передается,
    кнопка будет вести в главное меню"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            await create_back_button(callback_data)
        ]
    ])
    return kb
