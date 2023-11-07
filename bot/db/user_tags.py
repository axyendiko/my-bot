import datetime

from aiogram import loggers
from sqlalchemy import Column, Integer, VARCHAR, DateTime, BOOLEAN, ForeignKey, DATE,select
from sqlalchemy.orm import relationship, Mapped, sessionmaker, selectinload

from .base import Model,Base

class UserTags(Base, Model):
    __tablename__ = 'user_tags'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User",back_populates="user_tags")

    def __init__(self, user_id):
        self.user_id = user_id

async def get_last_tag(session_maker: sessionmaker):

    async with session_maker() as session:
        async with session.begin():
            result = await session.scalar(select(UserTags).order_by(UserTags.id.desc()).options(selectinload(UserTags.user)))
            return result

async def get_tag_by_id(id: int,session_maker: sessionmaker):

    async with session_maker() as session:
        async with session.begin():
            result = await session.scalar(select(UserTags).where(UserTags.id == id).order_by(UserTags.id.desc()).options(selectinload(UserTags.user)))
            return result


async def create_tag(user_id: int, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            userTag = UserTags(
                user_id = user_id
            )
            try:
                session.add(userTag)
            except Exception as e:
                loggers.dispatcher.info(e)
                pass