from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.requests import Database
from app.handlers.main_menu import show_main_menu
from app.keyboards.back_button_kb import create_back_kb
from app.keyboards.create_new_service_kb import new_service_password_kb, change_first_password_kb, skip_comment_kb
from app.states.create_new_service_st import NewService
from app.utils.clear_name import clean_text
from app.utils.create_password import generate_password
from app.utils.encryption_decryption_passwords import hash_password, check_password


router = Router()


# Срабатывает хэндлер на нажатие инлайн-кнопки "Новая запись" в главном меню
@router.callback_query(F.data == 'new_service')
async def add_new_service(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем название нового сервиса. Прикрепляется клавиатура с кнопкой 'Отмена'."""
    await state.clear()

    await callback.message.edit_text('Введите название сервиса\n\nПример: <code>Google</code>',
                                     reply_markup=await create_back_kb())
    await state.set_state(NewService.name)


@router.message(NewService.name)  # для состояния ввода имени
@router.callback_query(F.data.startswith('new_service__'))  # для кнопок с настройками пароля
async def get_new_service_name(msg_cbq: Message | CallbackQuery, state: FSMContext):
    """Если Message - получаем имя. Для обоих случаев: генерируется пароль, выводится клавиатура с настройками пароля.
    А именно: длина, есть ли заглавные, есть ли цифры, есть ли пунктуационные знаки"""
    if isinstance(msg_cbq, Message):
        await state.update_data(name=msg_cbq.text)
        length, uppercase, digits, punctuation = 15, 1, 1, 1
    else:
        length, uppercase, digits, punctuation = [int(i[1:]) for i in msg_cbq.data.split('__')[1].split('-')]

    password = await generate_password(length=length, uppercase=uppercase, digits=digits, punctuation=punctuation)
    await state.update_data(hashed_password=await hash_password(password))  # Сразу добавляем. Если что, перезапишется

    name = (await state.get_data())['name']
    text = (f"<b>Название сервиса:</b> {clean_text(name)}\n\n"
            f"<b>Длина:</b> {length}\n"
            f"<b>Заглавные буквы:</b> {'есть' if uppercase else 'нет'}\n"
            f"<b>Цифры:</b> {'есть' if digits else 'нет'}\n"
            f"<b>Пунктуационные знаки:</b> {'есть' if punctuation else 'нет'}\n\n"
            f"<b>Предлагаемый пароль:</b> <code>{clean_text(password)}</code>\n")
    kb = await new_service_password_kb(length=length, uppercase=uppercase, digits=digits, punctuation=punctuation)
    if isinstance(msg_cbq, Message):
        return await msg_cbq.answer(text=text, reply_markup=kb)
    else:
        return await msg_cbq.message.edit_text(text=text, reply_markup=kb)


# Срабатывает хэндлер при нажатии инлайн-кнопки "📜Указать свой"
@router.callback_query(F.data == 'enter_your_password')
async def enter_password(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем пароль у пользователя, запуская машину состояния"""
    await callback.message.edit_text('Введите свой пароль',
                                     reply_markup=await create_back_kb(f'new_service__l15-u1-d1-p1'))
    await state.set_state(NewService.password)


# Срабатывает хэндлер при состоянии машины для ввода собственного пароля
@router.message(NewService.password)
async def get_password(message: Message, state: FSMContext):
    """Получение пароля из машины состояния и запрос повторного ввода у пользователя (его сообщение удаляем)"""
    await message.delete()  # удаление сообщения с паролем пользователя

    await state.update_data(hashed_password=await hash_password(message.text))
    await state.set_state(NewService.password_again)
    msg = await message.answer('Введите пароль ещё раз', reply_markup=change_first_password_kb)
    return msg


@router.message(NewService.password_again)  # при состоянии машины для ПОВТОРНОГО ввода собственного пароля
@router.callback_query(F.data == 'save_password_new_service')  # При нажатии инлайн-кнопки "💾Сохранить"
async def get_password_again(msg_cbq: Message | CallbackQuery, state: FSMContext):
    """Если Callback - даем возможность написать комментарий к записи (с кнопкой отказа). Если Message - получаем
    повторный ввод пароля и сообщение удаляем: если совпадают - регистрируем и даем возможность написать комментарий к
    записи (с кнопкой отказа), а если не совпадают - просим ввести ещё раз"""
    if isinstance(msg_cbq, CallbackQuery):  # Т.е. если сгенерированный пароль, а не собственный
        msg = await msg_cbq.message.edit_text('Введите комментарий к записи или нажмите на кнопку снизу',
                                              reply_markup=skip_comment_kb)
        await state.set_state(NewService.comment)
    else:
        await msg_cbq.delete()  # удаляем сообщение с его паролем

        hashed_master_password = (await state.get_data())['hashed_password']
        if await check_password(password=msg_cbq.text, hashed_password=hashed_master_password):
            msg = await msg_cbq.answer('Введите комментарий к записи или нажмите на кнопку снизу',
                                       reply_markup=skip_comment_kb)
            await state.set_state(NewService.comment)
        else:
            await state.set_state(NewService.password_again)
            msg = await msg_cbq.answer('Пароли не совпадают. Попробуйте ещё раз',
                                       reply_markup=change_first_password_kb)
    return msg


@router.message(NewService.comment)  # для состояния ввода комментария
@router.callback_query(F.data == 'skip_comment')  # для кнопки "Пропустить"
async def handle_comment(msg_cbq: Message | CallbackQuery, state: FSMContext, db: Database):
    """Получаем комментарий, если Message. После чего, добавляем информацию в БД и показываем главное меню"""
    data = await state.get_data()
    await state.clear()

    if isinstance(msg_cbq, Message):  # если пользователь оставил комментарий
        owner_id = msg_cbq.from_user.id
        comment = msg_cbq.text
    else:  # если пользователь решил не оставлять комментарий
        owner_id = msg_cbq.from_user.id
        comment = None

    await db.add_password(owner_id=owner_id, name=data['name'],
                          hashed_password=data['hashed_password'], comment=comment)
    await show_main_menu(msg_cbq, text='Новая запись создана. Выберите нужную кнопку снизу')
