# Content Map Query Reference

Quick reference for querying content maps instead of Kurt CLI commands.

## Prerequisites

Ensure domain is mapped first:
```bash
python .claude/scripts/map_sitemap.py <domain> --recursive
```

## Common Query Patterns

### By Content Type

```bash
# Guides/Documentation
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "guide") |
  .key'

# Tutorials
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "tutorial") |
  .key'

# Blog posts
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "blog") |
  .key'

# API Reference
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "reference") |
  .key'

# Product pages
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "product_page") |
  .key'

# Info pages (about, support, FAQ)
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "info") |
  .key'

# Landing pages (pricing, contact, demo)
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "landing_page") |
  .key'

# Homepage
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "homepage") |
  .key'
```

### By URL Pattern

```bash
# URLs containing specific path
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.key | contains("/about")) |
  .key'

# URLs matching multiple patterns
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.key | contains("/about") or contains("/company")) |
  .key'
```

### By Status

```bash
# Only fetched URLs
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.status == "FETCHED") |
  .key'

# Only discovered (not yet fetched)
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.status == "DISCOVERED") |
  .key'

# Fetched URLs of specific type
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.status == "FETCHED" and .value.content_type == "guide") |
  .key'
```

### By Topics/Metadata

```bash
# URLs with specific topic
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.topics != null) |
  select(.value.topics | contains(["authentication"])) |
  .key'

# URLs in specific cluster
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.cluster == "getting-started") |
  .key'
```

### Get Specific URL Info

```bash
# Get all info for a URL
cat sources/<domain>/_content-map.json | jq '.sitemap["<url>"]'

# Check if URL is fetched
cat sources/<domain>/_content-map.json | jq -r '.sitemap["<url>"].status'

# Get URL topics
cat sources/<domain>/_content-map.json | jq -r '.sitemap["<url>"].topics[]'
```

### Statistics

```bash
# Count by content type
cat sources/<domain>/_content-map.json | jq '[.sitemap[]] |
  group_by(.content_type) |
  map({type: .[0].content_type, count: length})'

# Count fetched vs discovered
cat sources/<domain>/_content-map.json | jq '{
  total: (.sitemap | length),
  discovered: [.sitemap[] | select(.status == "DISCOVERED")] | length,
  fetched: [.sitemap[] | select(.status == "FETCHED")] | length
}'

# List all clusters
cat sources/<domain>/_content-map.json | jq '.clusters[] | {name, url_count: (.urls | length)}'
```

## Kurt CLI → Content Map Migration

| Old Kurt CLI Command | New Content Map Query |
|---------------------|----------------------|
| `kurt document list --url-contains /docs/` | `cat sources/<domain>/_content-map.json \| jq -r '.sitemap \| to_entries[] \| select(.value.content_type == "guide") \| .key'` |
| `kurt document list --url-contains /tutorial --status FETCHED` | `cat sources/<domain>/_content-map.json \| jq -r '.sitemap \| to_entries[] \| select(.value.status == "FETCHED" and .value.content_type == "tutorial") \| .key'` |
| `kurt document list --url <url>` | `cat sources/<domain>/_content-map.json \| jq '.sitemap["<url>"]'` |
| `kurt document get <url>` | `cat sources/<domain>/_content-map.json \| jq '.sitemap["<url>"]'` |
| `kurt ingest fetch <url>` | Use WebFetch tool (hooks auto-save + index) |

## Fetching Content

Instead of `kurt ingest fetch`, use WebFetch tool:
- WebFetch automatically saves to `/sources/<domain>/<path>.md`
- Hooks automatically extract metadata
- Content map automatically updated from DISCOVERED → FETCHED

## Notes

- Content maps are per-domain: `sources/<domain>/_content-map.json`
- Always map domain first with `map_sitemap.py`
- Use WebFetch for fetching (not Kurt CLI)
- Hooks handle all indexing automatically
