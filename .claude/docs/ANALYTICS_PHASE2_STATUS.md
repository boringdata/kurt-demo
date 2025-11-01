# Analytics Phase 2 Implementation Status

**Date:** 2025-10-30
**Status:** Phase 2A Complete, Phase 2B/2C/2D In Progress

---

## Summary

Phase 2 integrates analytics into Kurt workflows at multiple levels:
1. **CLI layer** (kurt-core) - Analytics filters and stats ✅ COMPLETE
2. **Analytics query skill** (kurt-demo) - Low-level ad-hoc queries 🚧 IN PROGRESS
3. **Content analysis skill** (kurt-demo) - Complex workflows using analytics ⏳ PENDING
4. **Project management integration** (kurt-demo) - Analytics in project workflows ⏳ PENDING

---

## Phase 2A: CLI Analytics Enhancements ✅ COMPLETE

### Changes Made in kurt-core

#### 1. Extended `src/kurt/document.py`

**Added analytics support to `list_documents()` function:**
- New parameters:
  - `with_analytics`: bool - Include analytics data in results (LEFT JOIN)
  - `pageviews_30d_min`: Optional[int] - Filter by minimum pageviews
  - `pageviews_30d_max`: Optional[int] - Filter by maximum pageviews
  - `pageviews_trend`: Optional[str] - Filter by trend (increasing/stable/decreasing)
  - `order_by`: Optional[str] - Sort by created_at, pageviews_30d, pageviews_60d, trend_percentage

**Added new function `get_analytics_stats(url_prefix)`:**
- Calculates percentile-based traffic thresholds (p25, p50, p75)
- Categories: ZERO (0 views), LOW (≤p25), MEDIUM (p25-p75), HIGH (>p75)
- Returns distribution statistics for domain

**Key Design Decision:** Percentile-based thresholds adapt to each site's traffic distribution

#### 2. Enhanced `src/kurt/commands/content.py`

**Updated `kurt content list` command:**
- Added CLI options:
  - `--with-analytics` - Show traffic columns
  - `--pageviews-30d-min <n>` - Filter minimum traffic
  - `--pageviews-30d-max <n>` - Filter maximum traffic
  - `--pageviews-trend <increasing|stable|decreasing>` - Filter by trend
  - `--order-by <field>` - Sort by analytics fields

**Enhanced table output:**
- When `--with-analytics` used:
  - Shows "Views (30d)" column
  - Shows "Trend" column with symbols (↑ ↓ →) and percentage
  - Color-coded trends (green=increasing, yellow=stable, red=decreasing)

**Enhanced JSON output:**
- When `--with-analytics` used, includes analytics object per document

**Updated `kurt content stats` command:**
- Added options:
  - `--url-starts-with <prefix>` - Scope to domain
  - `--show-analytics` - Display traffic distribution

**New analytics stats output:**
```
Analytics Statistics
────────────────────────────────────────
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
```

### Testing Commands

```bash
# List high-traffic pages
kurt content list \
  --with-analytics \
  --pageviews-30d-min 500 \
  --order-by pageviews_30d

# Find pages losing traffic
kurt content list \
  --with-analytics \
  --pageviews-trend decreasing \
  --order-by trend_percentage

# Get traffic distribution for domain
kurt content stats \
  --show-analytics \
  --url-starts-with https://docs.company.com
```

---

## Phase 2B: Analytics Query Skill 🚧 IN PROGRESS

### Planned Structure

**Location:** `.claude/skills/analytics-query-skill/`

**Purpose:** Low-level, ad-hoc analytics queries (simple operations)

**Operations to implement:**

1. **`top <N> [--metric pageviews_30d] [--url-prefix <domain>]`**
   ```bash
   kurt content list \
     --with-analytics \
     --order-by pageviews_30d \
     --limit 10
   ```

2. **`bottom <N> [--metric pageviews_30d] [--url-prefix <domain>]`**
   ```bash
   kurt content list \
     --with-analytics \
     --order-by pageviews_30d \
     --limit 10
   # (reverse order)
   ```

3. **`traffic-for <url-pattern>`**
   ```bash
   kurt content list \
     --url-contains "bigquery" \
     --with-analytics
   ```

4. **`trending [--direction increasing|decreasing]`**
   ```bash
   kurt content list \
     --with-analytics \
     --pageviews-trend decreasing \
     --order-by trend_percentage
   ```

5. **`summary <domain>`**
   ```bash
   kurt content stats \
     --show-analytics \
     --url-starts-with <domain>
   ```

