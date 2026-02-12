from aiogram.fsm.state import State, StatesGroup


class AdminMenu(StatesGroup):
    choosing_action = State()
    waiting_for_user_id = State()
