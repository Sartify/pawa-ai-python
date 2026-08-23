from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import raise_for_status

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class StorageResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client
        self.knowledge_base = KnowledgeBaseResource(client)


class KnowledgeBaseResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(self, **params: Any) -> dict[str, Any]:
        response = self._client._post("/store/knowledge-base", json=params)
        raise_for_status(response)
        return response.json()

    def list(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        params = {"page": page, "limit": limit, "search": search}
        response = self._client._get(
            "/store/knowledge-base",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        return response.json()

    def retrieve(self, knowledge_base_id: int) -> dict[str, Any]:
        response = self._client._get(f"/store/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    def update(self, knowledge_base_id: int, **params: Any) -> dict[str, Any]:
        response = self._client._put(f"/store/knowledge-base/{knowledge_base_id}", json=params)
        raise_for_status(response)
        return response.json()

    def delete(self, knowledge_base_id: int) -> dict[str, Any]:
        response = self._client._delete(f"/store/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    def list_files(self, knowledge_base_id: int) -> dict[str, Any]:
        response = self._client._get(f"/store/files/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    def semantic_retrieval(self, **params: Any) -> dict[str, Any]:
        response = self._client._post("/store/knowledge-base/semantic-retrieval", json=params)
        raise_for_status(response)
        return response.json()


class AsyncStorageResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client
        self.knowledge_base = AsyncKnowledgeBaseResource(client)


class AsyncKnowledgeBaseResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(self, **params: Any) -> dict[str, Any]:
        response = await self._client._post("/store/knowledge-base", json=params)
        raise_for_status(response)
        return response.json()

    async def list(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        params = {"page": page, "limit": limit, "search": search}
        response = await self._client._get(
            "/store/knowledge-base",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        return response.json()

    async def retrieve(self, knowledge_base_id: int) -> dict[str, Any]:
        response = await self._client._get(f"/store/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    async def update(self, knowledge_base_id: int, **params: Any) -> dict[str, Any]:
        response = await self._client._put(
            f"/store/knowledge-base/{knowledge_base_id}",
            json=params,
        )
        raise_for_status(response)
        return response.json()

    async def delete(self, knowledge_base_id: int) -> dict[str, Any]:
        response = await self._client._delete(f"/store/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    async def list_files(self, knowledge_base_id: int) -> dict[str, Any]:
        response = await self._client._get(f"/store/files/knowledge-base/{knowledge_base_id}")
        raise_for_status(response)
        return response.json()

    async def semantic_retrieval(self, **params: Any) -> dict[str, Any]:
        response = await self._client._post(
            "/store/knowledge-base/semantic-retrieval",
            json=params,
        )
        raise_for_status(response)
        return response.json()
