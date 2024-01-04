import asyncio
import functools
from typing import Any, Callable

import anyio.from_thread
import anyio.to_thread
import nest_asyncio
import sniffio

from backgrounder.concurrency import AsyncCallable
from backgrounder.tasks import Task

nest_asyncio.apply()


def background(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator used to run background tasks on the top
    of any function in async mode.
    """

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper covers for the decorator as individual as
        well as coming from the classes.
        """

        task = Task(fn, *args, **kwargs)
        try:
            sniffio.current_async_library()
            async_callable = AsyncCallable(fn)
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(async_callable(*args, **kwargs))
        except sniffio.AsyncLibraryNotFoundError:
            return anyio.run(task)

    return wrapper
