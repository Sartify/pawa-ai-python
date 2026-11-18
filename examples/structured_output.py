#!/usr/bin/env python3
"""
Pawa AI Python SDK — Structured Output Example.

Demonstrates requesting structured output conforming to a specified JSON Schema
using the response_format parameter.

Run:
    python examples/structured_output.py
"""

from __future__ import annotations

import json
import os
import sys

from pawa_ai import PawaAI
from pawa_ai.types import ResponseFormat


def require_api_key() -> str:
    api_key = os.environ.get("PAWA_AI_API_KEY")
    if not api_key:
        print("Error: set PAWA_AI_API_KEY before running this script.", file=sys.stderr)
        print('  export PAWA_AI_API_KEY="your_api_key_here"', file=sys.stderr)
        sys.exit(1)
    return api_key


def main() -> None:
    require_api_key()
    client = PawaAI()

    # Define schema for the desired structured output
    response_format: ResponseFormat = {
        "type": "json_schema",
        "json_schema": {
            "name": "book_info",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "published_year": {"type": "integer"},
                    "genres": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "summary": {"type": "string"},
                },
                "required": ["title", "author", "published_year", "genres", "summary"],
                "additionalProperties": False,
            },
        },
    }

    prompt = (
        "Provide information about the classic novel 'Things Fall Apart' "
        "by Chinua Achebe in structured format."
    )
    print("=== Requesting Structured Output ===")
    response = client.chat.create(
        model="pawa-v1-ember-20240924",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
        response_format=response_format,
    )

    content = response["data"]["request"][0]["message"]["content"]
    print("Raw assistant message:")
    print(content)

    print("\nParsed JSON:")
    try:
        data = json.loads(content)
        print(f"Title:          {data.get('title')}")
        print(f"Author:         {data.get('author')}")
        print(f"Published Year: {data.get('published_year')}")
        print(f"Genres:         {', '.join(data.get('genres', []))}")
        print(f"Summary:        {data.get('summary')}")
    except json.JSONDecodeError:
        print("Model returned non-JSON text:", content)


if __name__ == "__main__":
    main()
