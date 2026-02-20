from dishka import Provider, Scope, provide  # type: ignore
from infrastructure.config import Config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        return Config()