**When to use (documented in SKILL.md):**
- User asks simple traffic questions: "Which pages get the most traffic?"
- Spot-checking specific pages: "How's the traffic for X?"
- Identifying trends: "What's losing traffic?"

---

## Phase 2C: Content Analysis Skill ⏳ PENDING

### Planned Structure

**Location:** `.claude/skills/content-analysis-skill/`

**Purpose:** Complex workflow operations combining content + analytics

**Operations to implement:**

1. **`identify-affected --search-term <term> --content-type <type>`**
   - Used in: Workflow 1 (Tutorial Refresh)
   - Groups results by traffic: ZERO / LOW / MEDIUM / HIGH
   - Uses percentile thresholds from `get_analytics_stats()`
   - Flags declining-traffic pages as urgent

2. **`compare-traffic --own <domain> --competitor <domain>`**
   - Used in: Workflow 2 (Competitive Gap Analysis)
   - Compare traffic patterns between domains

3. **`audit-traffic --domain <domain>`**
   - Used in: Workflow 4 (Documentation Audit)
   - Flags:
     - High-traffic pages that are stale
     - Low-traffic pages on important topics
     - Pages with declining traffic

4. **`impact-estimate --topic <topic> --domain <domain>`**
   - Used in: Workflow 4 (Documentation Audit)
   - Estimate impact of creating missing content

**When to use:**
- Complex workflows from WORKFLOWS.md
- Need traffic-based prioritization
- Combining multiple filters + analytics
- Impact estimation

**Delegates to:**
- `analytics-query-skill` for simple queries
- `kurt content list` with analytics filters
- `kurt content stats --show-analytics`

---

## Phase 2D: Project Management Integration ⏳ PENDING

### Changes Needed

#### 1. Update `check-foundation.md` subskill

**Add analytics setup as optional step during content mapping:**

```markdown
## Step 2: Check for Organizational Content Map

...existing content map check...

### 2.3: Check Analytics Integration (Optional)

After content map is established, offer analytics setup:

**Check if analytics configured:**
```bash
kurt analytics list --format json
```

**If no analytics configured:**
```
💡 Tip: Enable analytics for traffic-based prioritization

Would you like to set up analytics for your content?

This allows Kurt to:
- Prioritize high-traffic pages for updates
- Identify declining-traffic pages needing refresh
- Spot zero-traffic pages (orphaned or low-quality)

Setup takes ~2 minutes. Set up now? (Y/n)
```

**If yes:**
```
Which domain has web analytics?
(e.g., docs.company.com, blog.company.com)

Domain: [user input]

I'll guide you through connecting PostHog analytics...

[Invoke kurt analytics onboard command]
```

**If no:**
```
You can enable analytics anytime with:
kurt analytics onboard <domain>
```
```

#### 2. Update `CLAUDE.md` documentation

**Add section after "Research Integration":**

```markdown
## Analytics Integration (Optional)

Kurt integrates with PostHog web analytics to enable **traffic-based content prioritization**.

### When Analytics Appears in Workflows

**During project setup (check-foundation):**
- Optional step after content mapping
- Prompts to connect PostHog for your domain

**When using content-analysis-skill:**
- Automatic traffic-based prioritization
- Groups results by ZERO/LOW/MEDIUM/HIGH traffic
- Flags declining-traffic pages as urgent

**Ad-hoc with analytics-query-skill:**
- "Show me top 10 pages by traffic"
- "Which pages are losing traffic?"
- "What's the traffic for X?"

### Example: Traffic-Based Tutorial Refresh

```
User: Update all BigQuery tutorials

Claude (uses content-analysis identify-affected):

Found 23 tutorials. Checking traffic data...

ZERO TRAFFIC (0 views/month): 2 tutorials
- "Advanced BigQuery ML" (0 views, 950 days old) - Consider archiving?
- "BigQuery Legacy SQL" (0 views, 1200 days old) - Deprecated content

LOW TRAFFIC (≤45 views/month): 5 tutorials
[...list...]

MEDIUM TRAFFIC (45-890 views/month): 10 tutorials
[...list...]

HIGH TRAFFIC (>890 views/month): 6 tutorials
1. "BigQuery Quickstart" (3,421 views, ↑ +15%, 850 days old)
2. "Python SDK Guide" (2,103 views, ↓ -8%, 720 days old) ⚠️ URGENT
3. "SQL Best Practices" (1,850 views, → stable, 450 days old)

