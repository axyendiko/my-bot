from aiogram import types, loggers
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import get_active_cooperators, get_all_cooperators
from bot.db.user_tags import get_last_tag, create_tag, get_tag_by_id


async def tag_user(message:types.Message, session_maker: sessionmaker)->None:
    if message.chat.id == -4066234169:
        try:
            activeCooperators = await get_active_cooperators(session_maker=session_maker)
            lastTaggedUser = await get_last_tag(session_maker=session_maker)
            activeCooperatorsIds = list(map(get_users_ids, activeCooperators))
            nearest_id = find_nearest_greater_value(activeCooperatorsIds, lastTaggedUser.user.id)
            user = await getEntry(activeCooperators, nearest_id)
            await message.answer(text=f'@{user.user_name}')
            await create_tag(user_id=user.id, session_maker=session_maker)
        except Exception as e:
            loggers.dispatcher.debug(e)
            await message.answer(text="sorry, try again")
    else:
        await message.answer(text=f'У тебя нет прав {message.chat.id}')
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
