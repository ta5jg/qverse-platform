#!/usr/bin/env python3
"""Q-Verse MCP bridge scaffold.

This file is a lightweight starting point for exposing Q-Verse Agent API
as a tool-compatible bridge for MCP-style clients.
"""
import json
import os
import sys
import urllib.request

ENDPOINT = os.getenv("QVERSE_API_URL", "https://api.q-verse.io/agents/chat")


def ask_qverse(message: str, context=None):
    payload = {
        "message": message,
        "source": "mcp",
        "user_id": os.getenv("USER", "mcp-user"),
        "username": os.getenv("USER", "mcp-user"),
        "context": context or {},
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) or "Hello Q-Verse from MCP"
    print(json.dumps(ask_qverse(message), indent=2, ensure_ascii=False))
