from sqlalchemy import Column, Integer, BigInteger, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, Sequence('chats_id_seq'), primary_key=True, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    upd_date = Column(DateTime, default=None, onupdate=datetime.utcnow, nullable=True)

async def getChatId(chatId: int, session_maker: sessionmaker):
    async with session_maker() as session:
        try:
        # Пытаемся найти запись с указанным chat_id
        chat = session.query(Chat).filter_by(chat_id=chat_id).one()
        return chat.id
    except NoResultFound:
        # Если запись не найдена, создаём новую
        new_chat = Chat(chat_id=chat_id, creation_date=datetime.utcnow())
        session.add(new_chat)
        session.commit()  # Сохраняем изменения в базе данных
        session.refresh(new_chat)  # Обновляем объект, чтобы получить его id
        return new_chat.id

