from aiogram.dispatcher.filters.state import State, StatesGroup


class Mark(StatesGroup):
    branch_id = State()
    department_id = State()
    user_id = State()
    employee_id = State()
    grade = State()
    comment = State()