Recommendation:
1. HIGH priority with declining traffic first (max impact + urgency)
2. Then HIGH priority with increasing traffic (capitalize on momentum)
3. Then MEDIUM/LOW traffic
4. Consider archiving ZERO traffic pages

Start with Python SDK Guide? (losing traffic, needs refresh urgently)
```
```

---

## Key Design Decisions

### 1. Percentile-Based Thresholds ✅ IMPLEMENTED
- Each domain has unique traffic distribution
- p25 = LOW threshold, p75 = HIGH threshold
- Calculated dynamically from actual data
- 4 categories: ZERO (0), LOW (≤p25), MEDIUM (p25-p75), HIGH (>p75)

### 2. Skill Hierarchy
- **analytics-query-skill** = Low-level, simple operations
  - Wraps CLI commands
  - Used by user directly OR by content-analysis-skill
- **content-analysis-skill** = High-level, complex workflows
  - Uses analytics-query-skill internally
  - Combines multiple operations
  - Traffic-based prioritization logic

### 3. Analytics in Project Setup
- Optional step during `check-foundation`
- Only appears AFTER content map is established
- Non-blocking (can skip and enable later)
- Prompts once per domain

### 4. Traffic Trend Symbols
- ↑ increasing (+10% or more)
- → stable (-10% to +10%)
- ↓ decreasing (-10% or more)
- Color-coded: green/yellow/red

---

## Next Steps

### Immediate (Phase 2B)
1. Create `.claude/skills/analytics-query-skill/SKILL.md`
2. Implement 5 operations (top, bottom, traffic-for, trending, summary)
3. Document when to use vs content-analysis-skill

### Then (Phase 2C)
1. Create `.claude/skills/content-analysis-skill/SKILL.md`
2. Implement 4 operations (identify-affected, compare-traffic, audit-traffic, impact-estimate)
3. Each operation uses analytics-query-skill + analytics-enhanced CLI
4. Test with Workflow 1 (Tutorial Refresh) scenario

### Finally (Phase 2D)
1. Update `check-foundation.md` with analytics setup step
2. Update `CLAUDE.md` with full analytics documentation
3. Test full workflow: create project → setup analytics → use in content work

---

## Files Modified (Phase 2A)

### kurt-core
```
src/kurt/
├── document.py                         (MODIFIED - added analytics params + get_analytics_stats)
└── commands/
    └── content.py                      (MODIFIED - analytics options + enhanced stats)
```

### kurt-demo
```
.claude/docs/
└── ANALYTICS_PHASE2_STATUS.md          (NEW - this file)
```

---

## Success Criteria

**Phase 2A** ✅
- ✅ `kurt content list --with-analytics` shows traffic columns
- ✅ `kurt content list --pageviews-30d-min 500` filters by traffic
- ✅ `kurt content stats --show-analytics` shows percentile-based distribution
- ✅ Percentiles calculated dynamically per domain

**Phase 2B** (In Progress)
- ⏳ User asks "show me top 10 pages" → analytics-query-skill top 10
- ⏳ User asks "what's losing traffic?" → analytics-query-skill trending --direction decreasing
- ⏳ Skill documentation clear on when to use

**Phase 2C** (Pending)
- ⏳ Workflow 1 scenario works: identify-affected returns traffic-prioritized list
- ⏳ Results grouped by ZERO/LOW/MEDIUM/HIGH using percentile thresholds
- ⏳ Declining-traffic pages flagged as urgent

**Phase 2D** (Pending)
- ⏳ check-foundation offers analytics setup after content map
- ⏳ CLAUDE.md documents analytics integration
- ⏳ Full workflow tested: create project → setup analytics → use in content work

---

## Testing After Full Implementation

```bash
# 1. Setup analytics
kurt analytics onboard docs.company.com
kurt analytics sync docs.company.com

# 2. Test CLI layer
kurt content stats --show-analytics --url-starts-with https://docs.company.com
kurt content list --with-analytics --order-by pageviews_30d --limit 10
kurt content list --pageviews-trend decreasing --with-analytics

# 3. Test analytics-query-skill
# (via Claude): "Show me the top 10 pages by traffic"
# (via Claude): "Which pages are losing traffic?"

# 4. Test content-analysis-skill
# (via Claude): "Find all BigQuery tutorials and prioritize by traffic"

# 5. Test project workflow
# (via Claude): "/create-project" → check-foundation → analytics setup prompt
```
