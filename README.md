# Pawa AI Python SDK

[![CI](https://github.com/Sartify/pawa-ai-python/actions/workflows/ci.yml/badge.svg)](https://github.com/Sartify/pawa-ai-python/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/pawa-ai.svg)](https://pypi.org/project/pawa-ai/)
[![Python versions](https://img.shields.io/pypi/pyversions/pawa-ai.svg)](https://pypi.org/project/pawa-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official Python library for the [Pawa AI API](https://docs.pawa-ai.com).

Pawa AI provides African-built small language models for chat, voice, embeddings, document parsing, agents, and knowledge bases.

## Installation

```bash
pip install pawa-ai
```

## Quickstart

Set your API key:

```bash
export PAWA_AI_API_KEY="your_api_key_here"
```

Get your key from the [Builders Dashboard](https://builder.pawa-ai.com/dashboard?page=keys).

See **[examples/](examples/)** for a full walkthrough from `pip install` to API responses.

### Chat

```python
from pawa_ai import PawaAI

client = PawaAI()

response = client.chat.create(
    model="pawa-v1-ember-20240924",
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Hello! How can I use AI in my app?"}],
        }
    ],
    stream=False,
)

# Always a dict matching the API JSON
print(response["success"])
print(response["data"]["request"][0]["message"]["content"])
print(response["data"].get("usage"))
```

### Streaming

```python
with client.chat.create(
    model="pawa-v1-ember-20240924",
    messages=[
        {"role": "user", "content": [{"type": "text", "text": "Explain RAG in simple terms"}]}
    ],
    stream=True,
) as stream:
    for delta in stream.text_deltas():
        print(delta, end="", flush=True)

    # Or collect the full response after streaming
    completion = stream.collect()
    print(completion["data"]["request"][0]["message"]["content"])
```

Async streaming:

```python
stream = await client.chat.create(..., stream=True)
text = await stream.collect_text()
```

### Text-to-Speech

```python
audio = client.voice.text_to_speech.create(
    model="pawa-tts-v1-20250704",
    text="Hello, this is Pawa AI speaking!",
    voice="liora",
)

with open("output.mp3", "wb") as f:
    f.write(audio)
```

### Embeddings

```python
response = client.vectors.create(
    model="pawa-embeddings-v1-20241001",
    sentences=["Embed this sentence.", "And this one too."],
    lang="multi",
)

embeddings = response.embeddings
```

### Retries with exponential backoff

```python
from pawa_ai import PawaAI, RetryConfig

client = PawaAI(
    retry_config=RetryConfig(
        max_retries=3,
        initial_delay=0.5,
        max_delay=8.0,
        exponential_base=2.0,
        jitter=0.1,
    )
)
```

Retries automatically apply to rate limits (429), server errors (500/502/503/504), and connection failures. The SDK respects `Retry-After` response headers when present.

### Async

```python
import asyncio
from pawa_ai import AsyncPawaAI

async def main():
    async with AsyncPawaAI() as client:
        response = await client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[
                {"role": "user", "content": [{"type": "text", "text": "Habari yako?"}]}
            ],
        )
        print(response["data"]["request"][0]["message"]["content"])

asyncio.run(main())
```

## API coverage

| Resource | Methods |
|----------|---------|
| `client.chat` | `create`, `completions` |
| `client.models` | `list`, `retrieve` |
| `client.voice.text_to_speech` | `create` |
| `client.voice.speech_to_text` | `create`, `transcribe` |
| `client.vectors` | `create`, `embeddings` |
| `client.documents` | `parse` |
| `client.agents` | `create`, `update`, `delete`, `list`, `retrieve` |
| `client.agents.chat` | `create` |
| `client.storage.knowledge_base` | CRUD, `list_files`, `semantic_retrieval` |
| `client.transcribe.workspaces` | CRUD, transcription management |

## Error handling

```python
from pawa_ai import PawaAI, AuthenticationError, RateLimitError

client = PawaAI()

try:
    response = client.chat.create(model="pawa-v1-ember-20240924", messages=[...])
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except RateLimitError as e:
    print(f"Rate limited: {e.status_code}")
```

## Documentation

- [Pawa AI Docs](https://docs.pawa-ai.com)
- [API Reference](https://docs.pawa-ai.com/api-reference/introduction)
- [Quickstart Guide](https://docs.pawa-ai.com/get-started/quickstart)

## License

MIT
