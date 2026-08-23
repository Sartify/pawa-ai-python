from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import build_multipart_files, raise_for_status

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class DocumentsResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def parse(
        self,
        *,
        documents: list[str | bytes | tuple[str, bytes, str | None]],
        model: str,
    ) -> dict[str, Any]:
        data = {"model": model}
        files = build_multipart_files("documents", documents)
        response = self._client._post("/documents/parse", data=data, files=files)
        raise_for_status(response)
        return response.json()


class AsyncDocumentsResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def parse(
        self,
        *,
        documents: list[str | bytes | tuple[str, bytes, str | None]],
        model: str,
    ) -> dict[str, Any]:
        data = {"model": model}
        files = build_multipart_files("documents", documents)
        response = await self._client._post("/documents/parse", data=data, files=files)
        raise_for_status(response)
        return response.json()
