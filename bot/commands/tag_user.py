from aiogram import types, loggers
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import get_active_cooperators, get_all_cooperators, getChatById
from bot.db.user_tags import get_last_tag, create_tag, get_tag_by_id

async def tag_user(message:types.Message, session_maker: sessionmaker)->None:
    try:
        chat = await getChatById(chat_id=int(message.chat.id), session_maker=session_maker)
    except Exception as e:
        await message.answer(text=f'Не карайсын? , {message.chat.id}')
        loggers.dispatcher.info(f'{e} ERROR')
        return
    if chat is not None and message.chat.id == chat.chat_id:
        try:
            activeCooperators = await get_active_cooperators(chat_id=chat.id, session_maker=session_maker)
            lastTaggedUser = await get_last_tag(session_maker=session_maker)
            activeCooperatorsIds = list(map(get_users_ids, activeCooperators))
            if lastTaggedUser is None:
                nearest_id = activeCooperatorsIds[0]
            else:
                nearest_id = find_nearest_greater_value(activeCooperatorsIds, lastTaggedUser.user.id)
            user = await getEntry(activeCooperators, nearest_id)
            await message.answer(text=f'@{user.user_name}')
            await create_tag(user_id=user.id, chat_id=chat.id, session_maker=session_maker)
        except Exception as e:
            loggers.dispatcher.debug(e)
            await message.answer(text="sorry, try again")
    else:
        loggers.dispatcher.info(chat)
        await message.answer(text=f'У тебя нет прав) {message.chat.id}')
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
