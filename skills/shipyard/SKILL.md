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

## Inner Skill: ios-simulator-skill

For ALL iOS simulator, build, test, and UI automation work, delegate to
the `ios-simulator-skill` (installed at `~/.claude-shared/skills/ios-simulator-skill/`).
It complements the SDK Registry below — SDK integration is shipyard's job,
build/test/simulator/UI automation is ios-simulator-skill's job.

It provides 22 Python scripts covering:
- Build + xcresult parsing with build cache (`build_and_test.py`)
- Simulator lifecycle (`simctl_boot.py`, `simctl_shutdown.py`, `simctl_create.py`, `simctl_delete.py`, `simctl_erase.py`, `sim_health_check.sh`)
- Semantic UI navigation via accessibility tree (`screen_mapper.py`, `navigator.py`, `gesture.py`, `keyboard.py`, `app_launcher.py`) — ~10 tokens vs 1.6K-6K for screenshots
- Accessibility audits, visual diffs, app state capture (`accessibility_audit.py`, `visual_diff.py`, `test_recorder.py`, `app_state_capture.py`, `model_inspector.py`)
- Push notifications, privacy permissions, clipboard, status bar overrides (`push_notification.py`, `privacy_manager.py`, `clipboard.py`, `status_bar.py`)
- Real-time log streaming with severity filtering (`log_monitor.py`)

Use these scripts instead of raw `xcrun simctl` / `xcodebuild` whenever
possible — they output structured JSON via `--json`, cache build results per-project,
and survive UI changes via semantic targeting on the accessibility tree.

## SDK Registry

| SDK | Purpose | CLI | MCP | Install Skill |
|-----|---------|-----|-----|---------------|
| PostHog | Product analytics, session replay, feature flags | `posthog` (npm) | `mcp__posthog__*` | `npx skills add posthog-setup` |
| Adapty | Paywalls, subscriptions, A/B testing | `adapty` (npm) | — | — |
| Firebase | Auth, Firestore, Analytics, Crashlytics | `firebase` (npm) | — | — |
| Meta/Facebook | Attribution, ad events, deep links | — | — | — |
| AppsFlyer | Install attribution, deep links | — | — | — |
| Superwall | Paywall experimentation (optional) | `superwall` | — | `npx skills add superwall-ios-quickstart` |
| App Store Connect | App management, subscriptions, TestFlight, metadata + screenshot sync | `asc` (brew) + custom Python client for full REST API | — | `npx skills add ios-marketing-capture` |
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

## Plan Execution & Build Cadence

**Scope:** Applies to every multi-task iOS/Android plan executed via `superpowers:subagent-driven-development`, `/shipyard:*` commands, or any session that's about to type `xcodebuild`. **This section overrides the generic "test after each step" cadence from `superpowers:writing-plans` / `superpowers:test-driven-development`** — those skills assume fast feedback loops; mobile native builds don't have one.

### Why a section on builds lives inside shipyard

Native iOS verification is the single most expensive action in the developer loop — a cold `xcodebuild test` on a real SDK-integrated app (Firebase + Adapty + PostHog + GRDB + Adhan) is 2–5 minutes. If you apply the generic "red→green→refactor, run tests after each change" pattern, a 3-file edit becomes a 20-minute session for zero extra signal. The rules here are cost-aware defaults.

### When to batch vs. keep solo

| Task shape | Strategy |
|------------|----------|
| Mechanical UI screens with concrete spec code (independent views, components, placeholder wiring) | Batch — one implementer, one combined review |
| Business logic (ViewModel methods, state machines, service contracts) | Solo — two-stage spec + quality review |
| Routing / activation forks / deep links | Solo — two-stage review |
| Cross-cutting analytics wiring | Solo — two-stage review |
| Localization strings | Direct edit; no review loop |
| Single-file paste-verbatim edits from a plan | Direct edit in main session; no subagent at all |
| Manual smoke / device walkthrough | User-driven; never dispatch |
| Final batched commit | Main session; never dispatch |

### Reviewer model tiering

| Model | Use for | Examples |
|-------|---------|----------|
| **Haiku** | Layout, naming, imports, glass usage, switch exhaustiveness, analytics key presence | Confirming `.glassEffect()` on cards, confirming a placeholder view exists per enum case |
| **Sonnet** | Pattern conformance, moderate multi-file coherence | Verifying ServiceContainer usage, reducer case coverage |
| **Opus** | State machine correctness, async safety, spec reconciliation | Reviewing `OnboardingVM.commit(choice:)` or activation-fork routing |

**Default:** Haiku for mechanical reviews, Opus for logic/routing/analytics reviews.

### Subagent-vs-direct-edit break-even

Before dispatching any subagent, ask: *is the edit mechanical enough that a single tool call in the main session would be faster and clearer?* A Haiku subagent dispatching on a "paste 100 lines into one file" task has routinely taken 6–8 minutes (12+ tool-use retries, redundant self-verification) when the main session would have done it in under a minute. Dispatch a subagent when work exceeds ~4 independent tool calls, when the implementer needs to iterate against build/test output, or when you want to isolate context from the main session. Do the edit inline otherwise.

### Reconciliation before dispatch

Plans drift from the codebase between authoring and execution — verify mock service constructors, VM init parameter order, repository method names, `@testable import` module name, and analytics key properties before briefing the implementer. A 2-minute reconciliation prevents a 30-minute failed implementation.

### Commit discipline

Implementer subagents must NOT `git add` or `git commit` per task during a multi-task plan. One batched commit (or a small handful of logical commits) at plan end from the main session. State this explicitly in every implementer prompt — they default to committing per task otherwise.

