# Kurt Analytics Integration

**Purpose**: Design document for integrating web analytics (PostHog) with Kurt's document intelligence system.

**Status**: Design document (not implementation)

---

## Table of Contents

1. [Overview](#overview)
2. [Key Principles](#key-principles)
3. [Architecture](#architecture)
4. [URL Normalization](#url-normalization)
5. [Database Schema](#database-schema)
6. [CLI Commands](#cli-commands)
7. [PostHog Integration](#posthog-integration)
8. [Session Start Hook](#session-start-hook)
9. [Impact on Workflows](#impact-on-workflows)
10. [Implementation Plan](#implementation-plan)

---

## Overview

Analytics integration enables **traffic-based prioritization** for content operations. By syncing web analytics data (pageviews, engagement metrics, trends) into the Kurt database, we can answer questions like:

- "Which stale tutorials get the most traffic?" (prioritize high-impact updates)
- "Which product pages have high bounce rates?" (quality issues)
- "Which topics are trending?" (content opportunity signals)

**Platform**: PostHog (starting point - technical product focus)

**Scope**: Domain-level (attached to sources, not projects)

---

## Key Principles

### 1. Domain-Scoped Analytics
Analytics are attached to **source domains**, not individual projects.

**Rationale**:
- A sitemap/domain (e.g., `docs.company.com`) has one PostHog project
- Multiple Kurt projects may reference content from the same domain
- Analytics data should be available to all projects using that domain

**Example**:
```
sources/
├── docs.company.com/           # Has PostHog analytics
│   ├── .analytics-meta.json    # PostHog config
│   └── [234 markdown files]
├── blog.company.com/           # Different PostHog project
│   ├── .analytics-meta.json
│   └── [67 markdown files]
├── competitor.com/             # No analytics (external)
└── research/                   # No analytics (research files)
```

### 2. URL Normalization
Normalize URLs for matching between Kurt documents and analytics events.

**Normalization rules**:
- Remove protocol (`https://`, `http://`)
- Remove `www.` prefix
- Remove trailing slashes
- Remove query parameters
- Remove fragments

**Example**:
```
https://www.docs.company.com/guides/quickstart/?utm_source=email#step-1
→ docs.company.com/guides/quickstart
```

### 3. Auto-Sync with Staleness Detection
Analytics data syncs automatically via session start hook if stale (>7 days).

**User experience**:
```
Claude Code session started

📊 Analytics data for docs.company.com is 8 days old.
Sync now? (recommended for accurate prioritization)

a) Yes, sync now
b) Skip for now
```

### 4. Rolling 60-Day Window
Store 60 days of analytics data split into two 30-day periods for MoM trend analysis.

**Time windows**:
- **60-day total**: Overall traffic volume
- **Last 30 days**: Recent performance
- **Previous 30 days** (days 31-60): Comparison baseline

**Trend calculation**:
```python
pageviews_trend = "increasing" if pageviews_30d > pageviews_previous_30d * 1.1 else
                  "decreasing" if pageviews_30d < pageviews_previous_30d * 0.9 else
                  "stable"

trend_percentage = ((pageviews_30d - pageviews_previous_30d) / pageviews_previous_30d) * 100
```

### 5. Default to Zero (with Domain Flag)
If a document exists but has no analytics data, default metrics to 0.

**Track domain-level data availability**:
- `AnalyticsDomain.has_data = true` means domain has analytics configured
- Individual documents may still have 0 pageviews (new content, low traffic)
- If `has_data = false`, analytics queries should ignore that domain

---

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Kurt CLI                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  kurt analytics onboard docs.company.com                    │
│  kurt analytics sync docs.company.com                       │
│  kurt content list --pageviews-30d-min 500                  │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Analytics Adapter Layer                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AnalyticsAdapter (abstract base)                           │
│  └── PostHogAdapter (implementation)                        │
│      - Normalize URLs                                       │
│      - Query PostHog API                                    │
│      - Calculate trends                                     │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Kurt Database (SQLite)                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AnalyticsDomain                                            │
│  - domain, platform, project_id, last_synced_at             │
│                                                              │
│  DocumentAnalytics                                          │
│  - document_id, pageviews, bounce_rate, trends              │
│                                                              │
│  Document (existing)                                        │
│  - Enhanced with analytics filters                          │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PostHog (External Service)                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Project: phc_abc123 (docs.company.com)                     │
│  - Pageview events                                          │
│  - Session duration                                         │
│  - Bounce rate                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**Onboarding**:
1. User runs `kurt analytics onboard docs.company.com`
2. Prompts for PostHog project ID and API key
3. Tests connection, saves config to `sources/docs.company.com/.analytics-meta.json`
4. Creates `AnalyticsDomain` record in database

**Syncing**:
1. User runs `kurt analytics sync docs.company.com` (or auto-triggered by hook)
2. Load all documents with `source_url` starting with `docs.company.com`
3. Normalize document URLs
4. Query PostHog API for pageview events (60-day window)
5. Normalize PostHog event URLs
6. Match normalized URLs
7. Calculate metrics and trends
8. Upsert `DocumentAnalytics` records
9. Update `AnalyticsDomain.last_synced_at`

**Querying**:
1. User runs `kurt content list --pageviews-30d-min 500`
2. Query joins `Document` with `DocumentAnalytics`
3. Filters by analytics metrics
4. Returns matching documents

---

## URL Normalization

### Normalization Function

```python
from urllib.parse import urlparse

def normalize_url_for_analytics(url: str) -> str:
    """
    Normalize URL for analytics matching.

    Removes:
    - Protocol (https://, http://)
    - www. prefix
    - Trailing slashes
    - Query parameters
    - Fragments

    Examples:
        https://www.docs.company.com/guides/quickstart/?utm=123#step-1
        → docs.company.com/guides/quickstart

        http://docs.company.com/guides/quickstart/
        → docs.company.com/guides/quickstart

        https://docs.company.com
        → docs.company.com
    """
    parsed = urlparse(url)

    # Remove www. from domain
    domain = parsed.netloc.replace('www.', '')

    # Remove trailing slash from path (unless it's root)
    path = parsed.path.rstrip('/') if parsed.path != '/' else ''

    # Combine domain + path (ignore query params and fragments)
    normalized = f"{domain}{path}"

    return normalized
```

### Matching Strategy

**Kurt side**:
```python
# Normalize document URLs during sync
for doc in documents:
    normalized_url = normalize_url_for_analytics(doc.source_url)
    url_to_doc_id[normalized_url] = doc.id
```

**PostHog side**:
```python
# Normalize PostHog event URLs
for event in posthog_events:
    event_url = event['properties']['$current_url']
    normalized_url = normalize_url_for_analytics(event_url)
    pageview_counts[normalized_url] += 1
```

**Matching**:
```python
# Join on normalized URLs
for normalized_url, doc_id in url_to_doc_id.items():
    pageviews = pageview_counts.get(normalized_url, 0)  # Default to 0 if no data
    # Create/update DocumentAnalytics record
```

### Edge Cases

**Handling URL variations**:
- Multiple Kurt documents with same normalized URL → Log warning, use first match
- PostHog event URL not in Kurt → Ignore (orphaned analytics data)
- Kurt document URL not in PostHog → Default to 0 pageviews

**Domain changes**:
- If domain changes (e.g., `old-docs.com` → `docs.company.com`), analytics won't match
- Solution: Manual URL mapping table (future enhancement)

---

## Database Schema

### AnalyticsDomain Table

Tracks which domains have analytics configured.

```python
class AnalyticsDomain(SQLModel, table=True):
    """Domains with analytics integration configured."""

    __tablename__ = "analytics_domains"

    # Primary key: domain name
    domain: str = Field(primary_key=True)  # "docs.company.com"

    # Platform configuration
    platform: str = "posthog"
    platform_project_id: str  # "phc_abc123"
    platform_api_key: str     # Encrypted/hashed

    # Data availability
    has_data: bool = True  # False if configured but no data synced yet

    # Sync metadata
    last_synced_at: Optional[datetime] = None
    sync_period_days: int = 60

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Example records**:
```sql
INSERT INTO analytics_domains VALUES (
  'docs.company.com',
  'posthog',
  'phc_abc123',
  'phx_xyz789',
  true,
  '2025-10-30 10:30:00',
  60,
  '2025-10-15 09:00:00',
  '2025-10-30 10:30:00'
);
```

### DocumentAnalytics Table

Stores synced analytics metrics for each document.

```python
class DocumentAnalytics(SQLModel, table=True):
    """Analytics metrics synced from external platform."""

    __tablename__ = "document_analytics"

    # Primary key and foreign key
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", index=True, unique=True)

    # Traffic metrics - 60-day total
    pageviews_60d: int = 0
    unique_visitors_60d: int = 0

    # Traffic metrics - Last 30 days
    pageviews_30d: int = 0
    unique_visitors_30d: int = 0

    # Traffic metrics - Previous 30 days (days 31-60)
    pageviews_previous_30d: int = 0
    unique_visitors_previous_30d: int = 0

    # Engagement metrics (session-based)
    avg_session_duration_seconds: Optional[float] = None
    bounce_rate: Optional[float] = None  # 0.0 to 1.0

    # Computed trends (derived from 30d vs previous_30d)
    pageviews_trend: Literal["increasing", "stable", "decreasing"] = "stable"
    trend_percentage: Optional[float] = None  # MoM change percentage

    # Time window metadata
    period_start: datetime  # Start of 60-day window
    period_end: datetime    # End of 60-day window

    # Sync metadata
    synced_at: datetime = Field(default_factory=datetime.utcnow)
```

**Example record**:
```sql
INSERT INTO document_analytics VALUES (
  'uuid-1234',
  'doc-uuid-5678',
  5432,  -- pageviews_60d
  1234,  -- unique_visitors_60d
  3421,  -- pageviews_30d
  987,   -- unique_visitors_30d
  2011,  -- pageviews_previous_30d
  654,   -- unique_visitors_previous_30d
  245.5, -- avg_session_duration_seconds
  0.35,  -- bounce_rate
  'increasing',
  70.2,  -- trend_percentage (+70%)
  '2025-09-01 00:00:00',
  '2025-10-30 23:59:59',
  '2025-10-30 10:30:00'
);
```

### Enhanced Document Queries

Existing `list_documents()` function extended with analytics filters:

```python
def list_documents(
    # Existing filters
    status: Optional[IngestionStatus] = None,
    url_prefix: Optional[str] = None,
    url_contains: Optional[str] = None,
    content_type: Optional[ContentType] = None,
    published_after: Optional[datetime] = None,
    published_before: Optional[datetime] = None,
    limit: Optional[int] = None,
    offset: int = 0,

    # NEW: Analytics filters
    pageviews_60d_min: Optional[int] = None,
    pageviews_30d_min: Optional[int] = None,
    pageviews_trend: Optional[Literal["increasing", "stable", "decreasing"]] = None,
    bounce_rate_min: Optional[float] = None,
    bounce_rate_max: Optional[float] = None,

    # NEW: Ordering by analytics metrics
    order_by: Optional[str] = None,  # "pageviews_30d", "bounce_rate", etc.
    order_direction: Literal["asc", "desc"] = "desc"
) -> list[Document]:
    """
    List documents with optional analytics filters.

    Examples:
        # High-traffic tutorials
        list_documents(
            content_type=ContentType.TUTORIAL,
            pageviews_30d_min=500,
            order_by="pageviews_30d",
            order_direction="desc"
        )

        # Trending content
        list_documents(
            pageviews_trend="increasing",
            order_by="trend_percentage",
            order_direction="desc"
        )

        # High bounce rate (quality issues)
        list_documents(
            bounce_rate_min=0.7,
            order_by="pageviews_30d",
            order_direction="desc"
        )
    """
    session = get_session()

    # Start with base query
    stmt = select(Document)

    # Join with DocumentAnalytics if any analytics filter is used
    if any([pageviews_60d_min, pageviews_30d_min, pageviews_trend,
            bounce_rate_min, bounce_rate_max, order_by in analytics_fields]):
        stmt = stmt.join(DocumentAnalytics, isouter=True)

    # Apply filters...
    # Apply ordering...

    return list(session.exec(stmt).all())
```

---

## CLI Commands

### 1. Onboard a Domain

**Interactive mode**:
```bash
kurt analytics onboard docs.company.com

# Prompts:
# Platform: PostHog
# PostHog Project ID: phc_abc123
# PostHog API Key: phx_***
#
# Testing connection...
# ✓ Connected to PostHog
# ✓ Found 234 pageview events
#
# Save configuration? (Y/n): Y
# ✓ Configuration saved to sources/docs.company.com/.analytics-meta.json
# ✓ Domain registered in analytics database
#
# Run initial sync now? (Y/n): Y
# [Runs kurt analytics sync docs.company.com]
```

**Non-interactive mode**:
```bash
kurt analytics onboard docs.company.com \
  --platform posthog \
  --project-id phc_abc123 \
  --api-key phx_xyz789 \
  --sync-now
```

### 2. Sync Analytics Data

**Sync specific domain**:
```bash
kurt analytics sync docs.company.com

# Output:
# Syncing analytics for docs.company.com...
# ✓ Connected to PostHog (project: phc_abc123)
# ✓ Querying pageview events (60-day window: Sep 1 - Oct 30)
# ✓ Processing 45,234 pageview events
# ✓ Matched 221/234 Kurt documents to PostHog events
# ✗ 13 documents have no analytics data (defaulting to 0)
# ✓ Calculating trends (30d vs previous 30d)
# ✓ Synced metrics for 234 documents
#
# Summary:
# - Total pageviews (60d): 45,234
# - Avg pageviews per page: 193
# - Avg bounce rate: 42%
# - Top page: "BigQuery Quickstart" (3,421 views, +15% trend)
# - Trending pages: 23 (>10% increase)
# - Declining pages: 12 (>10% decrease)
```

**Sync all configured domains**:
```bash
kurt analytics sync --all

# Syncs all domains found in sources/ with .analytics-meta.json
```

**Options**:
```bash
# Force re-sync even if recent
kurt analytics sync docs.company.com --force

# Custom time period
kurt analytics sync docs.company.com --period 90

# Quiet mode (no output except errors)
kurt analytics sync docs.company.com --quiet
```

### 3. List Analytics-Enabled Domains

```bash
kurt analytics list

# Output:
# Analytics-enabled domains:
#
# docs.company.com (PostHog)
#   Last synced: 2 hours ago
#   Documents: 234 (221 with data, 13 with no data)
#   Total pageviews (60d): 45,234
#   Avg bounce rate: 42%
#   Status: ✓ Up to date
#
# blog.company.com (PostHog)
#   Last synced: 5 days ago ⚠️
#   Documents: 67 (65 with data, 2 with no data)
#   Total pageviews (60d): 12,890
#   Avg bounce rate: 38%
#   Status: ⚠️ Needs refresh (>3 days old)
```

**JSON format**:
```bash
kurt analytics list --format json

# Output:
# [
#   {
#     "domain": "docs.company.com",
#     "platform": "posthog",
#     "last_synced_at": "2025-10-30T10:30:00Z",
#     "documents_total": 234,
#     "documents_with_data": 221,
#     "pageviews_60d_total": 45234,
#     "avg_bounce_rate": 0.42,
#     "status": "up_to_date"
#   }
# ]
```

### 4. Query with Analytics Filters

**High-traffic stale tutorials**:
```bash
kurt content list \
  --content-type tutorial \
  --published-before 2024-01-01 \
  --pageviews-30d-min 500 \
  --order-by pageviews_30d \
  --order-direction desc
```

**Trending content**:
```bash
kurt content list \
  --pageviews-trend increasing \
  --order-by trend_percentage \
  --order-direction desc
```

**High bounce rate (quality issues)**:
```bash
kurt content list \
  --bounce-rate-min 0.7 \
  --pageviews-30d-min 100 \
  --order-by pageviews_30d \
  --order-direction desc
```

**Low traffic (archive candidates)**:
```bash
kurt content list \
  --pageviews-60d-max 50 \
  --published-before 2023-01-01
```

### 5. Analytics Reports

**Top content by traffic**:
```bash
kurt analytics top --metric pageviews_30d --limit 20

# Output:
# Top 20 pages by pageviews (last 30 days):
#
# 1. BigQuery Quickstart
#    3,421 views (+15% trend)
#    docs.company.com/guides/bigquery-quickstart
#
# 2. Snowflake Integration
#    2,103 views (-8% trend)
#    docs.company.com/integrations/snowflake
#
# [... 18 more]
```

**Bottom content by engagement**:
```bash
kurt analytics bottom --metric avg_session_duration --limit 20

# Shows pages with lowest engagement (candidates for improvement)
```

**Domain summary**:
```bash
kurt analytics summary docs.company.com

# Output:
# Analytics Summary: docs.company.com
# Period: Sep 1 - Oct 30, 2025 (60 days)
#
# Traffic:
# - Total pageviews: 45,234
# - Unique visitors: 12,456
# - Avg pageviews per page: 193
#
# Engagement:
# - Avg time on page: 3m 45s
# - Avg bounce rate: 42%
#
# Content Distribution:
# - Top 10% (23 docs): 27,140 views (60% of traffic)
# - Middle 60% (140 docs): 15,832 views (35% of traffic)
# - Bottom 30% (71 docs): 2,262 views (5% of traffic)
#
# Trends:
# - Increasing traffic: 23 pages
# - Stable traffic: 186 pages
# - Decreasing traffic: 25 pages
#
# Quality Flags:
# - High bounce rate (>70%): 12 pages
# - Low engagement (<1m): 18 pages
```

---

## PostHog Integration

### PostHog API Overview

**Base URL**: `https://app.posthog.com/api`

**Authentication**: Personal API key (`phx_...`) or Project API key (`phc_...`)

**Key Endpoints**:
1. **Query API** - Flexible event querying
2. **Insights API** - Pre-built analytics queries

### Querying Pageviews

**Get pageviews by URL**:
```python
POST /api/projects/{project_id}/query

{
  "query": {
    "kind": "EventsQuery",
    "event": "$pageview",
    "after": "-60d",
    "before": "now",
    "select": [
      "properties.$current_url",
      "count()"
    ],
    "group_by": ["properties.$current_url"]
  }
}

# Response:
{
  "results": [
    ["https://docs.company.com/guides/quickstart", 3421],
    ["https://docs.company.com/integrations/snowflake", 2103],
    ...
  ]
}
```

**Get pageviews by time period (for trends)**:
```python
# Last 30 days
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "EventsQuery",
    "event": "$pageview",
    "after": "-30d",
    "before": "now",
    "select": ["properties.$current_url", "count()"],
    "group_by": ["properties.$current_url"]
  }
}

# Previous 30 days (days 31-60)
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "EventsQuery",
    "event": "$pageview",
    "after": "-60d",
    "before": "-30d",
    "select": ["properties.$current_url", "count()"],
    "group_by": ["properties.$current_url"]
  }
}
```

### Querying Engagement Metrics

**Bounce rate** (sessions with only 1 pageview):
```python
POST /api/projects/{project_id}/query

{
  "query": {
    "kind": "EventsQuery",
    "event": "$pageview",
    "after": "-60d",
    "select": [
      "properties.$current_url",
      "sum(case when properties.$pageviews_count = 1 then 1 else 0 end) / count(*)"
    ],
    "group_by": ["properties.$current_url"]
  }
}
```

**Average session duration**:
```python
POST /api/projects/{project_id}/query

{
  "query": {
    "kind": "EventsQuery",
    "event": "$pageview",
    "after": "-60d",
    "select": [
      "properties.$current_url",
      "avg(properties.$session_duration)"
    ],
    "group_by": ["properties.$current_url"]
  }
}
```

### PostHog Adapter Implementation

**File**: `src/kurt/analytics/adapters/posthog.py`

```python
from typing import Optional
import httpx
from datetime import datetime, timedelta

class PostHogAdapter(AnalyticsAdapter):
    """PostHog analytics adapter."""

    def __init__(self, project_id: str, api_key: str):
        self.project_id = project_id
        self.api_key = api_key
        self.base_url = "https://app.posthog.com"
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    def test_connection(self) -> bool:
        """Test PostHog API connection."""
        try:
            response = self.client.get(f"/api/projects/{self.project_id}")
            return response.status_code == 200
        except Exception:
            return False

    def sync_metrics(
        self,
        urls: list[str],
        period_days: int = 60
    ) -> dict[str, AnalyticsMetrics]:
        """
        Fetch analytics metrics from PostHog for given URLs.

        Args:
            urls: List of document URLs to fetch metrics for
            period_days: Number of days to query (default: 60)

        Returns:
            Dict mapping URL -> AnalyticsMetrics
        """
        # Calculate time windows
        now = datetime.utcnow()
        period_end = now
        period_start = now - timedelta(days=period_days)
        mid_point = now - timedelta(days=period_days // 2)

        # Query pageviews for full period
        pageviews_60d = self._query_pageviews(period_start, period_end)

        # Query pageviews for last 30 days
        pageviews_30d = self._query_pageviews(mid_point, period_end)

        # Query pageviews for previous 30 days
        pageviews_previous_30d = self._query_pageviews(period_start, mid_point)

        # Query engagement metrics
        engagement = self._query_engagement(period_start, period_end)

        # Build results for each URL
        results = {}
        for url in urls:
            normalized = normalize_url_for_analytics(url)

            pv_60d = pageviews_60d.get(normalized, 0)
            pv_30d = pageviews_30d.get(normalized, 0)
            pv_prev_30d = pageviews_previous_30d.get(normalized, 0)

            # Calculate trend
            if pv_prev_30d > 0:
                trend_pct = ((pv_30d - pv_prev_30d) / pv_prev_30d) * 100
                if trend_pct > 10:
                    trend = "increasing"
                elif trend_pct < -10:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend_pct = None
                trend = "stable"

            results[url] = AnalyticsMetrics(
                pageviews_60d=pv_60d,
                pageviews_30d=pv_30d,
                pageviews_previous_30d=pv_prev_30d,
                bounce_rate=engagement.get(normalized, {}).get('bounce_rate'),
                avg_session_duration_seconds=engagement.get(normalized, {}).get('avg_duration'),
                pageviews_trend=trend,
                trend_percentage=trend_pct,
                period_start=period_start,
                period_end=period_end
            )

        return results

    def _query_pageviews(
        self,
        start: datetime,
        end: datetime
    ) -> dict[str, int]:
        """Query PostHog for pageview counts by URL."""
        query = {
            "query": {
                "kind": "EventsQuery",
                "event": "$pageview",
                "after": start.isoformat(),
                "before": end.isoformat(),
                "select": ["properties.$current_url", "count()"],
                "group_by": ["properties.$current_url"]
            }
        }

        response = self.client.post(
            f"/api/projects/{self.project_id}/query",
            json=query
        )
        response.raise_for_status()

        # Parse results and normalize URLs
        results = {}
        for row in response.json()["results"]:
            url = row[0]
            count = row[1]
            normalized = normalize_url_for_analytics(url)
            results[normalized] = results.get(normalized, 0) + count

        return results

    def _query_engagement(
        self,
        start: datetime,
        end: datetime
    ) -> dict[str, dict]:
        """Query PostHog for engagement metrics (bounce rate, session duration)."""
        # Similar to _query_pageviews but with engagement calculations
        # Returns: {normalized_url: {"bounce_rate": 0.42, "avg_duration": 245.5}}
        pass
```

---

## Session Start Hook

### Hook Implementation

**File**: `.claude/hooks/session-start.sh`

```bash
#!/bin/bash
# Session start hook for Kurt analytics auto-sync

# Check if analytics is configured
ANALYTICS_DOMAINS=$(kurt analytics list --format json 2>/dev/null)

if [ -z "$ANALYTICS_DOMAINS" ] || [ "$ANALYTICS_DOMAINS" = "[]" ]; then
  # No analytics configured, skip
  exit 0
fi

# Check for stale analytics data
STALE_DOMAINS=$(echo "$ANALYTICS_DOMAINS" | jq -r '.[] | select(.days_since_sync > 7) | .domain')

if [ -z "$STALE_DOMAINS" ]; then
  # All domains are up to date
  exit 0
fi

# Prompt user to sync stale domains
echo ""
echo "📊 Analytics data is stale for:"
echo "$STALE_DOMAINS" | while read domain; do
  DAYS=$(echo "$ANALYTICS_DOMAINS" | jq -r ".[] | select(.domain == \"$domain\") | .days_since_sync")
  echo "  - $domain ($DAYS days old)"
done
echo ""
echo "Sync now? (recommended for accurate prioritization)"
echo "a) Yes, sync now"
echo "b) Skip for now"
echo ""

# Read user input
read -p "Choice (a/b): " choice

if [ "$choice" = "a" ]; then
  echo ""
  echo "Syncing analytics data..."
  echo "$STALE_DOMAINS" | while read domain; do
    kurt analytics sync "$domain"
  done
  echo ""
  echo "✓ Analytics data refreshed"
fi
```

### Configuration

**Enable hook**: User configures in Claude Code settings

```json
{
  "hooks": {
    "session_start": ".claude/hooks/session-start.sh"
  }
}
```

**Behavior**:
1. Runs automatically when Claude Code session starts
2. Checks if any analytics domains are stale (>7 days since sync)
3. Prompts user to sync if stale
4. Non-blocking (user can skip)

---

## Impact on Workflows

### Workflow 1: Tutorial Refresh

**Before analytics**:
```
User: Update all BigQuery tutorials

Claude: Found 23 tutorials mentioning BigQuery.
Which should we prioritize?

User: [Manually reviews list]
```

**After analytics**:
```
User: Update all BigQuery tutorials

Claude runs:
- kurt analytics sync docs.company.com (if stale)
- kurt content list --topic BigQuery --content-type tutorial --order-by pageviews_30d desc

Claude: Found 23 tutorials, prioritized by traffic:

HIGH PRIORITY (>1000 views/month):
1. "BigQuery Quickstart" (3,421 views/month, +15% trend, 850 days old)
2. "BigQuery Python SDK" (2,103 views/month, -8% trend, 720 days old)
[... 10 more]

MEDIUM PRIORITY (500-1000 views/month):
[... 8 more]

LOW PRIORITY (<500 views/month):
[... 5 more]

Should I focus on high-priority tutorials first? (12 tutorials)

User: Yes

[Creates project with 12 high-traffic tutorials]
```

**Impact**: Traffic-based prioritization ensures high-impact content gets updated first.

### Workflow 2: Competitive Gap Analysis

**After analytics**:
```
Claude runs:
- kurt analytics summary docs.company.com
- kurt content stats --group-by topics --metric pageviews_avg

Claude: Our high-performing topics (avg >1000 views/month):
- Authentication (2,300 avg views)
- Data connectors (1,800 avg views)
- SQL transformations (1,400 avg views)

Competitor has strong coverage on:
- Real-time CDC (15 docs)
- Data governance (8 docs)

Our traffic patterns suggest demand for connector-related content.
Recommendation: Create "Real-time CDC" content (likely to perform well based on topic affinity)
```

**Impact**: Use internal traffic patterns to predict which competitor topics will resonate.

### Workflow 3: Product Page Optimization

**After analytics**:
```
Claude runs:
- kurt content list --content-type product_page,landing_page --order-by pageviews_30d desc
- kurt analytics summary --content-type product_page

Claude: Product page performance analysis:

BEST PERFORMERS (high engagement):
1. "Platform Overview"
   - 4,500 views/month
   - 4.2 min avg time on page
   - 35% bounce rate
   - 450 conversions/month

2. "Integrations Page"
   - 3,200 views/month
   - 3.8 min avg time on page
   - 40% bounce rate
   - 320 conversions/month

WORST PERFORMERS (low engagement):
1. "Enterprise Features"
   - 890 views/month
   - 0.8 min avg time on page ⚠️
   - 85% bounce rate ⚠️
   - 12 conversions/month

2. "API Platform"
   - 650 views/month
   - 1.1 min avg time on page
   - 78% bounce rate
   - 8 conversions/month

Recommendation:
- Extract structure/messaging patterns from "Platform Overview"
- Apply to "Enterprise Features" and "API Platform"
- Low engagement suggests content quality issues (not just traffic)

Should I extract patterns from top performers?
```

**Impact**: Identify quality issues objectively (bounce rate, time on page) vs subjectively.

### Workflow 4: Documentation Audit

**After analytics**:
```
Claude runs:
- kurt analytics sync docs.company.com
- kurt content list --bounce-rate-min 0.7 --pageviews-30d-min 100

Claude: Documentation audit with traffic analysis:

CRITICAL QUALITY ISSUES (high traffic + high bounce):
1. "Troubleshooting Guide"
   - 2,100 views/month
   - 82% bounce rate ⚠️
   - Issue: Users arrive but leave immediately (likely confusing/incomplete)
   - Priority: HIGH (fix immediately)

2. "API Authentication"
   - 1,450 views/month
   - 76% bounce rate
   - Issue: High demand but poor user experience
   - Priority: HIGH

LOW-TRAFFIC CANDIDATES (archive?):
- 23 docs with <10 views/month in last 60 days
- Recommendation: Archive or consolidate into related docs

MISSING CONTENT (if search data available):
[Future: Use PostHog's site search events]
- Users searched for "disaster recovery" 450 times (no doc exists)
- Users searched for "monitoring setup" 320 times (only 1 basic doc)

Should I create a prioritized improvement plan?
```

**Impact**: Objectively identify quality issues and archive candidates using traffic + engagement data.

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1-2)

**Database**:
- [ ] Create `AnalyticsDomain` table migration
- [ ] Create `DocumentAnalytics` table migration
- [ ] Add indexes for analytics queries

**Adapters**:
- [ ] Implement `AnalyticsAdapter` base class
- [ ] Implement `PostHogAdapter` with:
  - [ ] Connection testing
  - [ ] Pageview queries (60d, 30d, previous 30d)
  - [ ] Engagement queries (bounce rate, session duration)
  - [ ] URL normalization

**CLI Commands**:
- [ ] `kurt analytics onboard <domain>` (interactive + flags)
- [ ] `kurt analytics sync <domain>` (with --all, --force, --period options)
- [ ] `kurt analytics list` (with --format json)

### Phase 2: Querying & Reporting (Week 3)

**Enhanced document queries**:
- [ ] Extend `list_documents()` with analytics filters
- [ ] Add join with `DocumentAnalytics` table
- [ ] Add ordering by analytics metrics

**CLI enhancements**:
- [ ] `kurt content list` with analytics filters
- [ ] `kurt analytics top --metric <metric> --limit <n>`
- [ ] `kurt analytics bottom --metric <metric> --limit <n>`
- [ ] `kurt analytics summary <domain>`

### Phase 3: Automation & UX (Week 4)

**Session start hook**:
- [ ] Implement `.claude/hooks/session-start.sh`
- [ ] Add staleness detection logic
- [ ] Add user prompt for sync

**Skills integration**:
- [ ] Update `content-analysis-skill` to use analytics data
- [ ] Update workflow docs with analytics examples
- [ ] Add analytics-based recommendations to audit operations

### Phase 4: Testing & Documentation (Week 5)

**Testing**:
- [ ] Unit tests for URL normalization
- [ ] Integration tests for PostHog adapter
- [ ] End-to-end tests for sync workflow

**Documentation**:
- [ ] Update README with analytics setup instructions
- [ ] Add PostHog onboarding guide
- [ ] Document analytics query patterns

---

## Future Enhancements

### PostHog Features to Leverage

1. **Site Search Events** - Identify missing content from user searches
2. **Session Recordings** - Understand why users bounce
3. **Funnels** - Track content journey (awareness → conversion)
4. **Cohorts** - Segment analytics by user type

### Additional Platforms

1. **Google Analytics 4** - For non-PostHog users
2. **Plausible Analytics** - Privacy-focused alternative
3. **Mixpanel** - Product analytics focus

### Advanced Analytics

1. **Content Performance Predictions** - ML to predict which new content will perform
2. **Automated Recommendations** - "This page should be refreshed based on declining trend"
3. **A/B Test Integration** - Track content experiments

### URL Mapping

1. **Historical URL mapping** - Handle domain migrations
2. **Redirect tracking** - Follow URL redirects
3. **Multiple URLs per document** - Handle canonical URLs

---

## Appendix

### PostHog Event Properties

**$pageview event** properties:
- `$current_url` - Full URL of the page
- `$pathname` - URL path
- `$host` - Domain
- `$session_duration` - Time spent in session (seconds)
- `$pageviews_count` - Number of pages in session
- `$timestamp` - Event timestamp

**Useful for analytics**:
- `$current_url` → Match to Kurt documents
- `$session_duration` → Avg time on page
- `$pageviews_count = 1` → Bounce detection

### Example PostHog Query Response

```json
{
  "results": [
    ["https://docs.company.com/guides/quickstart", 3421],
    ["https://docs.company.com/guides/quickstart?utm_source=email", 156],
    ["https://www.docs.company.com/guides/quickstart", 89],
    ["https://docs.company.com/integrations/snowflake", 2103]
  ]
}
```

**After normalization**:
```python
{
  "docs.company.com/guides/quickstart": 3666,  # 3421 + 156 + 89
  "docs.company.com/integrations/snowflake": 2103
}
```

### Configuration File Example

**File**: `sources/docs.company.com/.analytics-meta.json`

```json
{
  "platform": "posthog",
  "project_id": "phc_abc123xyz",
  "project_api_key": "phx_abc123xyz789",
  "has_data": true,
  "last_synced_at": "2025-10-30T10:30:00Z",
  "sync_period_days": 60,
  "created_at": "2025-10-15T09:00:00Z"
}
```

