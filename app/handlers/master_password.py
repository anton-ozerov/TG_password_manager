from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.requests import Database
from app.handlers.commands import start_command
from app.keyboards.master_password_kb import change_first_password
from app.states.master_password_st import MasterPassword
from app.utils.encryption_decryption_passwords import hash_password, check_password


router = Router()


# Срабатывает хэндлер на нажатие инлайн-кнопки "Задать пароль" или "Изменить первый пароль"
# "Задать пароль" - после команды /start
# "Изменить первый пароль" - после ввода мастер-пароля в первый раз
@router.callback_query(F.data == 'set_master_password')
async def set_state__master_password(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем мастер-пароль у пользователя, запуская машину состояния"""
    await callback.message.edit_text('Введите главный пароль')
    await state.set_state(MasterPassword.master_password)


# Срабатывает хэндлер при состоянии машины для ввода мастер-пароля
@router.message(MasterPassword.master_password)
async def get_master_password(message: Message, state: FSMContext):
    """Получение мастер-пароля из машины состояния и запрос повторного ввода у пользователя (его сообщение удаляем)"""
    await message.delete()  # удаляем сообщение с его паролем

    await state.update_data(hashed_master_password=await hash_password(message.text))
    await state.set_state(MasterPassword.again)
    msg = await message.answer('Введите пароль ещё раз', reply_markup=change_first_password)
    return msg


# Срабатывает хэндлер при состоянии машины для ПОВТОРНОГО ввода мастер-пароля
@router.message(MasterPassword.again)
async def again_get_master_password(message: Message, state: FSMContext, db: Database):
    """Получаем повторный ввод мастер-пароля и сообщение удаляем. Если совпадают - регистрируем и показываем
    главное меню. Нет - просим ввести ещё раз"""
    await message.delete()  # удаляем сообщение с его паролем

    hashed_master_password = (await state.get_data())['hashed_master_password']
    if await check_password(password=message.text, hashed_password=hashed_master_password):
        username: str | None = message.from_user.username
        await db.add_user(id=message.from_user.id, username=username, hashed_master_password=hashed_master_password)
        await state.clear()
        await start_command(message, db, text='Пароль успешно создан. Выберите нужную кнопку снизу')
    else:
        await state.set_state(MasterPassword.again)
        msg = await message.answer('Пароли не совпадают. Попробуйте ещё раз', reply_markup=change_first_password)
        return msg
