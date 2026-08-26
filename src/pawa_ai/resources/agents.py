from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import raise_for_status
from pawa_ai._streaming import AsyncChatCompletionStream, ChatCompletionStream

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
        **params: Any,
    ) -> dict[str, Any] | ChatCompletionStream:
        stream = bool(params.get("stream"))
        response = self._client._post("/agents/chat/request", json=params)
        if stream:
            from pawa_ai._http import Stream

            return ChatCompletionStream(Stream(response))

        raise_for_status(response)
        return response.json()


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
        **params: Any,
    ) -> dict[str, Any] | AsyncChatCompletionStream:
        stream = bool(params.get("stream"))
        response = await self._client._post("/agents/chat/request", json=params)
        if stream:
            from pawa_ai._http import AsyncStream

            return AsyncChatCompletionStream(AsyncStream(response))

        raise_for_status(response)
        return response.json()
