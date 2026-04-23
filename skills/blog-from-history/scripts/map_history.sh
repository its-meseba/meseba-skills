#!/usr/bin/env bash
# map_history.sh — Phase 0 terrain scan for blog-from-history
# Scans all ~/.claude* profiles and reports sizes, session counts,
# per-project activity, and memory-dir presence.
#
# Usage: bash map_history.sh
# Expected: called from inside ctx_execute so output is summarized, not streamed.

set +e

echo "=== PROFILES ==="
for d in "$HOME/.claude" "$HOME/.claude-shared" "$HOME/.claude-personal" "$HOME/.claude-work"; do
  if [ -d "$d" ]; then
    size=$(du -sh "$d" 2>/dev/null | cut -f1)
    echo "$d -> $size"
  fi
done

echo ""
echo "=== JSONL SESSION FILES PER PROFILE ==="
for d in "$HOME/.claude" "$HOME/.claude-personal" "$HOME/.claude-work" "$HOME/.claude-shared"; do
  if [ -d "$d/projects" ]; then
    count=$(find "$d/projects" -type f -name "*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
    size=$(find "$d/projects" -type f -name "*.jsonl" 2>/dev/null -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1)
    echo "$d/projects -> $count jsonl, $size"
  fi
done

echo ""
echo "=== HISTORY.JSONL LINE COUNTS ==="
for d in "$HOME/.claude" "$HOME/.claude-personal" "$HOME/.claude-work" "$HOME/.claude-shared"; do
  f="$d/history.jsonl"
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f" 2>/dev/null | tr -d ' ')
    echo "$f -> $lines lines"
  fi
done

echo ""
echo "=== TOP-LEVEL PROJECT DIRECTORIES (primary corpus) ==="
# Prefer .claude-shared since .claude etc. typically symlink there
CORPUS_ROOT="$HOME/.claude-shared/projects"
if [ ! -d "$CORPUS_ROOT" ]; then
  for alt in "$HOME/.claude-work/projects" "$HOME/.claude-personal/projects" "$HOME/.claude/projects"; do
    if [ -d "$alt" ]; then CORPUS_ROOT="$alt"; break; fi
  done
fi
echo "Using: $CORPUS_ROOT"
echo ""
echo "Project | JSONL count | Size | Has memory/ ?"
echo "--------|-------------|------|---------------"
if [ -d "$CORPUS_ROOT" ]; then
  for proj in "$CORPUS_ROOT"/*/; do
    name=$(basename "$proj")
    j=$(find "$proj" -maxdepth 1 -type f -name "*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
    s=$(du -sh "$proj" 2>/dev/null | cut -f1)
    m="no"
    [ -d "$proj/memory" ] && m="YES"
    echo "$name | $j | $s | $m"
  done
fi

echo ""
echo "=== CLAUDE DESKTOP (macOS) ==="
DSK="$HOME/Library/Application Support/Claude"
if [ -d "$DSK" ]; then
  size=$(du -sh "$DSK" 2>/dev/null | cut -f1)
  echo "$DSK -> $size (binary LevelDB — titles protobuf-locked; limited extractable content)"
else
  echo "no Claude Desktop dir found"
fi

echo ""
echo "=== SUMMARY ==="
total_jsonl=$(find "$HOME/.claude-shared/projects" -type f -name "*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
total_projects=$(ls -d "$HOME/.claude-shared/projects"/*/ 2>/dev/null | wc -l | tr -d ' ')
total_history=0
for d in "$HOME/.claude" "$HOME/.claude-personal" "$HOME/.claude-work"; do
  f="$d/history.jsonl"
  if [ -f "$f" ]; then
    total_history=$((total_history + $(wc -l < "$f" 2>/dev/null | tr -d ' ')))
  fi
done
echo "Total JSONL sessions: $total_jsonl"
echo "Total project dirs: $total_projects"
echo "Total prompt history lines: $total_history"
