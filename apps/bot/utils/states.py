from aiogram.fsm.state import StatesGroup, State


class RegistrationStateGroup(StatesGroup):
    language = State()
    phone = State()
    name = State()


class OrderStateGroup(StatesGroup):
    order_type = State()
    send_location = State()
    choose_branch_for_take_away = State()
    choose_food = State()
