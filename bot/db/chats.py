import datetime

from aiogram import loggers
from sqlalchemy import Column, Integer, VARCHAR,BigInteger, DateTime, BOOLEAN, ForeignKey, DATE,select
from sqlalchemy.orm import relationship, Mapped, sessionmaker, selectinload

from .base import Model,Base

class Chats(Base, Model):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger,unique=True,nullable=False)
    user_tags = relationship("UserTags", back_populates="chat")
    user = relationship("User", back_populates="chat")

async def create_chat(chat_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            chat = Chats(
                chat_id=chat_id,
            )
            try:
                session.add(chat)
            except Exception as e:
                loggers.dispatcher.info(e)
                pass

async def getChatById(chat_id: int, session_maker: sessionmaker)->object:
    async with session_maker() as session:
        async with session.begin():
            result = await session.scalar(select(Chats).where(Chats.chat_id == chat_id))
            return result