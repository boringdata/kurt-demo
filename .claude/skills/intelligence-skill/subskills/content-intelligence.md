# Content Intelligence Subskill

**Purpose:** Complex content analysis combining content metadata + analytics
**Parent Skill:** intelligence
**Operations:** identify-affected, audit-traffic, impact-estimate, compare-gaps, compare-coverage, compare-quality

---

## Overview

Provides sophisticated content analysis for project planning. These operations combine content metadata, traffic data, and competitive intelligence to help identify what content needs work.

**Primary use:** Project planning Step 4 (identify targets)

**When to use:**
- Finding content that needs updating (identify-affected, audit-traffic)
- Estimating value of new content (impact-estimate)
- Competitive analysis (compare-gaps, compare-coverage, compare-quality)

---

## Operations

### 1. `identify-affected --search-term <term> [--content-type <type>]`

**Purpose:** Find content by keyword with traffic-based prioritization

**Use case:** "Update all BigQuery tutorials" or "Find stale content about X"

**Implementation:**
```bash
# 1. Find matching content
kurt content list \
  --url-contains "<search-term>" \
  ${content_type:+--content-type $content_type} \
  --with-analytics \
  --order-by pageviews_30d desc

# 2. Get traffic thresholds
stats=$(kurt content stats --show-analytics --format json)
p25=$(echo "$stats" | jq '.p25_pageviews_30d')
p75=$(echo "$stats" | jq '.p75_pageviews_30d')

# 3. Categorize by traffic + urgency (traffic x trend)
# 4. Present prioritized results
```

**Example:**
```
intelligence identify-affected --search-term "bigquery" --content-type tutorial

Found 23 tutorials matching "bigquery":

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 CRITICAL PRIORITY (high traffic + declining):
1. "Python SDK Guide" (2,103 views/month, ↓ -8%, 720 days old)
   → Losing 168 views/month - needs urgent refresh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 HIGH PRIORITY (high traffic, >890 views/month):
2. "BigQuery Quickstart" (3,421 views/month, ↑ +15%, 850 days old)
   → Increasing traffic - update to capitalize on momentum
3. "SQL Best Practices" (1,850 views/month, → stable, 450 days old)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MEDIUM PRIORITY (medium traffic, 45-890 views/month):
[10 tutorials] - 2 declining, 8 stable/increasing

📝 LOW PRIORITY (low traffic, ≤45 views/month):
[5 tutorials]

⚠️ ZERO TRAFFIC (consider archiving):
- "Advanced BigQuery ML" (0 views, 950 days old)
- "Legacy SQL Guide" (0 views, 1200 days old)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation:
1. Start with CRITICAL (Python SDK) - urgent + high impact
2. Then HIGH priority (2 tutorials) - maintain momentum
3. Then MEDIUM declining - prevent further drops
```

**Prioritization Matrix:**

| Traffic | Declining | Stable | Increasing |
|---------|-----------|--------|------------|
| **HIGH** (>p75) | 🚨 CRITICAL | 🎯 HIGH | 🎯 HIGH |
| **MEDIUM** (p25-p75) | 📊 MEDIUM | 📝 LOW | 📝 LOW |
| **LOW** (>0, ≤p25) | 📝 LOW | 📝 LOW | 📝 LOW |
| **ZERO** (0) | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? |

---

### 2. `audit-traffic --domain <domain>`

**Purpose:** Comprehensive traffic audit identifying issues

**Use case:** "Audit docs.company.com to find what needs attention"

**Implementation:**
```bash
# 1. Get analytics summary
intelligence summary <domain>

# 2. Find high-traffic stale pages (>p75 traffic + >365 days old)
kurt content list \
  --url-starts-with <domain> \
  --with-analytics \
  --order-by pageviews_30d desc

# 3. Find declining traffic pages
kurt content list \
  --url-starts-with <domain> \
  --with-analytics \
  --pageviews-trend decreasing \
  --order-by trend_percentage

# 4. Find zero-traffic pages
kurt content list \
  --url-starts-with <domain> \
  --with-analytics
  # Filter pageviews_30d == 0

# 5. Present audit report
```

**Example:**
```
intelligence audit-traffic --domain docs.company.com

Traffic Audit: docs.company.com

Overview:
- 234 total pages
- 222 with traffic (95%)
- 12 ZERO traffic (5%)
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
Pages losing >10% traffic:

1. "Python SDK Guide" (↓ -8%, -168 views/month)
2. "Data Loading Guide" (↓ -12%, -168 views/month)

Possible causes:
- Content outdated
- Better alternatives published elsewhere
- Search ranking dropped

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ZERO TRAFFIC (orphaned or deprecated):
12 pages with 0 views in last 30 days

- "Advanced BigQuery ML" (950 days old)
- "Legacy SQL Guide" (1200 days old)
[10 more]

Actions:
1. Check if linked from anywhere
2. Review if still relevant
3. Archive or improve discoverability

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
1. Update 10 high-traffic stale pages - max impact
2. Investigate 14 declining pages - prevent further drops
3. Audit 12 zero-traffic pages - clean up or improve
```

---

### 3. `impact-estimate --topic <topic> --domain <domain>`

**Purpose:** Estimate traffic potential of creating new content

**Use case:** "Should we create security documentation? What's the impact?"

**Implementation:**
```bash
# 1. Find related existing content
kurt content list \
  --url-contains "<related-keyword>" \
  --url-starts-with <domain> \
  --with-analytics

# 2. Calculate related content traffic
total_views = sum(page.pageviews_30d)
avg_views = total_views / count

# 3. Estimate impact:
#    HIGH: >5000 views/month total
#    MEDIUM: 1000-5000 views/month
#    LOW: <1000 views/month
```

