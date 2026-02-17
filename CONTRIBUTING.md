# Contributing to Kallavi Turk Skills

Welcome! This guide will help you create high-quality skills for the Kallavi Turk Skills repository. Whether you're an AI agent or human contributor, follow these guidelines to ensure your skills are effective, maintainable, and compatible with the Anthropic skill standard.

## Table of Contents

- [Skill Anatomy](#skill-anatomy)
- [YAML Frontmatter Rules](#yaml-frontmatter-rules)
- [Naming Conventions](#naming-conventions)
- [Progressive Disclosure](#progressive-disclosure)
- [Writing Effective Descriptions](#writing-effective-descriptions)
- [Writing Instructions](#writing-instructions)
- [Skill Categories](#skill-categories)
- [Design Patterns](#design-patterns)
- [Testing Your Skill](#testing-your-skill)
- [Quick Validation Checklist](#quick-validation-checklist)
- [Turkish/Kallavi-Specific Guidelines](#turkishkallavi-specific-guidelines)

## Skill Anatomy

Every skill follows this folder structure:

```
skills/your-skill-name/
├── SKILL.md           # Required: Main skill file with YAML frontmatter
├── scripts/           # Optional: Executable scripts
├── references/        # Optional: Supporting documentation
└── assets/            # Optional: Images, data files, etc.
```

### File Requirements

- **SKILL.md**: REQUIRED. Must have exact casing (all caps for SKILL).
- **Folder name**: Must use kebab-case (e.g., `trading-assistant`, not `Trading_Assistant` or `tradingAssistant`).
- **Subfolders**: Optional. Create only if needed.

## YAML Frontmatter Rules

Every SKILL.md must begin with YAML frontmatter delimited by `---`:

```markdown
---
name: skill-name
description: What the skill does and when to use it with trigger phrases.
license: MIT
metadata:
  version: 1.0.0
  author: its-meseba
  tags: [trading, turkish]
compatibility:
  models: [claude-3-5-sonnet, claude-3-opus]
  platforms: [claude-ai, claude-code, api]
allowed-tools:
  - web_search
  - calculator
---

# Skill Instructions

Your detailed instructions here...
```

### Required Fields

- **name** (string): The skill identifier. Must match folder name. Use kebab-case.
- **description** (string): What the skill does AND when to use it. Include trigger phrases.

### Optional Fields

- **license** (string): License identifier (e.g., MIT, Apache-2.0)
- **metadata** (object): Version, author, tags, etc.
  - `version`: Semantic version (e.g., 1.0.0)
  - `author`: Creator name or organization
  - `tags`: Array of relevant keywords
- **compatibility** (object): Supported models and platforms
  - `models`: Array of model identifiers
  - `platforms`: Array of platform names
- **allowed-tools** (array): List of tools the skill can use
- **dependencies** (array): Other skills this skill depends on

### Security Restrictions

🚫 **NEVER** use XML angle brackets (`<`, `>`) in frontmatter values  
🚫 **NEVER** use "claude" or "anthropic" in skill names  
🚫 **NEVER** include credentials or API keys

## Naming Conventions

### Folder Names
- Use kebab-case: `trading-assistant` ✅
- Not snake_case: `trading_assistant` ❌
- Not camelCase: `tradingAssistant` ❌
- Not PascalCase: `TradingAssistant` ❌

### File Names
- Main file: `SKILL.md` (exact casing)
- Supporting files: Use clear, descriptive names (e.g., `technical-analysis-guide.md`)

### Skill Names (in frontmatter)
- Must match folder name
- Use kebab-case
- Be descriptive but concise
- No "claude-" or "anthropic-" prefixes

## Progressive Disclosure

Skills load information in three levels:

### Level 1: Frontmatter (Always Loaded)
- Always parsed and available to the agent
- Keep concise and informative
- Include essential triggering information

### Level 2: SKILL.md Body (Loaded on Relevance)
- Loaded when the agent determines the skill is relevant
- Contains main instructions and workflows
- Should be comprehensive but well-structured

### Level 3: Linked Files (Loaded on Demand)
- Referenced files in `scripts/`, `references/`, `assets/`
- Loaded only when explicitly needed
- Use for detailed references, large datasets, or optional content

**Design Principle**: Put the most frequently needed information in earlier levels to optimize context usage.

## Writing Effective Descriptions

The description field is critical for skill triggering. It must include:

1. **WHAT**: What the skill does
2. **WHEN**: When to use it (trigger phrases)

### Good Examples

✅ **Good**: "Analyzes market trends, provides trading signals, and helps manage portfolio positions for Turkish and global markets. Use when user says 'analyze market', 'trading signal', 'borsa analizi', 'al-sat sinyali', 'piyasa durumu'."

✅ **Good**: "Interactive guide for creating new Kallavi Turk skills. Walks the user through use case definition, frontmatter generation, instruction writing, folder structure creation, and validation. Use when user says 'yeni skill oluştur', 'create a new skill', 'skill yap', 'beceri ekle'."

### Bad Examples

❌ **Bad**: "Helps with trading." (Too vague, no triggers)

❌ **Bad**: "This skill will help you analyze markets and make trading decisions by providing signals." (No trigger phrases)

❌ **Bad**: "Use this for market analysis." (No specific trigger phrases in quotes)

### Tips for Trigger Phrases

- Include both Turkish and English phrases
- Use quotes around each phrase: `"phrase one", "phrase two"`
- Include variations and colloquialisms
- Think about how users naturally express the need
- Test with real user queries

## Writing Instructions

Organize your SKILL.md body using this recommended structure:

### 1. Overview
Brief introduction to what the skill does and its primary use cases.

### 2. Instructions
Main step-by-step workflow or procedures. Use numbered lists for sequential steps, bullet points for non-sequential items.

#### Example:
```markdown
## Instructions

When a user requests market analysis:

1. **Identify the market/instrument**: Ask which market or instrument to analyze (BIST, forex, crypto, etc.)
2. **Gather context**: Check current price, volume, recent news
3. **Perform technical analysis**: Apply relevant indicators (RSI, MACD, moving averages)
4. **Generate signal**: Provide buy/sell/hold recommendation with confidence level
5. **Risk assessment**: Calculate position size and stop-loss levels
6. **Present findings**: Summarize in clear, actionable format
```

### 3. Examples
Provide concrete examples of typical interactions or outputs.

### 4. Best Practices
List important considerations, tips, or guidelines for using the skill effectively.

### 5. Troubleshooting
Common issues and how to resolve them.

### 6. References
Link to additional resources or reference files.

## Skill Categories

Kallavi Turk Skills fall into these main categories:

### 1. Document/Asset Creation
Skills that generate content (reports, code, documents).

**Example**: Code generator, investment report creator

### 2. Workflow Automation
Skills that orchestrate multi-step processes.

**Example**: Trading workflow, portfolio rebalancing

### 3. MCP Enhancement
Skills that extend or improve MCP (Model Context Protocol) capabilities.

**Example**: Multi-source data aggregator, context optimizer

## Design Patterns

Use these proven patterns when designing skills:

### 1. Sequential Workflow Orchestration
For tasks with clear step-by-step processes.

**Template**:
```markdown
1. Validate inputs
2. Gather required information
3. Process/analyze data
4. Generate output
5. Verify and present
```

**Use for**: Trading workflows, code review processes, report generation

### 2. Multi-MCP Coordination
For skills that need to coordinate multiple data sources or tools.

**Template**:
```markdown
1. Identify required data sources
2. Query each source in parallel when possible
3. Aggregate and normalize results
4. Synthesize into coherent output
```

**Use for**: Market analysis (multiple exchanges), portfolio aggregation

### 3. Iterative Refinement
For tasks that improve through iteration.

**Template**:
```markdown
1. Generate initial output
2. Review against criteria
3. Identify improvements
4. Refine and regenerate
5. Repeat until satisfactory
```

**Use for**: Code optimization, document editing, strategy refinement

### 4. Context-Aware Tool Selection
For skills that dynamically choose tools based on context.

**Template**:
```markdown
1. Analyze user intent and context
2. Determine required capabilities
3. Select appropriate tools
4. Execute with selected tools
5. Adapt if initial approach fails
```

**Use for**: Problem-solving skills, adaptive assistants

### 5. Domain-Specific Intelligence
For skills with specialized domain knowledge.

**Template**:
```markdown
1. Load domain-specific knowledge
2. Apply domain rules and heuristics
3. Use domain-specific terminology
4. Provide domain-expert-level insights
```

**Use for**: Trading expertise, investment advisory, technical analysis

## Testing Your Skill

Before submitting a skill, test it thoroughly:

### Triggering Tests
- [ ] Test with expected trigger phrases
- [ ] Test with variations and typos
- [ ] Test with Turkish and English phrases
- [ ] Verify it doesn't trigger on unrelated queries

### Functional Tests
- [ ] Walk through each instruction step
- [ ] Test with typical use cases
- [ ] Test with edge cases
- [ ] Verify outputs are correct and useful
- [ ] Test with different input variations

### Performance Tests
- [ ] Check context window usage
- [ ] Ensure progressive disclosure works
- [ ] Verify large files are in references/ not inline
- [ ] Test response time with and without optional files

### Integration Tests
- [ ] Test with other skills (check for conflicts)
- [ ] Test with different models if specified
- [ ] Test on different platforms (Claude.ai, Claude Code, API)

## Quick Validation Checklist

Before submitting your PR, verify:

- [ ] **Folder name**: kebab-case, matches skill name
- [ ] **SKILL.md**: Exact casing, exists in skill folder
- [ ] **Frontmatter**: Valid YAML, includes `name` and `description`
- [ ] **Description**: Includes WHAT + WHEN + trigger phrases in quotes
- [ ] **No XML brackets**: No `<` or `>` in frontmatter
- [ ] **No restricted names**: No "claude" or "anthropic" in skill name
- [ ] **Turkish support**: Turkish trigger phrases included
- [ ] **Instructions**: Clear, structured, actionable
- [ ] **Examples**: At least one concrete example provided
- [ ] **Testing**: Skill has been tested with real queries
- [ ] **Files organized**: Scripts in scripts/, references in references/, etc.
- [ ] **No secrets**: No API keys, credentials, or sensitive data

## Turkish/Kallavi-Specific Guidelines

### Cultural Awareness
- Skills should be culturally appropriate for Turkish users
- Use Turkish terminology where relevant (e.g., "borsa" for stock exchange, "altın" for gold)
- Be aware of Turkish market hours (BIST opens at 09:30 Istanbul time)
- Understand Turkish financial instruments (DBS, government bonds, eurobonds)

### Language Support
- Always include both Turkish and English trigger phrases
- Use natural Turkish expressions, not direct translations
- Support Turkish characters (ç, ğ, ı, ö, ş, ü)
- When in doubt, provide bilingual outputs

### Kallavi Persona
- **Confident**: Provide clear, decisive guidance
- **Culturally Turkish**: Understand Turkish business culture and communication style
- **Versatile**: Seamlessly switch between trading, investing, coding, and personal tasks
- **Digital twin**: Learn and adapt to user preferences over time

### Domain Expertise
- **Trading**: Focus on both BIST (Turkish market) and global markets
- **Investing**: Understand Turkish investment instruments and regulations
- **Coding**: Support Turkish developer conventions and documentation
- **Personal assistant**: Handle both professional and personal tasks with Turkish cultural context

## Submitting Your Skill

1. Fork the repository
2. Create a new branch: `git checkout -b skill/your-skill-name`
3. Copy `_templates/skill-template/` to `skills/your-skill-name/`
4. Develop your skill following these guidelines
5. Test thoroughly
6. Run validation checklist
7. Commit with clear message: `git commit -m "Add your-skill-name skill"`
8. Push to your fork: `git push origin skill/your-skill-name`
9. Open a Pull Request using the template
10. Address any review feedback

## Getting Help

- Review existing skills in the `skills/` directory for examples
- Use the **kallavi-skill-creator** skill to guide you through creation
- Check the references in `skills/kallavi-skill-creator/references/`
- Open an issue for questions or discussions

---

Thank you for contributing to Kallavi Turk Skills! 🚀
