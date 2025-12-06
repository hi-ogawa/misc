#!/usr/bin/env python3
"""
AnkiConnect CLI wrapper.

Usage:
    python scripts/anki.py deckNames
    python scripts/anki.py findCards --params '{"query": "deck:Korean::TOPIK1"}'
    python scripts/anki.py cardsInfo --params '{"cards": [123, 456]}'
    python scripts/anki.py --url http://localhost:8765 deckNames
"""

import argparse
import json
import sys
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="AnkiConnect CLI wrapper")
    parser.add_argument("action", help="AnkiConnect action name")
    parser.add_argument("--params", default="{}", help="JSON params (default: {})")
    parser.add_argument("--url", default="http://localhost:8765", help="AnkiConnect URL")

    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON params: {e}", file=sys.stderr)
        return 1

    payload = {
        "action": args.action,
        "version": 6,
        "params": params
    }

    try:
        req = urllib.request.Request(
            args.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    print(json.dumps(result["result"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
