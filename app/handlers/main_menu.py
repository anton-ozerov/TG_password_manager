from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.keyboards.main_kb import main_menu_kb


router = Router()


# Срабатывает хэндлер на нажатие инлайн-кнопки "Назад" при соответствующем callback_data
@router.callback_query(F.data == 'main_menu')
async def show_main_menu(msg_cbq: CallbackQuery | Message, state: FSMContext = None,
                         text: str = 'Здравствуйте!\nВыберите нужную кнопку снизу'):
    """Показ главного меню со сбросом машины состояния, если есть"""
    if state:
        await state.clear()

    if isinstance(msg_cbq, Message):
        msg = await msg_cbq.answer(text, reply_markup=main_menu_kb)
    else:
        msg = await msg_cbq.message.edit_text(text, reply_markup=main_menu_kb)
    return msg
