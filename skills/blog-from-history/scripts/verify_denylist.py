#!/usr/bin/env python3
"""
verify_denylist.py — Word-bounded cross-file denylist sweep.

Used in Phase 3 (on BLOG-CATEGORIES.md) and Phase 5 (across all essays).
Word-bounded means it won't false-positive on common English substrings
(e.g., "CAM" as a codename will NOT match "became" or "campaign").

Usage:
    python3 verify_denylist.py <file-or-glob> [<file-or-glob> ...] <denylist-path>

Examples:
    python3 verify_denylist.py BLOG-CATEGORIES.md .denylist.txt
    python3 verify_denylist.py 'essays/*.md' .denylist.txt

The last argument is always the denylist file (one term per line, blanks
and lines starting with '#' ignored).

Exit code:
    0  = zero hits across all files
    1  = one or more hits found (printed to stderr)
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path


def load_denylist(path: str) -> list[str]:
    """Read denylist file. One term per line. '#' starts a comment."""
    terms: list[str] = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        terms.append(line)
    return terms


def scan_file(file_path: Path, terms: list[str]) -> list[tuple[str, int, str]]:
    """Return list of (term, line_number, line_content) hits for one file."""
    hits: list[tuple[str, int, str]] = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"ERROR reading {file_path}: {exc}", file=sys.stderr)
        return hits
    lines = text.splitlines()
    for term in terms:
        pattern = r"\b" + re.escape(term) + r"\b"
        rx = re.compile(pattern, re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            if rx.search(line):
                hits.append((term, idx, line.strip()[:160]))
    return hits


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    denylist_path = argv[-1]
    patterns = argv[:-1]

    try:
        terms = load_denylist(denylist_path)
    except FileNotFoundError:
        print(f"Denylist file not found: {denylist_path}", file=sys.stderr)
        return 2

    if not terms:
        print(f"Denylist {denylist_path} is empty — nothing to check.", file=sys.stderr)
        return 0

    # Expand globs
    files: list[Path] = []
    for pat in patterns:
        matched = glob.glob(pat)
        if not matched and Path(pat).exists():
            matched = [pat]
        files.extend(Path(m) for m in matched)

    if not files:
        print(f"No files matched: {patterns}", file=sys.stderr)
        return 2

    total_hits = 0
    per_file: dict[Path, list[tuple[str, int, str]]] = {}
    for f in files:
        hits = scan_file(f, terms)
        per_file[f] = hits
        total_hits += len(hits)

    # Report
    for f, hits in per_file.items():
        if not hits:
            print(f"  [{f}] CLEAN")
            continue
        print(f"  [{f}] {len(hits)} hits:")
        for term, line_no, line_content in hits:
            print(f"    L{line_no}: '{term}' — {line_content}")

    print(f"\nDenylist: {denylist_path} ({len(terms)} terms)")
    print(f"Files scanned: {len(files)}")
    print(f"Total word-bounded hits: {total_hits}")

    return 0 if total_hits == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
