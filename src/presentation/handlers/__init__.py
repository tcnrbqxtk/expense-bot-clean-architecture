from .add import router as add_handler_router

# from .admin import router as admin_handler_router
# from .clear import router as clear_handler_router
# from .help import router as help_handler_router
from .settings import router as settings_handler_router
from .start import router as start_handler_router
from .stats import router as stats_handler_router


all_handlers = (
    start_handler_router,
    # help_handler_router,
    add_handler_router,
    stats_handler_router,
    # clear_handler_router,
    settings_handler_router,
    # admin_handler_router,
)
