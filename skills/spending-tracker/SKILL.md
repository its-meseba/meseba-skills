---
name: spending-tracker
description: Track and report personal spending with categories, timestamps, and nice HTML reports.
---

# Spending Tracker

**Created by Nâzım** — 4 Kallavi Turks

Track your spending, get weekly and monthly reports in beautiful HTML.

---

## Usage

### Add Spending Entry

```
Spent 45 on ekmek
Spent 150 on fitness protein
Spent 299 on datafast subscription
```

Format: `Spent [amount] on [description]`

**Auto-detects category:**
- Food/Kitchen: ekmek, yemek, market, etc.
- Fitness: protein, gym, fitness, spor
- Personal Studies: datafast, subscription, coursera, udemy, learning

---

### View Reports

```
Show spending
Spending report this month
```

Shows current month by default with:
- Weeks breakdown
- Entries by category
- Per-category totals
- Grand total

---

### Query Spending

```
How much did I spend on fitness this month?
Total food spending last month
```

---

## Categories

1. **Food/Kitchen** — ekmek, market, yemek, groceries
2. **Fitness** — protein, gym, spor, fitness
3. **Personal Studies** — subscriptions, courses, learning
4. **Other** — everything else

---

## Storage

- **Data:** `/spending/data/YYYY-MM.json`
- **Reports:** `/spending/reports/YYYY-MM.html`

Reports are generated as nice shadcn-style HTML tables.
