from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


@router.message(F.text == 'salom')
async def message_salom(message: types.Message):
    await message.answer(f"Salom {message.from_user.first_name}")



