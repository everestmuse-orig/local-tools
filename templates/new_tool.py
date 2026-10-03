#!/usr/bin/env python3
"""TEMPLATE — copy me to start a new tool.

1. Copy this file to tools/mytool.py
2. Rename main()'s description, arguments, and logic
3. Run it:  python -m tools.mytool --help

Conventions (keep them so every tool feels the same):
- argparse for CLI, with --help that actually explains the tool
- --json flag for machine-readable output when it makes sense
- friendly errors: print to stderr, return 1 — never a traceback
- no API keys hardcoded; read them from environment variables
- stdlib only if possible; add third-party deps to requirements.txt
"""
import argparse
import json
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="What this tool does, in one sentence.")
    ap.add_argument("name", help="positional argument, e.g. an artist name")
    ap.add_argument("--json", action="store_true",
                    help="print machine-readable JSON")
    args = ap.parse_args(argv)

    try:
        result = {"hello": args.name}  # <-- your logic here
    except Exception as exc:  # noqa: BLE001 - friendly CLI error
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
