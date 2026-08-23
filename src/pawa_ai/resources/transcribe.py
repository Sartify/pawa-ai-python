from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import build_multipart_files, raise_for_status

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class TranscribeResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client
        self.workspaces = WorkspacesResource(client)


class WorkspacesResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(self, **params: Any) -> dict[str, Any]:
        response = self._client._post("/transcribe/workspace", json=params)
        raise_for_status(response)
        return response.json()

    def list(self) -> dict[str, Any]:
        response = self._client._get("/transcribe/workspace")
        raise_for_status(response)
        return response.json()

    def retrieve(self, workspace_id: int) -> dict[str, Any]:
        response = self._client._get(f"/transcribe/workspace/{workspace_id}")
        raise_for_status(response)
        return response.json()

    def update(self, workspace_id: int, **params: Any) -> dict[str, Any]:
        response = self._client._put(f"/transcribe/workspace/{workspace_id}", json=params)
        raise_for_status(response)
        return response.json()

    def delete(self, workspace_id: int) -> dict[str, Any]:
        response = self._client._delete(f"/transcribe/workspace/{workspace_id}")
        raise_for_status(response)
        return response.json()

    def upload_transcriptions(
        self,
        workspace_id: int,
        *,
        files: list[str | bytes | tuple[str, bytes, str | None]],
    ) -> dict[str, Any]:
        multipart_files = build_multipart_files("files", files)
        response = self._client._post(
            f"/transcribe/workspace/{workspace_id}/transcriptions",
            files=multipart_files,
        )
        raise_for_status(response)
        return response.json()

    def list_transcriptions(
        self,
        workspace_id: int,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        params = {"page": page, "limit": limit}
        response = self._client._get(
            f"/transcribe/workspace/{workspace_id}/transcriptions",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        return response.json()

    def update_transcription(
        self,
        workspace_id: int,
        transcription_id: int,
        **params: Any,
    ) -> dict[str, Any]:
        response = self._client._put(
            f"/transcribe/workspace/{workspace_id}/transcriptions/{transcription_id}",
            json=params,
        )
        raise_for_status(response)
        return response.json()

    def delete_transcription(self, workspace_id: int, transcription_id: int) -> dict[str, Any]:
        response = self._client._delete(
            f"/transcribe/workspace/{workspace_id}/transcriptions/{transcription_id}"
        )
        raise_for_status(response)
        return response.json()


class AsyncTranscribeResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client
        self.workspaces = AsyncWorkspacesResource(client)


class AsyncWorkspacesResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(self, **params: Any) -> dict[str, Any]:
        response = await self._client._post("/transcribe/workspace", json=params)
        raise_for_status(response)
        return response.json()

    async def list(self) -> dict[str, Any]:
        response = await self._client._get("/transcribe/workspace")
        raise_for_status(response)
        return response.json()

    async def retrieve(self, workspace_id: int) -> dict[str, Any]:
        response = await self._client._get(f"/transcribe/workspace/{workspace_id}")
        raise_for_status(response)
        return response.json()

    async def update(self, workspace_id: int, **params: Any) -> dict[str, Any]:
        response = await self._client._put(f"/transcribe/workspace/{workspace_id}", json=params)
        raise_for_status(response)
        return response.json()

    async def delete(self, workspace_id: int) -> dict[str, Any]:
        response = await self._client._delete(f"/transcribe/workspace/{workspace_id}")
        raise_for_status(response)
        return response.json()

    async def upload_transcriptions(
        self,
        workspace_id: int,
        *,
        files: list[str | bytes | tuple[str, bytes, str | None]],
    ) -> dict[str, Any]:
        multipart_files = build_multipart_files("files", files)
        response = await self._client._post(
            f"/transcribe/workspace/{workspace_id}/transcriptions",
            files=multipart_files,
        )
        raise_for_status(response)
        return response.json()

    async def list_transcriptions(
        self,
        workspace_id: int,
        *,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        params = {"page": page, "limit": limit}
        response = await self._client._get(
            f"/transcribe/workspace/{workspace_id}/transcriptions",
            params={k: v for k, v in params.items() if v is not None},
        )
        raise_for_status(response)
        return response.json()

    async def update_transcription(
        self,
        workspace_id: int,
        transcription_id: int,
        **params: Any,
    ) -> dict[str, Any]:
        response = await self._client._put(
            f"/transcribe/workspace/{workspace_id}/transcriptions/{transcription_id}",
            json=params,
        )
        raise_for_status(response)
        return response.json()

    async def delete_transcription(
        self,
        workspace_id: int,
        transcription_id: int,
    ) -> dict[str, Any]:
        response = await self._client._delete(
            f"/transcribe/workspace/{workspace_id}/transcriptions/{transcription_id}"
        )
        raise_for_status(response)
        return response.json()
