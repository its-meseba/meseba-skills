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

### 5. Update Linear issues (optional)

If the user provided Linear issue IDs or URLs alongside `/qgit`, post activity comments automatically.

**Accepted formats:**
- Issue IDs: `JOY-1534`, `JOY-1535`
- Full URLs: `https://linear.app/joyolabs/issue/JOY-1534/add-thumbs-up-down-reasons-table`
- Mixed: `JOY-1534 https://linear.app/.../JOY-1535/...`

**URL parsing:** Extract the issue identifier (e.g., `JOY-1534`) from the URL path segment after `/issue/`.

**Process:**
1. For each issue, use `get_issue` (search by identifier like `JOY-1534`) to get the issue ID
2. Analyze the commits being pushed — understand what was done from diffs and commit messages
3. Generate an **implementation summary** comment for each issue:
   - `## Implementation Complete ✅` header
   - `### What was done` — bullet list of changes relevant to that issue
   - `### Key files` — list of changed files with brief descriptions
   - `### Branch` — branch name and commit hash
4. Post as a comment on each issue using `save_comment` — **no confirmation needed**, just do it

This is **not the default** — only triggered when issue IDs/URLs are explicitly provided.

### 6. Report

One line: the commit hash, branch, and what was pushed. If Linear issues were updated, mention that too. Done.

## Commands

| Command | Purpose |
|---------|---------|
| `/qgit` | Stage, commit, and push in one shot |
| `/qgit JOY-123` | Stage, commit, push + post activity summary on Linear issue |
| `/qgit JOY-123 JOY-456` | Same, but updates multiple Linear issues |
| `/qgit https://linear.app/.../JOY-123/...` | Same, but accepts full Linear URLs |
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
/qgit                                              # just ship it
/qgit JOY-123                                      # ship + update Linear issue
/qgit JOY-123 JOY-456                              # ship + update multiple issues
/qgit https://linear.app/.../issue/JOY-123/...     # ship + update via Linear URL
```

Just say `/qgit`, "commit and push", "ship it", or "push this". Optionally pass Linear issue IDs or URLs to post an implementation summary as a comment.

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
