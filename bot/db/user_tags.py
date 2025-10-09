import datetime
from aiogram import loggers
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select

from .base import Base, Model

class UserTags(Base, Model):
    __tablename__ = 'user_tags'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Здесь можно оставить ссылку на пользователя, если она нужна
    chat_id = Column(BigInteger, nullable=False)  # Убираем связь с User
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id

# Функция для получения последнего тега
async def get_last_tag(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(UserTags)
                .where(UserTags.chat_id == chat_id)
                .order_by(UserTags.id.desc())
                .limit(1)  # Ограничиваем выборку только последним результатом
            )
            last_tag = result.scalars().first()  # Получаем первый (и единственный) результат
            return last_tag

# Функция для получения тега по ID
async def get_tag_by_id(id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(UserTags)
                .where(UserTags.id == id)
            )
            tag = result.scalars().first()  # Возвращаем первый (и единственный) результат
            return tag

# Функция для создания нового тега
async def create_tag(user_id: int, chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user_tag = UserTags(user_id=user_id, chat_id=chat_id)  # Убедитесь, что оба поля передаются
            session.add(user_tag)  # Добавляем объект в сессию
            await session.commit()  # Асинхронно сохраняем изменения в базе данных
            await session.refresh(user_tag)  # Обновляем объект, чтобы получить его id
            return user_tag.id  # Возвращаем id нового тега
