# Kallavi Turk Skills

**A comprehensive collection of skills for the Kallavi Turk agentic twin** — a Turkish digital twin capable of trading, investing, coding, and serving as your perfect digital assistant.

Imagine a Turkish digital twin who can analyze BIST stocks in real-time, manage your crypto portfolio with TL conversions, write Turkish business documents, execute complex trading strategies, and embody your personal decision-making style. This repository makes that vision a reality.

## What Are Kallavi Turk Skills?

Kallavi Turk Skills are **Agent Skills standard-compliant** skill modules that teach AI agents (Claude Code, OpenClaw, etc.) how to perform specific tasks. Each skill is a self-contained folder with clear instructions, examples, and supporting resources.

This repository follows the **Anthropic Agent Skills open standard**, ensuring compatibility across:
- **Claude Code** (local desktop app)
- **OpenClaw / clawdbot** (primary platform)
- **Claude.ai** (web interface)
- **Claude API** (`/v1/skills` endpoint)

Skills in this repository are designed specifically for a **Turkish digital twin**, incorporating:
- Turkish language support (bilingual TR/EN)
- Turkish market expertise (BIST, TL, Turkish economic indicators)
- Turkish cultural context and business practices
- Localized workflows for trading, investing, and daily routines

## Repository Structure

```
kallavi-turk-skills/
├── README.md                          # This file - repository overview
├── CONTRIBUTING.md                    # Contribution guidelines for humans
├── LICENSE                            # MIT License
├── create-kallavi-turk-skills/        # Meta-skill: teaches agents to create skills
│   └── SKILL.md
├── [future-skill-1]/                  # Your next skill here!
│   ├── SKILL.md
│   ├── scripts/                       # Optional: executable code
│   ├── references/                    # Optional: detailed documentation
│   └── assets/                        # Optional: templates, configs
└── [future-skill-2]/                  # And more skills...
    └── SKILL.md
```

Each skill follows a consistent structure:
- **Required**: `SKILL.md` with YAML frontmatter and instructions
- **Optional**: `scripts/`, `references/`, `assets/` subdirectories

## Compatibility

✅ **Claude Code** — Local skill directory integration  
✅ **OpenClaw (clawdbot)** — Primary target platform  
✅ **Claude.ai** — Upload as custom instructions  
✅ **Claude API** — Use via `/v1/skills` endpoint  

All skills are tested to work across these platforms.

## Quick Start

### Using a Skill with Claude Code

1. Clone this repository:
   ```bash
   git clone https://github.com/its-meseba/kallavi-turk-skills.git
   ```

2. Copy the skill folder(s) you want to Claude Code's skill directory:
   - **macOS**: `~/Library/Application Support/Claude/skills/`
   - **Windows**: `%APPDATA%/Claude/skills/`
   - **Linux**: `~/.config/Claude/skills/`

3. Restart Claude Code

4. Start using the skill by typing queries that match the skill's trigger phrases

### Using a Skill with OpenClaw

1. Clone this repository:
   ```bash
   git clone https://github.com/its-meseba/kallavi-turk-skills.git
   ```

2. Configure OpenClaw to load the skill directory:
   ```bash
   openclaw --skills-dir /path/to/kallavi-turk-skills
   ```

3. Test the skill with relevant queries

### Using a Skill with Claude.ai

1. Navigate to the skill folder you want to use
2. Copy the contents of `SKILL.md`
3. In Claude.ai, paste the skill content as a custom instruction or system prompt
4. Start your conversation

## How to Create a New Skill

There are two ways to create a new skill:

### Option 1: Let an AI Agent Do It (Recommended)

Use the **`create-kallavi-turk-skills`** meta-skill:

1. Add the `create-kallavi-turk-skills/` folder to your AI agent (Claude Code or OpenClaw)
2. Ask: "Create a new skill for analyzing Turkish stocks" or "Help me build a kallavi skill for portfolio management"
3. The agent will guide you through the entire skill creation process

### Option 2: Create Manually

Follow the guidelines in **[CONTRIBUTING.md](CONTRIBUTING.md)**:

1. Fork this repository
2. Create a new folder in kebab-case (e.g., `bist-stock-analyzer`)
3. Add a `SKILL.md` file with proper YAML frontmatter and instructions
4. Test your skill locally
5. Submit a pull request

## Skill Categories

Skills in this repository are organized into six main categories:

### 🔄 Trading & Finance
Real-time market analysis, technical indicators, BIST stocks, crypto trading, portfolio tracking, risk management

