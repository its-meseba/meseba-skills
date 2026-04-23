#!/usr/bin/env python3
"""
extract_user_messages.py — Sandbox-safe JSONL user-message extractor.

Embed this in a Wave-1 research agent's ctx_execute block. Reads every
.jsonl file in a project directory and prints the first N user messages
per session, sorted by file mtime. Only the user's INTENT prompts are
extracted — assistant responses and tool results are filtered out.

Why this exists: session .jsonl files are huge (often multi-MB each).
Reading them directly would flood any context window. Running this
inside a sandbox and printing only the distilled output gives an agent
just enough signal (user intent per session) without the noise of full
transcripts.

Usage:
    python3 extract_user_messages.py <project-dir> [--per-session N] [--max-recent N]

Arguments:
    project-dir    Path to a project dir containing *.jsonl files
    --per-session  How many user messages to keep per session (default 12)
    --max-recent   Only process the N most-recently-modified jsonl files
                   (default 0 = all files)
    --truncate     Max chars per user message (default 400)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def extract_from_session(
    path: Path, per_session: int, truncate: int
) -> list[str]:
    """Pull first N user prompts from a single jsonl session file."""
    messages: list[str] = []
    try:
        with path.open(encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "user":
                    continue
                content = obj.get("message", {}).get("content")
                # Skip structured content (tool results); only keep string prompts
                if not isinstance(content, str):
                    continue
                # Skip giant pasted blobs — usually not user intent
                if len(content) > 2000:
                    continue
                messages.append(content[:truncate])
                if len(messages) >= per_session:
                    break
    except OSError as exc:
        print(f"  [skip] {path.name}: {exc}", file=sys.stderr)
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir")
    parser.add_argument("--per-session", type=int, default=12)
    parser.add_argument("--max-recent", type=int, default=0)
    parser.add_argument("--truncate", type=int, default=400)
    args = parser.parse_args()

    root = Path(os.path.expanduser(args.project_dir))
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    jsonl_files = sorted(
        (p for p in root.glob("*.jsonl") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
    )
    if args.max_recent > 0:
        jsonl_files = jsonl_files[-args.max_recent:]

    print(f"=== {root.name} ({len(jsonl_files)} sessions) ===\n")
    for f in jsonl_files:
        msgs = extract_from_session(f, args.per_session, args.truncate)
        if not msgs:
            continue
        mtime = f.stat().st_mtime
        print(f"--- {f.name} (mtime {mtime:.0f}) ---")
        for m in msgs:
            snippet = m.replace("\n", " ")[:200]
            print(f"- {snippet}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
