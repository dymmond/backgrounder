import pytest

from backgrounder.decorator import background


@pytest.mark.asyncio
async def test_decorator():
    TOTAL = 0

    @background
    async def work(number):
        # Do something expensive here.
        nonlocal TOTAL
        TOTAL = number

    assert TOTAL == 0

    await work(2)

    assert TOTAL == 2
