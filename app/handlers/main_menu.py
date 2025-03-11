from aiogram import F, Router
from aiogram.types import Message
from app.keyboards.main_kb import main_menu_kb


router = Router()


# Срабатывает хэндлер на нажатие инлайн-кнопки "Назад" при соответствующем callback_data
@router.callback_query(F.data == 'main_menu')
async def show_main_menu(message: Message, text: str = 'Здравствуйте!\nВыберите нужную кнопку снизу'):
    """Показ главного меню"""
    msg = await message.answer(text, reply_markup=main_menu_kb)
    return msg
