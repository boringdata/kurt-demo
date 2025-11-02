---
name: analytics-query
description: Low-level analytics queries for ad-hoc traffic analysis (general)
---

# Analytics Query Skill

## Overview

This skill provides **low-level, ad-hoc analytics queries** for quick traffic analysis. Use this skill when users ask simple questions about page traffic, trends, or want to spot-check specific pages.

**Key principle:** This is a **utility skill** - it wraps `kurt content list` and `kurt content stats` commands with analytics filters. It can be used directly by users OR called by higher-level skills like `content-analysis-skill`.

---

## When to Use This Skill

✅ **Use analytics-query-skill when:**
- User asks simple traffic questions: "Which pages get the most traffic?"
- Spot-checking specific pages: "How's the traffic for the BigQuery tutorial?"
- Identifying trends: "What's losing traffic?"
- User wants quick analytics summary: "Show me traffic stats for docs.company.com"

❌ **Don't use analytics-query-skill when:**
- Complex workflows (Tutorial Refresh, Documentation Audit) → Use `content-analysis-skill`
- Need traffic-based prioritization across many pages → Use `content-analysis-skill identify-affected`
- Need impact estimation or gap analysis → Use `content-analysis-skill`

**Rule of thumb:** If it's a single analytics query or spot-check, use this skill. If it's part of a larger content workflow, use `content-analysis-skill` (which may call this skill internally).

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

**Example usage:**
```
User: Show me the top 10 pages by traffic

Claude (invokes analytics-query top 10):

Top 10 Pages by Traffic (last 30 days):

1. "BigQuery Quickstart" - 3,421 views  ↑ +15%
2. "Python SDK Guide" - 2,103 views  ↓ -8%
3. "SQL Best Practices" - 1,850 views  → stable
4. "Data Loading Guide" - 1,234 views  ↑ +22%
...

User: What about just docs.company.com?

Claude (invokes analytics-query top 10 --url-prefix https://docs.company.com):

Top 10 Pages on docs.company.com (last 30 days):
[filtered results]
```

**Supported metrics:**
- `pageviews_30d` (default)
- `pageviews_60d`
- `unique_visitors_30d`

---

### 2. `bottom <N> [--metric pageviews_30d] [--url-prefix <domain>]`

**Purpose:** Show bottom N pages by traffic metric (lowest traffic)

**Implementation:**
```bash
# Get traffic stats first to find threshold
kurt content stats --show-analytics ${url_prefix:+--url-starts-with $url_prefix}

# Then filter for low traffic + sort ascending
kurt content list \
  --with-analytics \
  --pageviews-30d-max ${p25_threshold} \
  --order-by pageviews_30d \
  --limit <N> \
  ${url_prefix:+--url-starts-with $url_prefix}
```

**Example usage:**
```
User: Show me pages getting almost no traffic

Claude (invokes analytics-query bottom 10):

Bottom 10 Pages by Traffic (last 30 days):

These pages are getting very little traffic (below 25th percentile: 45 views/month):

1. "Advanced BigQuery ML" - 0 views  [ZERO TRAFFIC]
2. "Legacy SQL Guide" - 0 views  [ZERO TRAFFIC]
3. "BigQuery Pricing API" - 12 views  → stable
4. "Historical Data Export" - 18 views  ↓ -45%
...

💡 Tip: ZERO traffic pages might be:
- Orphaned (not linked from anywhere)
- Deprecated content (consider archiving)
- Newly published (give it time)
```

---

### 3. `traffic-for <url-pattern>`

**Purpose:** Get traffic for specific URL(s) matching a pattern

**Implementation:**
```bash
kurt content list \
  --url-contains "<pattern>" \
  --with-analytics
```

**Example usage:**
```
User: What's the traffic for all BigQuery tutorials?

Claude (invokes analytics-query traffic-for "bigquery"):

Found 23 pages matching "bigquery":

HIGH TRAFFIC (>890 views/month): 6 pages
- "BigQuery Quickstart" - 3,421 views  ↑ +15%
- "Python SDK Guide" - 2,103 views  ↓ -8%
...

MEDIUM TRAFFIC (45-890 views/month): 10 pages
...

LOW TRAFFIC (≤45 views/month): 5 pages
...

ZERO TRAFFIC: 2 pages
- "Advanced BigQuery ML" - 0 views
- "Legacy SQL Guide" - 0 views

Total traffic (30d): 18,450 views across 23 pages
```

**Note:** Automatically groups results by traffic category using percentile thresholds from `kurt content stats --show-analytics`.

---

### 4. `trending [--direction increasing|decreasing] [--url-prefix <domain>]`

**Purpose:** Show pages with traffic trends (increasing or decreasing)

**Implementation:**
```bash
kurt content list \
  --with-analytics \
  --pageviews-trend ${direction} \
  --order-by trend_percentage \
  ${url_prefix:+--url-starts-with $url_prefix}
```

**Example usage:**
```
User: Which pages are losing traffic?

Claude (invokes analytics-query trending --direction decreasing):

Pages with Declining Traffic (last 30 days):

⚠️ HIGH-TRAFFIC pages losing visitors (urgent):
1. "Python SDK Guide" - 2,103 views  ↓ -8%  (losing 200 views/month)
2. "Data Loading Guide" - 1,234 views  ↓ -12%  (losing 168 views/month)

MEDIUM-TRAFFIC pages losing visitors:
3. "Query Optimization" - 456 views  ↓ -15%
...

LOW-TRAFFIC pages losing visitors:
...

Recommendation: Focus on high-traffic pages first - they have the biggest impact.
```

