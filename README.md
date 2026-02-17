# Kallavi Turk Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills-5-blue.svg)](#available-skills)

**Better Turkish Kallavi Skills for Agentic Twin** — A versatile Turkish digital twin capable of trading, investing, coding, and being your perfect personal assistant.

## Table of Contents

- [What are Skills?](#what-are-skills)
- [Repository Structure](#repository-structure)
- [Available Skills](#available-skills)
- [Installation & Usage](#installation--usage)
- [Contributing](#contributing)
- [License](#license)

## What are Skills?

Skills are modular capabilities that enhance AI agents with specialized knowledge and workflows. Each skill follows the Anthropic skill standard:

- **Declarative structure**: Skills are defined in `SKILL.md` files with YAML frontmatter
- **Progressive disclosure**: Information is loaded on-demand (frontmatter → instructions → linked files)
- **Context-aware triggering**: Skills activate based on user intent and trigger phrases
- **Self-contained**: Each skill includes instructions, scripts, references, and assets

Skills allow agents to excel at specific tasks while maintaining modularity and reusability.

## Repository Structure

```
kallavi-turk-skills/
├── README.md              # This file
├── CONTRIBUTING.md        # Skill creation guidelines
├── LICENSE                # MIT License
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── _templates/
│   └── skill-template/    # Copy this to create new skills
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
└── skills/
    ├── trading-assistant/     # Market analysis & trading signals
    ├── investment-advisor/    # Portfolio & investment guidance
    ├── code-assistant/        # Code writing & debugging
    ├── digital-twin/          # Personal digital twin
    └── kallavi-skill-creator/ # Meta-skill for creating skills
```

## Available Skills

### Core Skills

1. **[trading-assistant](skills/trading-assistant/)** — Analyzes market trends, provides trading signals, and helps manage portfolio positions for Turkish and global markets.
   - Triggers: "analyze market", "trading signal", "borsa analizi", "al-sat sinyali", "piyasa durumu"

2. **[investment-advisor](skills/investment-advisor/)** — Provides long-term investment guidance, portfolio allocation strategies, and financial planning for Turkish investors.
   - Triggers: "yatırım tavsiyesi", "portföy oluştur", "investment advice", "portfolio allocation", "emeklilik planı"

3. **[code-assistant](skills/code-assistant/)** — Helps write, review, debug, and optimize code across multiple languages with Turkish developer conventions.
   - Triggers: "kod yaz", "debug et", "code review", "write code", "hata bul", "optimize et"

4. **[digital-twin](skills/digital-twin/)** — Acts as your personal digital twin — learns your preferences, mimics your communication style, and handles routine tasks.
   - Triggers: "benim gibi yaz", "dijital ikizim", "act like me", "my style", "benim adıma yap"

### Meta Skills

5. **[kallavi-skill-creator](skills/kallavi-skill-creator/)** — Interactive guide for creating new Kallavi Turk skills. Use this to build new skills for the repository.
   - Triggers: "yeni skill oluştur", "create a new skill", "skill yap", "beceri ekle", "build a skill for kallavi"

## Installation & Usage

### Using with Claude.ai

1. Open a conversation in Claude.ai
2. Attach one or more skill folders from this repository
3. Claude will automatically discover and activate relevant skills based on your requests

### Using with Claude Code

1. Clone this repository locally
2. Open your project in Claude Code
3. Reference skills by including them in your workspace
4. Use trigger phrases to activate specific skills

### Using via API

Skills can be integrated into custom applications using the Claude API:

```python
# Example: Using skills with the Anthropic API
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Include skill content in the system prompt or as attachments
# Skills will be automatically discovered and used contextually
```

### Compatibility

- **Claude.ai**: Full support
- **Claude Code**: Full support
- **OpenClaw**: Full support
- **Anthropic API**: Full support

## Contributing

We welcome contributions from both humans and AI agents! To create a new skill:

1. Start with the skill template in `_templates/skill-template/`
2. Or use the **kallavi-skill-creator** skill to guide you through the process
3. Review the detailed guidelines in [CONTRIBUTING.md](CONTRIBUTING.md)
4. Submit a pull request using the provided template

**Key Guidelines:**
- Follow the Anthropic skill standard (SKILL.md with YAML frontmatter)
- Use kebab-case for folder names
- Include both Turkish and English trigger phrases
- Write clear, concise descriptions with WHAT + WHEN
- Test your skill thoroughly before submission

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete guide.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Kallavi Turk Skills** — Confident, culturally Turkish, versatile. Your perfect digital twin for trading, investing, coding, and beyond.
