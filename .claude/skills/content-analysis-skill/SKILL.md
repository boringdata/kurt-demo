---
name: content-analysis
description: Complex content analysis workflows with traffic-based prioritization (general)
---

# Content Analysis Skill

## Overview

This skill provides **complex content analysis workflows** that combine content intelligence with analytics for traffic-based prioritization. Use this skill for multi-step content workflows described in `WORKFLOWS.md`.

**Key principle:** This skill orchestrates complex operations by combining:
- Content queries (`kurt content list`)
- Analytics queries (via `analytics-query-skill`)
- Workflow-specific prioritization logic

---

## When to Use This Skill

✅ **Use content-analysis-skill when:**
- Complex workflows: Tutorial Refresh, Documentation Audit, Competitive Gap Analysis
- Need traffic-based prioritization across many pages
- Combining content metadata + analytics + workflow logic
- Impact estimation or gap analysis

❌ **Don't use content-analysis-skill when:**
- Simple analytics queries → Use `analytics-query-skill`
- Just listing content → Use `kurt content list`
- No analytics needed → Use content commands directly

**Rule of thumb:** If it's a workflow from `WORKFLOWS.md` or requires traffic-based prioritization logic, use this skill.

---

## Operations

### 1. `identify-affected --search-term <term> --content-type <type>`

**Purpose:** Find content by keyword with traffic-based prioritization

**Used in:** Workflow 1 (Tutorial Refresh)

**Implementation steps:**

1. **Find matching content:**
```bash
kurt content list \
  --url-contains "<search-term>" \
  ${content_type:+--content-type $content_type} \
  --with-analytics \
  --order-by pageviews_30d desc
```

2. **Get traffic thresholds:**
```bash
stats=$(kurt content stats --show-analytics --format json)
p25=$(echo "$stats" | jq '.p25_pageviews_30d')
p75=$(echo "$stats" | jq '.p75_pageviews_30d')
```

3. **Categorize by traffic + urgency:**
- **ZERO TRAFFIC** (0 views):
  - Consider archiving or improving discoverability
  - Sort by age (oldest first)

- **HIGH TRAFFIC** (>p75):
  - **Declining trend** = CRITICAL URGENCY (high impact + needs refresh)
  - **Increasing trend** = HIGH PRIORITY (capitalize on momentum)
  - **Stable** = MEDIUM PRIORITY (maintain quality)
  - Sort by: trend (declining first), then pageviews (highest first)

- **MEDIUM TRAFFIC** (p25-p75):
  - **Declining trend** = MEDIUM URGENCY
  - Sort by: trend (declining first), then pageviews

- **LOW TRAFFIC** (>0, ≤p25):
  - **Declining trend** = LOW URGENCY (small impact)
  - Sort by: pageviews (highest in category first)

4. **Present prioritized results:**

```
Found 23 tutorials matching "BigQuery":

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL PRIORITY (high traffic + declining):
1. "Python SDK Guide" (2,103 views/month, ↓ -8%, 720 days old)
   → Losing 168 views/month - needs urgent refresh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 HIGH PRIORITY (high traffic, >890 views/month):
2. "BigQuery Quickstart" (3,421 views/month, ↑ +15%, 850 days old)
   → Increasing traffic - update to capitalize on momentum
3. "SQL Best Practices" (1,850 views/month, → stable, 450 days old)
   → Stable high-traffic content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MEDIUM PRIORITY (medium traffic, 45-890 views/month):
[10 tutorials]
- 2 with declining traffic
- 8 stable or increasing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 LOW PRIORITY (low traffic, ≤45 views/month):
[5 tutorials]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ZERO TRAFFIC (consider archiving):
- "Advanced BigQuery ML" (0 views, 950 days old)
- "Legacy SQL Guide" (0 views, 1200 days old)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation:
1. Start with CRITICAL priority (Python SDK Guide) - urgent + high impact
2. Then HIGH priority (Quickstart + Best Practices) - maintain momentum
3. Then MEDIUM declining traffic - prevent further drops
4. Archive or improve ZERO traffic pages

Should I focus on CRITICAL + HIGH priority first? (Y/n)
```

**Example usage:**
```
User: Update all BigQuery tutorials

Claude (invokes content-analysis identify-affected --search-term "bigquery" --content-type tutorial):

[Shows prioritized results above]

User: Yes, focus on critical and high priority

Claude: I'll work on 3 tutorials in this order:
1. Python SDK Guide (CRITICAL - losing traffic)
2. BigQuery Quickstart (HIGH - capitalize on growth)
3. SQL Best Practices (HIGH - maintain quality)

Let's start with the Python SDK Guide...
```

