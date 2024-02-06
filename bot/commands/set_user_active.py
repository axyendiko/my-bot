from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.db import set_user_active
from bot.db.user import get_inactive_cooperators,getUserById


class SetUserActive(StatesGroup):
    set_active = State()

async def set_active_command(message:types.Message, session_maker: sessionmaker, state: FSMContext)->None:
    user = await getUserById(user_id=int(message.from_user.id), session_maker=session_maker)
    if user and user.role == 'administrator':
        try:
            users = await get_inactive_cooperators(chat_id= user.chat_id,session_maker=session_maker)
        except Exception as e:
            await message.answer('sorry, try again')
            return
        builder = InlineKeyboardBuilder()
        for user in users:
            builder.button(text=f'{user.user_name}', callback_data=f'set_active:{user.user_name}')
        builder.adjust(1)
        await message.answer(text=f'выберите пользователя чтобы выключить его', reply_markup=builder.as_markup())
        await state.set_state(SetUserActive.set_active)
    else:
        await message.answer(text='gotcha, bitch')

async def set_active_function(call:types.CallbackQuery, session_maker: sessionmaker, state: FSMContext)->None:
    await call.message.delete()
    user_name = call.data.split(':')[1]
    try:
        user = await set_user_active(user_name=user_name, session_maker=session_maker)
    except Exception as e:
        await call.message.answer('sorry, try again')
        return

    await call.message.answer(text='Успшено Өшірілген')





