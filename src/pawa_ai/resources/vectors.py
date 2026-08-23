from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import raise_for_status
from pawa_ai.models.embeddings import EmbeddingResponse

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class VectorsResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(
        self,
        *,
        raw: bool = False,
        sentences: list[str] | None = None,
        model: str = "pawa-embeddings-v1-20241001",
        lang: str = "multi",
        input: list[str] | None = None,
    ) -> EmbeddingResponse | dict[str, Any]:
        """Create embeddings for the given sentences."""
        texts = input if input is not None else sentences
        if not texts:
            raise ValueError("Either 'sentences' or 'input' must be provided.")

        payload = {
            "model": model,
            "lang": lang,
            "sentences": texts,
        }
        response = self._client._post("/vectors/embedding", json=payload)
        raise_for_status(response)
        body = response.json()
        if raw:
            return body
        return EmbeddingResponse.from_dict(body)

    def embeddings(self, **kwargs: Any) -> EmbeddingResponse | dict[str, Any]:
        return self.create(**kwargs)


class AsyncVectorsResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(
        self,
        *,
        raw: bool = False,
        sentences: list[str] | None = None,
        model: str = "pawa-embeddings-v1-20241001",
        lang: str = "multi",
        input: list[str] | None = None,
    ) -> EmbeddingResponse | dict[str, Any]:
        texts = input if input is not None else sentences
        if not texts:
            raise ValueError("Either 'sentences' or 'input' must be provided.")

        payload = {"model": model, "lang": lang, "sentences": texts}
        response = await self._client._post("/vectors/embedding", json=payload)
        raise_for_status(response)
        body = response.json()
        if raw:
            return body
        return EmbeddingResponse.from_dict(body)

    async def embeddings(self, **kwargs: Any) -> EmbeddingResponse | dict[str, Any]:
        return await self.create(**kwargs)
