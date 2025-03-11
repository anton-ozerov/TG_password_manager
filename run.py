import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.client.default import DefaultBotProperties
from app.database.base import Base
from app.handlers import commands, master_password, main_menu, create_new_service
from app.data.config import BOT_TOKEN, DB_NAME
from app.middlewares.db import DatabaseMiddleware
from app.middlewares.delete_old_reply_markup import RemoveReplyMarkupMiddleware
from app.middlewares.reset_states_to_commands import ResetStateMiddleware


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)

    engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_NAME}')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_sessionmaker(engine)

    dp.update.middleware(DatabaseMiddleware(session=session))  # для БД
    dp.update.middleware(ResetStateMiddleware())  # удаление состояний при вводе команд
    dp.update.middleware(RemoveReplyMarkupMiddleware())  # удаление инлайн клавиатур у Message при новом Message

    dp.include_routers(commands.router, master_password.router, main_menu.router, create_new_service.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
