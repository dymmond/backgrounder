import asyncio
import functools
from concurrent import futures
from typing import Any, Awaitable, Callable, Coroutine, TypeVar

import anyio.to_thread

from backgrounder._compat import is_async_callable

T = TypeVar("T")


def run_sync(async_function: Coroutine) -> Any:
    """
    Runs the queries in sync mode
    """
    try:
        return asyncio.run(async_function)
    except RuntimeError:
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, async_function)
            return future.result()


async def run_in_threadpool(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """
    Runs a callable in a threapool.
    Make sure the callable is always async.
    """
    def_func = AsyncCallable(func)
    return await def_func(*args, *kwargs)


def enforce_async_callable(func: Callable[..., Any]) -> Callable[..., Awaitable[T]]:
    """
    Enforces the callable to be async by returning an AsyncCallable.
    """
    return func if is_async_callable(func) else AsyncCallable(func)  # type:ignore


class AsyncCallable:
    """
    Creates an async callable and when called, runs in a thread pool.
    """

    __slots__ = ("_callable", "default_kwargs")

    def __init__(self, func: Callable[..., Any], **kwargs: Any) -> None:
        self._callable = func
        self.default_kwargs = kwargs

    def __call__(self, *args: Any, **kwargs: Any) -> Awaitable[T]:
        combined_kwargs = {**self.default_kwargs, **kwargs}
        return anyio.to_thread.run_sync(
            functools.partial(self._callable, **combined_kwargs), *args
        )

    async def run_in_threadpool(self, *args: Any, **kwargs: Any) -> T:
        return await self(*args, **kwargs)