### Verification cadence — the cost-aware iOS loop

**Run `xcodebuild ... test` at the END of a batch, not per task.** Test-per-task inflates runtime 5–10× without adding signal when tasks share no logic.

**Build-trigger checklist — only rebuild when one of these is true:**
- `pbxproj` regenerated (new files added via xcodegen)
- Shared types / protocols changed (module surface evolved)
- A logic task extended an existing test suite
- You crossed a `@MainActor` / concurrency boundary you're unsure about
- The final verification pass at the end of the batch

**Do NOT rebuild after:** pasting verbatim code inside an existing file, adding string-catalog entries, editing comments/whitespace/imports that don't change the module surface, or changing literal values inside an already-typed expression.

### xcodebuild speed flags — always use these

```bash
export BOOTED_UDID=$(xcrun simctl list devices booted | awk -F'[()]' '/Booted/{print $2; exit}')
[ -z "$BOOTED_UDID" ] && xcrun simctl boot "iPhone 15" && \
  BOOTED_UDID=$(xcrun simctl list devices | awk -F'[()]' '/iPhone 15 .*Booted/{print $2; exit}')

xcodebuild test \
  -project <Project>.xcodeproj \
  -scheme <Scheme> \
  -destination "platform=iOS Simulator,id=$BOOTED_UDID" \
  -derivedDataPath .build-xcode \
  -skipPackagePluginValidation \
  -skipMacroValidation \
  -quiet \
  2>&1 | tail -40
```

| Flag | Why | Savings |
|------|-----|---------|
| `-derivedDataPath .build-xcode` | Pin a per-repo cache so runs share compiled modules | 3–5 min → 30–60s on warm runs |
| `-destination "...id=$BOOTED_UDID"` | Reuse an already-booted simulator instead of respawning | 30–60s per run |
| `-skipPackagePluginValidation` | Skip first-run interactive SPM plugin prompt | 10–20s |
| `-skipMacroValidation` | Same, for Swift macros | 10–20s |
| `-disableAutomaticPackageResolution` (after first run) | Skip SPM freshness check when Package.resolved hasn't changed | 10–30s |
| `-quiet` + `2>&1 | tail -40` | Keep stdout small so only the summary enters context | context budget |

**Never mix destinations.** Using both `generic/platform=iOS Simulator` (build-only) and `platform=iOS Simulator,name=iPhone 15` (tests) in the same session busts the DerivedData cache and doubles total time.

### xcodegen gotchas

- **Always prefix in sandboxed shells:** `USER=$(whoami) LOGNAME=$(whoami) xcodegen generate`.
- **New source files need `xcodegen generate`.** Most `project.yml` files use the default `group` type for `sources:` entries, so filesystem additions are NOT auto-picked-up — the file will be on disk but not a target member, and `@testable import <App>` will fail with `No such module`. Run `xcodegen generate` immediately after creating any new `.swift` file under a target folder.
- **`type: folder` sources are the exception** — Xcode treats them as folder references that auto-pick-up. Used for resource folders (e.g. `Resources/EzkarImages`), rarely for source code.

### Trust xcodebuild, not SourceKit

The in-editor indexer (SourceKit LSP in Cursor/VSCode, or pre-reindex Xcode) routinely shows `No such module 'Adhan'` / `No such module 'Testing'` immediately after `xcodegen generate` or a file add — these clear on their own within seconds to a minute. Do not rewrite code to make the LSP happy; run `xcodebuild` and believe it.

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
| `/shipyard:asc-sync` | Push metadata + screenshots to App Store Connect for all locales (one command) |
| `/shipyard:dashboard <service>` | Open and configure a dashboard via Playwright browser automation |
| `/shipyard:status` | Health check of all SDK integrations in the current project |
| `/shipyard:prices <territory>` | Set subscription pricing for a specific market |
| `/shipyard:init-skills` | Auto-install all platform-appropriate Claude Code skills for the project |
| `/shipyard:learn-lessons` | Analyze current project end-to-end and extract lessons — writes `docs/LESSONS-LEARNED.md` + promotes generalizable lessons to `~/.claude-shared/shipyard-lessons/` |
| `/shipyard:update-learned-lessons` | Scan current project against every applicable lesson in the shared library, report gaps, offer to apply fixes (platform-aware) |
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

Reality check: the community `asc` CLI covers TestFlight and some subscription ops, but **NOT** full metadata or screenshot sync. For the "ship v1.0" workflow below, use the App Store Connect REST API via a Python client (see the **App Store Connect REST API** section later).

**Full v1.0 release prep workflow:**

1. **Auth setup (one-time per project)**
   - Create API key at https://appstoreconnect.apple.com/access/integrations/api with **Admin** or **App Manager** role
   - Download `.p8` ONCE (Apple never shows it again)
   - Place at `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8` (chmod 600)
   - Export in `~/.zshrc`: `APP_STORE_API_KEY`, `APP_STORE_API_ISSUER`

2. **Subscriptions (if monetized)**
   - Create subscription group via `asc` CLI or Playwright
   - Create subscription products with localized pricing
   - Set App Store server notification URL (for Adapty/RevenueCat webhook)
   - Configure sandbox testers

3. **Metadata sync (use `/shipyard:asc-sync`)** — see next section. Covers:
   - App info: name, subtitle, privacy URL, primary category per locale
   - Version: description, keywords, promotional text, release notes, marketing URL, support URL per locale
   - Version-level: copyright, release type
   - Review contact + notes
   - Screenshots per locale per device class

