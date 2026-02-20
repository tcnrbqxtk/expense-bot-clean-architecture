from dishka import Provider, Scope, provide  # type: ignore

from application.services.period import PeriodService
from application.services.stats_formatter import StatsFormatterService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def period_service_provide(self) -> PeriodService:
        return PeriodService()

    @provide()
    def stats_formatter_service_provide(self) -> StatsFormatterService:
        return StatsFormatterService()
