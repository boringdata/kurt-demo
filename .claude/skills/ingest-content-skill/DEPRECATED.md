# ⚠️ DEPRECATED: Ingest Content Skill

This skill is **deprecated** - replaced by sitemap mapping + WebFetch hooks.

## Replacement

Use **sitemap-mapping-skill** + **WebFetch tool** instead of Kurt CLI ingestion.

### What This Skill Did

- Mapped sitemaps to discover URLs (`kurt ingest map`)
- Fetched content from URLs (`kurt ingest fetch`)
- Stored content in database
- Required Kurt CLI and database setup

### New Approach

**File-based workflow** with no database required:

#### Step 1: Map Sitemap (Discovery)

```bash
python .claude/scripts/map_sitemap.py <domain> --recursive
```

**Output**: `sources/<domain>/_content-map.json` with all URLs marked `DISCOVERED`

#### Step 2: Fetch Content (Automatic Indexing)

Use **WebFetch tool** for URLs you need:
- Hooks automatically save to `/sources/<domain>/<path>.md`
- Hooks automatically extract metadata (topics, entities, etc.)
- Content map automatically updated to `FETCHED` status

**No manual fetch or index commands needed.**

## Comparison

| Old (This Skill) | New (File-Based) |
|------------------|------------------|
| `kurt ingest map <url>` | `python .claude/scripts/map_sitemap.py <domain> --recursive` |
| `kurt ingest fetch --url <url>` | Use WebFetch tool (hooks auto-save) |
| `kurt index --url <url>` | Automatic via hooks (no manual command) |
| Database required | No database - JSON files only |
| Manual orchestration | Automatic via hooks |

## Benefits of New Approach

1. **No Database** - All data in JSON files
2. **Automatic** - Hooks handle save + indexing
3. **Transparent** - Inspect content maps with `cat`, `jq`, any tool
4. **Fast** - No CLI subprocess calls
5. **Simple** - Map once, fetch as-needed

## Migration Path

1. **Map domain**: `python .claude/scripts/map_sitemap.py <domain> --recursive`
2. **Query content map**: See `.claude/docs/CONTENT-MAP-QUERIES.md`
3. **Fetch with WebFetch**: Hooks handle everything automatically

## See Also

- **sitemap-mapping-skill** - Maps sitemaps, classifies URLs
- **CONTENT-MAP-QUERIES.md** - Query reference for content maps
- **Session start hook** - Shows content map status automatically

**No Kurt CLI commands or database required.**
