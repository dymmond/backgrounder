import pytest

from backgrounder.decorator import background
from backgrounder.tasks import Task

GLOBAL = 0

pytestmark = pytest.mark.anyio


async def test_decorator_async():
    TOTAL = 0

    @background
    async def work():
        # Do something expensive here.
        nonlocal TOTAL
        TOTAL = 1

    await work()
    assert TOTAL == 1


async def test_task():
    TOTAL = 0

    async def work(number):
        # Do something expensive here.
        nonlocal TOTAL
        TOTAL = 1

    task = Task(work, 2)

    assert TOTAL == 0

    await task()

    assert TOTAL == 1


async def test_task_blocking():
    TOTAL = 0

    def work(number):
        # Do something expensive here.
        nonlocal TOTAL
        TOTAL = 1

    task = Task(work, 2)

    assert TOTAL == 0

    await task()

    assert TOTAL == 1


def test_decorator():
    TOTAL = 0

    @background
    def work(number):
        # Do something expensive here.
        nonlocal TOTAL
        TOTAL = number

    assert TOTAL == 0

    work(2)

    assert TOTAL == 2
