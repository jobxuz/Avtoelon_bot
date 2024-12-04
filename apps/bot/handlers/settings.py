from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from apps.bot.keyboards.inline import inline_settings
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction
from apps.bot.utils.db_manager import db

router = Router()


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.SETTINGS))
async def settings(callback_query: types.CallbackQuery, state: FSMContext):
    #users = await db.get_all_users()
    state = await state.get_data()
    #data1 =await state.get_data()
    user = callback_query.from_user
    user_data = await db.get_user(telegram_id=user.id)
    lang = user_data['language']
    data2 = callback_query.data
    if lang == "ru":
        language = "Русский"
    elif lang == "en":
        language = "English"
    else:
        language = "O'zbek"
    #phone = user.phone_number
    await callback_query.message.answer("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove())
    await callback_query.message.answer(f"<b>Muloqot tili: </b>{language}\n"
                                        f"<b>Telefon: {user_data['phone']}</b>  \n"
                                        "<b>Shahar: </b>Toshkent\n", parse_mode="HTML", reply_markup=inline_settings())