4. **Localization matrix**
   - Default locale = primary (e.g., `tr` for a Turkish-first app)
   - Add secondary locales (`en-US`, `ru`, etc.) even if app UI is single-language — App Store listings can still be multi-locale
   - Turkish diacritics must be correct: `Müslüman` not `Musluman`, `ÖZELLİKLER` not `OZELLIKLER`

### `/shipyard:asc-sync` — Push metadata + screenshots to App Store Connect

One-command sync for app listing: metadata for all locales + screenshots per locale + review info + category. Idempotent — safe to re-run.

**Prereq structure in project:**
```
marketing/
├── asc-metadata/
│   ├── shared.json                   # URLs, copyright, review contact, review notes, primary_category, release_type
│   ├── <locale>/
│   │   ├── name.txt                  # ≤30 chars (App Store limit)
│   │   ├── subtitle.txt              # ≤30 chars
│   │   ├── description.txt           # ≤4000 chars
│   │   ├── keywords.txt              # ≤100 chars, comma-separated, no spaces after commas
│   │   ├── promotional_text.txt      # ≤170 chars, editable anytime
│   │   └── release_notes.txt         # ≤4000 chars (ignored on first version)
└── asc-screenshots/
    └── <locale>/
        ├── iphone-6-9/*.png          # APP_IPHONE_67: 1290×2796 (or APP_IPHONE_69: 1320×2868)
        ├── iphone-6-5/*.png          # APP_IPHONE_65: 1242×2688
        └── ipad-12-9/*.png           # APP_IPAD_PRO_129: 2048×2732
```

**Execution order (the sync script does this):**

1. `GET /apps?filter[bundleId]=<bundle>` → resolve `app_id`
2. `GET /apps/<app_id>/appStoreVersions?filter[appStoreState]=PREPARE_FOR_SUBMISSION,...` → `version_id`
3. `GET /apps/<app_id>/appInfos` → pick editable → `app_info_id`
4. `PATCH /appInfos/<app_info_id>` — primaryCategory relationship (e.g., `LIFESTYLE`, `HEALTH_AND_FITNESS`)
5. `PATCH /appStoreVersions/<version_id>` — copyright, releaseType (`MANUAL` / `AFTER_APPROVAL` / `SCHEDULED`)
6. `PATCH` or `POST /appStoreReviewDetails` — contact name/phone/email + review notes
7. For each locale:
   - Upsert `appInfoLocalization` (name, subtitle, privacyPolicyUrl)
   - Upsert `appStoreVersionLocalization` (description, keywords, promotionalText, marketingUrl, supportUrl)
   - Try `PATCH whatsNew` separately — **catch `STATE_ERROR`** (first-version releases reject whatsNew)
   - Upsert `appScreenshotSet` per display type
   - Delete existing screenshots in set (clean slate per sync)
   - Upload new screenshots via 3-phase handshake (reservation → binary PUT → commit with MD5)

