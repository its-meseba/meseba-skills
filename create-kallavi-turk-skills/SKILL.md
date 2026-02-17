---
name: create-kallavi-turk-skills
description: Teaches AI agents how to create new skills for the Kallavi Turk agentic twin repository. Triggers when users say "create a new skill", "add a skill for trading", "help me build a kallavi skill", "I want to make a new turk skill", "generate a skill for investment", "create trading skill", "make a skill", or similar requests to build new capabilities for the Turkish digital twin.
metadata:
  author: its-meseba
  version: 1.0.0
  tags:
    - meta-skill
    - skill-creation
    - kallavi-turk
    - agent-skills
    - turkish-twin
---

# Create Kallavi Turk Skills

This meta-skill teaches AI agents (Claude Code, OpenClaw, etc.) how to create new skills for the **Kallavi Turk** agentic twin — a Turkish digital twin capable of trading, investing, coding, and serving as a comprehensive digital assistant.

## What is a Kallavi Turk Skill?

A **Kallavi Turk Skill** is an Agent Skills standard-compliant skill folder designed specifically for a Turkish digital twin. Each skill teaches the twin how to handle specific tasks, such as:

- Trading strategies and market analysis
- Investment analysis and portfolio management
- Coding workflows and development practices
- Turkish cultural knowledge and communication patterns
- Daily routines and personal decision-making frameworks
- Document creation (reports, presentations, business documents)
- Workflow automation and multi-step processes

Skills follow the **Anthropic Agent Skills open standard**, ensuring compatibility across multiple AI platforms including Claude Code, OpenClaw (clawdbot/openclaw), Claude.ai, and API integrations.

## Folder Structure Requirements

Every Kallavi Turk skill MUST follow this exact structure:

```
skill-name/
├── SKILL.md          # Required - must be exactly SKILL.md (case-sensitive)
├── scripts/           # Optional - Python, Bash, or other executable scripts
├── references/        # Optional - documentation, API guides, examples
└── assets/            # Optional - templates, icons, data files, configs
```

### Structure Rules

1. **SKILL.md is required** — This is the core instruction file. The filename MUST be `SKILL.md` with exact casing (not `skill.md`, `Skill.md`, or `README.md`).

2. **Folder name must be kebab-case** — Use lowercase letters with hyphens (e.g., `turkish-market-analysis`, `bist-stock-scanner`, `portfolio-rebalancer`). The folder name MUST match the `name` field in the YAML frontmatter.

3. **No README.md inside skill folders** — Use SKILL.md instead. This prevents confusion and maintains standard compliance.

4. **Optional subdirectories**:
   - `scripts/` — Store executable code, automation scripts, or tools
   - `references/` — Place detailed documentation, API references, examples, or research materials
   - `assets/` — Include templates, configuration files, images, or data files

## YAML Frontmatter Rules

Every `SKILL.md` file MUST start with YAML frontmatter enclosed in `---` delimiters. Be explicit about the following requirements:

### Required Fields

```yaml
---
name: skill-name-in-kebab-case
description: A clear description that includes WHAT the skill does and WHEN to trigger it (include example user phrases)
---
```

### Frontmatter Field Requirements

1. **`name` field**:
   - MUST be in kebab-case (lowercase with hyphens)
   - MUST NOT contain spaces or capital letters
   - MUST match the folder name exactly
   - MUST NOT start with "claude" or "anthropic"
   - Example: `turkish-market-analysis`, `crypto-trading-strategy`

2. **`description` field**:
   - MUST include WHAT the skill does (core functionality)
   - MUST include WHEN to trigger it (example user phrases or scenarios)
   - MUST be under 1024 characters
   - MUST NOT contain XML tags (no `<`, `>`, `&lt;`, `&gt;`)
   - Should be clear and actionable
   - Example: "Analyzes Turkish stock market (BIST) trends and provides investment recommendations. Triggers when users ask about Turkish stocks, BIST analysis, Turkish market trends, or Istanbul exchange insights."

### Optional Fields

