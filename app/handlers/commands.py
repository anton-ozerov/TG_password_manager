from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.requests import Database
from app.keyboards.main_kb import main_menu_kb
from app.keyboards.master_password_kb import set_master_password_kb

router = Router()


# Срабатывает хэндлер на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message, db: Database, text='Здравствуйте!\nВыберите нужную кнопку снизу'):
    """Если пользователь имеет мастер-пароль, то вызывается вывод главное меню.
    Иначе - предложит создать мастер-пароль."""
    if await db.check_is_registered(message.from_user.id):
        msg = await main_menu(message)
    else:
        msg = await message.answer(
            'Здравствуйте. Это бот-менеджер паролей. Для того, чтобы продолжить пользование им, вам '
            'сейчас предстоит придумать главный пароль, который стоит запомнить. С помощью него, вы '
            'будете получать доступ ко всем остальным своим паролям. Он не должен быть '
            'лёгким. Подумайте, а после чего нажмите кнопку снизу',
            reply_markup=set_master_password_kb)
    return msg


# Срабатывает хэндлер на нажатие инлайн-кнопки "Назад" при соответствующем callback_data
@router.message(F.data == 'main_menu')
async def main_menu(message: Message, text: str = 'Здравствуйте!\nВыберите нужную кнопку снизу'):
    """Показ главного меню"""
    msg = await message.answer(text, reply_markup=main_menu_kb)
    return msg
