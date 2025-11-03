# Available Utilities for Project Planning

## Overview

This document describes **intelligence operations** available during project planning. These utilities help you identify WHAT content to work on before you start writing.

**When to use:** During project planning (Step 4 of `create-project`) to identify target content based on data rather than guessing.

**Key principle:** Intelligence utilities = information gathering. They answer questions like:
- Which existing content needs updating? → `audit-traffic`, `identify-affected`
- What new content should we create? → `compare-gaps`, `impact-estimate`
- Where are opportunities? → `trending`, `compare-coverage`

**All operations accessed via:** `intelligence <operation> [args]`

---

## Quick Reference by Project Intent

| Project Intent | Primary Utilities | Use Case |
|----------------|------------------|----------|
| **(c) Update technical docs** | `audit-traffic`, `identify-affected` | Find stale or declining content |
| **(b) New marketing/sales assets** | `compare-gaps`, `impact-estimate` | Find content opportunities |
| **(d) Competitive response** | `compare-coverage`, `compare-quality` | Analyze competitor content |
| **(a) One-off article/post** | `search`, `trending` | Research + find trending topics |

---

## Analytics Operations (6)

Low-level traffic queries for spot-checking and analysis.

### `top <N> [--metric pageviews_30d] [--url-prefix <domain>]`

**What it does:** Shows top N pages by traffic metric

**When to use in planning:**
- Quick check: "What's our most popular content?"
- Identifying high-value pages to maintain
- Understanding traffic distribution

**Example:**
```bash
intelligence top 10
```

**Output:** List of top 10 pages with traffic + trends (↑ ↓ →)

---

### `bottom <N> [--metric pageviews_30d] [--url-prefix <domain>]`

**What it does:** Shows lowest traffic pages

**When to use in planning:**
- Finding zero-traffic pages (candidates for archiving)
- Identifying underperforming content
- Spotting orphaned or deprecated docs

**Example:**
```bash
intelligence bottom 10
```

**Output:** Bottom 10 pages categorized by traffic tier

---

### `check <url-pattern>`

**What it does:** Get traffic for specific URL(s) matching pattern

**When to use in planning:**
- Spot-checking traffic for specific content
- Verifying traffic claims
- Quick lookup during planning discussions

**Example:**
```bash
intelligence check "bigquery"
```

**Output:** All pages matching "bigquery" with traffic categories

---

### `trending [--url-prefix <domain>]`

**What it does:** Shows pages with increasing traffic

**When to use in planning:**
- Finding momentum topics (create more content here)
- Identifying successful content to build on
- Spotting emerging user interests

**Example:**
```bash
intelligence trending
```

**Output:** Pages gaining traffic with growth percentages

**Project planning use:** Create more content on trending topics

---

### `declining [--url-prefix <domain>]`

**What it does:** Shows pages with decreasing traffic

**When to use in planning:**
- Finding content that needs urgent attention
- Prioritizing updates (high traffic + declining = critical)
- Identifying potential problems

**Example:**
```bash
intelligence declining
```

**Output:** Pages losing traffic with urgency indicators

**Project planning use:** Add declining high-traffic pages as project targets

---

### `summary <domain>`

**What it does:** Shows overall analytics summary for domain

**When to use in planning:**
- Getting domain health overview
- Understanding traffic thresholds (p25/p75)
- Setting context before detailed analysis

**Example:**
```bash
intelligence summary docs.company.com
```

**Output:** Traffic distribution, thresholds, health check

**Project planning use:** Start here to understand baseline before diving deep

---

## Research Operations (6)

External research using AI and community monitoring.

### `search "<query>" [--recency hour|day|week|month] [--save]`

**What it does:** AI-powered research using Perplexity

**When to use in planning:**
- Step 3: Gathering reference sources for project
- Understanding topic landscape
- Finding recent developments/news
- Competitive intelligence

**Example:**
```bash
intelligence search "AI coding tools trends" --recency week --save
```

**Output:** Research summary with citations, saved to `sources/research/`

**Project planning use:** Research topics before writing, find reference material

**Recency guidance:**
- `hour` - Breaking news
- `day` - Recent news (default)
- `week` - Trends, weekly roundups
- `month` - Monthly analysis
- Omit - Timeless/general queries

---

### `list [--limit N]`

**What it does:** Browse past research results

**When to use in planning:**
- Reviewing previous research
- Finding past analysis for reuse
- Checking what's already been researched

**Example:**
```bash
intelligence list --limit 10
```

**Output:** Recent research files with metadata

---

### `get <filename>`

**What it does:** Display specific research result

**When to use in planning:**
- Retrieving past research details
- Referencing previous analysis
- Checking research sources

**Example:**
```bash
intelligence get 2025-11-02-dbt-vs-dataform
```

**Output:** Full research content with citations

---

### `reddit -s <subreddit> [--keywords "..."] [--min-score N]`

**What it does:** Monitor Reddit for trending discussions

**When to use in planning:**
- Finding what your audience is discussing
- Identifying pain points and questions
- Discovering content opportunities

