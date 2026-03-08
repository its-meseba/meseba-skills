---
name: qgit
description: Quick git add, commit, and push in one shot. Use when the user says "git add commit push", "qgit", "commit and push", "push this", "ship it", or any variation of wanting to stage, commit, and push changes without lengthy back-and-forth. Also triggers on "/qgit". This skill is about speed — get it done, report the result, move on.
---

# qgit — Quick Git Ship

Stage, commit, and push in one fluid motion. No unnecessary output, no hand-holding.

## Process

### 1. Gather context (parallel)

Run these three commands simultaneously:

- `git status` — see what's changed and untracked (never use `-uall`)
- `git diff --stat` — summary of staged + unstaged changes
- `git log --oneline -5` — recent commit style reference

### 2. Stage files

- Add changed and relevant untracked files by name — not `git add .` or `git add -A`
- Skip files that look like secrets (`.env`, credentials, tokens)
- If nothing to commit, say so and stop

### 3. Commit

Write a concise commit message that matches the repo's existing style (from the log). Focus on the "why" not the "what". Use a HEREDOC for formatting:

```bash
git commit -m "$(cat <<'EOF'
Your message here

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### 4. Push

```bash
git push
```

If there's no upstream, use `git push -u origin <branch>`.

### 5. Report

One line: the commit hash, branch, and what was pushed. Done.

## Commands

| Command | Purpose |
|---------|---------|
| `/qgit` | Stage, commit, and push in one shot |
| `/qgit:help` | Show help — what qgit does and how to use it |

## Help (`/qgit:help`)

When this sub-command is invoked, present the following to the user:

---

### qgit — Quick Git Ship

Stage, commit, and push in one fluid motion. One command, minimal output.

#### What it does

1. **Gathers context** — runs `git status`, `git diff --stat`, and `git log --oneline -5` in parallel
2. **Stages files** — adds changed and relevant untracked files by name (never `git add .`)
3. **Commits** — writes a concise commit message matching the repo's existing style, with co-author attribution
4. **Pushes** — pushes to remote (sets upstream if needed)
5. **Reports** — one line: commit hash, branch, what was pushed

#### Usage

```
/qgit
```

That's it. No arguments needed. Just say `/qgit`, "commit and push", "ship it", or "push this".

#### Safety rules

- Never amends — always creates new commits
- Never force pushes
- Never skips hooks (`--no-verify`)
- Skips files that look like secrets (`.env`, credentials)
- If push fails due to remote changes: informs you instead of auto-rebasing

---

## Rules

- Never amend unless explicitly asked — always create new commits
- Never force push
- Never skip hooks (`--no-verify`)
- If a pre-commit hook fails: fix the issue, re-stage, create a NEW commit (don't amend)
- If push fails due to remote changes: inform the user, don't auto-rebase
- Keep all output minimal — the user chose qgit because they want speed, not commentary