**Idempotency patterns (must implement in the sync script):**
- If `POST` returns `409 DUPLICATE`: refetch and `PATCH` instead
- If `PATCH` of `whatsNew` returns `409 STATE_ERROR`: skip silently on first-release versions
- If screenshot set doesn't exist: `POST`, otherwise reuse existing set ID
- Always wipe existing screenshots before upload to avoid stale mixed state

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

   **CRITICAL — Lazy-load discipline:** The project `CLAUDE.md` must reference ONLY `@ai-rules/rule-loading.md` (the index). Do NOT add `@ai-rules/general.md` or any other ai-rule file to `CLAUDE.md` via `@` — doing so defeats the progressive-disclosure design and silently costs ~130+ lines of context on every turn, even for tasks that don't touch Swift code (planning, docs, file lookups). `general.md` is loaded by the LLM on Swift code read/write triggers, not eagerly.

   **CRITICAL — Strict-but-fast philosophy:** Rule files enforce discipline (typed errors, DI, immutability, no magic numbers) but MUST NOT bloat every code change with ceremony. Apply these scope rules when writing rule files for a new project:

   - **Protocol + mock requirement is scoped**, not universal. Require protocols only for services that are (a) unit-tested with mocks, (b) routed/fanned-out (analytics routers), or (c) network-facing (repos, auth, paywall, LLM clients). Simple concrete helpers (image resize, theme math, pure utility wrappers) stay concrete-only. Phrase rule 4 accordingly.
   - **Localization is phased.** Views always use key-based localization (e.g. `Text("key")` for SwiftUI auto-extraction). VMs/Services are allowed raw English during the English-only shipping window; flip to `String(localized:)` in the same PR that adds the second locale. Phrase rule 5 accordingly — do NOT write "every user-facing string must be a localization key" as an absolute.
   - **Quality gates in ONE place.** Put a consolidated, scope-grouped `Session Quality Gates` block in `rule-loading.md`. Do NOT duplicate checklists into `general.md`, `view.md`, `view-model.md`, `services.md`, `testing.md` — each of those files should have a one-line pointer "See `rule-loading.md` → Session Quality Gates". Otherwise the LLM runs the same checklist 5× per task.
   - **File-size limits are soft guidance, not blockers.** 200-line view soft cap, 400-line file soft cap, 800-line hard cap. Don't force mid-implementation refactors before the feature is stable.

   **For iOS projects, create these files:**
   - `ai-rules/rule-loading.md` — index of all rule files with loading triggers and keywords (MUST list `app-store.md` with triggers: "submit", "release", "screenshot", "metadata", "ASC", "App Store Connect", "localization", "review notes")
   - `ai-rules/general.md` — core Swift engineering rules (**trigger-loaded on first Swift code read/write**, NOT via `@` in CLAUDE.md): progressive architecture, error handling, dependency injection, localization, quality gates, anti-patterns
   - `ai-rules/view.md` — SwiftUI view rules: Liquid Glass API patterns, modifier order, design system tokens, animation patterns (staggered reveal, celebration, content transitions), reusable components list, **`SINGLE_COMPONENT_PER_STATE`** (never render two views for the same piece of state — pick the most-contextual one and remove duplicates), **`ONE_TRUTH_PER_AFFORDANCE`** (an action lives in exactly one place per screen)
   - `ai-rules/view-model.md` — ViewModel rules: @Observable pattern, computed derived state, async data loading, String(localized:), state ownership
   - `ai-rules/services.md` — services/SDK rules: AnalyticsRouter pattern, graceful SDK fallbacks, revenue event formatting, HealthKit/FamilyControls patterns
   - `ai-rules/testing.md` — testing rules: test behavior not implementation, mock dependency injection, focus areas, test structure
   - `ai-rules/app-store.md` — App Store Connect submission readiness: metadata file layout, locale matrix, character limits, Turkish/diacritic correctness, screenshot specs, review info, idempotent sync patterns (see template below)

   **`rule-loading.md` trigger block for `app-store.md` (add to the trigger index):**

   ```
   ### app-store.md - App Store Connect Submission Readiness
   **Load when:**
   - Preparing for App Store submission or TestFlight release
   - Running `/shipyard:asc-sync`
   - Editing files under `marketing/asc-metadata/` or `marketing/asc-screenshots/`
   - Adding a new locale to the App Store listing
   - Reviewing/fixing screenshot sizes, character limits, or review info
   - Debugging ASC API 401/409 errors

   **Keywords:** App Store, ASC, asc-sync, submission, metadata, screenshot, localization, keywords, description, review notes, TestFlight, promotional text, release notes, locale, Turkish diacritics
   ```

   Each rule file uses the `<primary_directive>`, `<rule_N priority="...">`, `<pattern name="...">`, `<checklist>`, and `<avoid>` XML-like tag structure for optimal LLM parsing.

   **`ai-rules/app-store.md` template contents (copy into the file):**

   ```markdown
   <primary_directive>
   Before invoking `/shipyard:asc-sync` or submitting to App Store Connect, the project MUST have complete, validated metadata for every locale and screenshots at the correct display-type resolutions. Broken submissions are expensive: rejections delay releases by days.
   </primary_directive>

   <rule_1 priority="critical">
   **Metadata file layout is fixed.** The sync script expects exactly this structure. Do not invent new paths.

   ```
   marketing/
   ├── asc-metadata/
   │   ├── shared.json          (urls, copyright, review_contact, review_notes, primary_category, release_type)
   │   └── <locale>/            (e.g. tr, en-US, ru, ar)
   │       ├── name.txt             ≤30 chars
   │       ├── subtitle.txt         ≤30 chars
   │       ├── description.txt      ≤4000 chars
   │       ├── keywords.txt         ≤100 chars, comma-separated, NO space after comma
   │       ├── promotional_text.txt ≤170 chars (editable post-release)
   │       └── release_notes.txt    ≤4000 chars (ignored on v1.0)
   └── asc-screenshots/<locale>/<display-slug>/*.png
   ```
   </rule_1>

   <rule_2 priority="critical">
   **Character limits are enforced by Apple, not by the sync script.** The script just uploads — Apple rejects at submission time. Validate locally before running sync:
   - name ≤ 30, subtitle ≤ 30
   - keywords ≤ 100 total chars (including commas)
   - promotional_text ≤ 170
   - description ≤ 4000
   </rule_2>

   <rule_3 priority="critical">
   **Turkish and non-ASCII diacritics must be correct.** Common mojibake from copy-paste:
   - ✅ Müslüman, günlük, ÖZELLİKLER, İmsak, Öğle, Akşam
   - ❌ Musluman, gunluk, OZELLIKLER, Imsak, Ogle, Aksam

   Run a grep for ASCII-only variants of Turkish words before every sync. Same discipline for Arabic (`ar`), Russian (`ru`), German (`de`).
   </rule_3>

   <rule_4 priority="high">
   **Locales are independent of in-app language.** A Turkish-only app can (and should) have en-US and ru App Store listings. The listing text drives discovery; the app can be single-language.
   </rule_4>

   <rule_5 priority="high">
   **Screenshots must match display-type specs exactly.** Apple rejects with cryptic errors on off-by-one resolutions:

   | Slug | Resolution | Maps to |
   |---|---|---|
   | `iphone-6-9` | 1290×2796 | `APP_IPHONE_67` (covers 6.7"+6.9" in practice) |
   | `iphone-6-5` | 1242×2688 | `APP_IPHONE_65` |
   | `ipad-12-9` | 2048×2732 | `APP_IPAD_PRO_129` |

   If source captures are 1206×2622 (iPhone 17 Pro native), upscale to 1290×2796 with aspect-preserving black letterbox padding. Never stretch.

   3–10 screenshots per set. Same 10 images can be reused across locales when the UI is single-language.
   </rule_5>

   <rule_6 priority="high">
   **Review info is required before first submission.**
   - `shared.json.review_contact` — full name, phone with country code, email that Apple reviewers can actually reach
   - `shared.json.review_notes` — if the app needs a test account, include login credentials here. If it uses HealthKit/FamilyControls/special entitlements, document the permission flow
   - Missing review info = instant rejection with "Guideline 2.1"
   </rule_6>

   <rule_7 priority="medium">
   **Release notes (`whatsNew`) are NOT editable on v1.0.** Apple's logic: there's nothing "new" about a first release. The sync script catches `409 STATE_ERROR` and skips silently. For v1.0 builds, leave `release_notes.txt` empty or don't create it — avoid churn.
   </rule_7>

   <rule_8 priority="medium">
   **Primary category matters for discoverability.** Use the closest Apple category. Examples:
   - Prayer/religion apps → `LIFESTYLE`
   - Habit/health trackers → `HEALTH_AND_FITNESS`
   - Productivity/todo → `PRODUCTIVITY`

   Secondary category is set in ASC UI, not the sync script (REST limitation).
   </rule_8>

   <rule_9 priority="medium">
   **Release type decides when users get the update.**
   - `MANUAL` — release when I click the button (safest for risky changes)
   - `AFTER_APPROVAL` — release immediately after review passes
   - `SCHEDULED` — release at a specific date/time (requires `scheduledReleaseDate`)

   Set in `shared.json.release_type`.
   </rule_9>

   <pattern name="Pre-sync validation checklist">
   Run this BEFORE `/shipyard:asc-sync`:
   - [ ] All locale folders present with all 6 .txt files
   - [ ] Character counts under limits (`wc -m marketing/asc-metadata/*/*.txt`)
   - [ ] Turkish diacritics verified (grep for `Musluman`, `gunluk`, `OZELLIKLER` → should return nothing)
   - [ ] Keywords have no trailing spaces after commas (grep for `, ` in keywords.txt → should return nothing)
   - [ ] Screenshots resized to exact display-type resolution (imagemagick `identify` to verify)
   - [ ] `shared.json` has valid review_contact (reachable phone + email)
   - [ ] `APP_STORE_API_KEY` + `APP_STORE_API_ISSUER` env vars set
   - [ ] `.p8` file exists at `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`
   - [ ] Key role is **Admin** or **App Manager** (not Developer)
   </pattern>

   <pattern name="Idempotent re-runs">
   The sync is designed to be safe to re-run. Know what it does:
   - `POST` returns `409 DUPLICATE` → script falls back to GET + PATCH
   - `PATCH whatsNew` returns `409 STATE_ERROR` → script skips silently (v1.0)
   - Screenshot sets: existing set is reused, its contents are wiped and re-uploaded each run
   - Stale sets from old display types (e.g. leftover `APP_IPHONE_61`) must be cleaned manually — they cause "mixed sizes" warnings in ASC UI
   </pattern>

   <checklist>
   When adding a new locale:
   - [ ] Create `marketing/asc-metadata/<new-locale>/` with all 6 files
   - [ ] Create `marketing/asc-screenshots/<new-locale>/iphone-6-9/` (reuse primary-locale PNGs if UI is single-language)
   - [ ] Validate character limits and diacritics
   - [ ] Add locale to the sync script's locale list (if it has a hardcoded list)
   - [ ] Dry-run: `python3 Scripts/asc-sync.py --dry-run --locales <new-locale>`
   - [ ] Live run: `python3 Scripts/asc-sync.py --locales <new-locale>`
   - [ ] Verify in ASC UI that listing appears correctly
   </checklist>

   <avoid>
   - Hardcoding English copy for non-English locales ("en-US fallback" is lazy and tanks conversion)
   - Committing raw screenshots to git (binary bloat) — commit only the text metadata; screenshots are regenerated by capture scripts
   - Editing listing copy in the ASC web UI after the first sync (changes get overwritten on next sync — edit the `.txt` files instead)
   - Re-running sync without validating character counts — Apple may accept upload and reject at submission
   - Using `APP_IPHONE_61` (6.1") as the primary set — Apple now derives smaller displays from `APP_IPHONE_67`
   - Storing `.p8` files inside the repo — keychain or `~/.appstoreconnect/` only, chmod 600
   </avoid>
   ```

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

