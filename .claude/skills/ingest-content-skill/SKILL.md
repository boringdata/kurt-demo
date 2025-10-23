---
name: content-ingestion
description: Ingest web content into Kurt. Map sitemaps to discover URLs, then fetch content selectively.
---

# Content Ingestion

## Overview

This skill enables efficient web content ingestion with a map-then-fetch workflow. Discover URLs from sitemaps first, review what was found, then selectively download only the content you need. Supports single document fetching and fast parallel batch downloads.

Content is extracted as markdown with metadata (title, author, date, categories) and stored in the `sources/` directory.

## Quick Start

```bash
# 1. Discover URLs from sitemap (fast, no downloads)
kurt ingest map https://www.anthropic.com

# 2. Review what was found
kurt document list --status NOT_FETCHED

# 3. Fetch content (parallel batch)
kurt ingest fetch --url-prefix https://www.anthropic.com/
```

## Map-Then-Fetch Workflow

**Why two steps?**
- Sitemaps often contain hundreds or thousands of URLs
- Map step is fast (no downloads) - lets you review before committing
- Fetch step is slow (downloads + extraction) - run selectively
- Saves time, bandwidth, and storage

**Three-step process:**
1. **Map**: Discover URLs and create `NOT_FETCHED` records
2. **Review**: Examine discovered URLs using document management commands
3. **Fetch**: Download content selectively (single or batch)

## Core Operations

### Map Sitemap URLs

Discover URLs from sitemaps without downloading content.

```bash
# Discover all URLs from sitemap
kurt ingest map https://www.anthropic.com

# Limit discovery (useful for testing)
kurt ingest map https://example.com --limit 10

# Map and fetch immediately
kurt ingest map https://example.com --fetch

# JSON output for scripts
kurt ingest map https://example.com --output json
```

**What happens:**
- Automatically finds sitemap URLs (checks `/sitemap.xml`, `robots.txt`, etc.)
- Creates database records with `NOT_FETCHED` status
- Skips duplicate URLs gracefully
- Returns list of discovered documents

**Example output:**
```
✓ Found 317 URLs from sitemap
  Created: 317 new documents

  ✓ https://www.anthropic.com
     ID: 6203468a | Status: NOT_FETCHED
  ✓ https://www.anthropic.com/news/claude-3-7-sonnet
     ID: bc2bcf48 | Status: NOT_FETCHED
```

### Fetch Single Document

Download content for a specific document.

```bash
# Fetch by document ID
kurt ingest fetch 6203468a-e3dc-48f2-8e1f-6e1da34dab05

# Fetch by URL (creates document if needed)
kurt ingest fetch https://www.anthropic.com/company
```

**What happens:**
- Downloads HTML content
- Extracts markdown with trafilatura
- Saves to `sources/{domain}/{path}/page.md`
- Updates database: `FETCHED` status, content metadata
- Returns document details

### Batch Fetch Documents

Download multiple documents in parallel (5-10x faster than sequential).

```bash
# Fetch all from domain
kurt ingest fetch --url-prefix https://www.anthropic.com/

# Fetch all blog posts
kurt ingest fetch --url-contains /blog/

# Fetch everything NOT_FETCHED
kurt ingest fetch --all

# Increase parallelism (default: 5)
kurt ingest fetch --url-prefix https://example.com/ --max-concurrent 10

# Retry failed documents
kurt ingest fetch --status ERROR --url-prefix https://example.com/
```

**What happens:**
- Fetches documents concurrently (default: 5 parallel)
- Uses async httpx for fast downloads
- Extracts metadata: title, author, date, categories, language
- Stores content fingerprint for deduplication
- Updates all document records in batch

**Performance:**
- Sequential: ~2-3 seconds per document
- Parallel (5 concurrent): ~0.4-0.6 seconds per document
- Example: 82 documents in ~10 seconds vs ~3 minutes

**File structure after fetch:**
```
sources/
└── www.anthropic.com/
    ├── news/
    │   └── claude-3-7-sonnet.md
    └── company.md
```

