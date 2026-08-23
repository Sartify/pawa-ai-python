from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pawa_ai._http import AsyncStream, Stream, build_multipart_files, raise_for_status

if TYPE_CHECKING:
    from pawa_ai._client import AsyncPawaAI, PawaAI


class VoiceResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client
        self.text_to_speech = TextToSpeechResource(client)
        self.speech_to_text = SpeechToTextResource(client)


class TextToSpeechResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(self, **params: Any) -> bytes | Stream:
        """Convert text to speech. Returns raw audio bytes or a streaming response."""
        response = self._client._post(
            "/voice/text-to-speech",
            json=params,
            stream=True,
            accept="audio/mpeg",
        )
        raise_for_status(response)
        content_type = response.headers.get("content-type", "")
        if "audio" in content_type:
            return response.content
        return Stream(response)


class SpeechToTextResource:
    def __init__(self, client: PawaAI) -> None:
        self._client = client

    def create(
        self,
        *,
        files: list[str | bytes | tuple[str, bytes, str | None]],
        model: str,
        language: str,
        is_speaker_diarization: bool = False,
        prompt: str | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {
            "model": model,
            "language": language,
            "is_speaker_diarization": str(is_speaker_diarization).lower(),
        }
        if prompt is not None:
            data["prompt"] = prompt
        if temperature is not None:
            data["temperature"] = str(temperature)

        multipart_files = build_multipart_files("files", files)
        response = self._client._post(
            "/voice/speech-to-text",
            data=data,
            files=multipart_files,
        )
        raise_for_status(response)
        return response.json()

    def transcribe(self, **kwargs: Any) -> dict[str, Any]:
        return self.create(**kwargs)


class AsyncVoiceResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client
        self.text_to_speech = AsyncTextToSpeechResource(client)
        self.speech_to_text = AsyncSpeechToTextResource(client)


class AsyncTextToSpeechResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(self, **params: Any) -> bytes | AsyncStream:
        response = await self._client._post(
            "/voice/text-to-speech",
            json=params,
            stream=True,
            accept="audio/mpeg",
        )
        raise_for_status(response)
        content_type = response.headers.get("content-type", "")
        if "audio" in content_type:
            return response.content
        return AsyncStream(response)


class AsyncSpeechToTextResource:
    def __init__(self, client: AsyncPawaAI) -> None:
        self._client = client

    async def create(
        self,
        *,
        files: list[str | bytes | tuple[str, bytes, str | None]],
        model: str,
        language: str,
        is_speaker_diarization: bool = False,
        prompt: str | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {
            "model": model,
            "language": language,
            "is_speaker_diarization": str(is_speaker_diarization).lower(),
        }
        if prompt is not None:
            data["prompt"] = prompt
        if temperature is not None:
            data["temperature"] = str(temperature)

        multipart_files = build_multipart_files("files", files)
        response = await self._client._post(
            "/voice/speech-to-text",
            data=data,
            files=multipart_files,
        )
        raise_for_status(response)
        return response.json()

    async def transcribe(self, **kwargs: Any) -> dict[str, Any]:
        return await self.create(**kwargs)
