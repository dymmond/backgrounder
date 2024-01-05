__version__ = "0.2.0"

from .decorator import background
from .tasks import Task, Tasks

__all__ = ["background", "Task", "Tasks"]