---

### 2. `audit-traffic --domain <domain>`

**Purpose:** Identify traffic patterns and issues for a domain

**Used in:** Workflow 4 (Documentation Audit)

**Implementation steps:**

1. **Get analytics summary:**
```bash
analytics-query summary <domain>
```

2. **Find high-traffic stale pages:**
```bash
# Pages with >p75 traffic AND >365 days old
kurt content list \
  --url-starts-with <domain> \
  --with-analytics \
  --order-by pageviews_30d desc
# Filter for old published_date in results
```

3. **Find declining-traffic pages:**
```bash
kurt content list \
  --url-starts-with <domain> \
  --with-analytics \
  --pageviews-trend decreasing \
  --order-by trend_percentage
```

4. **Find zero-traffic pages:**
```bash
kurt content list \
  --url-starts-with <domain> \
  --with-analytics
# Filter for pageviews_30d == 0 in results
```

5. **Present audit report:**

```
Traffic Audit: docs.company.com

Overview:
- 234 total pages
- 222 pages with traffic (95%)
- 12 pages with ZERO traffic (5%)
- Average: 456.7 views/month

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 HIGH-TRAFFIC STALE CONTENT (needs refresh):
Pages with >890 views/month that are >365 days old:

1. "BigQuery Quickstart" (3,421 views, 850 days old)
   → High traffic but outdated - update for max impact

2. "Python SDK Guide" (2,103 views, 720 days old, ↓ -8%)
   → High traffic AND losing visitors - URGENT

[8 more pages]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📉 DECLINING TRAFFIC (needs investigation):
Pages losing >10% traffic month-over-month:

1. "Python SDK Guide" (↓ -8%, losing 168 views/month)
2. "Data Loading Guide" (↓ -12%, losing 168 views/month)
[12 more pages]

Possible causes:
- Content outdated
- Better alternatives published elsewhere
- Search ranking dropped

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ZERO TRAFFIC (orphaned or deprecated):
12 pages with 0 views in last 30 days:

- "Advanced BigQuery ML" (950 days old)
- "Legacy SQL Guide" (1200 days old)
[10 more pages]

Actions to consider:
1. Check if pages are linked from anywhere
2. Review if content is still relevant
3. Archive or improve discoverability

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
1. Update high-traffic stale content (10 pages) - max impact
2. Investigate declining traffic (14 pages) - prevent further drops
3. Audit zero-traffic pages (12 pages) - clean up or improve

Create project for high-traffic updates? (Y/n)
```

---

### 3. `impact-estimate --topic <topic> --domain <domain>`

**Purpose:** Estimate impact of creating missing content

**Used in:** Workflow 4 (Documentation Audit - after identifying gaps)

**Implementation steps:**

1. **Find related existing content:**
```bash
# Search for pages related to the missing topic
kurt content list \
  --url-contains "<related-keyword>" \
  --url-starts-with <domain> \
  --with-analytics
```

2. **Calculate related content traffic:**
```python
total_views = sum(page.pageviews_30d for page in related_pages)
avg_views = total_views / len(related_pages)
```

3. **Estimate potential impact:**
- **HIGH IMPACT**: Related content gets >5000 views/month total
- **MEDIUM IMPACT**: Related content gets 1000-5000 views/month
- **LOW IMPACT**: Related content gets <1000 views/month

4. **Present impact estimate:**

```
Impact Estimate: Missing "Security" documentation

Related Content Analysis:
- Found 8 pages related to security/authentication
- Total traffic: 8,500 views/month
- Average per page: 1,062 views/month

Top related pages:
1. "Authentication Overview" (2,340 views/month)
2. "API Keys Guide" (1,890 views/month)
3. "OAuth Setup" (1,450 views/month)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Impact Assessment: 🎯 HIGH IMPACT

Reasoning:
- Related content gets 8,500+ views/month
- Security is critical topic (users actively searching)
- Competitors have 5-8 security docs each

Estimated traffic for new security docs:
- Conservative: 500-1000 views/month per page
- Optimistic: 1000-2000 views/month per page

Missing content types:
- Security best practices guide
- Encryption tutorial
- Audit logging reference
- Compliance documentation

Recommendation:
Create security documentation suite - high user demand + high impact.

Suggested next steps:
1. Research competitor security docs
2. Identify critical gaps
3. Create content plan
4. Prioritize by importance (best practices > advanced topics)
```

