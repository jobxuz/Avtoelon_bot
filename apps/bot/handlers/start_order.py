from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from apps.bot.keyboards.inline import inline_main_menu
from apps.bot.keyboards.reply import reply_start_order, reply_send_location
from apps.bot.utils.callback_data import MainMenuCallbackData, MainMenuAction
from apps.bot.utils.states import OrderStateGroup

router = Router()


@router.callback_query(MainMenuCallbackData.filter(F.action == MainMenuAction.ORDER))
async def start_order(update: [types.CallbackQuery, types.Message], state: FSMContext):
    if isinstance(update, types.CallbackQuery):
        callback_query = update
        await callback_query.message.answer(
            f"Buyurtmani birga joylashtiramizmi? 🤗 Buyurtma turini tanlang?",
            reply_markup=reply_start_order())

    if isinstance(update, types.Message):
        message = update
        await message.answer("Buyurtmani birga joylashtiramizmi? �� Buyurtma turini tanlang?",
                             reply_markup=reply_start_order())

    await state.set_state(OrderStateGroup.order_type)


@router.message(F.text == "Orqaga")
async def order_message(message: types.Message, state: FSMContext):
    await message.answer("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=ReplyKeyboardRemove())
    await message.answer("Quyidagilardan birini tanlang", reply_markup=inline_main_menu())
    await state.clear()


@router.message(F.text == 'Borib olish', OrderStateGroup.order_type)
async def order_book_message(message: types.Message, state: FSMContext):
    await message.answer("Borib olish uchun geo-joylashuvni jo'nating, sizga yaqin bo'lgan filialni aniqlaymiz",
                         reply_markup=reply_send_location())
    await state.update_data({'type_order': 'take_away'})
    await state.set_state(OrderStateGroup.send_location)


@router.message(F.text == 'Eltib berish', OrderStateGroup.order_type)
async def order_delivery_message(message: types.Message, state: FSMContext):
    await message.answer("Eltib berish uchun geo - joylashuvni jo'nating yoki manzilni tanlang",
                         reply_markup=reply_send_location())
    await state.update_data({'type_order': 'delivery'})
    await state.set_state(OrderStateGroup.send_location)
