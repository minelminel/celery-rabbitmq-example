from .. import Config
from .supervisor import Supervisor


supervisor = Supervisor(
    enabled=Config.SUPERVISOR_ENABLED,
    debug=Config.SUPERVISOR_DEBUG
)
