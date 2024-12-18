from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from apps.bot.utils.states import NewDetecsiaStatesGroup, DetecsiaUpdate
from aiogram.types import CallbackQuery
from apps.bot.keyboards.inline import detecsi_key, mainmenu_key, create_car_brands_key, create_car_models_key,detecsia_key,detecsia_update_key
from asgiref.sync import sync_to_async
from apps.bot.models import CarBrand, CarModel,AllCar
from apps.user.models import  Detecsia
from apps.bot.handlers.commands import get_user_one
from aiogram.types import InputMediaPhoto


router = Router()



@sync_to_async
def create_user_detecsia(car_brand, car_model, user):
    return Detecsia.objects.create(
        car_brand=car_brand,
        car_model=car_model,
        user=user
    )


@sync_to_async
def detecsia_all(tg_id):
    return Detecsia.objects.filter(user__tg_id=tg_id)



@router.callback_query(lambda callback_query: callback_query.data == "new_detection")
async def handle_new_detection(callback_query: CallbackQuery, state: FSMContext):
    car_brands = await sync_to_async(list)(CarBrand.objects.all())

    # Birinchi sahifani chiqaramiz
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Avtomobil brandini tanlang!",
        reply_markup=create_car_brands_key(car_brands, page=1, page_size=10) 
    )
    await state.set_state(NewDetecsiaStatesGroup.brend)


@router.callback_query(lambda callback_query: callback_query.data.startswith("page:"))
async def handle_pagination(callback_query: CallbackQuery):
   
    page = int(callback_query.data.split(":")[1])
    car_brands = await sync_to_async(list)(CarBrand.objects.all())

   
    await callback_query.message.edit_reply_markup(
        reply_markup=create_car_brands_key(car_brands, page=page, page_size=10)
    )






@router.callback_query(NewDetecsiaStatesGroup.brend)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    carbrand = callback_query.data


    
    await state.update_data(carbrand=carbrand)
    car_models = await sync_to_async(list)(CarModel.objects.filter(brend__name=carbrand))

   
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Avtomobil modelini tanlang:",
        reply_markup=create_car_models_key(car_models, page=1, page_size=10)  
    )
    await state.set_state(NewDetecsiaStatesGroup.model)



@router.callback_query(lambda callback_query: callback_query.data.startswith("model_page:"))
async def handle_model_pagination(callback_query: CallbackQuery, state: FSMContext):
    
    page = int(callback_query.data.split(":")[1])

    user_data = await state.get_data()
    carbrand = user_data.get("carbrand")

    
    car_models = await sync_to_async(list)(CarModel.objects.filter(brend__name=carbrand))


    await callback_query.message.edit_reply_markup(
        reply_markup=create_car_models_key(car_models, page=page, page_size=10)
    )






@router.callback_query(NewDetecsiaStatesGroup.model)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    carmodel = callback_query.data
    print(callback_query.data)
    await state.update_data(carmodel=carmodel)

    

    await callback_query.message.delete()
    await callback_query.message.answer(f"Quyidagilardan birini tanlang!",reply_markup=detecsi_key)
    await state.set_state(NewDetecsiaStatesGroup.yaratish)
    


@router.callback_query(NewDetecsiaStatesGroup.yaratish)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'createdetecsia':
        print(callback_query.data)
        user_data = await state.get_data()
        carbrand = user_data.get('carbrand')
        carmodel = user_data.get('carmodel')

        user = await get_user_one(callback_query.from_user.id)

    
        await create_user_detecsia(
        carbrand,
        carmodel,
        user
            )


        #await callback_query.message.delete()
        all_cars_elon = await sync_to_async(list)(AllCar.objects.all()[:5])

        for all_cars_info in all_cars_elon:
            media = [
                InputMediaPhoto(media=all_cars_info.images_str[:89], caption=f"{all_cars_info.full_title}\nNarxi: {all_cars_info.price_text}\n{all_cars_info.description_params_str}\n{all_cars_info.main_url}"),
            ]

            await callback_query.message.bot.send_media_group(chat_id=callback_query.from_user.id, media=media)
        await callback_query.message.answer(f"Detecsia yaratildi\n\nAsosiy menu",reply_markup=mainmenu_key)
        await state.clear()
    else:
        await callback_query.message.answer("Noma'lum callback data")




@router.callback_query(lambda callback_query: callback_query.data == "activedetections")
async def detecsi_on_user_all(callback_query: CallbackQuery, state: FSMContext):
    activ_detecsia = await sync_to_async(list)(Detecsia.objects.filter(user__tg_id=callback_query.from_user.id))
    await callback_query.message.delete()
    await callback_query.message.answer("Sizning detecsiangiz!",reply_markup=detecsia_key(activ_detecsia))
    await state.set_state(DetecsiaUpdate.one_detecsia)
    




@router.callback_query(DetecsiaUpdate.one_detecsia)
async def process_brand(callback_query: CallbackQuery, state: FSMContext):
    detecsia_one = callback_query.data
    print(detecsia_one)
    print(detecsia_one.split('_')[0])
    print(detecsia_one.split('_')[-1])
    
    await state.update_data(detecsia_one=detecsia_one)
    #car_models = await sync_to_async(list)(CarModel.objects.filter(brend__name=carbrand))
    activ_detecsia = await sync_to_async(list)(Detecsia.objects.filter(user__tg_id=callback_query.from_user.id, car_brand=detecsia_one.split('_')[0], car_model=detecsia_one.split('_')[-1]))
    print(activ_detecsia)
    await callback_query.message.delete()
    await callback_query.message.answer("Birini tanlang",reply_markup= detecsia_update_key)
    await state.set_state(DetecsiaUpdate.update_detecsia)
    #await state.clear()
    #await state.finish()





@router.callback_query(DetecsiaUpdate.update_detecsia)
async def update_detecsia_user(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    detecsia_on = str(user_data.get('detecsia_one'))
    activ_detecsias = await sync_to_async(list)(Detecsia.objects.filter(user__tg_id=callback_query.from_user.id, car_brand=detecsia_on.split('_')[0], car_model=detecsia_on.split('_')[-1]))

    if str(callback_query.data) == 'detecsia_update':
        if activ_detecsias:  
            for activ_detecsia in activ_detecsias:
                activ_detecsia.is_active = not activ_detecsia.is_active 
                await sync_to_async(activ_detecsia.save)()  
                await callback_query.message.delete() 
                await callback_query.message.answer(f"{activ_detecsia.car_brand} holati o'zgartirildi: {activ_detecsia.is_active}",reply_markup= detecsia_update_key)
            #await state.clear()
        else:
            print("Detecsia topilmadi!")
            await state.clear()
    elif str(callback_query.data) == 'boshsahifa':
        await callback_query.message.delete()
        await callback_query.message.answer("Bosh sahifa",reply_markup=mainmenu_key)
        await state.clear()



