from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.back_button_kb import create_back_button


async def new_service_password_kb(length: int = 15, uppercase: bool = True,
                                  digits: bool = True, punctuation: bool = True) -> InlineKeyboardMarkup:
    """Создание клавиатуры на этапе пароля для создания нового сервиса"""
    # new_service__l15-u1-d1-p1
    # l - длина, u - 0/1 нужны ли заглавные буквы, d - 0/1 нужны ли цифры, p - 0/1 нужны ли пунктуационные символы
    upp, dig, pun = int(uppercase), int(digits), int(punctuation)  # превращаем в 0 или 1
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='💾Сохранить', callback_data="save_password_new_service")
        ],
        [
            InlineKeyboardButton(text='➕Длина +1', callback_data=f"new_service__l{length + 1}-u{upp}-d{dig}-p{pun}"),
            InlineKeyboardButton(text='➖Длина -1', callback_data=f"new_service__l{length - 1}-u{upp}-d{dig}-p{pun}"),
        ],
        [
            InlineKeyboardButton(text='✅ABCD' if upp else '⛔️ABCD',
                                 callback_data=f"new_service__l{length}-u{int(not upp)}-d{dig}-p{pun}"),
            InlineKeyboardButton(text='✅1234' if dig else '⛔️1234',
                                 callback_data=f"new_service__l{length}-u{upp}-d{int(not dig)}-p{pun}"),
            InlineKeyboardButton(text='✅!.,$' if pun else '⛔️!.,$',
                                 callback_data=f"new_service__l{length}-u{upp}-d{dig}-p{int(not pun)}")
        ],
        [
            InlineKeyboardButton(text='🔄Пересоздать', callback_data=f"new_service__l{length}-u{upp}-d{dig}-p{pun}")
        ],
        [
            InlineKeyboardButton(text='📜Указать свой', callback_data='enter_your_password')
        ],
        [
            await create_back_button('new_service')
        ]
    ])
    return kb


# эта клавиатура выводится, когда просят ввести собственный пароль ещё раз
change_first_password_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Изменить первый пароль', callback_data='enter_your_password')
    ]
])

# эта клавиатура выводится, когда предлагается добавить комментарий к новой записи
skip_comment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Пропустить', callback_data='skip_comment')
    ]
])
