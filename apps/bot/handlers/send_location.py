from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from apps.bot.handlers.start_order import start_order
from apps.bot.keyboards.inline import inline_categories, inline_nearest_branches
from apps.bot.utils.db_manager import db
from apps.bot.utils.functions import get_address, haversine
from apps.bot.utils.states import OrderStateGroup
from apps.bot.keyboards.reply import reply_choose_branch, reply_main_menu

router = Router()


@router.message(F.text == "Orqaga", OrderStateGroup.send_location)
async def order_message(message: types.Message, state: FSMContext):
    await start_order(update=message, state=state)


@router.message(F.location, OrderStateGroup.send_location)
async def order_book_message(message: types.Message, state: FSMContext, user):
    branches = await db.get_branches()
    user_longitude, user_latitude = message.location.longitude, message.location.latitude
    if not branches:
        return await message.answer("Hozirda restoranlar mavjud emas.")
    for branch in branches:
        branch.update({'distance': await haversine(
            user_longitude, user_latitude, branch['longitude'], branch['latitude']
        )})
    branches = sorted(branches, key=lambda branch: branch['distance'])

    address_line = await get_address(longitude=message.location.longitude, latitude=message.location.latitude)
    await message.answer(f"Sizning joylashuviz: {address_line}")

    order_data = await state.get_data()
    order_type = order_data.get('type_order', None)

    if order_type == 'delivery':

        if branches[0]['max_delivery_distance'] <= branches[0]['distance']:
            return await message.answer('Выбранная локация находится вне зоны доставки.')
        await state.update_data({'branch_id': branches[0]['branch_id']})

        categories = await db.get_categories()

        await message.answer("Lokatsiya qabul qilindi", reply_markup=reply_main_menu())
        await message.answer("Buyurtmani birga joylashtiramizmi? 🤗"
                             "\n Kategoriyalardan birini tanlang", reply_markup=await inline_categories(categories))
        await state.set_state(OrderStateGroup.choose_food)

        await db.create_order(user['telegram_id'], order_type, branches[0]['branch_id'], message.location.longitude,
                              message.location.latitude)

    if order_type == 'take_away':
        await message.answer("Eng yaqin restoranlar", reply_markup=inline_nearest_branches(branches))
        await state.set_state(OrderStateGroup.choose_branch_for_take_away)
