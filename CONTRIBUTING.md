# Contributing to Kallavi Turk Skills

Welcome to **Kallavi Turk Skills**! 🎉

This repository is a collection of skills for the **Kallavi Turk** agentic twin — a Turkish digital twin capable of trading, investing, coding, and serving as a comprehensive digital assistant. We welcome contributions from anyone who wants to enhance the twin's capabilities and help build a robust skill ecosystem.

## Philosophy

Kallavi Turk Skills follows the **Anthropic Agent Skills open standard**, making our skills compatible across multiple AI platforms including Claude Code, OpenClaw (clawdbot/openclaw), Claude.ai, and API integrations. Our goal is to create high-quality, reusable, and well-documented skills that are:

- **Actionable**: Clear, step-by-step instructions that AI agents can follow
- **Comprehensive**: Cover trading, investing, coding, Turkish cultural context, and personal workflows
- **Bilingual**: Support both Turkish and English where relevant
- **Well-tested**: Validated with real user queries before submission
- **Standards-compliant**: Follow the Agent Skills specification strictly

Whether you're adding a new trading strategy, a Turkish market analysis tool, a coding workflow, or a personal routine, your contribution helps make Kallavi Turk more capable and useful.

## How to Add a New Skill

Follow these steps to contribute a new skill to the repository:

### 1. Fork the Repository

Fork the `its-meseba/kallavi-turk-skills` repository to your own GitHub account.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/kallavi-turk-skills.git
cd kallavi-turk-skills
```

### 3. Create a New Branch

Create a descriptive branch name for your skill:

```bash
git checkout -b add-skill-your-skill-name
```

Example: `git checkout -b add-skill-bist-stock-analyzer`

### 4. Create the Skill Folder

Create a new folder for your skill using kebab-case naming:

```bash
mkdir your-skill-name
```

**Rules**:
- Use lowercase letters only
- Separate words with hyphens (kebab-case)
- No spaces, underscores, or capital letters
- Name should be descriptive and concise (2-4 words ideal)

Examples: `bist-stock-analyzer`, `turkish-email-writer`, `crypto-portfolio-tracker`

### 5. Create the SKILL.md File

Inside your skill folder, create a `SKILL.md` file (exact casing required):

```bash
touch your-skill-name/SKILL.md
```

**Important**: The file MUST be named `SKILL.md` (not `skill.md`, `Skill.md`, or `README.md`).

### 6. Write the Skill Content

Edit `SKILL.md` with the following structure:

#### YAML Frontmatter (Required)

Start with YAML frontmatter enclosed in `---`:

```yaml
---
name: your-skill-name
description: A clear description of what the skill does and when to trigger it. Include example phrases users might say like "analyze stocks", "write email", "check portfolio", etc. Keep it under 1024 characters.
metadata:
  author: your-github-username
  version: 1.0.0
  tags:
    - relevant-tag-1
    - relevant-tag-2
---
```

**Frontmatter Requirements**:
- `name` must match your folder name exactly (kebab-case)
- `name` must NOT start with "claude" or "anthropic"
- `description` must include WHAT the skill does AND WHEN to trigger it
- `description` must be under 1024 characters
- `description` must NOT contain XML tags (`<`, `>`)
- Add relevant tags to help categorize your skill

#### Body Instructions (Required)

After the frontmatter, write clear, actionable instructions. Include:

1. **Overview**: What the skill does and why it's useful
2. **Prerequisites**: Any required setup, API keys, or accounts
3. **Step-by-Step Workflow**: Numbered steps the AI should follow
4. **User Query Examples**: 3-5 example queries with expected behaviors
5. **Error Handling**: Common errors and how to handle them
6. **Turkish/Bilingual Notes** (if applicable): Language and cultural guidance

**Tips for writing instructions**:
- Be specific and actionable (avoid vague phrases like "validate properly")
- Use numbered steps for workflows
- Include code examples where relevant
- Document error scenarios and recovery steps
- For Turkish-related skills, include language detection and bilingual support guidance

### 7. Add Optional Subdirectories (If Needed)

Depending on your skill's complexity, you may add:

- **`scripts/`**: Executable code (Python, Bash, etc.)
- **`references/`**: Detailed documentation, API guides, examples
- **`assets/`**: Templates, configuration files, sample data

Example structure:
```
your-skill-name/
├── SKILL.md
├── scripts/
│   └── api_client.py
├── references/
│   ├── api-documentation.md
│   └── examples.md
└── assets/
    └── template.json