**Example:**
```
intelligence impact-estimate --topic "security" --domain docs.company.com

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
```

---

### 4. `compare-gaps --own <domain> --competitor <domain>`

**Purpose:** Find missing content vs competitor

**Use case:** "What content does competitor.com have that we don't?"

**Implementation:**
```bash
# 1. Get both content sets
own=$(kurt content list --url-starts-with <own-domain>)
competitor=$(kurt content list --url-starts-with <competitor-domain>)

# 2. Identify competitor topics/clusters not in your content
# 3. Prioritize by relevance + estimated traffic potential
```

**Example:**
```
intelligence compare-gaps --own docs.yourco.com --competitor docs.competitor.com

Content Gap Analysis: yourco vs competitor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MISSING TOPICS (they have, you don't):

🎯 HIGH PRIORITY:
1. Security & Compliance (8 docs)
   - Security best practices
   - Encryption guides
   - Audit logging
   - Compliance certifications

2. Integration Guides (12 docs)
   - Salesforce integration
   - AWS integration
   - Azure integration

📊 MEDIUM PRIORITY:
3. Advanced Features (5 docs)
4. Troubleshooting (7 docs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation:
Focus on Security & Compliance first - likely high traffic + critical for buyers.
```

---

### 5. `compare-coverage --own <domain> --competitor <domain>`

**Purpose:** Compare content type and topic coverage

**Use case:** "How does our documentation compare to theirs?"

**Implementation:**
```bash
# 1. Get content by type for both domains
own_by_type=$(kurt content list --url-starts-with <own> --format json | group by type)
competitor_by_type=$(kurt content list --url-starts-with <competitor> --format json | group by type)

# 2. Compare counts and topics
# 3. Show coverage matrix
```

**Example:**
```
intelligence compare-coverage --own docs.yourco.com --competitor docs.competitor.com

Content Coverage Comparison: yourco vs competitor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTENT TYPE COMPARISON:

Type            | Yours | Theirs | Gap
----------------|-------|--------|--------
Tutorials       |   15  |   28   | -13 ⚠️
API Reference   |   42  |   38   | +4 ✅
Guides          |   18  |   32   | -14 ⚠️
Examples        |    8  |   24   | -16 ⚠️
Troubleshooting |    5  |   18   | -13 ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOPIC COVERAGE:

Topic Cluster  | Yours | Theirs | Coverage
---------------|-------|--------|----------
Getting Started|   12  |   10   | 120% ✅
Authentication |    8  |   15   | 53% ⚠️
Data Management|   10  |   18   | 56% ⚠️
Integrations   |    6  |   24   | 25% 🚨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
1. Add 13+ tutorials - biggest gap
2. Expand integrations coverage (6 vs 24)
3. Strengthen troubleshooting (5 vs 18)
```

---

### 6. `compare-quality --own <domain> --competitor <domain>`

**Purpose:** Compare content depth and quality metrics

**Use case:** "Are our docs as comprehensive as theirs?"

**Implementation:**
```bash
# 1. Get content with metadata
own=$(kurt content list --url-starts-with <own> --format json)
competitor=$(kurt content list --url-starts-with <competitor> --format json)

# 2. Calculate metrics:
#    - Average word count
#    - Code examples per doc
#    - Images/diagrams per doc
#    - Update frequency

# 3. Compare by content type
```

**Example:**
```
intelligence compare-quality --own docs.yourco.com --competitor docs.competitor.com

Content Quality Comparison: yourco vs competitor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEPTH METRICS (by content type):

Tutorials:
  Avg word count:     1,200 vs 2,400  ⚠️ (50% of theirs)
  Code examples/doc:    1.2 vs 3.8    ⚠️
  Images/doc:           0.8 vs 2.1    ⚠️

API Reference:
  Avg word count:       800 vs 650    ✅
  Code examples/doc:    2.5 vs 2.1    ✅
  Images/doc:           0.3 vs 0.4    →

Guides:
  Avg word count:     1,800 vs 2,200  → (82% of theirs)
  Code examples/doc:    2.1 vs 3.2    ⚠️
  Images/doc:           1.5 vs 2.8    ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UPDATE FREQUENCY:

Your content:
  Last 30 days:   3 updates
  Last 90 days:  12 updates
  Average age:   420 days

Their content:
  Last 30 days:  15 updates  ⚠️ (5x more active)
  Last 90 days:  48 updates
  Average age:   180 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
1. Expand tutorials - 50% shorter than theirs
2. Add more code examples across all types
3. Increase visual content (diagrams, screenshots)
4. Update content more frequently (quarterly → monthly)
```

---

## Error Handling

### Analytics not configured
```
⚠️ Analytics required for this operation

To enable:
1. kurt analytics onboard <domain>
2. kurt analytics sync <domain>

Operations requiring analytics:
- identify-affected (needs traffic data)
- audit-traffic (needs traffic data)
- impact-estimate (estimates based on related traffic)
```

### No results found
```
No content found matching criteria

Try:
- Broader search term
- Different content type
- Check if content is fetched: kurt content list
```

### Competitor content not fetched
```
⚠️ Competitor content not indexed yet

To analyze competitor:
1. kurt map url <competitor-url>
2. kurt fetch --include "<competitor-domain>/*"
3. kurt cluster-urls (to organize into topics)
4. Re-run comparison
```

---

## Key Principles

1. **Traffic-based prioritization** - Always factor in traffic + urgency
2. **Actionable recommendations** - Suggest specific next steps
3. **Context for planning** - Used during project planning (Step 4)
4. **Combines data sources** - Content metadata + analytics + competitive intel
5. **Visual hierarchy** - Clear categories (CRITICAL/HIGH/MEDIUM/LOW/ZERO)
