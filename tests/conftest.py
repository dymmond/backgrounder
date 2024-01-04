import functools

import pytest
from esmerald.testclient import TestClient


@pytest.fixture(scope="module")
def anyio_backend():
    return ("asyncio", {"debug": True})


@pytest.fixture
def test_client_factory(anyio_backend_name, anyio_backend_options):
    return functools.partial(
        TestClient,
        backend=anyio_backend_name,
        backend_options=anyio_backend_options,
    )
