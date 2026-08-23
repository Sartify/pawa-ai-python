from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from pawa_ai._exceptions import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
)


def _status_error_class(status_code: int) -> type[APIStatusError]:
    if status_code == 400:
        return BadRequestError
    if status_code == 401:
        return AuthenticationError
    if status_code == 404:
        return NotFoundError
    if status_code == 429:
        return RateLimitError
    return APIStatusError


def _parse_error_body(response: httpx.Response) -> Any:
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
    return response.text


def _error_message(body: Any, fallback: str) -> str:
    if isinstance(body, dict):
        message = body.get("message")
        if isinstance(message, str) and message:
            return message
    if isinstance(body, str) and body:
        return body
    return fallback


def raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return

    body = _parse_error_body(response)
    message = _error_message(body, f"HTTP {response.status_code}")
    error_class = _status_error_class(response.status_code)
    raise error_class(message, status_code=response.status_code, body=body)


def parse_stream_line(line: str) -> dict[str, Any] | None:
    line = line.strip()
    if not line:
        return None
    if line.startswith("data:"):
        line = line[5:].strip()
    if line == "[DONE]":
        return None
    return json.loads(line)


class Stream:
    """Sync iterator over newline-delimited JSON stream chunks."""

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self._iterator = response.iter_lines()

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return self

    def __next__(self) -> dict[str, Any]:
        for line in self._iterator:
            chunk = parse_stream_line(line)
            if chunk is not None:
                return chunk
        raise StopIteration

    def __enter__(self) -> Stream:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._response.close()


class AsyncStream:
    """Async iterator over newline-delimited JSON stream chunks."""

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self._iterator = response.aiter_lines()

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self

    async def __anext__(self) -> dict[str, Any]:
        async for line in self._iterator:
            chunk = parse_stream_line(line)
            if chunk is not None:
                return chunk
        raise StopAsyncIteration

    async def __aenter__(self) -> AsyncStream:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._response.aclose()


def build_multipart_files(
    field_name: str,
    files: list[str | bytes | tuple[str, bytes, str | None]],
) -> list[tuple[str, tuple[str, bytes, str | None]]]:
    """Build httpx multipart file tuples from paths or raw bytes."""
    multipart: list[tuple[str, tuple[str, bytes, str | None]]] = []
    for index, item in enumerate(files):
        if isinstance(item, str):
            with open(item, "rb") as handle:
                data = handle.read()
            filename = item.rsplit("/", 1)[-1]
            multipart.append((field_name, (filename, data, None)))
            continue

        if isinstance(item, tuple):
            multipart.append((field_name, item))
            continue

        multipart.append((field_name, (f"file_{index}", item, None)))
    return multipart