---

### 4. `compare-traffic --own <domain> --competitor <domain>`

**Purpose:** Compare traffic patterns between your domain and competitor

**Used in:** Workflow 2 (Competitive Gap Analysis)

**Note:** This operation requires competitor analytics (usually not available). For initial implementation, this can return "Competitor analytics not available - use content comparison instead" and delegate to topic/quality comparison workflows.

**Future implementation** (if competitor analytics become available via SEMrush/Ahrefs integration):
- Compare traffic distribution
- Identify topics where competitor gets more traffic
- Estimate traffic opportunity

---

## Delegation Pattern

This skill **delegates to**:
- **analytics-query-skill** for simple queries (top, trending, summary)
- **kurt content list** with analytics filters for complex queries
- **kurt content stats --show-analytics** for threshold calculation

**Example delegation:**
```python
def identify_affected(search_term, content_type):
    # Step 1: Get documents (delegates to CLI)
    docs = run_command(f"kurt content list --url-contains {search_term} --with-analytics")

    # Step 2: Get thresholds (delegates to analytics-query)
    thresholds = analytics_query.get_thresholds(domain)

    # Step 3: Apply workflow logic (this skill's responsibility)
    categorized = categorize_by_traffic_and_urgency(docs, thresholds)

    # Step 4: Present results (this skill's responsibility)
    present_prioritized_results(categorized)
```

---

## Prioritization Logic

### Traffic + Urgency Matrix

| Traffic Level | Declining | Stable | Increasing |
|---------------|-----------|--------|------------|
| **HIGH** (>p75) | 🚨 CRITICAL | 🎯 HIGH | 🎯 HIGH |
| **MEDIUM** (p25-p75) | 📊 MEDIUM | 📝 LOW | 📝 LOW |
| **LOW** (>0, ≤p25) | 📝 LOW | 📝 LOW | 📝 LOW |
| **ZERO** (0) | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? |

### Sort Order Within Categories

**CRITICAL (high traffic + declining):**
- Sort by: absolute pageviews DESC (biggest impact first)

**HIGH (high traffic, stable or increasing):**
- Declining first (if any)
- Then by pageviews DESC

**MEDIUM:**
- Declining first
- Then by pageviews DESC

**LOW:**
- By pageviews DESC (highest in category first)

**ZERO:**
- By age DESC (oldest first - likely deprecated)

---

## Error Handling

### No analytics data

```
⚠️ Analytics not configured

This operation requires analytics data for prioritization.

To enable:
1. Run: kurt analytics onboard <domain>
2. Sync data: kurt analytics sync <domain>

Without analytics, I can still show matching content, but won't be able to prioritize by traffic.

Continue without analytics? (Y/n)
```

If yes: Show results without traffic data, sorted by recency or alphabetically.

### No matching content

```
No content found matching "<search-term>"

Try:
- Broader search term
- Different content type
- Check if content exists: kurt content list --url-contains "<term>"
```

---

## Integration with Workflows

### Workflow 1: Tutorial Refresh

```
User: Update all BigQuery tutorials

Claude: I'll use content-analysis to find and prioritize BigQuery tutorials...

Claude (invokes content-analysis identify-affected --search-term "bigquery" --content-type tutorial):

[Shows prioritized results with traffic-based urgency]

User: Focus on critical and high priority

Claude: Working on 3 tutorials:
1. Python SDK Guide (CRITICAL)
2. Quickstart (HIGH)
3. Best Practices (HIGH)

[Proceeds with content-writing-skill for each]
```

### Workflow 4: Documentation Audit

```
User: Audit docs.company.com documentation

Claude (invokes content-analysis audit-traffic --domain docs.company.com):

[Shows audit report with traffic issues]

Based on the audit, I recommend:
1. Update 10 high-traffic stale pages
2. Investigate 14 pages with declining traffic
3. Review 12 zero-traffic pages

Which should we tackle first?
```

---

## Key Principles

1. **Traffic-based prioritization** - Always factor in traffic + urgency
2. **Actionable recommendations** - Suggest next steps based on results
3. **Workflow context** - Tailor presentation to workflow type
4. **Delegates complexity** - Uses analytics-query-skill for simple queries
5. **Clear categories** - CRITICAL/HIGH/MEDIUM/LOW/ZERO with visual hierarchy

---

## See Also

- **analytics-query-skill** - Low-level queries used by this skill
- **WORKFLOWS.md** - Full workflow scenarios using this skill
- **CLAUDE.md** - User-facing documentation
