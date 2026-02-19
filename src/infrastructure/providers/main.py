from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dishka import Provider, Scope, provide  # type: ignore

from infrastructure.config import Config


class AiogramProvider(Provider):
    scope = Scope.APP

    @provide()
    async def provide_bot(self, config: Config) -> Bot:
        return Bot(token=config.BOT_TOKEN)

    @provide()
    async def provide_dispatcher(self, bot: Bot) -> Dispatcher:
        dp = Dispatcher(storage=MemoryStorage())
        return dp
