from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.db import create_user,getUserById


class AddUserState(StatesGroup):
    user_name = State()
    role = State()
    update_name = State()
    finish = State()

async def add_user_start(call:types.CallbackQuery, state: FSMContext,session_maker:sessionmaker)->None:
    user = await getUserById(user_id=int(call.message.chat.id), session_maker=session_maker)
    if user and user.role == 'administrator':
        await state.set_state(AddUserState.user_name)
        await call.message.answer(text='Enter user name from telegram(without "@"):')
    else:
        await call.message.answer(text='gotcha, bitch')

async def add_user_name(message:types.Message, state: FSMContext)->None:
    await state.update_data(user_name=message.text)
    builder = InlineKeyboardBuilder()
    builder.button(text='Administrator',callback_data='role:administrator')
    builder.button(text='Cooperator',callback_data='role:copywriter')
    builder.adjust(1)
    await message.answer(text='Select user role:', reply_markup=builder.as_markup())
    await state.set_state(AddUserState.role)

async def add_user_role(call:types.CallbackQuery, state: FSMContext)->None:
    await state.update_data(role=call.data.split(':')[1])
    await call.message.delete()
    data = await state.get_data()
    builder = InlineKeyboardBuilder()
    for key in data.keys():
        builder.button(text=f'{key}:{data[key]}', callback_data=f'update:{key}')
    builder.button(text='Save', callback_data=f"update:False")
    builder.adjust(1)
    await call.message.answer('Create user with values', reply_markup=builder.as_markup())
    await state.set_state(AddUserState.finish)

async def finish(call:types.CallbackQuery,session_maker:sessionmaker, state:FSMContext)->None:
    data = await state.get_data()
    await call.message.delete()
    if call.data.split(':')[1] == 'False':
        try:
            await create_user(user_id=call.from_user.id,user_name=data['user_name'],role=data['role'],session_maker=session_maker)
            await call.message.answer(text='User created')
            await state.clear()
        except:
            await call.message.answer(text='Exception, try again')
            await state.clear()
    elif call.data.split(':')[1] == 'user_name':
        await call.message.answer(text='Enter user name from telegram(without "@"):')
        await state.set_state(AddUserState.update_name)
    elif call.data.split(':')[1] == 'role':
        builder = InlineKeyboardBuilder()
        builder.button(text='Administrator', callback_data='role:administrator')
        builder.button(text='Cooperator', callback_data='role:copywriter')
        builder.adjust(1)
        await call.message.answer(text='Select user role:', reply_markup=builder.as_markup())
        await state.set_state(AddUserState.role)


async def update_user_name(message:types.Message, state: FSMContext)->None:
    try:
        await state.update_data(user_name=message.text)
        data = await state.get_data()
        builder = InlineKeyboardBuilder()
        for key in data.keys():
            builder.button(text=f'{key}:{data[key]}', callback_data=f'update:{key}')
        builder.button(text='Save', callback_data=f"update:False")
        builder.adjust(1)
        await message.answer('Create user with values', reply_markup=builder.as_markup())
        await state.set_state(AddUserState.finish)
    except:
        await message.answer('sorry,try again')
        await state.clear()