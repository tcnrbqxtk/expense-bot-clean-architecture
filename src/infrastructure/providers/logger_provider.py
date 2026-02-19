from dishka import Provider, provide, Scope  # type: ignore
import logging
from infrastructure.config import Config
from infrastructure.logger.logging_prod import setup_logging as setup_logging_prod
from infrastructure.logger.logging_dev import setup_logging as setup_logging_dev

class LoggerProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_logger(self, config: Config) -> logging.Logger:
        if config.ENV.upper() == "PROD":
            setup_logging_prod()
        else:
            setup_logging_dev()
        return logging.getLogger(__name__)