from aiogram.fsm.state import State, StatesGroup


class SettingsMenu(StatesGroup):
    choosing_action = State()
    waiting_for_currency = State()
    waiting_for_limit = State()