**Example skills** (coming soon):
- `bist-stock-scanner` — Real-time BIST market analysis
- `crypto-trading-bot` — Automated crypto trading with TL conversions
- `portfolio-risk-analyzer` — Risk assessment and rebalancing

### 📊 Investment
Fundamental analysis, Turkish economic indicators, real estate, gold/TL dynamics, long-term planning

**Example skills** (coming soon):
- `turkish-real-estate-analyzer` — Turkish property investment analysis
- `gold-investment-strategy` — Gold and commodity analysis for Turkish markets
- `dividend-tracker` — Track dividends with Turkish tax considerations

### 💻 Coding & Development
Code generation, review, Turkish dev conventions, API clients, database design

**Example skills** (coming soon):
- `turkish-api-client-generator` — Generate API clients for Turkish services
- `code-review-assistant` — Code review with Turkish context
- `database-schema-builder` — Database design and optimization

### 🤖 Digital Twin / Personal
Daily routines, communication style, decision-making frameworks, cultural behaviors

**Example skills** (coming soon):
- `morning-routine-optimizer` — Personalized morning workflow
- `turkish-communication-style` — Embody Turkish communication patterns
- `decision-framework` — Personal decision-making model

### 📝 Document & Asset Creation
Reports, presentations, Turkish business documents, charts, social media content

**Example skills** (coming soon):
- `turkish-business-letter-writer` — Generate official Turkish documents
- `financial-report-generator` — Create financial reports and analyses
- `chart-creator` — Data visualization and infographics

### ⚙️ Workflow Automation
Multi-step processes, MCP integrations, scheduled tasks, cross-platform automation

**Example skills** (coming soon):
- `morning-market-briefing` — Automated daily market summary
- `portfolio-rebalancing-workflow` — Scheduled portfolio adjustments
- `mcp-trading-integration` — MCP server integration for trading platforms

## Contributing

We welcome contributions! Whether you want to add a new trading strategy, a Turkish market analysis tool, a coding workflow, or a personal routine, your contribution helps make Kallavi Turk more capable.

**Read the full contribution guidelines**: [CONTRIBUTING.md](CONTRIBUTING.md)

**Quick contribution checklist**:
- [ ] Skill folder is kebab-case
- [ ] `SKILL.md` file exists with proper frontmatter
- [ ] Description includes trigger phrases
- [ ] Instructions are clear and actionable
- [ ] Tested with at least 3 user queries
- [ ] Turkish/bilingual support included (if applicable)

## Meta-Skill: Create Kallavi Turk Skills

New to skill creation? Start with the **`create-kallavi-turk-skills`** meta-skill:

📖 **[View the meta-skill](create-kallavi-turk-skills/SKILL.md)**

This skill teaches AI agents how to create new skills for this repository. Simply add it to your AI agent and ask it to create a skill — it will handle:
- Determining the skill name and structure
- Writing proper YAML frontmatter
- Creating clear, actionable instructions
- Adding examples and error handling
- Running validation checks

## License

This repository is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

You are free to use, modify, and distribute these skills for any purpose, including commercial use.

## About Kallavi Turk

Kallavi Turk is an **agentic Turkish digital twin** — an AI-powered assistant that embodies Turkish market expertise, cultural knowledge, and personal decision-making capabilities. The twin can:

- 📈 Trade and invest in Turkish and international markets
- 💰 Analyze BIST stocks, crypto, gold, and TL dynamics
- 💻 Code, review, and deploy software projects
- 📄 Create Turkish business documents and reports
- 🤖 Automate complex workflows and routines
- 🇹🇷 Operate bilingually in Turkish and English

This repository is the **skill library** that powers the twin's capabilities.

## Support & Community

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/its-meseba/kallavi-turk-skills/issues)
- **Discussions**: Ask questions and share ideas in [GitHub Discussions](https://github.com/its-meseba/kallavi-turk-skills/discussions)
- **Pull Requests**: Contribute new skills via [Pull Requests](https://github.com/its-meseba/kallavi-turk-skills/pulls)

## Useful Resources

- 📚 [Anthropic Agent Skills Documentation](https://docs.anthropic.com/claude/docs/agent-skills)
- 🛠️ [OpenClaw / clawdbot](https://github.com/clawdbot/openclaw)
- 💼 [BIST (Istanbul Stock Exchange)](https://www.borsaistanbul.com/)
- 🏦 [TCMB (Turkish Central Bank)](https://www.tcmb.gov.tr/)

---

**Start building the future of Turkish agentic AI!** 🚀🇹🇷

*Contributions welcome • MIT Licensed • Built with ❤️ for the Turkish AI community*
