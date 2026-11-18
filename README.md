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

### Tools Calling (Function Calling)

Define function schemas and let models invoke tools (run `python examples/tools_calling.py` for full sample):

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather conditions for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "e.g. Dar es Salaam, Nairobi"},
                },
                "required": ["city"],
            },
        },
    }
]

response = client.chat.create(
    model="pawa-v1-blaze-20250318",
    messages=[
        {"role": "user", "content": [{"type": "text", "text": "What's the weather in Dar es Salaam?"}]}
    ],
    tools=tools,
)

message = response["data"]["request"][0]["message"]
tool_calls = message.get("tool_calls", [])
for call in tool_calls:
    print(f"Tool to invoke: {call['function']['name']}, args: {call['function']['arguments']}")
```

### RAG (Retrieval-Augmented Generation)

Ground chat completions using your existing Pawa AI Knowledge Bases (see `examples/rag_example.py`):

```python
# Ground chat responses using a knowledge base ID from your dashboard
response = client.chat.create(
    model="pawa-v1-ember-20240924",
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Eleza kuhusu hisa na huduma zake"}],
        }
    ],
    rag={
        "knowledgeBaseId": 81,  # ID of your knowledge base
        "topK": 3,
    },
)

print(response["data"]["request"][0]["message"]["content"])
```

You can also run direct semantic retrieval on knowledge bases:

```python
results = client.storage.knowledge_base.semantic_retrieval(
    query="Hisa na huduma za soko",
    knowledgeBaseId=81,
    top_k=3,
)
```

### Agentic RAG & Autonomous Agents

Configure and chat with intelligent agents equipped with tools and knowledge bases (see `examples/agentic_rag.py`):

```python
# 1. Create an agent with specific instructions and description
agent = client.agents.create(
    name="Customer Support Agent",
    description="Handles customer inquiries grounded in documentation",
    instruction="Answer queries strictly based on connected knowledge bases and policies.",
)

# 2. Chat directly with the agent
agent_chat = client.agents.chat.create(
    name="Customer Support Agent",
    description="Handles customer inquiries grounded in documentation",
    instruction="Answer queries strictly based on connected knowledge bases and policies.",
    message={"role": "user", "content": [{"type": "text", "text": "Msaada kuhusu akaunti"}]},
    model="pawa-v1-blaze-20250318",
    agents=[agent["data"]["id"]],
)
print(agent_chat["data"]["request"][0]["message"]["content"])
```

### Structured Output

Enforce strict JSON schemas in model responses (see `examples/structured_output.py`):

```python
import json

response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "contact_info",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "role": {"type": "string"},
            },
            "required": ["name", "email", "role"],
            "additionalProperties": False,
        },
    },
}

response = client.chat.create(
    model="pawa-v1-ember-20240924",
    messages=[
        {"role": "user", "content": [{"type": "text", "text": "Extract: Juma Ally, Lead Engineer at juma@example.com"}]}
    ],
    response_format=response_format,
)

content = response["data"]["request"][0]["message"]["content"]
data = json.loads(content)
print(data["name"], data["email"], data["role"])
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
