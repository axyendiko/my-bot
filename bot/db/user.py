import datetime
from typing import List

from aiogram import loggers
from sqlalchemy import Column, Integer, VARCHAR, BigInteger, Enum, DATE, BOOLEAN, ForeignKey, select, update  # type: ignore
from sqlalchemy.orm import sessionmaker, selectinload  # type: ignore

from .base import Base, Model  # type: ignore

class User(Base, Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=True)
    user_name = Column(VARCHAR(32), unique=True, nullable=False)
    role = Column(VARCHAR(32), nullable=False)
    is_active = Column(BOOLEAN, default=True)
    chat_id = Column(Integer)
    
    # Если у вас есть связь с другими таблицами, добавьте её здесь:
    # posts = relationship("Post", back_populates="user")  # Пример связи с другой моделью

# Функция для получения пользователя по user_id
async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(selectinload(User.posts))  # Убедитесь, что у User есть связь с posts
                .filter(User.user_id == user_id)
            )
            return result.scalars().one()

# Функция для получения пользователя по имени
async def get_user_by_name(user_name: str, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(selectinload(User.posts))  # Убедитесь, что у User есть связь с posts
                .filter(User.user_name == user_name)
            )
            return result.scalars().one()

# Функция для создания нового пользователя
async def create_user(user_id: int, user_name: str, role: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,  # добавим user_id
                user_name=user_name,
                role=role,
            )
            try:
                session.add(user)
                await session.commit()  # Не забывайте вызвать commit, чтобы сохранить изменения
            except Exception as e:
                loggers.dispatcher.info(f"Error creating user: {e}")
                pass

# Функция для получения пользователя по user_id
async def getUserById(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.scalar(select(User).where(User.user_id == user_id))
            return result

# Функция для проверки существования пользователя по user_id
async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            return bool(sql_res.scalars().first())  # Исправлено для извлечения первого результата

# Получение всех активных сотрудников для указанного chat_id
async def get_active_cooperators(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(select(User).where(User.role == 'copywriter')
                                            .where(User.chat_id == chat_id)
                                            .where(User.is_active == True)
                                            .order_by(User.id))
            return sql_res.fetchall()

# Получение всех сотрудников
async def get_all_cooperators(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(select(User).where(User.role == 'copywriter'))
            return sql_res.all()  # Используем all() для получения всех результатов

# Получение всех неактивных сотрудников
async def get_inactive_cooperators(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.role == 'copywriter').where(User.is_active == False))
            return sql_res.scalars().all()

# Функция для активации пользователя
async def set_user_active(user_name: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = await session.execute(
                update(User)
                .values(is_active=True)
                .where(User.user_name == user_name)
            )
            await session.commit()  # Не забывайте делать commit

# Функция для деактивации пользователя
async def set_user_inactive(user_name: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = await session.execute(
                update(User)
                .values(is_active=False)
                .where(User.user_name == user_name)
            )
            await session.commit()  # Не забывайте делать commit
