from aiogram.fsm.state import StatesGroup, State


class RegistrationStateGroup(StatesGroup):
    language = State()
    phone = State()
    name = State()



class NewDetecsiaStatesGroup(StatesGroup):
    brend = State()
    model = State()
    yaratish = State()



class DetecsiaUpdate(StatesGroup):
    one_detecsia = State()
    update_detecsia = State()
    update_filter = State()
    delete_detecsia = State()
    report_detecsia = State()