### `/shipyard:learn-lessons` — Extract lessons from the current project

Analyze the current project end-to-end (git history, plans, architecture, SDK integrations, localization, extensions) and capture what was learned. Produces a project-local retrospective document and promotes generalizable lessons to the shared library at `~/.claude-shared/shipyard-lessons/`.

**Process:**

1. **Detect platform** — same signals as `/shipyard:init` (iOS, Android, Flutter, RN Expo)
2. **Gather project intelligence** — `git log`, plans folder, architecture docs, SDK fingerprints, localization surface, extension targets, memory records
3. **Extract lessons across 10 dimensions** — architecture, platform, SDK, process, product, localization, performance, security, deployment, design — asking "what pattern worked?" and "what mistake did we make?" for each
4. **Classify each lesson** — polarity (`require` / `avoid`), severity (critical / high / medium / low), scope (project-specific vs generalizable)
5. **Write `docs/LESSONS-LEARNED.md`** — systematic table format (summary table, category tables, metrics snapshot, top takeaways)
6. **Promote generalizable lessons** — create `lessons/L-XXX-NNN-*.md` files in `~/.claude-shared/shipyard-lessons/lessons/` with full frontmatter, Detect shell block, Fix steps, worked examples
7. **Dedupe** — before creating a new lesson, scan existing ones; if substantially the same, update `last_verified` and add to `## Also observed in` instead
8. **Update `INDEX.md`** — append new rows, keep sorted by ID, update totals and source-projects table
9. **Commit** — `docs: learned-lessons for <project>` and `docs(shipyard-lessons): add L-XXX-NNN from <project>`

