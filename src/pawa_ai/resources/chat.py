from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import Stream, raise_for_status
from pawa_ai._streaming import AsyncChatCompletionStream, ChatCompletionStream
from pawa_ai.models.chat import ChatCompletion

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI
    from pawa_ai.types import ChatRequest


class ChatResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(
        self,
        *,
        raw: bool = False,
        **params: Any,
    ) -> ChatCompletion | ChatCompletionStream | Stream | dict[str, Any]:
        """Send a chat completion request.

        Set ``stream=True`` to receive a :class:`ChatCompletionStream`.
        Pass ``raw=True`` to receive untyped dict/Stream responses.
        """
        stream = bool(params.get("stream"))
        response = self._client._post("/chat/request", json=params)
        if stream:
            base_stream = Stream(response)
            if raw:
                return base_stream
            return ChatCompletionStream(base_stream)

        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        return ChatCompletion.from_dict(payload)

    def completions(self, **params: Any) -> ChatCompletion | ChatCompletionStream | dict[str, Any]:
        """Alias for :meth:`create`."""
        return self.create(**params)


class AsyncChatResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(
        self,
        *,
        raw: bool = False,
        **params: ChatRequest | Any,
    ) -> ChatCompletion | AsyncChatCompletionStream | dict[str, Any]:
        stream = bool(params.get("stream"))
        response = await self._client._post("/chat/request", json=params)
        if stream:
            from pawa_ai._http import AsyncStream

            base_stream = AsyncStream(response)
            if raw:
                return base_stream
            return AsyncChatCompletionStream(base_stream)

        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        return ChatCompletion.from_dict(payload)

    async def completions(
        self, **params: ChatRequest | Any
    ) -> ChatCompletion | AsyncChatCompletionStream | dict[str, Any]:
        return await self.create(**params)
