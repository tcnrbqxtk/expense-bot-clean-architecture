from dishka import make_async_container
from infrastructure.providers.config_provider import ConfigProvider
from infrastructure.providers.logger_provider import LoggerProvider
from infrastructure.providers.main_provider import AiogramProvider
from infrastructure.providers.repository_provider import RepositoryProvider
from infrastructure.providers.interactor_provider import InteractorProvider

container = make_async_container(
    ConfigProvider(),
    LoggerProvider(),
    RepositoryProvider(),
    InteractorProvider(),
    AiogramProvider()
)