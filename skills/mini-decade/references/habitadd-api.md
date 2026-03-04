# HabitAdd Agent API Reference

## Overview

HabitAdd (app.habitadd.com) is the user's habit tracking app. The agent can read/write habits and entries via Firebase callable functions.

## Configuration

Config stored at: `/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/0. What is MiniDecade/Tools/.habitadd-config.json`

```json
{
  "apiKey": "<raw API key>",
  "projectId": "habits-x",
  "region": "us-central1"
}
```

## Authentication

All requests require `apiKey` parameter. The key is validated server-side against SHA-256 hash in `agent_api_keys` collection. User ID is derived from the key document (not passed by caller).

## Calling Functions

```bash
curl -X POST "https://us-central1-habits-x.cloudfunctions.net/{functionName}" \
  -H "Content-Type: application/json" \
  -d '{"data": {"apiKey": "hab_xxx-xxx-xxx", ...params}}'
```

## Functions

### agentGetHabits

Get all habits.

- **Params:** `apiKey`, `includeArchived` (optional, default false)
- **Returns:** `{ habits: Habit[] }`

### agentLogEntry

Log a habit completion/value.

- **Params:** `apiKey`, `habitId`, `date` (YYYY-MM-DD), `value` (number), `completed` (boolean)
- **Returns:** `{ entry: HabitEntry }`
- Entry ID: `{habitId}_{date}` (upserts)

### agentGetEntries

Get entries for a date range.

- **Params:** `apiKey`, `startDate`, `endDate`, `habitId` (optional), `limit` (optional, max 1000)
- **Returns:** `{ entries: HabitEntry[], totalCount }`

### agentGetAnalytics

Get streak and completion analytics.

- **Params:** `apiKey`, `habitId`, `days` (optional, default 30, max 365)
- **Returns:** `{ currentStreak, longestStreak, completionRate, completedEntries, missedDays, averageValue, entries[] }`

### agentCreateHabit

Create a new habit from MiniDecade plan.

- **Params:** `apiKey`, `name`, `type` ("check"|"number"), `color`, `goal`, `frequency` ("daily"|"weekly"|"monthly"), `goalType` ("at_least"|"at_most"), `question` (optional), `unit` (optional), `notes` (optional)
- **Returns:** `{ habit: Habit }`

### agentUpdateHabit

Update habit settings.

- **Params:** `apiKey`, `habitId`, `updates` (partial: name, question, unit, color, goal, frequency, goalType, notes, archived, index)
- **Returns:** `{ habitId, updatedFields[] }`
- Immutable: id, userId, createdAt, peer fields

## Common Workflows

### Pull today's data for weekly review

```bash
# Get all habits
curl ... agentGetHabits {"data":{"apiKey":"..."}}

# Get this week's entries
curl ... agentGetEntries {"data":{"apiKey":"...","startDate":"2026-03-01","endDate":"2026-03-07"}}
```

### Create habit from MiniDecade plan

```bash
curl ... agentCreateHabit {"data":{"apiKey":"...","name":"Read 30 min (Context Engineering)","type":"check","color":"#EE9F41","goal":1,"frequency":"daily","goalType":"at_least"}}
```

### Get 30-day analytics for progress report

```bash
curl ... agentGetAnalytics {"data":{"apiKey":"...","habitId":"abc123","days":30}}
```

## Error Codes

| Code | Meaning |
|------|---------|
| `unauthenticated` | Invalid/expired/revoked API key |
| `permission-denied` | Missing scope or not premium |
| `not-found` | Habit doesn't exist |
| `invalid-argument` | Bad parameters |