```
User: What's trending up?

Claude (invokes analytics-query trending --direction increasing):

Pages with Growing Traffic (last 30 days):

🚀 HIGH-TRAFFIC pages gaining visitors:
1. "BigQuery Quickstart" - 3,421 views  ↑ +15%  (gaining 450 views/month)
2. "Streaming Inserts" - 1,890 views  ↑ +28%  (gaining 412 views/month)

Consider:
- Creating more content on these topics
- Linking related pages to capitalize on momentum
```

---

### 5. `summary <domain>`

**Purpose:** Show overall analytics summary for a domain

**Implementation:**
```bash
kurt content stats --show-analytics --url-starts-with <domain>
```

**Example usage:**
```
User: Give me an analytics overview of docs.company.com

Claude (invokes analytics-query summary docs.company.com):

Analytics Summary: docs.company.com

Document Statistics:
Total Documents: 234
  Fetched: 234

Analytics Statistics:
Documents with Analytics: 234

Traffic Distribution (30d pageviews):
  Average:        456.7 views/month
  Median (p50):   123 views/month
  75th %ile:      890 views/month  (HIGH traffic threshold)
  25th %ile:      45 views/month   (LOW traffic threshold)

Traffic Categories:
  ZERO traffic:     12 pages (5%)
  LOW traffic:      58 pages (25%)  (≤ p25)
  MEDIUM traffic:  116 pages (50%)  (p25-p75)
  HIGH traffic:     48 pages (21%)  (> p75)

Health Check:
✅ Most pages (95%) have traffic
⚠️ 5% pages have ZERO traffic (consider auditing)
✅ Strong high-traffic content (21% of pages)
```

---

## Implementation Details

### Getting Traffic Thresholds

All operations that categorize by traffic (ZERO/LOW/MEDIUM/HIGH) should:

1. **Get thresholds from stats:**
```bash
stats=$(kurt content stats --show-analytics --url-starts-with <domain> --format json)
p25=$(echo "$stats" | jq '.p25_pageviews_30d')
p75=$(echo "$stats" | jq '.p75_pageviews_30d')
```

2. **Categorize results:**
- ZERO: pageviews_30d == 0
- LOW: 0 < pageviews_30d <= p25
- MEDIUM: p25 < pageviews_30d <= p75
- HIGH: pageviews_30d > p75

3. **Present grouped results:**
Show highest priority first (ZERO > HIGH > MEDIUM > LOW or reverse depending on context).

### Conversational Presentation

**Always provide:**
- Clear category labels (ZERO/LOW/MEDIUM/HIGH with thresholds explained)
- Traffic trend symbols (↑ ↓ →) with percentages
- Contextual recommendations based on results
- Tips for next steps

**Example good presentation:**
```
Found 23 tutorials:

ZERO TRAFFIC (0 views): 2 tutorials
⚠️ These pages may be orphaned or deprecated
- "Advanced BigQuery ML" (0 views, 950 days old)
- Consider: Archive or improve discoverability?

HIGH TRAFFIC (>890 views): 6 tutorials
🎯 Focus here for maximum impact
1. "Python SDK Guide" (2,103 views, ↓ -8%) ⚠️ URGENT
   → Losing traffic - needs refresh

Recommendation: Start with Python SDK Guide (high traffic + declining = urgent + high impact)
```

---

## Integration with Other Skills

### Called BY content-analysis-skill

`content-analysis-skill` uses this skill for individual queries:

```python
# content-analysis-skill: identify-affected operation

# Step 1: Find matching content
matching_docs = search_content(term, content_type)

# Step 2: Get traffic data using analytics-query-skill
traffic_data = analytics_query.traffic_for(term)

# Step 3: Apply workflow-specific prioritization logic
prioritized = prioritize_by_urgency(matching_docs, traffic_data)
```

### Used DIRECTLY by user

User can invoke directly for ad-hoc queries without a workflow context.

---

## Error Handling

### Analytics not configured

```
⚠️ Analytics not configured for this domain

To enable analytics:
1. Run: kurt analytics onboard <domain>
2. Provide PostHog credentials
3. Sync data: kurt analytics sync <domain>

Proceeding with results (no traffic data shown)...
```

### Analytics data stale

```
⚠️ Analytics data is 10 days old

For accurate results, sync now:
kurt analytics sync <domain>

Sync now? (Y/n)
```

### No results found

```
No documents found matching "<pattern>"

Try:
- Broader search term
- Check spelling
- Check if content is fetched: kurt content list --url-contains "<term>"
```

---

## Key Principles

1. **Low-level utility** - Simple, composable operations
2. **Wraps CLI commands** - No complex logic, just intelligent presentation
3. **Used by humans and skills** - API-like interface + conversational output
4. **Traffic-aware presentation** - Always show traffic context (ZERO/LOW/MEDIUM/HIGH)
5. **Actionable recommendations** - Suggest next steps based on results

---

## See Also

- **content-analysis-skill** - High-level workflows using this skill
- **WORKFLOWS.md** - Complex scenarios where content-analysis-skill is used
- **CLAUDE.md** - Full analytics integration documentation
