from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.db import get_active_cooperators, set_user_active, set_user_inactive


class SetUserInactive(StatesGroup):
    set_inactive = State()

async def set_inactive_command(message:types.Message, session_maker: sessionmaker, state: FSMContext)->None:
    try:
        users = await get_active_cooperators(session_maker=session_maker)
    except Exception as e:
        await message.answer('sorry, try again')
        return
    builder = InlineKeyboardBuilder()
    for user in users:
        builder.button(text=f'{user.user_name}', callback_data=f'set_inactive:{user.user_name}')
    builder.adjust(1)
    await message.answer(text=f'select user to set active', reply_markup=builder.as_markup())
    await state.set_state(SetUserInactive.set_inactive)

async def set_inactive_function(call:types.CallbackQuery, session_maker: sessionmaker, state: FSMContext)->None:
    user_name = call.data.split(':')[1]
    try:
        user = await set_user_inactive(user_name=user_name, session_maker=session_maker)
    except Exception as e:
        await call.message.answer('sorry, try again')
        return

    await call.message.answer(text='success')