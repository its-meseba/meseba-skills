---
name: shipyard
description: Mobile app development automation — SDK integration, CLI orchestration, dashboard configuration, and app store operations. Use when setting up or managing mobile app SDKs (PostHog, Adapty, Firebase, Meta, AppsFlyer, Superwall), configuring app stores (App Store Connect, Google Play), or automating dashboard tasks via browser. Triggers on "set up SDK", "configure analytics", "connect app store", "set up paywall", "mobile setup", "shipyard", or any mobile app infrastructure task.
---

# Shipyard

Professional mobile app development automation. One skill to set up, configure, and manage every SDK, CLI tool, and dashboard your app needs — across iOS (SwiftUI), Android (Kotlin/Compose), Flutter, and React Native (Expo).

## Philosophy

**CLI-first, browser-fallback, code-always.** Every action follows this priority:
1. **CLI tool** — fastest, scriptable, repeatable (adapty, asc, firebase, posthog)
2. **REST API** — when CLI doesn't cover it (curl with auth tokens)
3. **Playwright browser** — when dashboards have no API (visual builders, OAuth flows)
4. **Manual guidance** — last resort, with exact click-by-click instructions

## Platform Detection

Before any setup, detect the project platform:

```
project.yml / *.xcodeproj     → iOS (SwiftUI)
build.gradle.kts / build.gradle → Android (Kotlin/Compose)
pubspec.yaml                   → Flutter
package.json + app.json/app.config.js → React Native (Expo)
```

Adapt ALL SDK integration patterns to the detected platform:
- **iOS**: SPM packages in `project.yml` or `Package.swift`, Swift service classes, `@MainActor` patterns
- **Android**: Gradle dependencies, Kotlin service classes, Hilt DI
- **Flutter**: `pubspec.yaml` dependencies, Dart service classes, Provider/Riverpod
- **React Native**: `package.json` dependencies, TypeScript service modules, hooks

## SDK Registry

| SDK | Purpose | CLI | MCP | Install Skill |
|-----|---------|-----|-----|---------------|
| PostHog | Product analytics, session replay, feature flags | `posthog` (npm) | `mcp__posthog__*` | `npx skills add posthog-setup` |
| Adapty | Paywalls, subscriptions, A/B testing | `adapty` (npm) | — | — |
| Firebase | Auth, Firestore, Analytics, Crashlytics | `firebase` (npm) | — | — |
| Meta/Facebook | Attribution, ad events, deep links | — | — | — |
| AppsFlyer | Install attribution, deep links | — | — | — |
| Superwall | Paywall experimentation (optional) | `superwall` | — | `npx skills add superwall-ios-quickstart` |
| App Store Connect | App management, subscriptions, TestFlight | `asc` (brew) | — | `npx skills add ios-marketing-capture` |
| Google Play Console | Android app management | — | — | — |

## Architecture Pattern

All SDK integrations MUST follow the **AnalyticsRouter pattern** — a single fan-out service that routes events to all providers. Never call SDKs directly from ViewModels or Views.

```
Views → ViewModels → AnalyticsRouter → [Firebase, PostHog, Meta, AppsFlyer]
                   → AdaptyService   → [Adapty SDK]
```

**Key principles:**
- SDK services are `private` — only the router touches them
- Revenue events use provider-specific conventions (`$revenue` for PostHog, `AFEventParamRevenue` for AppsFlyer)
- Feature flags from PostHog are exposed via the router
- Opt-out/opt-in (GDPR/ATT) flows through the router

**Graceful fallbacks:** When API keys are placeholders, SDKs auto-disable via guard checks in `SDKKeys`. No crashes, no error UI — just silent no-ops with DEBUG console warnings.

## Browser Automation (Playwright)

When CLI/API doesn't cover a task (e.g., Adapty paywall visual builder), use Playwright MCP.

**Always dispatch Playwright work as a subagent** — never inline browser automation in the main context. Use the Agent tool with the appropriate model tier based on task complexity (see Model Selection below).

### Model Selection for Playwright Subagents

Pick the model based on how much reasoning the browser task requires:

