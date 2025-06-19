import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import structure, utils, similarity, descriptors


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_routers(structure.router,
                   utils.router,
                   similarity.router,
                   descriptors.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
