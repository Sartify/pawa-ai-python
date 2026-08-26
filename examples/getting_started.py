#!/usr/bin/env python3
"""
Pawa AI Python SDK — getting started examples.

Install:
    pip install pawa-ai

Set your API key:
    export PAWA_AI_API_KEY="your_api_key_here"

Run:
    python examples/getting_started.py
"""

from __future__ import annotations

import asyncio
import os
import sys


def require_api_key() -> str:
    api_key = os.environ.get("PAWA_AI_API_KEY")
    if not api_key:
        print("Error: set PAWA_AI_API_KEY before running this script.", file=sys.stderr)
        print('  export PAWA_AI_API_KEY="your_api_key_here"', file=sys.stderr)
        sys.exit(1)
    return api_key


def example_chat() -> None:
    """Basic chat completion — returns the API JSON as a dict."""
    from pawa_ai import PawaAI

    client = PawaAI()

    response = client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a helpful assistant for developers in Africa.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello! How can I use AI in my app?"}
                ],
            },
        ],
        stream=False,
    )

    reply = response["data"]["request"][0]["message"]["content"]
    usage = response["data"].get("usage") or {}

    print("=== Chat completion ===")
    print(f"Success: {response['success']}")
    print(f"Model:   {response['data'].get('model')}")
    print(f"Reply:   {reply}")
    if usage:
        print(f"Tokens:  in={usage.get('tokens_in')}, out={usage.get('tokens_out')}")
    print()


def example_streaming() -> None:
    """Stream chat tokens as they arrive, then collect the full reply."""
    from pawa_ai import PawaAI

    client = PawaAI()

    print("=== Streaming chat ===")
    print("Reply:   ", end="", flush=True)

    with client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "Explain RAG in one short paragraph."}],
            }
        ],
        stream=True,
    ) as stream:
        for delta in stream.text_deltas():
            print(delta, end="", flush=True)

        print()
        collected = stream.collect()
        reply = collected["data"]["request"][0]["message"]["content"]
        print(f"Collected: {reply[:80]}...")
    print()


def example_embeddings() -> None:
    """Create embeddings for a list of sentences."""
    from pawa_ai import PawaAI

    client = PawaAI()

    response = client.vectors.create(
        model="pawa-embeddings-v1-20241001",
        sentences=["Embed this sentence.", "And this one too."],
        lang="multi",
    )

    print("=== Embeddings ===")
    print(f"Success:     {response.success}")
    print(f"Count:       {len(response.embeddings)} vectors")
    if response.embeddings:
        print(f"Dimensions:  {len(response.embeddings[0])}")
    print()


def example_list_models() -> None:
    """List available models on the platform."""
    from pawa_ai import PawaAI

    client = PawaAI()

    models = client.models.list(limit=5)

    print("=== Models ===")
    print(f"Success: {models.success}")
    for model in models.models[:5]:
        name = model.name or "unknown"
        model_type = model.model_type or "unknown"
        print(f"  - {name} ({model_type})")
    print()


def example_error_handling() -> None:
    """Handle common API errors."""
    from pawa_ai import AuthenticationError, PawaAI, RateLimitError

    client = PawaAI()

    try:
        client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[],  # invalid — triggers a 400 from the API
        )
    except AuthenticationError as exc:
        print(f"Auth error ({exc.status_code}): {exc.message}")
    except RateLimitError as exc:
        print(f"Rate limited ({exc.status_code}): {exc.message}")
    except Exception as exc:
        print(f"Expected validation error: {exc.__class__.__name__}: {exc}")
    print()


async def example_async_chat() -> None:
    """Async chat completion."""
    from pawa_ai import AsyncPawaAI

    async with AsyncPawaAI() as client:
        response = await client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[
                {"role": "user", "content": [{"type": "text", "text": "Habari yako?"}]}
            ],
        )

    print("=== Async chat ===")
    print(f"Reply: {response['data']['request'][0]['message']['content']}")
    print()


def main() -> None:
    require_api_key()

    print("Pawa AI Python SDK examples\n")

    example_chat()
    example_streaming()
    example_embeddings()
    example_list_models()
    example_error_handling()

    asyncio.run(example_async_chat())

    print("Done.")


if __name__ == "__main__":
    main()
