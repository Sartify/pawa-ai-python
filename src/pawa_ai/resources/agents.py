from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import Stream, raise_for_status
from pawa_ai._streaming import AsyncChatCompletionStream, ChatCompletionStream
from pawa_ai.models.chat import ChatCompletion

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class AgentsResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client
        self.chat = AgentChatResource(client)

    def create(self, **params: Any) -> dict[str, Any]:
        response = self._client._post("/agents/create", json=params)
        raise_for_status(response)
        return response.json()

    def update(self, agent_id: int, **params: Any) -> dict[str, Any]:
        response = self._client._put(f"/agents/update/{agent_id}", json=params)
        raise_for_status(response)
        return response.json()

    def delete(self, agent_id: int) -> dict[str, Any]:
        response = self._client._delete(f"/agents/delete/{agent_id}")
        raise_for_status(response)
        return response.json()

    def list(self) -> dict[str, Any]:
        response = self._client._get("/agents/view")
        raise_for_status(response)
        return response.json()

    def retrieve(self, agent_id: int) -> dict[str, Any]:
        response = self._client._get(f"/agents/view/{agent_id}")
        raise_for_status(response)
        return response.json()


class AgentChatResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(
        self,
        *,
        raw: bool = False,
        **params: Any,
    ) -> ChatCompletion | ChatCompletionStream | Stream | dict[str, Any]:
        stream = bool(params.get("stream"))
        response = self._client._post("/agents/chat/request", json=params)
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


class AsyncAgentsResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client
        self.chat = AsyncAgentChatResource(client)

    async def create(self, **params: Any) -> dict[str, Any]:
        response = await self._client._post("/agents/create", json=params)
        raise_for_status(response)
        return response.json()

    async def update(self, agent_id: int, **params: Any) -> dict[str, Any]:
        response = await self._client._put(f"/agents/update/{agent_id}", json=params)
        raise_for_status(response)
        return response.json()

    async def delete(self, agent_id: int) -> dict[str, Any]:
        response = await self._client._delete(f"/agents/delete/{agent_id}")
        raise_for_status(response)
        return response.json()

    async def list(self) -> dict[str, Any]:
        response = await self._client._get("/agents/view")
        raise_for_status(response)
        return response.json()

    async def retrieve(self, agent_id: int) -> dict[str, Any]:
        response = await self._client._get(f"/agents/view/{agent_id}")
        raise_for_status(response)
        return response.json()


class AsyncAgentChatResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(
        self,
        *,
        raw: bool = False,
        **params: Any,
    ) -> ChatCompletion | AsyncChatCompletionStream | dict[str, Any]:
        stream = bool(params.get("stream"))
        response = await self._client._post("/agents/chat/request", json=params)
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
