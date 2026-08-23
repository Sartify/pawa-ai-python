from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from pawa_ai._exceptions import APIConnectionError


@dataclass
class RetryConfig:
    """Configuration for request retries with exponential backoff."""

    max_retries: int = 2
    initial_delay: float = 0.5
    max_delay: float = 8.0
    exponential_base: float = 2.0
    jitter: float = 0.1
    retry_status_codes: frozenset[int] = field(
        default_factory=lambda: frozenset({429, 500, 502, 503, 504})
    )

    def compute_delay(self, attempt: int, *, retry_after: float | None = None) -> float:
        if retry_after is not None:
            return retry_after

        delay = min(self.initial_delay * (self.exponential_base**attempt), self.max_delay)
        if self.jitter > 0:
            delay += random.uniform(0, self.jitter * delay)
        return delay


def _parse_retry_after(response: httpx.Response) -> float | None:
    retry_after = response.headers.get("Retry-After")
    if not retry_after:
        return None

    try:
        return float(retry_after)
    except ValueError:
        pass

    try:
        retry_date = parsedate_to_datetime(retry_after)
        if retry_date.tzinfo is None:
            return None
        return max(0.0, (retry_date.timestamp() - time.time()))
    except (TypeError, ValueError, OverflowError):
        return None


def _should_retry(response: httpx.Response, attempt: int, config: RetryConfig) -> bool:
    return attempt < config.max_retries and response.status_code in config.retry_status_codes


def request_with_retry(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    retry_config: RetryConfig | None = None,
    **kwargs: Any,
) -> httpx.Response:
    config = retry_config or RetryConfig()
    last_error: Exception | None = None

    for attempt in range(config.max_retries + 1):
        try:
            response = client.request(method, url, **kwargs)
            if _should_retry(response, attempt, config):
                delay = config.compute_delay(attempt, retry_after=_parse_retry_after(response))
                response.close()
                time.sleep(delay)
                continue
            return response
        except httpx.RequestError as exc:
            last_error = exc
            if attempt >= config.max_retries:
                break
            delay = config.compute_delay(attempt)
            time.sleep(delay)

    raise APIConnectionError(str(last_error) if last_error else "Request failed")


async def async_request_with_retry(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    *,
    retry_config: RetryConfig | None = None,
    **kwargs: Any,
) -> httpx.Response:
    config = retry_config or RetryConfig()
    last_error: Exception | None = None

    for attempt in range(config.max_retries + 1):
        try:
            response = await client.request(method, url, **kwargs)
            if _should_retry(response, attempt, config):
                delay = config.compute_delay(attempt, retry_after=_parse_retry_after(response))
                await response.aclose()
                await asyncio.sleep(delay)
                continue
            return response
        except httpx.RequestError as exc:
            last_error = exc
            if attempt >= config.max_retries:
                break
            delay = config.compute_delay(attempt)
            await asyncio.sleep(delay)

    raise APIConnectionError(str(last_error) if last_error else "Request failed")
