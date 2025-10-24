# ⚠️ DEPRECATED: Document Indexing Skill

This skill is **deprecated** - indexing now happens automatically via hooks.

## Replacement

**WebFetch hooks** handle all metadata extraction automatically.

### What This Skill Did

- Extracted metadata from documents using LLM
- Classified content types
- Extracted topics and entities
- Computed clusters

### New Approach

**All indexing is automatic** when content is fetched:

1. **Use WebFetch tool** to fetch any URL
2. **Hook auto-saves** file to `/sources/<domain>/<path>.md` with frontmatter
3. **Hook auto-extracts** metadata (topics, entities, summary, content_type)
4. **Hook auto-updates** content map with metadata
5. **Hook auto-assigns** to cluster (or creates new cluster)

**No manual indexing needed.**

## How It Works

### Hook Chain

```
WebFetch https://example.com/page
  ↓
webfetch-to-file.sh (PostToolUse hook)
  → Saves: sources/example.com/page.md
  → Adds: YAML frontmatter (title, url, date)
  ↓
extract-metadata-hook.sh (PostToolUse hook on Write)
  → Checks: URL not already indexed
  → Extracts: topics, entities, summary, content_type via Claude API
  → Updates: sources/example.com/_content-map.json
  → Assigns: cluster based on topic overlap
  ↓
Content ready with full metadata
```

### Files Involved

- **Hook scripts**:
  - `.claude/scripts/webfetch-to-file.sh` - Saves fetched content
  - `.claude/scripts/extract-metadata-hook.sh` - Triggers metadata extraction
  - `.claude/scripts/extract_metadata.py` - Claude API for metadata extraction
  - `.claude/scripts/update_content_map.py` - Updates content map JSON

- **Configuration**: `.claude/settings.json` - PostToolUse hooks

## What Metadata is Extracted

- **title**: Extracted from content
- **topics**: 3-5 keyword topics
- **entities**: Companies, products, technologies mentioned
- **summary**: 1-2 sentence summary
- **content_type**: Classified using kurt-core ContentType enum
- **cluster**: Assigned based on 2+ topic overlap

## Migration

No migration needed - just use WebFetch tool and hooks handle everything automatically.

**Content is indexed in real-time as it's fetched.**