**Output:** Compact summary showing the project-local doc path, new library IDs, reinforced existing IDs, top 3 takeaways.

**When to use:** At any project milestone, after shipping a major feature, or as a retrospective. Every project you ship should make the next one easier.

**Library conventions:**
- ID scheme: `L-IOS-NNN` (iOS), `L-AND-NNN` (Android), `L-FLU-NNN` (Flutter), `L-RNE-NNN` (RN/Expo), `L-CRS-NNN` (cross-platform), `L-PRC-NNN` (process). IDs never reused.
- Filenames: kebab-case, imperative (`register-extension-bundle-ids-early.md`)
- Every lesson must cite a commit hash, file path, or memory record — never invented

### `/shipyard:update-learned-lessons` — Apply the lessons library to this project

Scan the current project against every applicable lesson in `~/.claude-shared/shipyard-lessons/` and apply the fixes where gaps are detected. Platform-aware — only runs lessons tagged for the detected platform plus cross-platform and process lessons.

**Process:**

1. **Detect platform** — same logic as `/shipyard:learn-lessons`
2. **Load applicable lessons** — read `INDEX.md`, filter by matching `platforms:` frontmatter (plus `all`/`cross-platform` and all `L-PRC-*`)
3. **Run each Detect check** — either the `# detect:` shell block (exit 0 = pattern PRESENT) or a manual checklist
4. **Classify each lesson:**
   - ✅ applied — require polarity + pattern present, OR avoid polarity + mistake absent
   - ⚠️ gap — require polarity + pattern absent, OR avoid polarity + mistake present
   - ❓ indeterminate — manual checklist, script errored, or Detect inconclusive
   - ➖ not applicable — `applies_when` precondition not satisfied
5. **Present gap report** — grouped by severity (CRITICAL + HIGH shown by default; `--all` for MEDIUM/LOW)
6. **Offer to apply fixes** — batch mode or per-lesson y/N confirmation; automated where a `# fix:` shell block exists, manual-guided otherwise
7. **Re-verify after each fix** — re-run Detect; if still failing, flag for human review
8. **Update `docs/LESSONS-LEARNED.md`** — append to `## Update log` with applied/deferred IDs
9. **Commit** — `chore: apply shipyard lessons L-XXX-NNN, L-YYY-NNN`

**Flags:**
- `--all` — include MEDIUM and LOW severity in the report (default: critical + high only)
- `--dry-run` — detect and report only, never apply
- `--only <id>` — run a single lesson by ID
- `--category <name>` — filter by category (sdk, architecture, process, …)
- `--auto` — apply CRITICAL + HIGH automated fixes without per-lesson confirmation (use with caution)

**Safety rules:**
- Platform filter is mandatory — never run an Android-tagged lesson on an iOS project
- Never apply a fix whose Detect verification still fails afterward — flag instead
- Never modify library lessons from this command — that's `/shipyard:learn-lessons`'s job
- Fixes touching `.github/`, `Fastfile`, or `settings.json` should be proposed via PR, not applied directly

**When to use:** After `/shipyard:init` on a new project (proactive gap check), when picking up a project after a pause, or before a release cut to catch regressions against known good patterns.

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
| `app-store-screenshots-2` | AI-driven screenshot generation — analyzes codebase to discover features, generates copy, builds slides |
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

## Figma Integration

Organize screenshots and assets in Figma for design review and App Store submission prep.

### What Figma REST API CAN do
- **Read** file structure, pages, nodes, styles, components
- **Export** existing nodes as PNG/SVG/PDF
- **Update** image fills on existing nodes (replace, not create)
- **Post** comments on frames
- **Read** component/style metadata

### What Figma REST API CANNOT do
- Create new nodes (frames, rectangles, text) on canvas
- Place/position images on a page
- Create new pages
- Arrange layouts or set auto-layout properties

### Figma REST API usage
```python
import urllib.request, json

# Get file structure
req = urllib.request.Request(
    f"https://api.figma.com/v1/files/{FILE_KEY}?depth=1",
    headers={"X-Figma-Token": FIGMA_TOKEN}
)
data = json.loads(urllib.request.urlopen(req).read())

# Export a node as PNG
req = urllib.request.Request(
    f"https://api.figma.com/v1/images/{FILE_KEY}?ids={NODE_ID}&format=png&scale=2",
    headers={"X-Figma-Token": FIGMA_TOKEN}
)
```

### Recommended workflow
Since programmatic image placement is not possible, use this workflow:

1. **Generate screenshots** — use `app-store-screenshots` or `app-store-screenshots-2` skill to export PNGs
2. **Prepare Figma file** — create frames/pages manually in Figma (or use existing ones)
3. **Import to Figma** — drag-and-drop exported PNGs onto the canvas, or use **Cmd+Shift+K** (Place Image) to fill existing frames
4. **Use REST API for reads** — verify file structure, export finalized assets, post review comments

### Figma MCP (not currently available)
As of 2026-04, Figma's official Dev Mode MCP (`figma-developer-mcp`) is **read-only** — it inspects designs for code generation but cannot create or modify canvas nodes. No write-capable Figma MCP exists yet. If one becomes available, it would be the preferred method.

### Token resolution
- Check env var `FIGMA_PERSONAL_TOKEN` first
- If not set, ask the user for their Figma Personal Access Token
- NEVER hardcode or store tokens in files
- Remind user to rotate token after use if shared in conversation

