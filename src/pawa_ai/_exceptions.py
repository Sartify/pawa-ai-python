from __future__ import annotations

from typing import Any


class PawaAIError(Exception):
    """Base exception for all Pawa AI SDK errors."""


class APIError(PawaAIError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, *, body: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.body = body


class APIConnectionError(PawaAIError):
    """Raised when a request fails due to a network or connection issue."""


class APIStatusError(APIError):
    """Raised when the API returns a non-success HTTP status code."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: Any | None = None,
    ) -> None:
        super().__init__(message, body=body)
        self.status_code = status_code


class AuthenticationError(APIStatusError):
    """Raised when authentication fails (HTTP 401)."""


class BadRequestError(APIStatusError):
    """Raised when the request is invalid (HTTP 400)."""


class NotFoundError(APIStatusError):
    """Raised when a resource is not found (HTTP 404)."""


class RateLimitError(APIStatusError):
    """Raised when rate limits are exceeded (HTTP 429)."""
