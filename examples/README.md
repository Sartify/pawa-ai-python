# Examples

Runnable examples for the [pawa-ai](https://pypi.org/project/pawa-ai/) package.

## 1. Install

```bash
pip install pawa-ai
```

Or install from source while developing this repo:

```bash
pip install -e ".[dev]"
```

## 2. Set your API key

Get a key from the [Pawa AI Builders Dashboard](https://builder.pawa-ai.com/dashboard?page=keys).

```bash
export PAWA_AI_API_KEY="your_api_key_here"
```

Or pass it in code:

```python
from pawa_ai import PawaAI

client = PawaAI(api_key="your_api_key_here")
```

## 3. Run the examples

```bash
python examples/getting_started.py
```

This script runs:

| Example | What you get back |
|---------|-------------------|
| Chat | API JSON `dict` (`success`, `message`, `data`) |
| Streaming | Token deltas printed live, then full dict via `.collect()` |
| Embeddings | `EmbeddingResponse` with `.embeddings` (list of vectors) |
| Models | `ModelList` with `.models` |
| Error handling | Catches `AuthenticationError`, `RateLimitError`, etc. |
| Async chat | Same as chat, using `AsyncPawaAI` |

## 4. Minimal chat example

```python
from pawa_ai import PawaAI

client = PawaAI()

response = client.chat.create(
    model="pawa-v1-ember-20240924",
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Hello!"}],
        }
    ],
)

print(response["data"]["request"][0]["message"]["content"])
```

## 5. More capabilities

See the [main README](../README.md) for text-to-speech, speech-to-text, documents, agents, and knowledge base usage.

## Links

- [Pawa AI Docs](https://docs.pawa-ai.com)
- [API Reference](https://docs.pawa-ai.com/api-reference/introduction)
