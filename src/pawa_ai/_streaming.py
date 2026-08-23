from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from pawa_ai._http import AsyncStream, Stream
from pawa_ai.models.chat import ChatCompletion, ChatStreamChunk


class ChatCompletionStream:
    """Rich helper for streaming chat completions."""

    def __init__(self, stream: Stream) -> None:
        self._stream = stream

    def __iter__(self) -> Iterator[ChatStreamChunk]:
        return self

    def __next__(self) -> ChatStreamChunk:
        return ChatStreamChunk.from_dict(next(self._stream))

    def __enter__(self) -> ChatCompletionStream:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def chunks(self) -> Iterator[ChatStreamChunk]:
        """Yield typed stream chunks."""
        for raw in self._stream:
            yield ChatStreamChunk.from_dict(raw)

    def text_deltas(self) -> Iterator[str]:
        """Yield only the text delta from each chunk."""
        for chunk in self.chunks():
            if chunk.delta:
                yield chunk.delta

    def collect_text(self) -> str:
        """Collect all text deltas into a single string."""
        return "".join(self.text_deltas())

    def collect(self) -> ChatCompletion:
        """Build a :class:`ChatCompletion` from the full streamed text."""
        text = self.collect_text()
        return ChatCompletion.from_dict(
            {
                "success": True,
                "message": "Stream collected",
                "data": {
                    "request": [
                        {
                            "finish_reason": "stop",
                            "message": {"role": "assistant", "content": text},
                        }
                    ],
                    "created": "",
                    "model": "",
                    "object": "chat.request",
                },
            }
        )

    def close(self) -> None:
        self._stream.close()


class AsyncChatCompletionStream:
    """Async rich helper for streaming chat completions."""

    def __init__(self, stream: AsyncStream) -> None:
        self._stream = stream

    def __aiter__(self) -> AsyncIterator[ChatStreamChunk]:
        return self.chunks()

    async def chunks(self) -> AsyncIterator[ChatStreamChunk]:
        async for raw in self._stream:
            yield ChatStreamChunk.from_dict(raw)

    async def text_deltas(self) -> AsyncIterator[str]:
        async for chunk in self.chunks():
            if chunk.delta:
                yield chunk.delta

    async def collect_text(self) -> str:
        parts: list[str] = []
        async for delta in self.text_deltas():
            parts.append(delta)
        return "".join(parts)

    async def collect(self) -> ChatCompletion:
        text = await self.collect_text()
        return ChatCompletion.from_dict(
            {
                "success": True,
                "message": "Stream collected",
                "data": {
                    "request": [
                        {
                            "finish_reason": "stop",
                            "message": {"role": "assistant", "content": text},
                        }
                    ],
                    "created": "",
                    "model": "",
                    "object": "chat.request",
                },
            }
        )

    async def close(self) -> None:
        await self._stream.close()

    async def __aenter__(self) -> AsyncChatCompletionStream:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
