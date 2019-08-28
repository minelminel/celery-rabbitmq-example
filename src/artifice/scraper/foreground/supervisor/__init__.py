import artifice.scraper.config.settings as settings
from .supervisor import Supervisor


supervisor = Supervisor(
    enabled=settings.SUPERVISOR_ENABLED,
    debug=settings.SUPERVISOR_DEBUG,
    polite=settings.SUPERVISOR_POLITE,
)
