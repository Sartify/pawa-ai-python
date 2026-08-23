from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import raise_for_status
from pawa_ai.models.models import Model, ModelList

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class ModelsResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def list(
        self,
        *,
        raw: bool = False,
        id: int | None = None,
        search: str | None = None,
        model_type: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> ModelList | dict[str, Any]:
        params = {
            "id": id,
            "search": search,
            "modelType": model_type,
            "page": page,
            "limit": limit,
        }
        response = self._client._get(
            "/models",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        return ModelList.from_dict(payload)

    def retrieve(self, model_id: int, *, raw: bool = False) -> Model | dict[str, Any]:
        response = self._client._get(f"/models/{model_id}")
        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        data = payload.get("data")
        if isinstance(data, dict):
            return Model.from_dict(data)
        return Model.from_dict(payload)


class AsyncModelsResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def list(
        self,
        *,
        raw: bool = False,
        id: int | None = None,
        search: str | None = None,
        model_type: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> ModelList | dict[str, Any]:
        params = {
            "id": id,
            "search": search,
            "modelType": model_type,
            "page": page,
            "limit": limit,
        }
        response = await self._client._get(
            "/models",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        return ModelList.from_dict(payload)

    async def retrieve(self, model_id: int, *, raw: bool = False) -> Model | dict[str, Any]:
        response = await self._client._get(f"/models/{model_id}")
        raise_for_status(response)
        payload = response.json()
        if raw:
            return payload
        data = payload.get("data")
        if isinstance(data, dict):
            return Model.from_dict(data)
        return Model.from_dict(payload)
