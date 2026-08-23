import httpx
import pytest

from pawa_ai._exceptions import APIConnectionError
from pawa_ai._retry import RetryConfig, async_request_with_retry, request_with_retry


def test_retry_config_delay_exponential():
    config = RetryConfig(initial_delay=1.0, exponential_base=2.0, max_delay=10.0, jitter=0.0)
    assert config.compute_delay(0) == 1.0
    assert config.compute_delay(1) == 2.0
    assert config.compute_delay(2) == 4.0
    assert config.compute_delay(5) == 10.0


def test_retry_respects_retry_after_header():
    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(
                503,
                headers={"Retry-After": "2"},
                json={"success": False, "message": "Unavailable"},
            )
        return httpx.Response(200, json={"ok": True})

    config = RetryConfig(max_retries=1, initial_delay=0.0, jitter=0.0)
    client = httpx.Client(transport=httpx.MockTransport(handler))

    with pytest.MonkeyPatch.context() as mp:
        slept: list[float] = []

        def fake_sleep(seconds: float) -> None:
            slept.append(seconds)

        mp.setattr("pawa_ai._retry.time.sleep", fake_sleep)
        response = request_with_retry(client, "GET", "https://example.com", retry_config=config)

    assert response.status_code == 200
    assert attempts["count"] == 2
    assert slept == [2.0]


def test_retry_connection_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed")

    config = RetryConfig(max_retries=1, initial_delay=0.0, jitter=0.0)
    client = httpx.Client(transport=httpx.MockTransport(handler))

    with pytest.raises(APIConnectionError):
        request_with_retry(client, "GET", "https://example.com", retry_config=config)


@pytest.mark.asyncio
async def test_async_retry_on_server_error():
    attempts = {"count": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(500, json={"success": False, "message": "error"})
        return httpx.Response(200, json={"ok": True})

    config = RetryConfig(max_retries=1, initial_delay=0.0, jitter=0.0)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await async_request_with_retry(
            client,
            "GET",
            "https://example.com",
            retry_config=config,
        )

    assert response.status_code == 200
    assert attempts["count"] == 2
