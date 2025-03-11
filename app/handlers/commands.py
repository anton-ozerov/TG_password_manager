from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.requests import Database
from app.handlers.main_menu import show_main_menu
from app.keyboards.master_password_kb import set_master_password_kb

router = Router()


# Срабатывает хэндлер на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message, db: Database):
    """Если пользователь имеет мастер-пароль, то вызывается вывод главное меню.
    Иначе - предложит создать мастер-пароль."""
    if await db.check_is_registered(message.from_user.id):
        msg = await show_main_menu(message)
    else:
        msg = await message.answer(
            'Здравствуйте. Это бот-менеджер паролей. Для того, чтобы продолжить пользование им, вам '
            'сейчас предстоит придумать главный пароль, который стоит запомнить. С помощью него, вы '
            'будете получать доступ ко всем остальным своим паролям. Он не должен быть '
            'лёгким. Подумайте, а после чего нажмите кнопку снизу',
            reply_markup=set_master_password_kb)
    return msg
