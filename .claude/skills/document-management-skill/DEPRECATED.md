# ⚠️ DEPRECATED: Document Management Skill

This skill is **deprecated** as of the migration to file-based content maps.

## Replacement

Use **content map queries** instead of Kurt CLI database commands.

### What This Skill Did

- Listed documents from Kurt database
- Queried documents by URL patterns
- Retrieved document metadata
- Managed document status

### New Approach

All functionality is now available via content map JSON files:

**Location**: `sources/<domain>/_content-map.json`

**Common Operations**:

| Old (This Skill) | New (Content Map) |
|------------------|-------------------|
| `kurt document list` | `cat sources/<domain>/_content-map.json \| jq '.sitemap \| keys'` |
| `kurt document list --url-contains /docs/` | `cat sources/<domain>/_content-map.json \| jq -r '.sitemap \| to_entries[] \| select(.key \| contains("/docs/")) \| .key'` |
| `kurt document get <url>` | `cat sources/<domain>/_content-map.json \| jq '.sitemap["<url>"]'` |
| Filter by status | `jq -r '.sitemap \| to_entries[] \| select(.value.status == "FETCHED") \| .key'` |
| Filter by content type | `jq -r '.sitemap \| to_entries[] \| select(.value.content_type == "guide") \| .key'` |

## Complete Reference

See **`.claude/docs/CONTENT-MAP-QUERIES.md`** for comprehensive query patterns and examples.

## Migration Path

1. Ensure domain is mapped: `python .claude/scripts/map_sitemap.py <domain> --recursive`
2. Query content map with `jq`
3. Fetch content with WebFetch tool (hooks auto-save + index)

**No database setup or Kurt CLI commands required.**