## Alternative: Manual URL Addition

When sitemap discovery fails or you want to add specific URLs.

### Add Single URLs

```bash
# Add URL without fetching
kurt ingest add https://example.com/page1
kurt ingest add https://example.com/page2

# Then fetch when ready
kurt ingest fetch https://example.com/page1
```

### Direct Fetch (Add + Fetch)

Create document record and fetch content in one step.

```bash
# Creates document if doesn't exist, then fetches
kurt ingest fetch https://example.com/specific-page
```

## Advanced Usage

For custom extraction behavior beyond the CLI, use trafilatura Python library directly.

### Custom Crawling

Control crawl depth, URL patterns, language filters, and more.

```python
# See scripts/advanced_crawl_and_import.py
from trafilatura.spider import focused_crawler

todo = focused_crawler(
    homepage,
    max_seen_urls=100,
    max_known_urls=50
)
```

[Trafilatura Crawls Documentation](https://trafilatura.readthedocs.io/en/latest/crawls.html)

### Custom Extraction Settings

Fine-tune extraction: precision vs recall, include comments, handle tables.

```python
# See scripts/advanced_fetch_custom_extraction.py
from trafilatura import extract

content = extract(
    html,
    include_comments=False,
    include_tables=True,
    favor_precision=True
)
```

[Trafilatura Core Functions](https://trafilatura.readthedocs.io/en/latest/corefunctions.html)

### Custom Extraction Config

Configure timeouts, minimum text size, date extraction.

```python
# See scripts/custom_extraction_config.py
from trafilatura.settings import use_config

config = use_config()
config.set('DEFAULT', 'MIN_EXTRACTED_SIZE', '500')
```

[Trafilatura Settings](https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction-settings)

## Quick Reference

| Task | Command | Performance |
|------|---------|-------------|
| Map sitemap | `kurt ingest map <url>` | Fast (no downloads) |
| Fetch single | `kurt ingest fetch <id\|url>` | ~2-3s per doc |
| Batch fetch | `kurt ingest fetch --url-prefix <url>` | ~0.4-0.6s per doc |
| Add URL | `kurt ingest add <url>` | Instant |
| Review discovered | `kurt document list --status NOT_FETCHED` | Instant |
| Retry failures | `kurt ingest fetch --status ERROR` | Varies |

## Python API

```python
# URL Discovery
from kurt.ingest_map import (
    map_sitemap,              # Discover URLs from sitemap
    map_blogrolls,            # Discover from blogroll/changelog pages
    identify_blogroll_candidates,  # Find potential blogroll pages
    extract_chronological_content,  # Extract posts with dates
)

# Content Fetching
from kurt.ingest_fetch import (
    add_document,             # Add single URL
    fetch_document,           # Fetch single document
    fetch_documents_batch,    # Batch fetch (async parallel)
)

# Map sitemap
docs = map_sitemap("https://example.com", limit=100)

# Add document
doc = add_document("https://example.com/page")

# Fetch single
result = fetch_document(document_id="abc-123")

# Batch fetch
results = fetch_documents_batch(
    document_ids=["abc-123", "def-456"],
    max_concurrent=10
)
```

See:
- [ingest_map.py](https://github.com/boringdata/kurt-core/blob/main/src/kurt/ingest_map.py) - URL discovery
- [ingest_fetch.py](https://github.com/boringdata/kurt-core/blob/main/src/kurt/ingest_fetch.py) - Content fetching

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No sitemap found" | Use `kurt ingest add <url>` or `kurt ingest fetch <url>` directly |
| Slow batch fetch | Increase `--max-concurrent` (default: 5, try 10) |
| Extraction quality low | See advanced extraction scripts for custom settings |
| Duplicate content | Kurt automatically deduplicates using content hashes |
| Rate limiting | Reduce `--max-concurrent` or add delays |

## Next Steps

- For document management, see **document-management-skill**
- For custom extraction, see [scripts/](scripts/) directory
- For trafilatura details, see [Trafilatura Documentation](https://trafilatura.readthedocs.io/)
