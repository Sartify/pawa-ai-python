from unittest.mock import patch

import httpx
import pytest

from pawa_ai import (
    AsyncPawaAI,
    AuthenticationError,
    ChatCompletion,
    ChatCompletionStream,
    PawaAI,
    RetryConfig,
)
from pawa_ai._http import parse_stream_line, raise_for_status
from pawa_ai._streaming import AsyncChatCompletionStream
from pawa_ai.models.chat import ChatCompletion as ChatCompletionModel
from pawa_ai.models.chat import ChatStreamChunk


def test_parse_stream_line():
    assert parse_stream_line('{"success": true}') == {"success": True}
    assert parse_stream_line("data: {\"a\": 1}") == {"a": 1}
    assert parse_stream_line("") is None
    assert parse_stream_line("[DONE]") is None


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("PAWA_AI_API_KEY", raising=False)
    with pytest.raises(AuthenticationError):
        PawaAI()


def test_client_builds_auth_header():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"ok": True}))
    client = PawaAI(api_key="test-key", http_client=httpx.Client(transport=transport))

    client._get("/models")
    assert client._http_client is not None


def test_chat_create_returns_typed_model():
    payload = {
        "success": True,
        "message": "Chat request processed successfully",
        "data": {
            "request": [
                {
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": "Hello there"},
                    "matched_stop": 106,
                }
            ],
            "created": "1753304351",
            "model": "pawa-v1-ember-20240924",
            "object": "chat.request",
            "usage": {"tokens_in": 10, "tokens_out": 5},
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    client = PawaAI(api_key="test-key", http_client=httpx.Client(transport=transport))

    response = client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
        stream=False,
    )
    assert isinstance(response, ChatCompletion)
    assert response.success is True
    assert response.text == "Hello there"
    assert response.usage is not None
    assert response.usage.tokens_in == 10


def test_chat_create_raw_response():
    payload = {"success": True, "message": "ok", "data": {}}
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    client = PawaAI(api_key="test-key", http_client=httpx.Client(transport=transport))

    response = client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
        raw=True,
    )
    assert response["success"] is True


def test_raise_for_status_maps_errors():
    response = httpx.Response(401, json={"success": False, "message": "Unauthorized access"})
    with pytest.raises(AuthenticationError) as exc:
        raise_for_status(response)
    assert exc.value.status_code == 401
    assert exc.value.message == "Unauthorized access"


def test_stream_helpers():
    body = (
        '{"success":true,"data":{"message":{"content":"Hel"}}}\n'
        '{"success":true,"data":{"message":{"content":"lo"}}}\n'
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)

    transport = httpx.MockTransport(handler)
    client = PawaAI(api_key="test-key", http_client=httpx.Client(transport=transport))

    with client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
        stream=True,
    ) as stream:
        assert isinstance(stream, ChatCompletionStream)
        assert stream.collect_text() == "Hello"

    collected = client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
        stream=True,
    ).collect()
    assert isinstance(collected, ChatCompletionModel)
    assert collected.text == "Hello"


@pytest.mark.asyncio
async def test_async_chat_create_success():
    payload = {
        "success": True,
        "message": "ok",
        "data": {
            "request": [
                {"finish_reason": "stop", "message": {"role": "assistant", "content": "A"}},
            ],
            "created": "",
            "model": "pawa-v1-ember-20240924",
            "object": "chat.request",
        },
    }

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)
    async with AsyncPawaAI(
        api_key="test-key",
        http_client=httpx.AsyncClient(transport=transport),
    ) as client:
        response = await client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
        )
        assert response.text == "A"


@pytest.mark.asyncio
async def test_async_stream_collect_text():
    body = '{"success":true,"data":{"message":{"content":"Hi"}}}\n'

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)

    transport = httpx.MockTransport(handler)
    async with AsyncPawaAI(
        api_key="test-key",
        http_client=httpx.AsyncClient(transport=transport),
    ) as client:
        stream = await client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
            stream=True,
        )
        assert isinstance(stream, AsyncChatCompletionStream)
        assert await stream.collect_text() == "Hi"


def test_retry_on_rate_limit():
    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(429, json={"success": False, "message": "Rate limit exceeded"})
        return httpx.Response(200, json={"success": True, "message": "ok", "data": {}})

    transport = httpx.MockTransport(handler)
    config = RetryConfig(max_retries=2, initial_delay=0.0, jitter=0.0)
    client = PawaAI(
        api_key="test-key",
        retry_config=config,
        http_client=httpx.Client(transport=transport),
    )

    with patch("pawa_ai._retry.time.sleep"):
        response = client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[{"role": "user", "content": [{"type": "text", "text": "Hi"}]}],
            raw=True,
        )

    assert attempts["count"] == 2
    assert response["success"] is True


def test_chat_stream_chunk_from_dict():
    chunk = ChatStreamChunk.from_dict(
        {
            "success": True,
            "message": "chunk",
            "data": {"message": {"content": "Hi", "role": "assistant"}},
        }
    )
    assert chunk.delta == "Hi"
    assert chunk.role == "assistant"