```

**Do NOT** create a `README.md` file inside the skill folder. Use `SKILL.md` instead.

### 8. Test Your Skill Locally

Before submitting, test your skill with Claude Code or OpenClaw:

#### Testing with Claude Code:
1. Copy your skill folder to Claude Code's skill directory
2. Start Claude Code
3. Test with 3-5 different user queries
4. Verify the AI follows your instructions correctly

#### Testing with OpenClaw:
1. Place your skill in OpenClaw's skill directory
2. Run OpenClaw with your skill loaded
3. Test with various user queries
4. Check that error handling works as expected

### 9. Run the Validation Checklist

Verify your skill meets all requirements:

- [ ] File is named `SKILL.md` with exact casing
- [ ] Folder is in kebab-case (lowercase with hyphens)
- [ ] Folder name matches the `name` in frontmatter
- [ ] Frontmatter has `---` delimiters at start and end
- [ ] `name` and `description` fields are present
- [ ] Description includes WHAT and WHEN (trigger phrases)
- [ ] Description is under 1024 characters
- [ ] No XML tags in description
- [ ] Name doesn't start with "claude" or "anthropic"
- [ ] Instructions are clear, specific, and actionable
- [ ] Step-by-step workflows are included
- [ ] User query examples are documented
- [ ] Error handling is present
- [ ] Turkish/bilingual support is included (if applicable)
- [ ] No `README.md` file in skill folder
- [ ] Tested with at least 3 different user queries

### 10. Commit Your Changes

```bash
git add your-skill-name/
git commit -m "Add [your-skill-name] skill for [brief description]"
```

Example: `git commit -m "Add bist-stock-analyzer skill for Turkish market analysis"`

### 11. Push to Your Fork

```bash
git push origin add-skill-your-skill-name
```

### 12. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Write a clear PR description:
   - What the skill does
   - Which category it belongs to (Trading, Investment, Coding, etc.)
   - How you tested it
   - Any special considerations or dependencies
4. Submit the PR to the `its-meseba/kallavi-turk-skills` repository

## Skill Standards Summary

### Naming Conventions

- **Folder names**: kebab-case, lowercase, no spaces (e.g., `turkish-market-analyzer`)
- **File name**: Exactly `SKILL.md` (case-sensitive)
- **Skill name in frontmatter**: Must match folder name
- **No forbidden prefixes**: Don't start names with "claude" or "anthropic"

### Required Structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/           # Optional
├── references/        # Optional
└── assets/            # Optional
```

### Frontmatter Requirements

```yaml
---
name: skill-name              # Required: kebab-case, matches folder
description: What and when    # Required: <1024 chars, no XML tags
metadata:                     # Optional but recommended
  author: github-username
  version: 1.0.0
  tags:
    - tag1
    - tag2
---
```

### Instruction Quality

- **Specific**: "Call API endpoint `/v1/stocks/{ticker}`" not "Get the data"
- **Actionable**: Numbered steps, clear workflows
- **Examples**: Include 3-5 user query examples with expected behaviors
- **Error handling**: Document common errors and recovery steps
- **Bilingual**: For Turkish skills, include language detection and cultural context

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- **Be respectful**: Treat all contributors with respect and kindness
- **Be constructive**: Provide helpful feedback and suggestions
- **Be inclusive**: Welcome contributors of all backgrounds and skill levels
- **Stay on topic**: Keep discussions relevant to the skill or feature being developed
- **Give credit**: Acknowledge others' contributions and ideas

We do not tolerate harassment, discrimination, or abusive behavior. If you experience or witness unacceptable behavior, please report it by opening an issue or contacting the maintainers.

## Pull Request Process

1. **Fork and branch**: Create a new branch from `main` for your skill
2. **Follow standards**: Ensure your skill meets all naming and structure requirements
3. **Test thoroughly**: Test with at least 3 different user queries
4. **Document clearly**: Write a comprehensive PR description
5. **Review feedback**: Respond to reviewer comments and make requested changes
6. **Merge**: Once approved, maintainers will merge your PR

### What to Expect During Review

Reviewers will check:
- Compliance with Agent Skills standard
- Quality and clarity of instructions
- Proper error handling
- Testing evidence
- Turkish language support (if applicable)
- Code quality for any scripts

Reviews typically take 1-3 days. Please be patient and responsive to feedback.

## Style Guide

### Markdown Formatting

