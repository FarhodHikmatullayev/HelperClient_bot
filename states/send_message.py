from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMessageState(StatesGroup):
    content = State()
