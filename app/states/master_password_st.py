from aiogram.fsm.state import StatesGroup, State


class MasterPassword(StatesGroup):
    master_password = State()
    again = State()
