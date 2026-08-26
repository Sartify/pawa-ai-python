# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `client.chat.create` and `client.agents.chat.create` always return the API JSON as a `dict` (no `raw=True` / `.raw`)
- `stream.collect()` returns a dict in the same shape as a non-streaming chat response

## [0.2.0] - 2026-08-23

First public release on [PyPI](https://pypi.org/project/pawa-ai/).

### Added

- Sync client (`PawaAI`) and async client (`AsyncPawaAI`)
- Chat completions with streaming helpers (`ChatCompletionStream`, `text_deltas`, `collect_text`)
- Voice: text-to-speech and speech-to-text
- Embeddings, document parsing, agents, knowledge base, and transcribe APIs
- Typed response models (`ChatCompletion`, `EmbeddingResponse`, `ModelList`, etc.)
- Retry/backoff via `RetryConfig`
- GitHub Actions CI and PyPI publish workflow with Trusted Publishing

### Install

```bash
pip install pawa-ai
```

[0.2.0]: https://github.com/Sartify/pawa-ai-python/releases/tag/v0.2.0