```yaml
---
name: skill-name
description: What it does and when to trigger it
license: MIT
compatibility:
  - claude-code
  - openclaw
  - claude-api
metadata:
  author: its-meseba
  version: 1.0.0
  mcp-server: server-name-if-applicable
  tags:
    - trading
    - turkish-market
    - finance
---
```

## Writing Effective Instructions

The body of `SKILL.md` (after the frontmatter) contains the actual instructions for the AI agent. Follow these guidelines to make instructions clear and actionable:

### 1. Be Specific and Actionable

❌ **Bad**: "Validate things properly before proceeding"  
✅ **Good**: "Validate the API key by making a test request to `/api/v1/auth/verify` and checking for a 200 status code"

❌ **Bad**: "Handle errors appropriately"  
✅ **Good**: "If the API returns a 429 status code, wait 60 seconds and retry up to 3 times. If all retries fail, inform the user that the rate limit has been exceeded."

### 2. Use Progressive Disclosure

- **Core instructions** go in SKILL.md — Essential workflows, key steps, common scenarios
- **Detailed documentation** goes in `references/` — API specs, extended examples, edge cases, technical deep-dives
- **Supporting assets** go in `assets/` — Templates, configuration files, sample data

Example structure:
```
turkish-market-analysis/
├── SKILL.md                          # Core: How to analyze BIST stocks
├── references/
│   ├── bist-api-documentation.md     # Detailed API specs
│   ├── turkish-economic-indicators.md # Context on Turkish economy
│   └── example-analyses.md            # Sample analysis outputs
└── assets/
    └── analysis-template.json         # JSON template for results
```

### 3. Include Step-by-Step Workflows

Structure your instructions with numbered steps for clarity:

```markdown
## How to Analyze a Turkish Stock

1. **Validate the stock ticker**: Check that the ticker is valid for BIST (e.g., THYAO, GARAN, ISCTR)
2. **Fetch current price data**: Use the BIST API endpoint `/v1/stocks/{ticker}/price`
3. **Retrieve historical data**: Get 90-day price history from `/v1/stocks/{ticker}/history?days=90`
4. **Calculate technical indicators**:
   - Simple Moving Average (SMA) for 20 and 50 days
   - Relative Strength Index (RSI)
   - Trading volume trends
5. **Analyze fundamental data**: Check P/E ratio, market cap, and sector performance
6. **Generate recommendation**: Combine technical and fundamental analysis to provide a buy/hold/sell recommendation
7. **Present results**: Format the analysis in a clear, bilingual (Turkish/English) summary
```

### 4. Include Examples of User Queries and Expected Behavior

Show how users will interact with the skill:

```markdown
## Example User Queries

**Query 1**: "THYAO hissesini analiz et" (Analyze THYAO stock)
**Expected Behavior**:
- Recognize Turkish query
- Fetch THYAO (Turkish Airlines) data
- Perform technical and fundamental analysis
- Respond in Turkish with actionable insights

**Query 2**: "What's the best BIST stock to buy right now?"
**Expected Behavior**:
- Scan top 10 BIST stocks by market cap
- Apply ranking criteria (RSI, volume, sector trends)
- Provide top 3 recommendations with rationale
- Include risk disclaimers

**Query 3**: "Show me the trading volume for GARAN this week"
**Expected Behavior**:
- Fetch GARAN (Garanti BBVA) 7-day volume data
- Present as a simple chart or table
- Highlight any unusual volume spikes
```

### 5. Include Error Handling and Troubleshooting

Always address what to do when things go wrong:

```markdown
## Error Handling

### API Connection Errors
- **Error**: `Connection timeout to BIST API`
- **Action**: Retry up to 3 times with 10-second intervals. If all retries fail, inform the user and suggest checking the BIST website directly.

### Invalid Stock Ticker
- **Error**: `Ticker not found on BIST`
- **Action**: Suggest similar ticker names if available. Ask the user to verify the ticker symbol on the BIST official list.

### Rate Limiting
- **Error**: `429 Too Many Requests`
- **Action**: Wait 60 seconds before retrying. Inform the user about the rate limit and suggest batching requests.

### Turkish Language Processing
- **Issue**: User input contains Turkish characters that may not be properly encoded
- **Action**: Use UTF-8 encoding for all text processing. Normalize Turkish characters (ğ, ü, ş, ı, ö, ç) before API calls if needed.
```

