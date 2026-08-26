from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import raise_for_status
from pawa_ai._streaming import AsyncChatCompletionStream, ChatCompletionStream

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI
    from pawa_ai.types import ChatRequest


class ChatResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(
        self,
        **params: Any,
    ) -> dict[str, Any] | ChatCompletionStream:
        """Send a chat completion request.

        Returns the API JSON as a ``dict``. Set ``stream=True`` to receive a
        :class:`ChatCompletionStream`.
        """
        stream = bool(params.get("stream"))
        response = self._client._post("/chat/request", json=params)
        if stream:
            from pawa_ai._http import Stream

            return ChatCompletionStream(Stream(response))

        raise_for_status(response)
        return response.json()

    def completions(self, **params: Any) -> dict[str, Any] | ChatCompletionStream:
        """Alias for :meth:`create`."""
        return self.create(**params)


class AsyncChatResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(
        self,
        **params: ChatRequest | Any,
    ) -> dict[str, Any] | AsyncChatCompletionStream:
        stream = bool(params.get("stream"))
        response = await self._client._post("/chat/request", json=params)
        if stream:
            from pawa_ai._http import AsyncStream

            return AsyncChatCompletionStream(AsyncStream(response))

        raise_for_status(response)
        return response.json()

    async def completions(
        self, **params: ChatRequest | Any
    ) -> dict[str, Any] | AsyncChatCompletionStream:
        return await self.create(**params)
