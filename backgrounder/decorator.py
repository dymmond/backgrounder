from typing import Any, Callable

from backgrounder.tasks import Task


def background(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator used to run background tasks on the top
    of any function in async mode.
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper covers for the decorator as individual as
        well as coming from the classes.
        """
        task = Task(fn, *args, **kwargs)
        return await task()

    return wrapper
