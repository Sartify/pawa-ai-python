#!/usr/bin/env python3
"""
Pawa AI Python SDK — Agentic RAG Example.

Demonstrates configuring autonomous agents with attached knowledge bases
and executing agent-driven chat queries.

Run:
    python examples/agentic_rag.py
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

    print("=== 1. Listing Available Agents ===")
    agents_list = client.agents.list()
    print(f"Agents status: {agents_list.get('success')}")

    agent_id = None
    existing_agents = agents_list.get("data", [])
    if existing_agents:
        agent_id = existing_agents[0].get("id")
        agent_name = existing_agents[0].get("name", "Support Agent")
        print(f"Using existing agent '{agent_name}' (ID: {agent_id})")

    if not agent_id:
        print("Creating a new Agent with knowledge capabilities...")
        instruction = (
            "You are an intelligent support agent equipped with organization knowledge bases. "
            "Ground your answers using attached documents."
        )
        new_agent = client.agents.create(
            name="Support Research Agent",
            description="Assists users with knowledge-grounded support",
            instruction=instruction,
        )
        agent_id = new_agent.get("data", {}).get("id") or 1
        print(f"Created agent ID: {agent_id}")

    print("\n=== 2. Running Agent Chat Request ===")
    prompt = "What steps should a customer take when troubleshooting account access?"
    instruction_str = (
        "You are an intelligent support agent equipped with organization knowledge bases. "
        "Ground your answers using attached documents."
    )
    agent_response = client.agents.chat.create(
        name="Support Research Agent",
        description="Assists users with knowledge-grounded support",
        instruction=instruction_str,
        message={"role": "user", "content": [{"type": "text", "text": prompt}]},
        model="pawa-v1-blaze-20250318",
        agents=[agent_id],
    )

    reply = agent_response["data"]["request"][0]["message"]["content"]
    print(f"Agent response:\n{reply}")


if __name__ == "__main__":
    main()
