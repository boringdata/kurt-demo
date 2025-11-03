# Analytics Subskill

**Purpose:** Low-level traffic queries for spot-checking and analysis
**Parent Skill:** intelligence
**Operations:** top, bottom, check, trending, declining, summary

---

## Overview

Provides quick analytics queries for traffic analysis. These operations wrap `kurt content list --with-analytics` and `kurt content stats --show-analytics` commands.

**When to use:**
- Quick spot-checks: "What are my top pages?"
- Finding issues: "Which pages have zero traffic?"
- Trend analysis: "What's losing traffic?"
- Domain overview: "Show me analytics summary"

---

## Operations

### 1. `top <N> [--metric pageviews_30d] [--url-prefix <domain>]`

**Purpose:** Show top N pages by traffic metric

**Implementation:**
```bash
kurt content list \
  --with-analytics \
  --order-by pageviews_30d \
  --limit <N> \
  ${url_prefix:+--url-starts-with $url_prefix}
```

**Example:**
```
intelligence top 10

Top 10 Pages by Traffic (last 30 days):

1. "BigQuery Quickstart" - 3,421 views  ↑ +15%
2. "Python SDK Guide" - 2,103 views  ↓ -8%
3. "SQL Best Practices" - 1,850 views  → stable
...
```

**Options:**
- `--metric`: pageviews_30d (default), pageviews_60d, unique_visitors_30d
- `--url-prefix`: Filter to specific domain

---

### 2. `bottom <N> [--metric pageviews_30d] [--url-prefix <domain>]`

**Purpose:** Show lowest traffic pages

**Implementation:**
```bash
# Get traffic thresholds
kurt content stats --show-analytics ${url_prefix:+--url-starts-with $url_prefix}

# Filter for low traffic
kurt content list \
  --with-analytics \
  --pageviews-30d-max ${p25_threshold} \
  --order-by pageviews_30d \
  --limit <N>
```

**Example:**
```
intelligence bottom 10

Bottom 10 Pages by Traffic (last 30 days):

These pages are below 25th percentile (45 views/month):

1. "Advanced BigQuery ML" - 0 views  [ZERO TRAFFIC]
2. "Legacy SQL Guide" - 0 views  [ZERO TRAFFIC]
3. "BigQuery Pricing API" - 12 views  → stable
...

💡 ZERO traffic pages might be orphaned or deprecated
```

---

### 3. `check <url-pattern>`

**Purpose:** Get traffic for specific URL(s)

**Implementation:**
```bash
kurt content list \
  --url-contains "<pattern>" \
  --with-analytics
```

**Example:**
```
intelligence check "bigquery"

Found 23 pages matching "bigquery":

HIGH TRAFFIC (>890 views/month): 6 pages
- "BigQuery Quickstart" - 3,421 views  ↑ +15%
- "Python SDK Guide" - 2,103 views  ↓ -8%

MEDIUM TRAFFIC (45-890 views/month): 10 pages
...

LOW TRAFFIC (≤45 views/month): 5 pages
...

ZERO TRAFFIC: 2 pages
- "Advanced BigQuery ML" - 0 views

Total: 18,450 views across 23 pages
```

---

### 4. `trending [--url-prefix <domain>]`

**Purpose:** Show pages with increasing traffic

**Implementation:**
```bash
kurt content list \
  --with-analytics \
  --pageviews-trend increasing \
  --order-by trend_percentage \
  ${url_prefix:+--url-starts-with $url_prefix}
```

**Example:**
```
intelligence trending

Pages with Growing Traffic (last 30 days):

🚀 HIGH-TRAFFIC pages gaining visitors:
1. "BigQuery Quickstart" - 3,421 views  ↑ +15%  (+450 views/month)
2. "Streaming Inserts" - 1,890 views  ↑ +28%  (+412 views/month)

Consider:
- Creating more content on these topics
- Linking related pages to capitalize on momentum
```

---

### 5. `declining [--url-prefix <domain>]`

**Purpose:** Show pages with decreasing traffic

**Implementation:**
```bash
kurt content list \
  --with-analytics \
  --pageviews-trend decreasing \
  --order-by trend_percentage \
  ${url_prefix:+--url-starts-with $url_prefix}
```

**Example:**
```
intelligence declining

Pages with Declining Traffic (last 30 days):

⚠️ HIGH-TRAFFIC pages losing visitors (URGENT):
1. "Python SDK Guide" - 2,103 views  ↓ -8%  (-200 views/month)
   → High traffic + declining = needs immediate attention

MEDIUM-TRAFFIC pages losing visitors:
2. "Query Optimization" - 456 views  ↓ -15%
...

Recommendation: Focus on high-traffic pages first for maximum impact.
```

---

### 6. `summary <domain>`

**Purpose:** Show overall analytics summary

**Implementation:**
```bash
kurt content stats --show-analytics --url-starts-with <domain>
```

**Example:**
```
intelligence summary docs.company.com

Analytics Summary: docs.company.com

Document Statistics:
  Total: 234 documents

Traffic Distribution (30d pageviews):
  Average: 456.7 views/month
  Median: 123 views/month
  75th percentile: 890 views/month  (HIGH threshold)
  25th percentile: 45 views/month   (LOW threshold)

Traffic Categories:
  ZERO traffic:     12 pages (5%)   ⚠️
  LOW traffic:      58 pages (25%)  (≤45 views/month)
  MEDIUM traffic:  116 pages (50%)  (45-890 views/month)
  HIGH traffic:     48 pages (21%)  (>890 views/month)

Health Check:
✅ Most pages (95%) have traffic
⚠️ 5% have ZERO traffic (consider auditing)
✅ Strong high-traffic content (21% of pages)
```

---

## Presentation Guidelines

**Always provide:**
- Traffic categories (ZERO/LOW/MEDIUM/HIGH) with thresholds
- Trend symbols: ↑ increasing, ↓ decreasing, → stable
- Contextual recommendations
- Next steps suggestions

**Traffic Categorization:**
1. Get thresholds: `kurt content stats --show-analytics --format json`
2. Extract: p25 (LOW threshold), p75 (HIGH threshold)
3. Categorize:
   - ZERO: pageviews == 0
   - LOW: 0 < pageviews ≤ p25
   - MEDIUM: p25 < pageviews ≤ p75
   - HIGH: pageviews > p75

---

## Error Handling

### Analytics not configured
```
⚠️ Analytics not configured for this domain

To enable:
1. kurt analytics onboard <domain>
2. Provide PostHog credentials
3. kurt analytics sync <domain>

Proceeding without traffic data...
```

### Analytics data stale
```
⚠️ Analytics data is 10 days old

For accurate results:
kurt analytics sync <domain>

Sync now? (Y/n)
```

### No results found
```
No documents found matching "<pattern>"

Try:
- Broader search term
- Check if content is fetched: kurt content list
```

---

## Key Principles

1. **Simple wrappers** - Wrap kurt CLI commands with smart presentation
2. **Traffic-aware** - Always show traffic categories
3. **Actionable** - Provide recommendations based on results
4. **Context-efficient** - Quick queries, focused results
