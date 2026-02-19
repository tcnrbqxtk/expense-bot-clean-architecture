import asyncio
import logging
from aiogram import Bot, Dispatcher

from presentation.handlers import all_handlers
from infrastructure.providers.container import container
from dishka.integrations.aiogram import setup_dishka
from infrastructure.config import Config

logger = logging.getLogger(__name__)


async def main():
    config: Config = await container.get(Config)
    logger: logging.Logger = await container.get(logging.Logger)

    if not config.BOT_TOKEN:
        logger.error("Bot token is not found in .env")
        return

    bot: Bot = await container.get(Bot)
    dp: Dispatcher = await container.get(Dispatcher)
    
    setup_dishka(container=container, router=dp)

    dp.include_routers(*all_handlers)

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("🤖 Бот запущен (polling)")
    await dp.start_polling(bot)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
