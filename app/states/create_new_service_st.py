from aiogram.fsm.state import StatesGroup, State


class NewService(StatesGroup):
    name = State()
    password = State()
    password_again = State()
    comment = State()
