from backgrounder.decorator import background


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
