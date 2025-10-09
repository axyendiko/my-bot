import datetime
from typing import List

from aiogram import loggers
from sqlalchemy import Column, Integer, VARCHAR, select, BigInteger, Enum, DATE, BOOLEAN, update, ForeignKey # type: ignore
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, relationship, selectinload, Mapped  # type: ignore

from bot.db.user_tags import UserTags
from bot.db.chat import Chat
from .base import Base , Model  # type: ignore

class User(Base, Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,unique=True,nullable=True)
    user_name = Column(VARCHAR(32), unique=True, nullable=False)
    role = Column(VARCHAR(32), nullable=False)
    is_active = Column(BOOLEAN, default=True)
    chat_id = Column(Integer)
    

async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(selectinload(User.posts))
                .filter(User.user_id == user_id)  # type: ignore
            )
            return result.scalars().one()

async def get_user_by_name(user_name: str, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(selectinload(User.posts))
                .filter(User.user_name == user_name)  # type: ignore
            )
            return result.scalars().one()



async def create_user(user_id: int, user_name: str, role: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_name=user_name,
                role=role,
            )
            try:
                session.add(user)
            except Exception as e:
                loggers.dispatcher.info(e)
                pass
async def getUserById(user_id: int, session_maker: sessionmaker)->object:
    async with session_maker() as session:
        async with session.begin():
            result = await session.scalar(select(User).where(User.user_id == user_id))
            return result
async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            return bool(sql_res)

async def get_active_cooperators(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(select(User).where(User.role == 'copywriter').where(User.chat_id == chat_id).order_by(User.id).where(User.is_active == True))
            return sql_res.fetchall()

async def get_all_cooperators(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(select(User).where(User.role == 'copywriter'))
            return sql_res

async def get_inactive_cooperators(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.role == 'copywriter').where(User.is_active == False))
            return sql_res.scalars()

async def set_user_active(user_name: str ,session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = await session.execute(update(User).values({"is_active":True}).where(User.user_name == user_name))
            return user
async def set_user_inactive(user_name: str ,session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = await session.execute(update(User).values({"is_active":False}).where(User.user_name == user_name))
            return user