### 6. Turkish-Specific Skills: Cultural Context and Bilingual Support

For skills related to Turkish markets, culture, or communication, include guidance on handling Turkish language and cultural context:

```markdown
## Turkish Language Support

- **Detect language**: If the user query contains Turkish characters or Turkish keywords, respond in Turkish
- **Bilingual outputs**: For financial/technical data, provide key terms in both Turkish and English (e.g., "Piyasa Değeri (Market Cap)")
- **Cultural context**: When discussing Turkish business practices, acknowledge cultural norms (e.g., importance of personal relationships, business hours, holidays like Ramazan Bayramı)
- **Turkish number formatting**: Use Turkish decimal separator (comma) for prices when responding in Turkish: "123.456,78 TL" not "123,456.78 TL"
- **Currency handling**: Always specify TRY/TL for Turkish Lira amounts to avoid confusion with USD

## Turkish Market Specifics

- **BIST trading hours**: 09:40 - 18:00 Istanbul time (GMT+3)
- **Turkish holidays**: Factor in Ramazan Bayramı, Kurban Bayramı, and official Turkish holidays when trading
- **Economic indicators**: Monitor TCMB (Turkish Central Bank) announcements, inflation reports, and USD/TRY exchange rate
```

## Skill Categories for Kallavi Turk

Organize your skills into these main categories. When creating a new skill, determine which category it belongs to:

### 1. Trading & Finance
Skills for active trading, market analysis, and financial operations:
- Real-time market data analysis
- Technical analysis (RSI, MACD, Bollinger Bands)
- Turkish stock market (BIST) expertise
- Cryptocurrency trading strategies
- Portfolio tracking and alerts
- Risk management and stop-loss strategies

**Example skills**: `bist-stock-scanner`, `crypto-trading-bot`, `portfolio-risk-analyzer`

### 2. Investment
Skills for long-term investment analysis and decision-making:
- Fundamental analysis (P/E, DCF, sector analysis)
- Turkish economic indicators (inflation, interest rates, USD/TRY)
- Real estate investment analysis (Turkey-specific)
- Gold and commodity analysis (important in Turkish markets)
- Dividend tracking and tax considerations
- Retirement and savings planning

**Example skills**: `turkish-real-estate-analyzer`, `gold-investment-strategy`, `dividend-tracker`

### 3. Coding & Development
Skills for software development and engineering tasks:
- Code generation in multiple languages
- Code review and refactoring
- Turkish development community conventions
- API integration and testing
- Database design and optimization
- DevOps and deployment workflows

**Example skills**: `turkish-api-client-generator`, `code-review-assistant`, `database-schema-builder`

### 4. Digital Twin / Personal
Skills that embody personal behaviors, routines, and decision-making:
- Daily routines and habits
- Communication style and tone (Turkish/English)
- Decision-making frameworks
- Cultural behaviors and preferences
- Personal productivity systems
- Health and wellness tracking

**Example skills**: `morning-routine-optimizer`, `turkish-communication-style`, `decision-framework`

### 5. Document & Asset Creation
Skills for generating documents, reports, and creative content:
- Financial reports and presentations
- Turkish business documents (official letters, contracts)
- Data visualization and charts
- Markdown and technical documentation
- Social media content (Turkish/English)
- Email drafting and translation

**Example skills**: `turkish-business-letter-writer`, `financial-report-generator`, `chart-creator`

### 6. Workflow Automation
Skills for complex, multi-step processes and integrations:
- Multi-step trading workflows
- Data collection and processing pipelines
- MCP (Model Context Protocol) server integrations
- Scheduled tasks and monitoring
- Cross-platform automation (GitHub, Notion, trading platforms)
- Alert and notification systems

