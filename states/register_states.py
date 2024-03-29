from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStatesGroup(StatesGroup):
    fullname = State()
    phone = State()
    school = State()
    pinfl = State()
