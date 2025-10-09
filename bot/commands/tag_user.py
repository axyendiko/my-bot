from aiogram import types, loggers
from sqlalchemy.orm import sessionmaker
from bot.db import get_active_cooperators
from bot.db.user_tags import get_last_tag, create_tag
from bot.db.chat import getChatId

async def tag_user(message: types.Message, session_maker: sessionmaker) -> None:
    try:
        chatId = await getChatId(chatId=message.chat.id, session_maker=session_maker)
        if chatId is None:
            await message.answer("Chat ID not found.")
            return

        activeCooperators = await get_active_cooperators(chatId, session_maker=session_maker)
        if not activeCooperators:
            await message.answer("No active cooperators found.")
            return

        lastTaggedUser = await get_last_tag(chatId, session_maker=session_maker)

        # Если нет последнего тэгнутого, берём первого пользователя из списка
        if not lastTaggedUser:
            user_to_tag = activeCooperators[0]
        else:
            activeCooperatorsIds = [user.id for user in activeCooperators]
            nearest_id = find_nearest_greater_value(activeCooperatorsIds, lastTaggedUser.user_id)
            user_to_tag = await getEntry(activeCooperators, nearest_id)

        if user_to_tag:
            await message.answer(text=f'@{user_to_tag.user_name}')
            await create_tag(user_id=user_to_tag.id, session_maker=session_maker)
        else:
            await message.answer("User not found.")
            
    except Exception as e:
        loggers.dispatcher.debug(e)
        await message.answer(text="Sorry, an error occurred. Please try again.")

# Вспомогательные функции остаются прежними
def find_nearest_greater_value(lst, target):
    if not lst:
        return None
    nearest_greater = None
    for item in lst:
        if item > target:
            if nearest_greater is None or item < nearest_greater:
                nearest_greater = item
    return nearest_greater if nearest_greater is not None else lst[0]

async def getEntry(lst, target):
    return next((x for x in lst if x.id == target), None)