**Example skills**: `morning-market-briefing`, `portfolio-rebalancing-workflow`, `mcp-trading-integration`

## Compatibility Notes

All Kallavi Turk skills must be compatible with:

1. **Claude Code (Desktop App)**:
   - Local skill directory: Skills should work when placed in Claude Code's skill folders
   - File paths: Use relative paths for any file references

2. **OpenClaw / clawdbot** (Primary Target):
   - This is the primary platform for Kallavi Turk
   - Skills should leverage OpenClaw's features and integrations
   - Test thoroughly with OpenClaw before submitting

3. **Claude.ai (Web)**:
   - Skills can be uploaded as custom instructions
   - Keep skill size reasonable (under 100KB for SKILL.md)

4. **Claude API**:
   - Skills should work via `/v1/skills` endpoint
   - Follow API token limits and best practices

5. **MCP Servers** (Optional Enhancement):
   - If a skill benefits from MCP integration, document the required server in `metadata.mcp-server`
   - Provide setup instructions in `references/mcp-setup.md`

## Testing Checklist

After creating a new skill, run through this validation checklist before submitting:

- [ ] **File naming**: `SKILL.md` exists with exact casing (not `skill.md` or `Skill.md`)
- [ ] **Folder naming**: Folder is in kebab-case with no spaces or capitals
- [ ] **Folder-name match**: Folder name matches the `name` field in frontmatter exactly
- [ ] **Frontmatter delimiters**: YAML frontmatter has `---` at the start and end
- [ ] **Required fields**: Frontmatter includes `name` and `description`
- [ ] **Description quality**: Description includes WHAT the skill does AND WHEN to trigger it (example phrases)
- [ ] **No XML tags**: Description has no XML tags (`<`, `>`, or escaped versions)
- [ ] **Character limit**: Description is under 1024 characters
- [ ] **No forbidden names**: Name does not start with "claude" or "anthropic"
- [ ] **Instructions are clear**: Instructions are specific, actionable, and avoid vague language
- [ ] **Step-by-step workflows**: Key processes are broken down into numbered steps
- [ ] **Examples included**: User query examples and expected behaviors are documented
- [ ] **Error handling**: Error scenarios and troubleshooting steps are included
- [ ] **Turkish/bilingual**: If applicable, Turkish language and cultural context guidance is present
- [ ] **File structure**: Optional folders (`scripts/`, `references/`, `assets/`) are used appropriately
- [ ] **No README.md**: Skill folder does not contain a `README.md` file
- [ ] **Testing**: Skill has been tested with at least 3 different user queries
- [ ] **Dependencies**: Any required libraries or APIs are documented in `references/`

## Step-by-Step Workflow for Creating a New Skill

When a user asks you to create a new skill for Kallavi Turk, follow this workflow:

### Step 1: Understand the Domain/Task

Ask the user what the skill should do:
- "What domain or task should this skill cover?"
- "Who will use this skill and in what scenarios?"
- "Are there any specific Turkish market or cultural considerations?"

**Example user responses**:
- "I need a skill for analyzing BIST stocks in real-time"
- "Create a skill to help me draft Turkish business emails"
- "Make a skill for managing my crypto portfolio with TL conversions"

### Step 2: Determine the Skill Name

Based on the domain, generate a kebab-case skill name:
- Use descriptive, action-oriented names
- Keep it concise (2-4 words ideal)
- Make it specific to the task

**Examples**:
- Domain: "BIST stock analysis" → `bist-stock-analyzer`
- Domain: "Turkish business emails" → `turkish-business-email-writer`
- Domain: "Crypto portfolio with TL" → `crypto-portfolio-manager-tl`

Confirm the name with the user: "I'll create a skill called `bist-stock-analyzer`. Does that work?"

### Step 3: Generate the Folder Structure

Create the skill folder and subdirectories:

