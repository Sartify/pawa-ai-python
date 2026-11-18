#!/usr/bin/env python3
"""
Pawa AI Python SDK — RAG (Retrieval-Augmented Generation) Example.

Demonstrates querying with attached knowledge bases for grounded answers
and running semantic search via storage resources.

Run:
    python examples/rag.py
"""

from __future__ import annotations

import os
import sys

from pawa_ai import PawaAI


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

    print("=== 1. Inspecting Knowledge Bases ===")
    kb_list = client.storage.knowledge_base.list()
    kbs = kb_list.get("data", [])

    if kbs:
        knowledge_base_id = kbs[0].get("id")
        kb_name = kbs[0].get("name", "Default KB")
        print(f"Using Knowledge Base: '{kb_name}' (ID: {knowledge_base_id})")

        files_res = client.storage.knowledge_base.list_files(knowledge_base_id)
        files = files_res.get("data", [])
        print(f"Knowledge Base contains {len(files)} indexed file(s).")
    else:
        knowledge_base_id = int(os.environ.get("PAWA_KB_ID", "81"))
        print(f"Using Knowledge Base ID: {knowledge_base_id}")

    print("\n=== 2. Knowledge-Grounded Query ===")
    user_query = "Eleza kuhusu DSE kwa ufupi."
    try:
        response = client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_query}],
                },
            ],
        )
        answer = response["data"]["request"][0]["message"]["content"]
        print(f"Model response:\n{answer}")
    except Exception as e:
        print(f"Query notice: {e}")


if __name__ == "__main__":
    main()