**Example:**
```bash
intelligence reddit -s dataengineering --timeframe day --min-score 10
```

**Output:** Trending posts with scores and relevance

**Project planning use:** Find topics users are actively discussing

---

### `hackernews [--keywords "..."] [--min-score N]`

**What it does:** Monitor Hacker News for trending tech discussions

**When to use in planning:**
- Finding trending tech topics
- Understanding developer interests
- Spotting newsworthy developments

**Example:**
```bash
intelligence hackernews --keywords "AI" --timeframe day
```

**Output:** Trending HN stories with points and comments

**Project planning use:** Identify timely topics for content

---

### `feeds <feed-url> [--keywords "..."] [--since "7 days"]`

**What it does:** Monitor RSS/Atom feeds for new content

**When to use in planning:**
- Tracking competitor blog posts
- Monitoring industry announcements
- Finding reference sources

**Example:**
```bash
intelligence feeds https://blog.getdbt.com/rss.xml --since "7 days"
```

**Output:** Recent feed entries matching criteria

**Project planning use:** Monitor competitor content for competitive analysis

---

## Content Intelligence Operations (6)

Complex analysis combining content metadata + analytics for project planning.

### `identify-affected --search-term <term> [--content-type <type>]`

**What it does:** Find content by keyword with traffic-based prioritization

**When to use in planning:**
- **Intent (c)**: "Update all BigQuery tutorials"
- Finding content about specific topic
- Traffic-based urgency matrix (CRITICAL → HIGH → MEDIUM → LOW → ZERO)

**Example:**
```bash
intelligence identify-affected --search-term "bigquery" --content-type tutorial
```

**Output:** Prioritized list with urgency matrix:

| Traffic | Declining | Stable | Increasing |
|---------|-----------|--------|------------|
| **HIGH** | 🚨 CRITICAL | 🎯 HIGH | 🎯 HIGH |
| **MEDIUM** | 📊 MEDIUM | 📝 LOW | 📝 LOW |
| **LOW** | 📝 LOW | 📝 LOW | 📝 LOW |
| **ZERO** | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? | ⚠️ ARCHIVE? |

**Project planning use:**
1. Run for topic
2. Select CRITICAL and HIGH priority items as project targets
3. Record in project.md "How Identified" section

---

### `audit-traffic --domain <domain>`

**What it does:** Comprehensive traffic audit identifying issues

**When to use in planning:**
- **Intent (c)**: "Make sure docs are up-to-date"
- Domain-wide content health check
- Finding multiple types of issues at once

**Example:**
```bash
intelligence audit-traffic --domain docs.company.com
```

**Output:** Audit report with:
- High-traffic stale content (needs refresh)
- Declining traffic pages (needs investigation)
- Zero-traffic pages (orphaned or deprecated)

**Project planning use:**
1. Run audit on domain
2. Review findings by category
3. Select highest-priority issues as project targets
4. Document analysis in project.md

---

### `impact-estimate --topic <topic> --domain <domain>`

**What it does:** Estimate traffic potential of creating new content

**When to use in planning:**
- **Intent (b)**: "Should we create security documentation?"
- Prioritizing new content opportunities
- Justifying content investments

**Example:**
```bash
intelligence impact-estimate --topic "security" --domain docs.company.com
```

**Output:** Impact assessment:
- HIGH: >5000 views/month total related traffic
- MEDIUM: 1000-5000 views/month
- LOW: <1000 views/month

**Project planning use:**
1. Run for each potential topic
2. Prioritize HIGH impact topics
3. Add to project targets with impact justification

---

### `compare-gaps --own <domain> --competitor <domain>`

**What it does:** Find missing content vs competitor

**When to use in planning:**
- **Intent (b)**: "Write new marketing assets"
- **Intent (d)**: "Competitive response"
- Finding content opportunities
- Identifying strategic gaps

**Example:**
```bash
intelligence compare-gaps --own docs.yourco.com --competitor docs.competitor.com
```

**Output:** Missing topics categorized by priority

**Project planning use:**
1. Run gap analysis
2. Review HIGH PRIORITY gaps
3. Combine with `impact-estimate` for each gap
4. Select gaps to fill as project targets

**Prerequisites:** Competitor content must be indexed:
```bash
kurt map url <competitor-url>
kurt fetch --include "<competitor-domain>/*"
kurt cluster-urls  # Organize into topics
```

---

### `compare-coverage --own <domain> --competitor <domain>`

**What it does:** Compare content type and topic coverage

**When to use in planning:**
- **Intent (b)**: Understanding content mix gaps
- **Intent (d)**: Competitive benchmarking
- Identifying structural differences

**Example:**
```bash
intelligence compare-coverage --own docs.yourco.com --competitor docs.competitor.com
```

**Output:** Coverage comparison tables:
- Content type comparison (Tutorials, Guides, Examples, etc.)
- Topic cluster comparison
- Identifies areas you're under-investing

