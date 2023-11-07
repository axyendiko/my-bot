from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.db import create_chat

class AddChatState(StatesGroup):
    add_chat = State()

async def add_chat(message:types.Message,state: FSMContext)->None:
    await state.set_state(AddChatState.add_chat)
    await message.message.answer(text='text me chat id')

async def save_chat_id(message:types.Message, state:FSMContext, session_maker:sessionmaker)->None:
    try:
        await create_chat(chat_id=int(message.text), session_maker=sessionmaker)
        await message.answer(text='success')
    except:
        await message.answer(text='fail, try again')