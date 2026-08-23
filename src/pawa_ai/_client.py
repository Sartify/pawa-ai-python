from __future__ import annotations

import os
from typing import Any

import httpx

from pawa_ai._exceptions import AuthenticationError
from pawa_ai._retry import RetryConfig, async_request_with_retry, request_with_retry
from pawa_ai.resources.agents import AgentsResource, AsyncAgentsResource
from pawa_ai.resources.chat import AsyncChatResource, ChatResource
from pawa_ai.resources.documents import AsyncDocumentsResource, DocumentsResource
from pawa_ai.resources.models import AsyncModelsResource, ModelsResource
from pawa_ai.resources.storage import AsyncStorageResource, StorageResource
from pawa_ai.resources.transcribe import AsyncTranscribeResource, TranscribeResource
from pawa_ai.resources.vectors import AsyncVectorsResource, VectorsResource
from pawa_ai.resources.voice import AsyncVoiceResource, VoiceResource

DEFAULT_BASE_URL = "https://api.pawa-ai.com/v1"
DEFAULT_TIMEOUT = 60.0


def _resolve_api_key(explicit_key: str | None) -> str:
    api_key = explicit_key or os.environ.get("PAWA_AI_API_KEY")
    if not api_key:
        raise AuthenticationError(
            "Missing API key. Pass api_key=... or set the PAWA_AI_API_KEY environment variable.",
            status_code=401,
        )
    return api_key


class PawaAI:
    """Synchronous Pawa AI API client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 2,
        retry_config: RetryConfig | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.api_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig(max_retries=max_retries)
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.Client(timeout=timeout)

        self.chat = ChatResource(self)
        self.models = ModelsResource(self)
        self.voice = VoiceResource(self)
        self.vectors = VectorsResource(self)
        self.documents = DocumentsResource(self)
        self.agents = AgentsResource(self)
        self.storage = StorageResource(self)
        self.transcribe = TranscribeResource(self)

    def _headers(self, *, accept: str | None = None) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if accept:
            headers["Accept"] = accept
        return headers

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        accept: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers = {**self._headers(accept=accept), **headers}
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")

        return request_with_retry(
            self._http_client,
            method,
            self._url(path),
            headers=headers,
            timeout=self.timeout,
            retry_config=self.retry_config,
            **kwargs,
        )

    def _get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def _post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("POST", path, **kwargs)

    def _put(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("PUT", path, **kwargs)

    def _delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("DELETE", path, **kwargs)

    def close(self) -> None:
        if self._owns_client:
            self._http_client.close()

    def __enter__(self) -> PawaAI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncPawaAI:
    """Asynchronous Pawa AI API client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 2,
        retry_config: RetryConfig | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_key = _resolve_api_key(api_key)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig(max_retries=max_retries)
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(timeout=timeout)

        self.chat = AsyncChatResource(self)
        self.models = AsyncModelsResource(self)
        self.voice = AsyncVoiceResource(self)
        self.vectors = AsyncVectorsResource(self)
        self.documents = AsyncDocumentsResource(self)
        self.agents = AsyncAgentsResource(self)
        self.storage = AsyncStorageResource(self)
        self.transcribe = AsyncTranscribeResource(self)

    def _headers(self, *, accept: str | None = None) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if accept:
            headers["Accept"] = accept
        return headers

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def _request(
        self,
        method: str,
        path: str,
        *,
        accept: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers = {**self._headers(accept=accept), **headers}
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")

        return await async_request_with_retry(
            self._http_client,
            method,
            self._url(path),
            headers=headers,
            timeout=self.timeout,
            retry_config=self.retry_config,
            **kwargs,
        )

    async def _get(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("GET", path, **kwargs)

    async def _post(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("POST", path, **kwargs)

    async def _put(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("PUT", path, **kwargs)

    async def _delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("DELETE", path, **kwargs)

    async def close(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> AsyncPawaAI:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