### When to use
- After `app-store-screenshots` export — read Figma file structure, post comments for review
- After `ios-marketing-capture` — guide user on importing raw screenshots into Figma
- After `/shipyard:connect appstore` — verify asset organization before submission

## App Store Screenshot Skills

Two screenshot generator skills are available. Choose based on your needs:

| Skill | Approach | Best for |
|-------|----------|----------|
| `app-store-screenshots` | Next.js project, manual copy input, pixel-perfect control | When you have specific copy and know exactly what each slide should look like |
| `app-store-screenshots-2` | AI-driven, analyzes codebase for features, generates copy automatically | Quick-start when you want AI to figure out what to highlight |

Both support multi-locale, export at all Apple required sizes, and iPhone mockup frames.

## App Store Connect REST API

The `asc` CLI covers TestFlight and some subscription operations, but full metadata and screenshot sync require the REST API directly. Build a small Python client — it's ~100 LOC and replaces a mess of curl commands and brittle browser automation.

### Auth setup

1. **Create API key** at https://appstoreconnect.apple.com/access/integrations/api
   - Role: **Admin** or **App Manager** (Developer role cannot edit App Store listings — you'll get 401 on every metadata endpoint even with a valid JWT)
2. **Download the `.p8` exactly ONCE** — Apple never shows it again. If lost, revoke and regenerate.
3. **Store at fixed path:**
   ```
   ~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8  (chmod 600)
   ```
4. **Export in `~/.zshrc`:**
   ```bash
   export APP_STORE_API_KEY="<10-char key ID>"
   export APP_STORE_API_ISSUER="<UUID from ASC Integrations page>"
   ```

### JWT signing — the one gotcha

App Store Connect requires ES256 with signature in **raw r||s** format per RFC 7515 §A.3.

**⚠ PyJWT 1.x emits DER-encoded ECDSA signatures, which Apple rejects with a generic 401.** The JWT looks perfect, the issuer matches, the key has Admin role, `date -u` matches Apple's clock — and it still fails. This wasted several hours of debugging on a real project.

**Solution:** Either use PyJWT ≥2.0 or sign with `cryptography` directly. The `cryptography` approach has no version-drift risk:

```python
import base64, json, time
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def make_token(key_id: str, issuer: str, p8_path: Path, ttl: int = 1200) -> str:
    pk = serialization.load_pem_private_key(p8_path.read_bytes(), password=None)
    now = int(time.time())
    header = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    payload = {"iss": issuer, "iat": now, "exp": now + ttl, "aud": "appstoreconnect-v1"}
    h = _b64url(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    der = pk.sign(f"{h}.{p}".encode(), ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(der)
    raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return f"{h}.{p}.{_b64url(raw)}"
```

Apple tokens max out at **20 minutes** (`exp - iat ≤ 1200`). Mint fresh per run; don't cache.

### The resource tree

App Store Connect's data model isn't obvious from the docs. Keep this map handy:

```
app (bundle ID resolves here)
├── appInfos
│   └── appInfoLocalizations (one per locale)
│       ├── name                ← app name per locale
│       ├── subtitle            ← app subtitle per locale
│       └── privacyPolicyUrl
│   └── primaryCategory         ← LIFESTYLE, HEALTH_AND_FITNESS, etc.
└── appStoreVersions (one editable at a time)
    ├── copyright
    ├── releaseType              ← MANUAL / AFTER_APPROVAL / SCHEDULED
    ├── appStoreReviewDetail     ← review contact + notes
    └── appStoreVersionLocalizations (one per locale)
        ├── description
        ├── keywords             ← comma-separated, no trailing spaces, ≤100 chars
        ├── promotionalText      ← editable anytime, ≤170 chars
        ├── whatsNew             ← release notes, NOT editable on v1.0 initial release
        ├── marketingUrl
        ├── supportUrl
        └── appScreenshotSets (one per display type)
            └── appScreenshots (3–10 per set)
```

**Critical distinction:** `name`/`subtitle` live on `appInfoLocalization` (app-wide). `description`/`keywords`/`whatsNew` live on `appStoreVersionLocalization` (version-specific). Beginners confuse these and keep hitting the wrong endpoint.

### Finding the editable version

```python
def find_editable_version(client, app_id):
    r = client.get(
        f"/apps/{app_id}/appStoreVersions",
        **{"filter[appStoreState]": "PREPARE_FOR_SUBMISSION,DEVELOPER_REJECTED,REJECTED,METADATA_REJECTED,WAITING_FOR_REVIEW,INVALID_BINARY"},
    )
    data = r.get("data", [])
    return data[0] if data else None
```

Use comma-separated states. If no editable version exists, the user needs to create one in ASC first (requires an uploaded build).

### Screenshot upload — the 3-phase handshake

Apple uses a reservation-then-PUT-then-commit protocol so abandoned uploads don't leave dangling files:

```python
import hashlib, requests

def upload_screenshot(client, set_id: str, path: Path):
    data = path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()

    # Phase 1: reserve
    resv = client.post("/appScreenshots", {
        "data": {
            "type": "appScreenshots",
            "attributes": {"fileName": path.name, "fileSize": len(data)},
            "relationships": {
                "appScreenshotSet": {"data": {"type": "appScreenshotSets", "id": set_id}}
            },
        }
    })
    sid = resv["data"]["id"]
    ops = resv["data"]["attributes"]["uploadOperations"]

    # Phase 2: PUT each chunk to Apple's presigned URL
    for op in ops:
        headers = {h["name"]: h["value"] for h in op.get("requestHeaders", [])}
        chunk = data[op["offset"] : op["offset"] + op["length"]]
        requests.request(op["method"], op["url"], headers=headers, data=chunk, timeout=120).raise_for_status()

    # Phase 3: commit
    client.patch(f"/appScreenshots/{sid}", {
        "data": {
            "type": "appScreenshots",
            "id": sid,
            "attributes": {"uploaded": True, "sourceFileChecksum": md5},
        }
    })
```

Skip Phase 3 and the screenshot sits forever in `UPLOADING` state. Always include the MD5 — Apple rejects commits without it.

### Display types and sizes

| Display type | Resolution | Device |
|---|---|---|
| `APP_IPHONE_67` | 1290×2796 | iPhone 14/15/16/17 Pro Max, Plus |
| `APP_IPHONE_69` | 1320×2868 | iPhone 16/17 Pro Max |
| `APP_IPHONE_65` | 1242×2688 or 1284×2778 | iPhone XS Max, 11 Pro Max, 12/13 Pro Max |
| `APP_IPHONE_61` | 1179×2556 | iPhone 14/15 (non-Pro) |
| `APP_IPAD_PRO_129` | 2048×2732 | iPad Pro 12.9" |
| `APP_IPAD_PRO_3GEN_129` | 2064×2752 | iPad Pro M4 13" |

For iPhone 17 Pro captures (native 1206×2622, 6.3"), upscale to 1290×2796 (`APP_IPHONE_67`) — Apple accepts it and derives the 6.9" display from there. Pad with black bars if aspect ratios don't match.

### Idempotency patterns (critical for re-runnable sync)

Mobile metadata sync has to be safe to re-run. These error patterns show up every time:

1. **`409 DUPLICATE` on POST** — locale already exists (auto-created by Apple when version was made). Fall back to GET + PATCH:
   ```python
   try:
       return client.post("/appStoreVersionLocalizations", payload)["data"]
   except RuntimeError as e:
       if "DUPLICATE" in str(e) or "already exists" in str(e):
           current = get_version_localizations(client, version_id).get(locale)
           return client.patch(f"/appStoreVersionLocalizations/{current['id']}", patch_payload)["data"]
       raise
   ```

2. **`409 STATE_ERROR` on `whatsNew`** — Apple disallows "What's New" on first-version submissions (1.0). There's nothing "new" about a first release. Either skip entirely for 1.0 or try-catch:
   ```python
   def _try_patch_whats_new(client, loc_id, whats_new):
       try:
           client.patch(f"/appStoreVersionLocalizations/{loc_id}",
               {"data": {"type": "appStoreVersionLocalizations", "id": loc_id,
                         "attributes": {"whatsNew": whats_new}}})
       except RuntimeError as e:
           if "STATE_ERROR" in str(e) or "cannot be edited" in str(e):
               return  # silently skip on first release
           raise
   ```

3. **Screenshot set: create once, wipe contents each run.** Don't delete the `appScreenshotSet` itself — its relationship to `appStoreVersionLocalization` is stable. Just delete all `appScreenshots` inside it and re-upload.

4. **Stale sets from past display-type changes** — if someone uploaded to `APP_IPHONE_61` in a prior run and you're now uploading to `APP_IPHONE_67`, the old set lingers. Clean it up or ASC shows mixed sizes.

### Recommended file layout

Store metadata as files so they're reviewable in git (without the raw binaries — .gitignore `marketing/`):

```
marketing/
├── asc-metadata/
│   ├── shared.json                    ← URLs, copyright, review info, category, release type
│   └── <locale>/
│       ├── name.txt
│       ├── subtitle.txt
│       ├── description.txt
│       ├── keywords.txt
│       ├── promotional_text.txt
│       └── release_notes.txt
└── asc-screenshots/
    └── <locale>/<display-slug>/*.png
```

This separates content (editable by marketing/copywriters) from the sync logic (editable by engineers). Copywriters PR their `.txt` changes; engineers re-run the sync.

### Common 401 debugging flow

When you get 401 `NOT_AUTHORIZED` with a correctly formed JWT:

1. **Check key role** at https://appstoreconnect.apple.com/access/integrations/api — must be **Admin** or **App Manager**
2. **Check "Last used" column** — if it updates after your attempts, Apple IS receiving the token; problem is with signature or issuer match
3. **Check signature format** — if using PyJWT, check version with `pip show pyjwt`. Anything <2.0 emits DER format → rejected. Upgrade or switch to `cryptography` direct signing
4. **Check Issuer ID** — the UUID at the top of the Integrations page, above the keys table. Must match `APP_STORE_API_ISSUER` exactly
5. **Check `.p8` file integrity** — `openssl ec -in AuthKey_XXX.p8 -noout` should succeed; ECDSA P-256 key
6. **Clock skew** — `date -u` vs `curl -sI https://api.appstoreconnect.apple.com/ | grep -i date:`. Apple tolerates ~5 min drift
7. **Nuclear option** — revoke key, generate new one, download new `.p8`, update env. Cheapest way to rule out stale/mismatched key material

### When to use the `asc` CLI vs REST API

| Task | Tool |
|---|---|
| Upload build from CLI | `xcrun altool` or `asc` CLI |
| TestFlight group/tester management | `asc` CLI |
| App metadata (name, description, keywords) sync | REST API (Python client) |
| Screenshot upload | REST API (CLI support is flaky) |
| Subscription product CRUD | Either (REST is more reliable for bulk ops) |
| Review submission | REST API via `reviewSubmissions` endpoint |
| Pricing tier updates | REST API |

---

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
