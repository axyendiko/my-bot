from aiogram import types, loggers
from sqlalchemy.orm import sessionmaker
from bot.db import get_active_cooperators
from bot.db.user_tags import get_last_tag, create_tag
from bot.db.chat import getChatId

async def tag_user(message: types.Message, session_maker: sessionmaker) -> None:
    try:
        # Получаем chat_id
        chatId = await getChatId(chatId=message.chat.id, session_maker=session_maker)
        if chatId is None:
            await message.answer("Chat ID not found.")
            return

        # Получаем всех активных сотрудников
        activeCooperators = await get_active_cooperators(chatId, session_maker=session_maker)
        if not activeCooperators:
            await message.answer("No active cooperators found.")
            return

        # Получаем последнего отмеченного пользователя
        lastTaggedUser = await get_last_tag(chatId, session_maker=session_maker)
        if not lastTaggedUser:
            await message.answer("No last tagged user found.")
            return
        
        # Получаем IDs всех активных сотрудников
        activeCooperatorsIds = [user.id for user in activeCooperators]
        
        # Находим ближайшее большее значение
        nearest_id = find_nearest_greater_value(activeCooperatorsIds, lastTaggedUser.user_id)
        
        # Ищем пользователя по найденному ID
        user = await getEntry(activeCooperators, nearest_id)
        
        if user:
            await message.answer(text=f'@{user.user_name}')
            await create_tag(user_id=user.id, chat_id=chatId, session_maker=session_maker)
        else:
            await message.answer("User not found.")
    except Exception as e:
        loggers.dispatcher.debug(e)
        await message.answer(text="Sorry, an error occurred. Please try again.")

def find_nearest_greater_value(lst, target):
    # Если список пустой, возвращаем None
    if not lst:
        return None

    nearest_greater = None
    for item in lst:
        if item > target:
            if nearest_greater is None or item < nearest_greater:
                nearest_greater = item

    if nearest_greater is None:
        return lst[0]  # Если ближайшее большее не найдено, возвращаем первый элемент
    return nearest_greater

async def getEntry(lst, target):
    # Находим объект в списке по целевому ID
    return next((x for x in lst if x.id == target), None)

# Функция для извлечения id пользователей
def get_users_ids(user):
    return user.id  # предполагается, что user — это объект с атрибутом id
