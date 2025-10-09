from sqlalchemy import Column, Integer, BigInteger, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select  # Для асинхронных запросов
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import NoResultFound

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, Sequence('chats_id_seq'), primary_key=True, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    upd_date = Column(DateTime, default=None, onupdate=datetime.utcnow, nullable=True)

# Исправленная асинхронная функция getChatId
async def getChatId(chatId: int, session_maker: sessionmaker):
    async with session_maker() as session:
        try:
            # Пытаемся найти запись с указанным chat_id
            result = await session.execute(select(Chat).filter_by(chat_id=chatId))
            chat = result.scalars().first()  # Извлекаем первый результат
            if chat:
                return chat.id
            else:
                # Если запись не найдена, создаём новую
                new_chat = Chat(chat_id=chatId, creation_date=datetime.utcnow())
                session.add(new_chat)
                await session.commit()  # Асинхронно сохраняем изменения
                await session.refresh(new_chat)  # Обновляем объект, чтобы получить его id
                return new_chat.id
        except NoResultFound:
            # Если запись не найдена, создаём новую
            new_chat = Chat(chat_id=chatId, creation_date=datetime.utcnow())
            session.add(new_chat)
            await session.commit()  # Асинхронно сохраняем изменения
            await session.refresh(new_chat)  # Обновляем объект, чтобы получить его id
            return new_chat.id
