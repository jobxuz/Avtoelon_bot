from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from apps.bot.handlers.start_order import order_book_message
from apps.bot.keyboards.inline import inline_categories
from apps.bot.utils.callback_data import BranchCallbackData
from apps.bot.utils.db_manager import db
from apps.bot.utils.states import OrderStateGroup

router = Router()


@router.message(F.state == OrderStateGroup.choose_branch_for_take_away, F.text == 'Orqaga')
async def back_to_send_location(message: types.Message, state: FSMContext):
    await order_book_message(message, state)


@router.callback_query(BranchCallbackData.filter(), F.state == OrderStateGroup.choose_branch_for_take_away)
async def show_branch_details(callback_query: types.CallbackQuery, callback_data: BranchCallbackData,
                              state: FSMContext, user):
    branch_id = callback_data.branch_id
    categories = await db.get_categories()

    order_data = await state.get_data()

    await state.update_data({'branch_id': branch_id})
    await callback_query.message.answer("Buyurtmani birga joylashtiramizmi? 🤗",
                                        reply_markup=types.ReplyKeyboardRemove())
    await callback_query.message.answer("Kategoriyalardan birini tanlang.", parse_mode="HTML",
                                        reply_markup=await inline_categories(categories))
    await state.set_state(OrderStateGroup.choose_food)
    await db.create_order(user['id'], order_data['order_type'], branch_id, None, None)
