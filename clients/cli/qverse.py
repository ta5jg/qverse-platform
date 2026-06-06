#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict

try:
    import requests
except ImportError:
    print("Missing dependency: requests. Install with: pip install requests", file=sys.stderr)
    raise

DEFAULT_ENDPOINT = os.getenv("QVERSE_API_URL", "https://api.q-verse.io/agents/chat")


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            context = {"raw_context": args.context}
    return {
        "message": args.message,
        "source": args.source,
        "user_id": args.user_id,
        "username": args.username,
        "context": context,
    }


def main():
    parser = argparse.ArgumentParser(description="Q-Verse CLI Client V10.1+")
    parser.add_argument("message", help="Message to send to Q-Verse Agent")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Q-Verse chat endpoint")
    parser.add_argument("--source", default="cli", help="Client source name")
    parser.add_argument("--user-id", default=os.getenv("USER", "local-user"), help="User id")
    parser.add_argument("--username", default=os.getenv("USER", "local-user"), help="Username")
    parser.add_argument("--context", default="{}", help="JSON context")
    parser.add_argument("--json", action="store_true", help="Print full JSON response")
    args = parser.parse_args()

    payload = build_payload(args)
    try:
        response = requests.post(args.endpoint, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data.get("reply") or data.get("message") or json.dumps(data, ensure_ascii=False))
    except Exception as exc:
        print(f"Q-Verse request failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
