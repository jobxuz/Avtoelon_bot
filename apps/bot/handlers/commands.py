from aiogram import Router, types, F
from aiogram.filters import Command
from apps.user.models import CustomUser, Detecsia
from django.utils.timezone import now
from aiogram.fsm.context import FSMContext
from apps.bot.keyboards.inline import language_key, mainmenu_key
from apps.bot.keyboards.reply import reply_send_phone_number
from asgiref.sync import sync_to_async
from apps.bot.utils.states import RegistrationStateGroup
from aiogram.types import CallbackQuery
from apps.bot.models import AllCar
from aiogram.types import InputMediaPhoto

from apps.bot.utils.send_detecsia_user import get_user_active_cars





router = Router()


@sync_to_async
def create_user_in_db(username, tg_id, language, phone, first_name):
    return CustomUser.objects.create(
        username=username,
        tg_id=tg_id,
        language=language,
        phone_number=phone,
        first_name=first_name
    )






@sync_to_async
def get_user_by_tg_id(tg_id):
    return CustomUser.objects.filter(tg_id=tg_id).exists()



@sync_to_async
def get_user_one(tg_id):
    return CustomUser.objects.get(tg_id=tg_id)



@router.message(Command('start'))
async def start_command(message: types.Message,state: FSMContext):
    print(message.text)
    tg_id = str(message.from_user.id)

    user_exists = await get_user_by_tg_id(tg_id)

    if user_exists:
        await message.answer(f"Yana ko'rishdik, {message.from_user.first_name}!\n\nKerakli bo'limni tanlang!",reply_markup=mainmenu_key)

    else:
        
        await message.reply(f"🇺🇿 Tilni tanlang\n🇺🇸 Select a language\n🇷🇺 Выберите язык", reply_markup=language_key)
        await state.set_state(RegistrationStateGroup.language)




@router.callback_query(RegistrationStateGroup.language)
async def process_language(callback_query: CallbackQuery, state: FSMContext):
    language = callback_query.data  
    await state.update_data(language=language)

    await callback_query.message.delete()
    await callback_query.message.answer("Telefon raqamingizni kiriting:",reply_markup=reply_send_phone_number())
    await state.set_state(RegistrationStateGroup.phone)


@router.message(RegistrationStateGroup.phone)
async def process_phone(message: types.Message, state: FSMContext):
    
    if message.contact:  
        phone = message.contact.phone_number
    else:  
        phone = message.text
    await state.update_data(phone=phone)

    await message.answer("Ismingizni kiriting:",reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationStateGroup.name)



@router.message(RegistrationStateGroup.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    
    user_data = await state.get_data()
    language = user_data.get('language')
    phone = user_data.get('phone')
    name = user_data.get('name')

    await create_user_in_db(
    message.from_user.first_name + str(message.from_user.id),
    str(message.from_user.id),
    language,
    phone,
    name
)

    all_cars = await sync_to_async(list)(AllCar.objects.all())
    await message.answer(f"Ro'yxatdan o'tdingiz! Kerakli bo'limni tanlang.",reply_markup=mainmenu_key)
    await state.clear()






@router.message(Command('avto'))
async def help_command(message: types.Message):
    user = await get_user_one(tg_id=message.from_user.id)

    user_cars = await get_user_active_cars(user)

    for car in user_cars:
        print(car.carbrand, car.carmodel)

    for car in user_cars:

        if car.images_str:
            media = [
                InputMediaPhoto(
                    media=car.images_str[:89], 
                    caption=f"{car.full_title}\nNarxi: {car.price_text}\n{car.description_params_str}\n{car.main_url}"
                )
            ]
            await message.bot.send_media_group(chat_id=message.chat.id, media=media)
        else:
            await message.answer(
                f"{car.full_title}\nNarxi: {car.price_text}\n{car.description_params_str}\n{car.main_url}"
            )