from dishka import Provider, Scope, provide  # type: ignore

from infrastructure.config import Config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    def provide_admin_ids(self, config: Config) -> list[str]:
        return config.admin_ids_list
