import logging

from dishka import Provider, Scope, provide  # type: ignore

from infrastructure.config import Config
from infrastructure.logger.logging_dev import setup_logging as setup_logging_dev
from infrastructure.logger.logging_prod import setup_logging as setup_logging_prod


class LoggerProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_logger(self, config: Config) -> logging.Logger:
        if config.ENV.upper() == "PROD":
            setup_logging_prod()
        else:
            setup_logging_dev()
        return logging.getLogger(__name__)