```bash
mkdir -p skill-name
mkdir -p skill-name/scripts     # If executable code is needed
mkdir -p skill-name/references  # If detailed docs are needed
mkdir -p skill-name/assets      # If templates/configs are needed
```

### Step 4: Write the YAML Frontmatter

Create `SKILL.md` with proper frontmatter:

```yaml
---
name: skill-name
description: [Clear description of WHAT the skill does] Triggers when users [list example phrases like "analyze BIST stocks", "check Turkish market", "show me THYAO analysis", etc.]
metadata:
  author: its-meseba
  version: 1.0.0
  tags:
    - [relevant-tag-1]
    - [relevant-tag-2]
---
```

**Example for BIST stock analyzer**:
```yaml
---
name: bist-stock-analyzer
description: Analyzes Turkish stock market (BIST) stocks with technical and fundamental analysis, providing buy/hold/sell recommendations. Triggers when users ask "analyze BIST stock", "check THYAO price", "should I buy GARAN", "Turkish stock analysis", "BIST market trends", or similar investment queries about Turkish equities.
metadata:
  author: its-meseba
  version: 1.0.0
  tags:
    - trading
    - turkish-market
    - bist
    - stock-analysis
    - finance
---
```

### Step 5: Write the Body Instructions

Follow the "Writing Effective Instructions" guidelines above. Include:

1. **Overview**: What this skill does and why it's useful
2. **Prerequisites**: Any required API keys, accounts, or setup
3. **Core Workflow**: Step-by-step numbered instructions
4. **User Query Examples**: Show 3-5 example queries and expected behaviors
5. **Error Handling**: Document common errors and how to handle them
6. **Turkish/Bilingual Notes**: If applicable, language and cultural guidance
7. **Advanced Usage**: Optional advanced features in `references/`

### Step 6: Add Scripts/References/Assets (If Needed)

Determine if the skill needs supporting files:

- **Scripts**: If the skill requires executable code (Python for API calls, Bash for automation)
  - Create well-documented scripts in `scripts/`
  - Include installation instructions (pip packages, etc.)

- **References**: If the skill needs detailed documentation
  - API documentation → `references/api-docs.md`
  - Extended examples → `references/examples.md`
  - Research or context → `references/context.md`

- **Assets**: If the skill uses templates or data files
  - JSON/YAML templates → `assets/template.json`
  - Configuration files → `assets/config.yaml`
  - Sample data → `assets/sample-data.csv`

### Step 7: Run Through the Validation Checklist

Go through each item in the "Testing Checklist" section above. Fix any issues before proceeding.

### Step 8: Suggest Testing Queries

Provide the user with 3-5 test queries to validate the skill:

**Example for `bist-stock-analyzer`**:
1. "THYAO hissesini analiz et" (Test Turkish language input)
2. "What's the current price of GARAN?" (Test basic data fetching)
3. "Should I buy or sell ISCTR based on technical analysis?" (Test full analysis workflow)
4. "Compare AKBNK and YKBNK" (Test comparative analysis)
5. "What happened with BIST stocks today?" (Test market overview)

Ask the user to test these queries and report if the skill works as expected.

### Step 9: Documentation and Submission

Once the skill is validated:
1. Ensure all files are committed to the repository
2. Update the main repository README.md to list the new skill (if applicable)
3. Follow the PR process in CONTRIBUTING.md for submission

## Summary

Creating a Kallavi Turk skill is about:
1. **Understanding the task** the skill needs to accomplish
2. **Following the structure** (kebab-case folder, SKILL.md, optional subdirectories)
3. **Writing clear frontmatter** (name, description with triggers, metadata)
4. **Providing actionable instructions** (step-by-step, examples, error handling)
5. **Testing thoroughly** (use the validation checklist)
6. **Supporting Turkish context** (language, cultural norms, market specifics)

By following this meta-skill, you'll create high-quality, standards-compliant skills that enhance the Kallavi Turk agentic twin's capabilities across trading, investing, coding, and personal workflows.

---

**Ready to create a skill?** Ask the user: "What skill would you like me to create for Kallavi Turk?"
