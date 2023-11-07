import os
import asyncio
import sys

from aiogram import Bot, Dispatcher, loggers
import logging
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()
from .commands import register_commands
from .db import *
async def main()->None:
    postgres_url = 'postgresql+asyncpg://postgres:postgres@db:5433/sxodim'
    sys.path.append("..")
    loggers.dispatcher.info(postgres_url)
    print(postgres_url)
    logging.basicConfig(level=logging.DEBUG)
    dp=Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))

    register_commands(dp)
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, Base.metadata)
    await dp.start_polling(bot,session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt,SystemExit):
        print('Bot stopped')