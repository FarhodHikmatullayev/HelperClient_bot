from aiogram.dispatcher.filters.state import State, StatesGroup


class AddEmployeeState(StatesGroup):
    waiting_for_excel_file = State()