- Use standard Markdown syntax
- Include clear headings (`##`, `###`) for sections
- Use code blocks with language tags (```yaml, ```python, ```bash)
- Use numbered lists for step-by-step workflows
- Use bullet points for requirements or checklists

### Code Style (for scripts/)

- **Python**: Follow PEP 8, use type hints, include docstrings
- **Bash**: Use `#!/bin/bash`, include comments, handle errors with `set -e`
- **JavaScript/Node.js**: Follow standard JS conventions, use ESLint-compatible style
- **Other languages**: Follow community-standard style guides

### Bilingual Content (Turkish/English)

- **Primary language**: Instructions should be in English
- **Turkish examples**: Include Turkish user queries in examples
- **Turkish output**: Document when the skill should respond in Turkish
- **Cultural context**: Note Turkish market hours, holidays, number formats, etc.
- **Character encoding**: Always use UTF-8 for Turkish characters (ğ, ü, ş, ı, ö, ç)

Example:
```markdown
## Example User Queries

**Query**: "THYAO hissesini analiz et" (Turkish)
**Expected Behavior**: Detect Turkish input, analyze THYAO stock, respond in Turkish

**Query**: "Analyze THYAO stock" (English)
**Expected Behavior**: Analyze THYAO stock, respond in English
```

## Testing Your Skill

### Local Testing with Claude Code

1. Install Claude Code (if not already installed)
2. Copy your skill folder to the Claude Code skills directory:
   - macOS: `~/Library/Application Support/Claude/skills/`
   - Windows: `%APPDATA%/Claude/skills/`
   - Linux: `~/.config/Claude/skills/`
3. Restart Claude Code
4. Test with multiple queries:
   - Basic functionality
   - Edge cases
   - Error scenarios
   - Turkish language input (if applicable)
5. Verify the AI follows your instructions correctly

### Local Testing with OpenClaw

1. Install OpenClaw (clawdbot/openclaw)
2. Configure OpenClaw to load your skill directory
3. Run OpenClaw and test your skill
4. Check logs for any errors or unexpected behavior
5. Test compatibility with other OpenClaw features

### Testing Checklist

Before submitting your PR, verify:

- [ ] Skill works with at least 3 different user queries
- [ ] Edge cases are handled (invalid input, API failures, etc.)
- [ ] Error messages are clear and helpful
- [ ] Turkish language input works correctly (if applicable)
- [ ] Output format matches examples in SKILL.md
- [ ] No unexpected errors or crashes
- [ ] Dependencies are documented in `references/` or `scripts/`

## Skill Categories

Organize your skill into one of these categories:

- **Trading & Finance**: Real-time analysis, BIST stocks, crypto, portfolio tracking
- **Investment**: Fundamental analysis, economic indicators, real estate, long-term planning
- **Coding & Development**: Code generation, review, API clients, Turkish dev conventions
- **Digital Twin / Personal**: Routines, communication style, decision frameworks, habits
- **Document & Asset Creation**: Reports, presentations, Turkish business documents, charts
- **Workflow Automation**: Multi-step processes, MCP integrations, scheduled tasks

Mention the category in your PR description to help reviewers.

## Useful Resources

- **Anthropic Agent Skills Documentation**: [https://docs.anthropic.com/claude/docs/agent-skills](https://docs.anthropic.com/claude/docs/agent-skills)
- **This Repository's Meta-Skill**: See `create-kallavi-turk-skills/SKILL.md` for detailed guidance
- **OpenClaw Documentation**: [https://github.com/clawdbot/openclaw](https://github.com/clawdbot/openclaw)
- **Claude Code**: [https://claude.ai/code](https://claude.ai/code)
- **BIST (Istanbul Stock Exchange)**: [https://www.borsaistanbul.com/](https://www.borsaistanbul.com/)
- **Turkish Economic Data**: TCMB (Turkish Central Bank) at [https://www.tcmb.gov.tr/](https://www.tcmb.gov.tr/)

## Need Help?

If you're stuck or have questions:

1. **Check the meta-skill**: Read `create-kallavi-turk-skills/SKILL.md` for detailed guidance
2. **Look at existing skills**: See how other skills in this repository are structured
3. **Open an issue**: Ask questions by creating a GitHub issue
4. **Join discussions**: Participate in GitHub Discussions (if enabled)

## License

By contributing to this repository, you agree that your contributions will be licensed under the MIT License (same as the repository).

---

**Thank you for contributing to Kallavi Turk Skills!** 🚀

Your contributions help build a more capable and intelligent Turkish digital twin. Whether you're adding a trading algorithm, a cultural insight, or a coding workflow, every skill makes Kallavi Turk better.

Happy coding! 🇹🇷💻
