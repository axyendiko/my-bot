from aiogram import types, loggers
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from bot.db import get_active_cooperators, get_all_cooperators
from bot.db.user_tags import get_last_tag, create_tag, get_tag_by_id
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
        if not lastTaggedUser:
            await message.answer("No last tagged user found.")
            return

        activeCooperatorsIds = list(map(get_users_ids, activeCooperators))
        nearest_id = find_nearest_greater_value(activeCooperatorsIds, lastTaggedUser.user.id)
        user = await getEntry(activeCooperators, nearest_id)
        
        if user:
            await message.answer(text=f'@{user.user_name}')
            await message.answer(text=f'@{nearest_id}')
            await message.answer(text=f'@{activeCooperatorsIds}')
            await create_tag(user_id=user.id, session_maker=session_maker)
        else:
            await message.answer("User not found.")
    except Exception as e:
        loggers.dispatcher.debug(e)
        await message.answer(text="Sorry, an error occurred. Please try again.")

def find_nearest_greater_value(lst, target):
    lst = list(lst)
    nearest_greater = None
    for item in lst:
        if item > target:
            if nearest_greater is None or item < nearest_greater:
                nearest_greater = item
    if nearest_greater is None:
            return lst[0]
    return nearest_greater
async def getEntry(lst, target):
  return next((x for x in lst if x.id == target), None)

def get_users_ids(user: list):
    return user.id
