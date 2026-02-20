from dishka import make_async_container

from infrastructure.providers.config import ConfigProvider
from infrastructure.providers.logger import LoggerProvider
from infrastructure.providers.main import AiogramProvider
from infrastructure.providers.repostiory import RepositoryProvider
from infrastructure.providers.interactor import InteractorProvider
from infrastructure.providers.service import ServiceProvider


container = make_async_container(
    ConfigProvider(), LoggerProvider(), RepositoryProvider(), AiogramProvider(), InteractorProvider(), ServiceProvider()
)
