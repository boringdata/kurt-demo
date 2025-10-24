# Sitemap Mapping Skill

Discover and classify URLs from a website's sitemap without using Kurt CLI.

## Purpose

Map all URLs from a domain's sitemap, classify them by content type, and store in the content map for later fetching and indexing. This replaces the `kurt ingest map` command with a file-based approach that works entirely within Claude Code.

## When to Use

- Starting a new project with a new domain
- Discovering what content is available on a website
- Planning which pages to fetch for analysis
- Before extracting style/structure rules (to see what content exists)

## What It Does

1. **Discovers sitemap** from domain or URL:
   - Tries common locations: `/sitemap.xml`, `/sitemap_index.xml`
   - Handles sitemap indexes (with `--recursive` flag)
   - Parses XML to extract all URLs

2. **Classifies URLs** by content type:
   - Blog posts, docs, tutorials, API reference
   - Product pages, pricing, about, homepage
   - Based on URL path patterns
   - Extracts dates from URL patterns (e.g., `/2024/01/15/`)

3. **Updates content map** (`_content-map.json`):
   - Adds all URLs with status: `DISCOVERED`
   - Stores content_type, published_date
   - Preserves existing `FETCHED` entries (doesn't overwrite)
   - Shows summary of what was found

## Usage

### Basic Usage (Single Sitemap)

```bash
python .claude/scripts/map_sitemap.py docs.getdbt.com
```

### Sitemap Index (Recursive)

```bash
python .claude/scripts/map_sitemap.py docs.getdbt.com --recursive
```

### Direct Sitemap URL

```bash
python .claude/scripts/map_sitemap.py https://docs.getdbt.com/sitemap.xml
```

## Content Type Classification

The script classifies URLs based on path patterns, matching kurt-core's ContentType enum:

| Content Type | URL Patterns | Description |
|--------------|--------------|-------------|
| `reference` | `/api/`, `/api-reference/`, `/api-docs/` | API documentation, technical references |
| `tutorial` | `/tutorial`, `/quickstart`, `/getting-started` | Step-by-step tutorials |
| `guide` | `/docs/`, `/documentation/`, `/guide/`, `/how-to` | Documentation, how-to guides |
| `blog` | `/blog/`, `/article/`, `/post/`, `/news/` | Blog posts, articles, news |
| `product_page` | `/product/`, `/features/` | Product and feature pages |
| `solution_page` | `/solutions/`, `/use-case` | Solutions, use cases |
| `homepage` | `/` (root) | Site homepage |
| `case_study` | `/case-study`, `/customer-stories`, `/customers/` | Customer stories, case studies |
| `event` | `/event`, `/webinar`, `/conference` | Events, webinars |
| `info` | `/about`, `/company`, `/support/`, `/faq`, `/changelog` | About, support, FAQ, changelog |
| `landing_page` | `/pricing`, `/contact`, `/demo`, `/signup` | Marketing landing pages |
| `other` | Everything else | Default classification |

## Date Discovery

Automatically extracts dates from URL patterns:

- `/2024/01/15/title` → `2024-01-15`
- `/blog/2024-01-15-title` → `2024-01-15`
- `/2024/01/` → `2024-01-01`

Also uses `<lastmod>` from sitemap if available.

## Output

The script outputs JSON summary:

```json
{
  "domain": "docs.getdbt.com",
  "sitemap_url": "https://docs.getdbt.com/sitemap.xml",
  "total_urls": 2128,
  "new_urls": 2128,
  "existing_urls": 0,
  "content_map_path": "sources/docs.getdbt.com/_content-map.json",
  "content_types": {
    "guide": 1856,
    "blog": 145,
    "tutorial": 89,
    "info": 102,
    "product_page": 18,
    "reference": 45,
    "other": 8
  }
}
```

## Content Map Structure

Creates/updates `sources/{domain}/_content-map.json`:

```json
{
  "domain": "docs.getdbt.com",
  "last_updated": "2025-10-24T13:30:00Z",
  "sitemap": {
    "https://docs.getdbt.com/docs/build/incremental-models": {
      "status": "DISCOVERED",
      "file_path": null,
      "title": null,
      "author": null,
      "published_date": null,
      "content_type": "guide",
      "source": "sitemap",
      "discovered_at": "2025-10-24T13:30:00Z"
    }
  },
  "clusters": [],
  "topics": {}
}
```

## Integration with Other Tools

### Workflow: Map → Fetch → Index

```
1. Map URLs (this skill)
   ↓ DISCOVERED status in content map

2. Fetch content (WebFetch or selective fetch)
   ↓ FETCHED status, file saved

3. Extract metadata (extract-metadata-hook)
   ↓ Topics, entities, clusters added
```

### Selective Fetching After Mapping

Once URLs are mapped, you can:

1. **Filter by content type**:
   ```bash
   # Get all guide URLs
   jq '.sitemap | to_entries[] | select(.value.content_type == "guide") | .key' \
     sources/docs.getdbt.com/_content-map.json
   ```

2. **Filter by date**:
   ```bash
   # Get posts from 2024
   jq '.sitemap | to_entries[] | select(.value.published_date? // "" | startswith("2024")) | .key' \
     sources/docs.getdbt.com/_content-map.json
   ```

3. **Fetch selectively**:
   - Use extraction skills auto-discovery (they read content map)
   - Manually fetch specific URLs with WebFetch
   - Batch fetch by pattern

## Smart Update Behavior

- **New URLs**: Added with `DISCOVERED` status
- **Existing FETCHED URLs**: Preserved (not overwritten)
- **Existing DISCOVERED URLs**: Updated with latest metadata
- **Last updated timestamp**: Tracks when mapping last ran

## Example Session

```
User: "Map all the pages on docs.getdbt.com so we can see what content is available"

Claude: "I'll map the sitemap to discover all available pages."

[Runs: python .claude/scripts/map_sitemap.py docs.getdbt.com --recursive]

✅ Sitemap mapped successfully!

📊 Summary:
- Domain: docs.getdbt.com
- Total URLs: 2,128
- New URLs: 2,120
- Already fetched: 8

📁 Content types discovered:
- guide: 1,856 pages
- blog: 145 posts
- tutorial: 89 guides
- info: 132 pages
- product_page: 8 pages
- reference: 45 pages

📂 Content map: sources/docs.getdbt.com/_content-map.json

Next steps:
1. Use extraction skills with --auto-discover to intelligently sample
2. WebFetch specific pages you need
3. All fetched pages will be automatically indexed via hooks
```

## Error Handling

- **Sitemap not found**: Tries common locations, errors if none found
- **XML parse error**: Clear error message with details
- **Network errors**: Timeout after 30 seconds with error message
- **Invalid domain**: Automatically adds `https://` if missing

## Prerequisites

- Python 3 with `requests` library
- Internet connection to fetch sitemap
- Write access to `/sources/` directory

## Comparison to Kurt CLI

| Feature | Kurt CLI | This Skill |
|---------|----------|------------|
| Database | Required | Not used |
| Sitemap parsing | ✓ | ✓ |
| URL classification | ✓ | ✓ |
| Date discovery | ✓ | ✓ |
| Recursive sitemaps | ✓ | ✓ |
| Content map | No | Yes (JSON file) |
| Integration | Separate step | Seamless with hooks |

## Best Practices

1. **Start with mapping** before fetching content
2. **Use --recursive** for large sites with sitemap indexes
3. **Review content types** to understand site structure
4. **Filter before fetching** to avoid downloading unnecessary pages
5. **Re-map periodically** to discover new content

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Sitemap not found" | Check domain is correct, try direct sitemap URL |
| "XML parse error" | Sitemap may not be valid XML - check URL in browser |
| "No URLs found" | May be sitemap index - add `--recursive` flag |
| "Permission denied" | Ensure `/sources/` directory exists and is writable |

## Integration with Extraction Skills

All extraction skills support `--auto-discover` mode which reads the content map. After mapping, you can:

```bash
# Map first
invoke sitemap-mapping-skill with domain: docs.getdbt.com

# Then extract (uses content map for discovery)
invoke style-extraction-skill --type tutorial --auto-discover
invoke structure-extraction-skill --type docs --auto-discover
invoke publisher-profile-extraction-skill --auto-discover
```

The extraction skills will intelligently sample from the DISCOVERED URLs by content type.
