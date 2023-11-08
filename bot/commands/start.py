import logging
import os

from aiogram import types
from aiogram import loggers
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from bot.db.user import getUserById

async def start(message:types.Message, session_maker:sessionmaker)->None:
    user = await getUserById(user_id= int(message.from_user.id),session_maker=session_maker)
    if user and user.role == 'administrator':
        builder = InlineKeyboardBuilder()
        builder.button(text='Создать пользователя', callback_data='function:addUser')
        builder.adjust(1)
        postgres_url = URL.create(
            "postgresql+asyncpg",
            username=os.getenv('db_user_name'),
            password=os.getenv('db_password'),
            host='localhost',
            database=os.getenv('db_name'),
            port=os.getenv('db_port'),
        )
        loggers.dispatcher.info(postgres_url)
        await message.answer(text=f'Приует {user.user_name},выбери команду \ncommands: \n /active - список активных адамов \n /inactive -  список неактивных адамов \n /chat- доабвить рабочий чатик с друзьяшками', reply_markup=builder.as_markup())
    else:
        await message.answer(text=f"{message.from_user.id}")