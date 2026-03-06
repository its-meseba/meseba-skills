#!/usr/bin/env node

/**
 * Spending Tracker - Nâzım
 * Tracks spending, generates HTML reports
 * 
 * Usage: node spending-tracker.js <command> [args]
 * 
 * Commands:
 *   add <amount> <description>  - Add spending entry
 *   report [month]              - Show HTML report
 *   list                        - List all spending
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = '/root/.openclaw/workspace/kallavi-turk-configs/spending/data';
const REPORTS_DIR = '/root/.openclaw/workspace/kallavi-turk-configs/spending/reports';

// Category keywords
const CATEGORIES = {
  'Food/Kitchen': ['ekmek', 'yemek', 'market', 'grocery', 'simit', 'poğaça', 'kahvaltı', 'dinner', 'lunch', 'breakfast', 'food'],
  'Fitness': ['protein', 'gym', 'fitness', 'spor', 'supplement', 'Creatine', 'BCAA', 'whey'],
  'Personal Studies': ['datafast', 'subscription', 'coursera', 'udemy', 'learn', 'course', 'book', 'learning', 'membership', 'tools']
};

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function detectCategory(description) {
  const lower = description.toLowerCase();
  for (const [cat, keywords] of Object.entries(CATEGORIES)) {
    if (keywords.some(k => lower.includes(k))) {
      return cat;
    }
  }
  return 'Other';
}

function getMonthKey(date = new Date()) {
  return date.toISOString().slice(0, 7); // YYYY-MM
}

function loadMonthData(monthKey) {
  const file = path.join(DATA_DIR, `${monthKey}.json`);
  if (fs.existsSync(file)) {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  }
  return { entries: [] };
}

function saveMonthData(monthKey, data) {
  const file = path.join(DATA_DIR, `${monthKey}.json`);
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function addEntry(amount, description) {
  const now = new Date();
  const monthKey = getMonthKey(now);
  
  ensureDir(DATA_DIR);
  
  const data = loadMonthData(monthKey);
  
  const entry = {
    id: Date.now(),
    amount: parseFloat(amount),
    description: description,
    category: detectCategory(description),
    timestamp: now.toISOString(),
    week: getWeekNumber(now)
  };
  
  data.entries.push(entry);
  saveMonthData(monthKey, data);
  
  // Generate report after update
  generateReport(monthKey);
  
  // Commit to git
  commitToGit(`Add spending: ${amount} TL on ${description}`);
  
  return entry;
}

function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

function getMonthlyReport(monthKey = getMonthKey()) {
  const data = loadMonthData(monthKey);
  
  if (data.entries.length === 0) {
    return { month: monthKey, entries: [], categories: {}, total: 0, weeks: {} };
  }
  
  // Group by category
  const categories = {};
  for (const entry of data.entries) {
    if (!categories[entry.category]) {
      categories[entry.category] = 0;
    }
    categories[entry.category] += entry.amount;
  }
  
  // Group by week
  const weeks = {};
  for (const entry of data.entries) {
    const weekKey = `Week ${entry.week}`;
    if (!weeks[weekKey]) {
      weeks[weekKey] = { entries: [], total: 0 };
    }
    weeks[weekKey].entries.push(entry);
    weeks[weekKey].total += entry.amount;
  }
  
  const total = data.entries.reduce((sum, e) => sum + e.amount, 0);
  
  return { month: monthKey, entries: data.entries, categories, total, weeks };
}

function generateReport(monthKey) {
  const report = getMonthlyReport(monthKey);
  ensureDir(REPORTS_DIR);
  
  const html = generateHTML(report);
  const htmlFile = path.join(REPORTS_DIR, `${monthKey}.html`);
  fs.writeFileSync(htmlFile, html);
  
  console.log(`Report generated: ${htmlFile}`);
  return htmlFile;
}

function generateHTML(report) {
  const { month, entries, categories, total, weeks } = report;
  const [year, mon] = month.split('-');
  const monthName = new Date(year, mon - 1).toLocaleString('en-US', { month: 'long', year: 'numeric' });
  
  let entriesHTML = entries
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .map(e => `
      <tr>
        <td class="px-4 py-2 text-muted-foreground">${new Date(e.timestamp).toLocaleDateString('tr-TR')}</td>
        <td class="px-4 py-2">${e.description}</td>
        <td class="px-4 py-2">
          <span class="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium">${e.category}</span>
        </td>
        <td class="px-4 py-2 text-right font-mono">${e.amount.toFixed(2)} TL</td>
      </tr>
    `).join('');
  
  let categoriesHTML = Object.entries(categories)
    .map(([cat, amount]) => `
      <tr>
        <td class="px-4 py-2 font-medium">${cat}</td>
        <td class="px-4 py-2 text-right font-mono">${amount.toFixed(2)} TL</td>
      </tr>
    `).join('');
  
  let weeksHTML = Object.entries(weeks)
    .map(([week, data]) => `
      <tr>
        <td class="px-4 py-2 font-medium">${week}</td>
        <td class="px-4 py-2 text-right font-mono">${data.total.toFixed(2)} TL</td>
      </tr>
    `).join('');
  
  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spending Report - ${monthName}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-background text-foreground min-h-screen">
  <div class="container mx-auto py-8 px-4 max-w-4xl">
    <h1 class="text-3xl font-bold mb-2">Spending Report</h1>
    <p class="text-muted-foreground mb-8">${monthName}</p>
    
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="rounded-lg border bg-card p-6">
        <div class="text-sm text-muted-foreground">Total</div>
        <div class="text-3xl font-bold font-mono">${total.toFixed(2)} TL</div>
      </div>
      <div class="rounded-lg border bg-card p-6">
        <div class="text-sm text-muted-foreground">Entries</div>
        <div class="text-3xl font-bold">${entries.length}</div>
      </div>
      <div class="rounded-lg border bg-card p-6">
        <div class="text-sm text-muted-foreground">Categories</div>
        <div class="text-3xl font-bold">${Object.keys(categories).length}</div>
      </div>
    </div>
    
    <!-- By Category -->
    <div class="rounded-lg border bg-card p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">By Category</h2>
      <table class="w-full">
        <tbody>${categoriesHTML}</tbody>
      </table>
    </div>
    
    <!-- By Week -->
    <div class="rounded-lg border bg-card p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">By Week</h2>
      <table class="w-full">
        <tbody>${weeksHTML}</tbody>
      </table>
    </div>
    
    <!-- All Entries -->
    <div class="rounded-lg border bg-card">
      <div class="px-6 py-4 border-b">
        <h2 class="text-xl font-semibold">All Entries</h2>
      </div>
      <table class="w-full">
        <thead>
          <tr class="border-b">
            <th class="px-4 py-2 text-left text-sm font-medium text-muted-foreground">Date</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-muted-foreground">Description</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-muted-foreground">Category</th>
            <th class="px-4 py-2 text-right text-sm font-medium text-muted-foreground">Amount</th>
          </tr>
        </thead>
        <tbody>${entriesHTML}</tbody>
      </table>
    </div>
  </div>
</body>
</html>`;
}

function commitToGit(message) {
  try {
    const { execSync } = require('child_process');
    execSync('cd /root/.openclaw/workspace/kallavi-turk-configs && git add -A && git commit -m "' + message + '" && git push origin main', { stdio: 'ignore' });
    console.log('Committed and pushed to Git');
  } catch (e) {
    console.log('Could not commit:', e.message);
  }
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

if (command === 'add' && args[1] && args[2]) {
  const entry = addEntry(args[1], args.slice(2).join(' '));
  console.log(`Added: ${entry.amount} TL - ${entry.description} (${entry.category})`);
} else if (command === 'report' || command === 'show') {
  const monthKey = args[1] || getMonthKey();
  const report = getMonthlyReport(monthKey);
  console.log(JSON.stringify(report, null, 2));
} else if (command === 'list') {
  const data = loadMonthData(getMonthKey());
  console.log(JSON.stringify(data, null, 2));
} else {
  console.log(`
Spending Tracker - Usage:
  
  node spending-tracker.js add <amount> <description>
  node spending-tracker.js report [month]
  node spending-tracker.js list
  
Examples:
  node spending-tracker.js add 45 ekmek
  node spending-tracker.js add 150 protein
  node spending-tracker.js report 2026-03
  `);
}
