#!/usr/bin/env python3
"""
Pawa AI Python SDK — Tools Calling Example.

Demonstrates defining a function tool, passing it to the chat completion API,
and inspecting the model's tool calls.

Run:
    python examples/tools_calling.py
"""

from __future__ import annotations

import json
import os
import sys

from pawa_ai import PawaAI
from pawa_ai.types import Tool


def require_api_key() -> str:
    api_key = os.environ.get("PAWA_AI_API_KEY")
    if not api_key:
        print("Error: set PAWA_AI_API_KEY before running this script.", file=sys.stderr)
        print('  export PAWA_AI_API_KEY="your_api_key_here"', file=sys.stderr)
        sys.exit(1)
    return api_key


def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Mock function to simulate fetching weather data."""
    return json.dumps({
        "location": location,
        "temperature": "28",
        "unit": unit,
        "condition": "Sunny",
    })


def main() -> None:
    require_api_key()
    client = PawaAI()

    # Define tools using Pawa AI schema
    tools: list[Tool] = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get current weather conditions for a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or location name, e.g. Dar es Salaam, Nairobi",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature scale unit",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is the weather like in Dar es Salaam right now?"}
            ],
        }
    ]

    print("=== Calling Chat with Tools ===")
    model_name = os.environ.get("PAWA_TOOL_MODEL", "pawa-v1-blaze-20250318")

    try:
        response = client.chat.create(
            model=model_name,
            messages=messages,
            tools=tools,
        )
    except Exception as e:
        print(f"Chat tool calling notice: {e}")
        print("Falling back to standard chat completion...")
        response = client.chat.create(
            model="pawa-v1-ember-20240924",
            messages=messages,
        )

    choice = response["data"]["request"][0]["message"]
    print(f"Assistant response: {choice.get('content')}")

    # Check if the model decided to invoke a tool
    tool_calls = choice.get("tool_calls", [])
    if tool_calls:
        print(f"\nModel requested {len(tool_calls)} tool call(s):")
        for tool_call in tool_calls:
            func = tool_call["function"]
            print(f"  Tool ID: {tool_call.get('id')}")
            print(f"  Function: {func.get('name')}")
            print(f"  Arguments: {func.get('arguments')}")

            # Execute the local function if matched
            if func.get("name") == "get_current_weather":
                args = json.loads(func.get("arguments", "{}"))
                result = get_current_weather(**args)
                print(f"  Execution result: {result}")
    else:
        print("No tool call was requested; standard text response returned.")


if __name__ == "__main__":
    main()