| Model | Use when | Examples |
|-------|----------|---------|
| **Haiku** | Pure mechanical action — click, type, navigate, screenshot. No decisions needed. | Filling a form with known values, clicking a known button, navigating to a URL, taking screenshots for verification |
| **Sonnet** | Needs to understand UI structure, pick from options, adapt to what it sees on screen. | Selecting a paywall template, customizing copy fields, navigating an unfamiliar dashboard flow |
| **Opus** | Complex multi-step flows with branching decisions, error recovery, or ambiguous UI states. | Setting up a completely new dashboard with many unknown steps, recovering from auth failures mid-flow, cross-dashboard orchestration |

**Default:** Start with Haiku. If the task requires judgment calls (which template to pick, how to interpret UI), use Sonnet. Reserve Opus for flows that repeatedly fail or require deep reasoning about the UI state.

### Dispatching Playwright Subagents

Use the Agent tool. Always include in the prompt:
1. Current browser state (URL, what's visible)
2. Exact steps to perform (the more specific, the better for Haiku)
3. What copy/values to enter
4. What to return (screenshots paths, what succeeded/failed)

```
Agent({
  description: "Fill Adapty paywall form fields",
  model: "haiku",          // or "sonnet" / "opus"
  prompt: "The browser is already at https://app.adapty.io/paywalls/123/edit.
           Click the headline field (ref: e42), clear it, type 'Touch Grass First'.
           Click Save. Take a screenshot. Return: success/failure + screenshot path."
})
```

### Setup

Playwright MCP must be configured to use the user's existing Chrome profile:

```json
{
  "playwright": {
    "command": "<path-to>/playwright-mcp",
    "args": ["--browser", "chrome", "--user-data-dir", "<user-home>/Library/Application Support/Google/Chrome"]
  }
}
```

**Critical:** The user must close Chrome before Playwright can use the profile. Always warn before launching.

### Authentication Flow

1. Navigate to the target dashboard (e.g., `https://app.adapty.io`)
2. If redirected to login → click "Sign in with Google" → Chrome profile handles OAuth automatically
3. Wait for redirect back to dashboard
4. Proceed with automation

### Dashboard Operations

| Dashboard | What to automate | Model | How |
|-----------|-----------------|-------|-----|
| Adapty | Paywall visual builder, template selection | Sonnet | Playwright subagent — no API available |
| Adapty | Simple field edits, button clicks after builder is open | Haiku | Playwright subagent |
| PostHog | Project settings, dashboards | Haiku | PostHog MCP (`mcp__posthog__*`) or CLI preferred |
| Firebase | Project creation, service accounts | Haiku | `firebase` CLI preferred |
| App Store Connect | Everything | Haiku | `asc` CLI (covers 95% of operations) |
| AppsFlyer | Dashboard setup, complex flows | Sonnet | Playwright subagent (limited API) |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/shipyard` | Main entry — detect platform and guide to the right sub-command |
| `/shipyard:init` | Initialize SDK integrations for a new or existing mobile app |
| `/shipyard:abilities` | Audit installed CLIs, MCPs, skills — show ready vs missing |
| `/shipyard:setup <sdk>` | Deep setup for one SDK (posthog, adapty, firebase, meta, appsflyer, superwall) |
| `/shipyard:connect <store>` | Connect app stores — subscriptions, pricing, localizations, webhooks |
| `/shipyard:dashboard <service>` | Open and configure a dashboard via Playwright browser automation |
| `/shipyard:status` | Health check of all SDK integrations in the current project |
| `/shipyard:prices <territory>` | Set subscription pricing for a specific market |
| `/shipyard:init-skills` | Auto-install all platform-appropriate Claude Code skills for the project |
| `/shipyard:help` | Show all commands with examples |

---

### `/shipyard:init` — Initialize SDK integrations

Interactive setup wizard for a new or existing mobile app.

**Process:**

1. **Detect platform** — scan project files to identify iOS/Android/Flutter/RN
2. **Scan existing integrations** — check for already-installed SDKs (grep imports, check dependency files)
3. **Ask user** — "Which SDKs do you need?" with defaults:
   - [x] PostHog (analytics + session replay + feature flags)
   - [x] Firebase (auth + crashlytics)
   - [x] Adapty (paywalls + subscriptions)
   - [x] Meta (attribution)
   - [x] AppsFlyer (install attribution)
   - [ ] Superwall (optional — paywall experimentation)
4. **For each selected SDK:**
   a. Check if CLI is installed → install if missing
   b. Check if CLI is authenticated → authenticate if needed
   c. Check if API key exists → create app/project if needed, extract key
   d. Add SDK dependency to project (SPM/Gradle/pubspec/package.json)
   e. Create service class following the platform's patterns
   f. Wire into AnalyticsRouter (or create one if it doesn't exist)
   g. Add graceful fallback guards in SDKKeys
5. **Create SDKKeys config** — centralized key management with auto-derived enable flags
6. **Configure ATT/GDPR** — wire opt-in/opt-out through the router
7. **Validate** — build the project, check for errors

**Output:** Summary of what was set up, what keys are still placeholder, and next steps.

### `/shipyard:abilities` — Show available tools and gaps

Audit the development environment for mobile app tooling.

**Process:**

1. **Check installed CLIs:**
   ```bash
   which adapty firebase posthog asc superwall 2>/dev/null
   adapty auth status 2>/dev/null
   firebase login:list 2>/dev/null
   asc auth status 2>/dev/null
   ```
2. **Check MCP servers:**
   - Playwright MCP → connected? Chrome profile configured?
   - PostHog MCP → connected? Authenticated?
   - Context7 MCP → available for docs?
3. **Check installed skills:**
   ```bash
   ls ~/.claude-shared/skills/ | grep -E "superwall|ios-marketing|posthog|firebase|adapty"
   ```
4. **Report:**
   ```
   READY:
   ✅ adapty CLI v0.1.5 — authenticated as semih
   ✅ asc CLI v1.2.1 — authenticated as Runlock
   ✅ Playwright MCP — Chrome profile configured

   MISSING:
   ❌ posthog CLI — install: npm i -g posthog-cli
   ❌ firebase CLI — install: npm i -g firebase-tools
   ⚠️ superwall CLI — optional, install: brew install superwall

   SKILLS TO ADD:
   📦 npx skills add ParthJadhav/ios-marketing-capture -g
   📦 npx skills add superwall-ios-quickstart -g
   ```
5. **Auto-fix option:** "Want me to install the missing tools now?"

### `/shipyard:setup <sdk>` — Set up a specific SDK

Deep setup for one SDK. Available SDKs: `posthog`, `adapty`, `firebase`, `meta`, `appsflyer`, `superwall`.

**Example: `/shipyard:setup adapty`**

1. Check `adapty` CLI installed and authenticated
2. Check if app exists → `adapty apps list` → create if not
3. Extract SDK key → update `SDKKeys.swift` (or platform equivalent)
4. Create access level `premium`
5. Create products (weekly/monthly/annual) with platform product IDs
6. Create paywalls (onboarding + upgrade) with all products
7. Create placements matching code constants
8. Open Playwright → Adapty dashboard → pick paywall template → customize copy → publish
9. Set up App Store server notifications URL via `asc app-setup`
10. Validate: build project, check SDK initialization

### `/shipyard:connect <store>` — Connect app stores

Set up app store integrations. Available: `appstore`, `playstore`.

**Example: `/shipyard:connect appstore`**

1. Authenticate `asc` CLI if not already
2. Create subscription group
3. Create subscription products with localized pricing
4. Add localizations (detect from project — e.g., TR + EN)
5. Set App Store server notification URL (for Adapty/RevenueCat webhook)
6. Configure sandbox testers
7. Upload review screenshots if available

### `/shipyard:dashboard <service>` — Open and configure a dashboard

Use Playwright to automate dashboard configuration.

**Process:**

1. **Pre-flight:** Check Playwright MCP is connected
2. **Warn user:** "I need to open Chrome with your profile. Please close Chrome if it's open."
3. **Navigate** to the dashboard (adapty/posthog/firebase/appstoreconnect)
4. **Authenticate** — use Google SSO via Chrome profile
5. **Perform configuration** — template selection, settings changes, etc.
6. **Screenshot** each step for verification
7. **Report** what was configured

### `/shipyard:status` — Overall integration health check

Quick overview of all SDK integrations in the current project.

1. Read `SDKKeys` (or equivalent) — check which keys are real vs placeholder
2. Check each service file for proper guard patterns
3. Verify AnalyticsRouter wiring
4. Check dependency versions (outdated?)
5. Report:
   ```
   SDK Status:
   ✅ PostHog — key set, session replay enabled, ATT wired
   ✅ Adapty — key set, 2 paywalls, 3 products, webhook configured
   ⚠️ AppsFlyer — placeholder key, will silently disable
   ⚠️ Meta — no FACEBOOK_APP_ID in build settings
   ✅ Firebase — configured, anonymous auth active
   ```

### `/shipyard:prices <territory>` — Set subscription pricing

Recommend and configure subscription prices for a specific market.

1. Research competitive pricing for the territory
2. Map to Apple/Google price tiers
3. Create/update subscriptions via `asc` CLI
4. Add localizations for the territory
5. Report pricing table with savings percentages

### `/shipyard:init-skills` — Auto-install platform skills

Detects the project platform and installs all relevant Claude Code skills via `git clone` to `~/.claude-shared/skills/`.

**Process:**

1. **Detect platform** — scan project files (see Platform Detection above)
2. **Resolve skill directory** — `SKILLS_DIR="$HOME/.claude-shared/skills"`
3. **For each skill in the platform registry:**
   a. Check if `$SKILLS_DIR/<skill-name>/SKILL.md` already exists → skip if present
   b. `git clone <repo-url> $SKILLS_DIR/<skill-name>`
   c. If SKILL.md is nested (e.g., `<skill-name>/<nested-dir>/SKILL.md`), flatten: `cp -r <nested-dir>/* .`
   d. Verify `SKILL.md` exists at root level
4. **Update project CLAUDE.md** — read the project's `CLAUDE.md`, find the platform rules section, and add `Skill Reference` lines for every installed skill that isn't already listed. Each line follows the format:
   ```
   - **Skill Reference**: Use `<skill-name>` skill for <purpose>
   ```
   Only add references for skills relevant to the detected platform. Do NOT duplicate references that already exist in the file.
5. **Create `ai-rules/` folder** — if it doesn't exist, create `ai-rules/` in the project root with domain-specific rule files tailored to the detected platform. This follows the Zabłocki progressive-disclosure pattern: a `rule-loading.md` index tells the LLM which rules to load on demand.

   **For iOS projects, create these files:**
   - `ai-rules/rule-loading.md` — index of all rule files with loading triggers and keywords
   - `ai-rules/general.md` — core Swift engineering rules (always loaded): progressive architecture, error handling, dependency injection, localization, quality gates, anti-patterns
   - `ai-rules/view.md` — SwiftUI view rules: Liquid Glass API patterns, modifier order, design system tokens, animation patterns (staggered reveal, celebration, content transitions), reusable components list
   - `ai-rules/view-model.md` — ViewModel rules: @Observable pattern, computed derived state, async data loading, String(localized:), state ownership
   - `ai-rules/services.md` — services/SDK rules: AnalyticsRouter pattern, graceful SDK fallbacks, revenue event formatting, HealthKit/FamilyControls patterns
   - `ai-rules/testing.md` — testing rules: test behavior not implementation, mock dependency injection, focus areas, test structure

   Each rule file uses the `<primary_directive>`, `<rule_N priority="...">`, `<pattern name="...">`, `<checklist>`, and `<avoid>` XML-like tag structure for optimal LLM parsing.

   **Skip if `ai-rules/` already exists** — don't overwrite existing rule files.

6. **Update project CLAUDE.md** — two additions:
   a. Add a **Rule Index** section near the top pointing to `@ai-rules/rule-loading.md`
   b. Add `Skill Reference` lines for every installed skill not already listed
   Only add references for skills relevant to the detected platform. Do NOT duplicate.
7. **Report:** installed count, skipped count, any failures, CLAUDE.md references added, ai-rules created (yes/no)

**CLAUDE.md Skill Reference Templates (by platform):**

#### iOS Skill References
```markdown
- **Skill Reference**: Use `swiftui-liquid-glass` skill for Liquid Glass implementation patterns
- **Skill Reference**: Use `swiftui-ui-patterns` skill for SwiftUI best practices
- **Skill Reference**: Use `swift-concurrency-expert` skill for async/await patterns
- **Skill Reference**: Use `swiftui-pro` skill for advanced SwiftUI patterns and component design
- **Skill Reference**: Use `swift-concurrency-pro` skill for structured concurrency and actor patterns
- **Skill Reference**: Use `swift-architecture` skill for MVVM, Clean Architecture, and design patterns
- **Skill Reference**: Use `swift-security-expert` skill for iOS security best practices (keychain, encryption, ATT)
- **Skill Reference**: Use `swift-testing-pro` skill for Swift Testing framework patterns
- **Skill Reference**: Use `swiftdata-pro` skill for SwiftData persistence patterns
- **Skill Reference**: Use `core-data-expert` skill for Core Data patterns (if needed alongside SwiftData)
- **Skill Reference**: Use `app-store-aso` skill for App Store Optimization
- **Skill Reference**: Use `shipyard` skill for SDK integration, CLI orchestration, and app store operations
```

#### Android Skill References
```markdown
- **Skill Reference**: Use `mobile-android-design` skill for Material 3 patterns
- **Skill Reference**: Use `app-store-aso` skill for Play Store listing optimization
- **Skill Reference**: Use `shipyard` skill for SDK integration, CLI orchestration, and app store operations
```

**Platform Skill Registries:**

#### iOS Skills
| Skill Name | Repo | Purpose |
|------------|------|---------|
| swiftui-pro | `github.com/twostraws/SwiftUI-Agent-Skill` | Advanced SwiftUI patterns and best practices |
| swiftdata-pro | `github.com/twostraws/SwiftData-Agent-Skill` | SwiftData persistence patterns |
| swift-concurrency-pro | `github.com/twostraws/Swift-Concurrency-Agent-Skill` | Async/await and structured concurrency |
| swift-testing-pro | `github.com/twostraws/Swift-Testing-Agent-Skill` | Swift Testing framework patterns |
| swift-architecture | `github.com/efremidze/swift-architecture-skill` | Swift architecture patterns (MVVM, Clean, etc.) |
| swift-security-expert | `github.com/ivan-magda/swift-security-skill` | iOS security best practices |
| core-data-expert | `github.com/AvdLee/Core-Data-Agent-Skill` | Core Data patterns and migrations |
| app-store-aso | `github.com/timbroddin/app-store-aso-skill` | App Store Optimization |

**Note:** Skills already bundled in user config (swiftui-liquid-glass, swiftui-ui-patterns, swift-concurrency-expert, app-onboarding-questionnaire, shipyard, marketing-psychology, onboarding-cro) are NOT cloned — they are already available.

**Example output:**
```
Skills installed for iOS project:
✅ swiftui-pro — already installed, skipped
✅ swiftdata-pro — installed
✅ swift-concurrency-pro — installed
✅ swift-testing-pro — installed
✅ swift-architecture — already installed, skipped
✅ swift-security-expert — installed
✅ core-data-expert — installed
✅ app-store-aso — installed

6 installed, 2 skipped, 0 failed
```

#### Android Skills
| Skill Name | Repo | Purpose |
|------------|------|---------|
| app-store-aso | `github.com/timbroddin/app-store-aso-skill` | Store listing optimization |

_(Android skill registry will grow as community skills are published)_

#### Flutter Skills
_(Flutter skill registry will grow as community skills are published)_

#### React Native (Expo) Skills
_(React Native skill registry will grow as community skills are published)_

**Auto-trigger:** When `/shipyard:init` completes SDK setup, it should suggest running `/shipyard:init-skills` to install platform skills.

---

### `/shipyard:help` — Show all commands

Display the full command reference with examples.

---

## Tool Installation Commands

When abilities are missing, provide exact install commands:

```bash
# CLIs
npm install -g @playwright/mcp@latest
npm install -g adapty
npm install -g firebase-tools
brew install app-store-connect-cli  # provides `asc` binary

# Skills (clone to ~/.claude-shared/skills/)
# Use /shipyard:init-skills to auto-install all platform skills
# Manual install example:
SKILLS_DIR="$HOME/.claude-shared/skills"
git clone https://github.com/twostraws/SwiftUI-Agent-Skill.git "$SKILLS_DIR/swiftui-pro"
# If SKILL.md is nested, flatten: cd "$SKILLS_DIR/swiftui-pro" && cp -r swiftui-pro/* . 2>/dev/null

# MCP servers
claude mcp add playwright -- npx @playwright/mcp@latest
# PostHog MCP — available as built-in claude.ai MCP, authenticate via mcp__posthog__authenticate
```

## Chrome Session Management

**Always use the user's existing Chrome profile** for dashboard automation. This preserves:
- Google SSO sessions (Adapty, Firebase, PostHog)
- App Store Connect sessions
- Any dashboard sessions

**Config pattern (in settings.json `mcpServers`):**
```json
{
  "playwright": {
    "command": "/path/to/playwright-mcp",
    "args": ["--browser", "chrome", "--user-data-dir", "~/Library/Application Support/Google/Chrome"]
  }
}
```

**Important notes:**
- User MUST close Chrome before Playwright can use the profile (Chrome locks it)
- After Playwright is done, user can reopen Chrome normally
- The `--user-data-dir` path varies by OS:
  - macOS: `~/Library/Application Support/Google/Chrome`
  - Linux: `~/.config/google-chrome`
  - Windows: `%LOCALAPPDATA%\Google\Chrome\User Data`

## Dynamic Path Resolution

Never hardcode user-specific paths. Resolve dynamically:

```bash
# Home directory
HOME=$(eval echo ~)

# Node binary path
NODE_BIN=$(dirname $(which node))

# Chrome profile (macOS)
CHROME_PROFILE="$HOME/Library/Application Support/Google/Chrome"

# Project bundle ID
BUNDLE_ID=$(grep "PRODUCT_BUNDLE_IDENTIFIER" project.yml | head -1 | awk '{print $2}')
```

## Integration with Other Skills

| Skill | When to use together |
|-------|---------------------|
| `ship-wreck-check` | After `/shipyard:init` — verify SDK integration quality |
| `qgit` | After setup — commit and push changes |
| `ios-marketing-capture` | Capture raw in-app screenshots from simulator |
| `app-store-screenshots` | Generate marketing advertisement slides (Next.js) — headlines, mockup frames, multi-locale, export at all Apple sizes |
| `superwall-*-quickstart` | Platform-specific Superwall setup |
| `analytics-tracking` | Plan analytics event taxonomy |
| `app-store-optimization` | ASO after app store connection |
| `paywall-upgrade-cro` | Optimize paywall conversion after Adapty setup |
| `app-onboarding-questionnaire` | Design and build questionnaire-style onboarding flows (Duolingo/Noom pattern) |
| `swiftui-pro` | Advanced SwiftUI patterns — auto-installed by `/shipyard:init-skills` |
| `swift-concurrency-pro` | Async/await and structured concurrency — auto-installed by `/shipyard:init-skills` |
| `swift-testing-pro` | Swift Testing framework patterns — auto-installed by `/shipyard:init-skills` |
| `swift-architecture` | Architecture patterns (MVVM, Clean, etc.) — auto-installed by `/shipyard:init-skills` |
| `swift-security-expert` | iOS security best practices — auto-installed by `/shipyard:init-skills` |

## Rules

- **Never hardcode paths** — resolve dynamically from environment
- **Always check before installing** — `which <tool>` before `npm install -g`
- **Always authenticate before using** — check auth status before CLI operations
- **Always use graceful fallbacks** — placeholder keys = silent disable, not crash
- **Always follow platform conventions** — SPM for iOS, Gradle for Android, etc.
- **Always use the AnalyticsRouter pattern** — never call SDKs directly from UI
- **Always preserve existing code** — read before writing, extend don't replace
- **Always warn before Playwright** — user must close Chrome first
- **Revenue events need provider-specific formatting** — `$revenue` for PostHog, `AFEventParamRevenue` for AppsFlyer, etc.
- **Client SDK keys are safe to compile** — they're public tokens, not server secrets