**Project planning use:**
1. Run coverage analysis
2. Identify content type gaps (e.g., need more tutorials)
3. Create project focusing on underrepresented types

---

### `compare-quality --own <domain> --competitor <domain>`

**What it does:** Compare content depth and quality metrics

**When to use in planning:**
- **Intent (c)**: "Make docs more comprehensive"
- **Intent (d)**: Competitive quality assessment
- Setting quality bar for content

**Example:**
```bash
intelligence compare-quality --own docs.yourco.com --competitor docs.competitor.com
```

**Output:** Quality comparison:
- Average word count by content type
- Code examples per doc
- Images/diagrams per doc
- Update frequency

**Project planning use:**
1. Run quality analysis
2. Identify quality gaps (e.g., tutorials 50% shorter)
3. Set quality targets for project
4. Document quality bar in project.md

---

## Integration with Project Planning

### Step-by-Step: Using Utilities in `create-project`

**Step 4: Identify Target Content** uses these utilities to find WHAT to work on.

#### For Intent (c): Update/maintain technical docs

**Option 1: Traffic Analysis**
```bash
# Get domain overview
intelligence summary docs.company.com

# Find issues
intelligence audit-traffic --domain docs.company.com

# Result: 10 high-traffic stale pages identified
# → Select 5 critical priority items as targets
```

**Option 2: Topic-Specific**
```bash
# Find content about specific topic
intelligence identify-affected --search-term "authentication" --content-type guide

# Result: 8 guides found, 3 CRITICAL priority
# → Add CRITICAL items as targets
```

#### For Intent (b): Write new marketing/sales assets

**Option 1: Gap Analysis**
```bash
# Find what competitor has that you don't
intelligence compare-gaps --own docs.yourco.com --competitor docs.competitor.com

# Estimate impact of filling gaps
intelligence impact-estimate --topic "security" --domain docs.yourco.com

# Result: Security docs have HIGH impact (8,500 views/month related)
# → Create project to build security content
```

**Option 2: Coverage Analysis**
```bash
# Compare content types
intelligence compare-coverage --own docs.yourco.com --competitor docs.competitor.com

# Result: Need 13 more tutorials (15 vs 28)
# → Create project to expand tutorial coverage
```

#### For Intent (d): Competitive response

**Comprehensive Analysis**
```bash
# 1. Find gaps
intelligence compare-gaps --own docs.yourco.com --competitor docs.competitor.com

# 2. Compare coverage
intelligence compare-coverage --own docs.yourco.com --competitor docs.competitor.com

# 3. Compare quality
intelligence compare-quality --own docs.yourco.com --competitor docs.competitor.com

# Result: Multiple dimensions of competitive position
# → Create project addressing highest-priority competitive gaps
```

#### For Intent (a): One-off article/post

**Research + Trend Analysis**
```bash
# Research topic
intelligence search "AI coding tools trends" --recency week --save

# Check trending discussions
intelligence reddit -s programming --keywords "AI coding"
intelligence hackernews --keywords "AI tools"

# Result: Trending topics + research sources
# → Write article on timely topic with solid research
```

---

## Documenting Analysis in project.md

When you use utilities during planning, document in project.md:

```markdown
## How These Were Identified

Analysis: `intelligence audit-traffic --domain docs.company.com`

Results:
- Found 10 high-traffic stale pages (>365 days old, >890 views/month)
- Found 14 pages with declining traffic (>10% drop)
- Selected: 5 critical priority items (high traffic + declining)

Prioritization rationale:
- "Python SDK Guide" (2,103 views/month, ↓ -8%, 720 days old)
  → Losing 168 views/month - highest impact to fix
```

This creates audit trail and justifies target selection.

---

## Error Handling

### Analytics not configured
```
⚠️ Analytics required for traffic-based operations

To enable:
1. kurt analytics onboard <domain>
2. kurt analytics sync <domain>

Operations requiring analytics:
- identify-affected, audit-traffic, impact-estimate
- top, bottom, trending, declining, summary, check
```

### Competitor content not indexed
```
⚠️ Competitor content not indexed yet

To analyze competitor:
1. kurt map url <competitor-url>
2. kurt fetch --include "<competitor-domain>/*"
3. kurt cluster-urls (to organize into topics)
4. Re-run comparison
```

### No results found
```
No content found matching criteria

Try:
- Broader search term
- Different content type filter
- Check if content is fetched: kurt content list
```

---

## Key Principles

1. **Used during planning** - These utilities help you decide WHAT to work on (Step 4)
2. **Data-driven decisions** - Traffic + metadata beats guessing
3. **Prioritization** - Always factor in traffic + urgency
4. **Documented rationale** - Record analysis in project.md "How Identified" section
5. **Composable** - Combine multiple utilities for comprehensive analysis

---

## See Also

- **`intelligence-skill`** - Technical implementation of these operations
- **`project-management-skill`** - Uses utilities in Step 4 of create-project
- **`workflow-skill`** - Default workflows compose utility operations
- **`.claude/workflows/default-workflows.yaml`** - Built-in workflow examples
