---
name: cms-interaction
description: Complete CMS integration - onboard, search, fetch, import, and publish content (Sanity, Contentful, WordPress)
---

# CMS Interaction Skill

Complete toolkit for interacting with your Content Management System. Discover schemas, search content, download as markdown, import to Kurt database, and publish drafts back to CMS.

## Overview

This skill provides end-to-end CMS integration with 5 focused operations:

| Operation | Purpose | Documentation |
|-----------|---------|---------------|
| **Onboard** | Configure your CMS schema mappings | [onboard/SKILL.md](skills/onboard/SKILL.md) |
| **Search** | Query CMS content with filters | [search/SKILL.md](skills/search/SKILL.md) |
| **Fetch** | Download content as markdown files | [fetch/SKILL.md](skills/fetch/SKILL.md) |
| **Import** | Load into Kurt database for analysis | [import/SKILL.md](skills/import/SKILL.md) |
| **Publish** | Push updated drafts back to CMS | [publish/SKILL.md](skills/publish/SKILL.md) |

**Supported CMSs:**
- ✅ **Sanity** - Full support with GROQ queries
- 🚧 **Contentful** - Coming soon
- 🚧 **WordPress** - Coming soon

## Quick Start

### 1. Onboard Your CMS

**First time setup - maps your custom schema to Kurt:**

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity
```

This discovers your content types and maps field names (headline vs title, richText vs body, etc.).

See [skills/onboard/SKILL.md](skills/onboard/SKILL.md)

### 2. Search for Content

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial" \
  --output json > results.json
```

See [skills/search/SKILL.md](skills/search/SKILL.md)

### 3. Fetch Content

```bash
cat results.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --from-stdin
```

See [skills/fetch/SKILL.md](skills/fetch/SKILL.md)

### 4. Import to Kurt

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/
```

See [skills/import/SKILL.md](skills/import/SKILL.md)

### 5. Publish Updated Content

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/my-project/assets/updated-draft.md \
  --document-id abc-123
```

See [skills/publish/SKILL.md](skills/publish/SKILL.md)

## Complete Workflow Example

**Update CMS tutorials with new feature documentation:**

```bash
# Step 1: Onboard (one-time setup)
python scripts/cms_onboard.py --cms sanity
# Interactive: Map your content types and fields

# Step 2: Search for outdated tutorials
python scripts/cms_search.py --cms sanity \
  --filter "publishedAt=<2024-01-01" \
  --filter "tags=[tutorial]" \
  --output json > outdated-tutorials.json

# Step 3: Fetch tutorials
cat outdated-tutorials.json | \
python scripts/cms_fetch.py --cms sanity --from-stdin

# Step 4: Import to Kurt
python scripts/cms_import.py --cms sanity \
  --source-dir sources/cms/sanity/

# Step 5: Create update project
/create-project
# Name: tutorial-refresh
# Sources: sources/cms/sanity/article/
# Also add new feature docs as sources

# Step 6: Create updated drafts
for tutorial in quickstart advanced integration; do
  content-writing-skill draft tutorial-refresh $tutorial
done

# Step 7: Publish drafts to CMS
for draft in projects/tutorial-refresh/assets/*-draft.md; do
  cms_id=$(head -20 "$draft" | grep "cms_id:" | cut -d'"' -f2)
  python scripts/cms_publish.py --cms sanity \
    --file "$draft" --document-id "$cms_id"
done

# Step 8: Review and publish in CMS
# (User reviews draft URLs and publishes when ready)
```

## Operations Guide

### Onboarding (Required First Step)

**Problem:** Every CMS has custom schemas. Your "article" type might use `headline` instead of `title`, `richText` instead of `body`, etc.

**Solution:** Interactive onboarding discovers your schema and creates field mappings.

**When to use:**
- First time setup
- Adding new content types
- After schema changes

**See:** [skills/onboard/SKILL.md](skills/onboard/SKILL.md)

### Search

Find content in your CMS before fetching or updating.

**Features:**
- Text search across title and body
- Filter by content type, tags, dates
- CMS-specific queries (GROQ for Sanity)
- JSON output for piping

**See:** [skills/search/SKILL.md](skills/search/SKILL.md)

### Fetch

Download CMS content as markdown files with full metadata.

**Features:**
- Single or batch download
- YAML frontmatter with all metadata
- Uses configured field mappings
- Organized by content type

**See:** [skills/fetch/SKILL.md](skills/fetch/SKILL.md)

### Import

Load CMS content into Kurt database for analysis and querying.

**Features:**
- AI-powered metadata extraction
- Makes content searchable in Kurt
- Enables lineage tracking
- Links files to database records

**See:** [skills/import/SKILL.md](skills/import/SKILL.md)

### Publish

Push updated content back to CMS as drafts (never auto-publishes).

**Features:**
- Draft-only mode (safe)
- Full metadata support
- Uses configured field mappings
- Returns draft URL for review

**See:** [skills/publish/SKILL.md](skills/publish/SKILL.md)

## Why Onboarding Matters

**Without onboarding:**
```python
# Scripts assume standard field names
title = doc.get('title')          # ❌ Your field is 'headline'
content = doc.get('body')         # ❌ Your field is 'richText'
slug = doc.get('slug.current')    # ❌ Your field is 'urlSlug'
```

**After onboarding:**
```python
# Scripts use YOUR field mappings
title = doc.get('headline')       # ✅ Configured
content = doc.get('richText')     # ✅ Configured
slug = doc.get('urlSlug')         # ✅ Configured
```

**Result:** All 5 operations work with your custom schema!

## Configuration

### Location

`.claude/scripts/cms-config.json` (gitignored)

### Format

```json
{
  "sanity": {
    "project_id": "abc123",
    "dataset": "production",
    "token": "read-token",
    "write_token": "write-token",
    "base_url": "https://yoursite.com",

    "content_type_mappings": {
      "article": {
        "enabled": true,
        "content_field": "body",
        "title_field": "title",
        "slug_field": "slug.current",
        "metadata_fields": {
          "author": "author->name",
          "published_date": "publishedAt",
          "tags": "tags[]",
          "categories": "categories[]->title"
        }
      }
    }
  }
}
```

Generated by onboarding script, or manually editable.

## Common Use Cases

### Use Case 1: Content Audit

Find and analyze all CMS content:

```bash
# Search all content
python scripts/cms_search.py --cms sanity \
  --output json > all-content.json

# Analyze by type
cat all-content.json | jq -r '.[] | .content_type' | sort | uniq -c

# Analyze by date
cat all-content.json | jq -r '.[] | .published_date' | cut -d'-' -f1 | sort | uniq -c

# Fetch and import for deeper analysis
cat all-content.json | python scripts/cms_fetch.py --cms sanity --from-stdin
python scripts/cms_import.py --cms sanity --source-dir sources/cms/sanity/
```

### Use Case 2: Bulk Content Updates

Update multiple articles with new information:

```bash
# 1. Search for articles to update
python scripts/cms_search.py --cms sanity \
  --content-type article \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# 2. Fetch, import, create project
cat tutorials.json | python scripts/cms_fetch.py --cms sanity --from-stdin
python scripts/cms_import.py --cms sanity --source-dir sources/cms/sanity/
/create-project  # tutorial-refresh

# 3. Create updated drafts
for tutorial in tutorial-1 tutorial-2 tutorial-3; do
  content-writing-skill draft tutorial-refresh $tutorial
done

# 4. Publish all drafts
for draft in projects/tutorial-refresh/assets/*-draft.md; do
  cms_id=$(head -20 "$draft" | grep "cms_id:" | cut -d'"' -f2)
  python scripts/cms_publish.py --cms sanity --file "$draft" --document-id "$cms_id"
done
```

### Use Case 3: New Content Creation

Create new content with Kurt assistance:

```bash
# 1. Fetch reference content
python scripts/cms_search.py --cms sanity \
  --filter "tags=[tutorial]" --limit 5 --output json | \
python scripts/cms_fetch.py --cms sanity --from-stdin
python scripts/cms_import.py --cms sanity --source-dir sources/cms/sanity/

# 2. Create project with references
/create-project  # new-postgres-tutorial

# 3. Create new content
content-writing-skill outline new-postgres-tutorial postgres-guide
content-writing-skill draft new-postgres-tutorial postgres-guide

# 4. Publish as new article
python scripts/cms_publish.py --cms sanity \
  --file projects/new-postgres-tutorial/assets/postgres-guide-draft.md \
  --create-new --content-type article --slug "postgres-integration-guide"
```

### Use Case 4: Migration/Backup

Backup all CMS content locally:

```bash
# Fetch everything
python scripts/cms_search.py --cms sanity --output json | \
python scripts/cms_fetch.py --cms sanity --from-stdin \
  --output backups/$(date +%Y-%m-%d)/

# Version control
cd backups/$(date +%Y-%m-%d)
git init
git add .
git commit -m "CMS backup $(date)"
```

## Integration with Other Skills

### With content-writing-skill

CMS content becomes source material:

```bash
# Fetch from CMS
python scripts/cms_fetch.py --cms sanity --document-id abc-123
python scripts/cms_import.py --cms sanity --file sources/cms/sanity/article/guide.md

# Use in content creation
content-writing-skill draft my-project updated-guide
# Lineage tracks CMS source

# Publish back
python scripts/cms_publish.py --cms sanity \
  --file projects/my-project/assets/updated-guide-draft.md --document-id abc-123
```

### With project-management-skill

Track CMS updates in projects:

```markdown
## project.md

### Sources
- sources/cms/sanity/article/ (23 tutorials)
- sources/docs.yoursite.com/features/ (new feature docs)

### Tasks
- [x] Fetch CMS tutorials
- [x] Import to Kurt
- [ ] Create updated drafts (0/23)
- [ ] Publish to CMS (0/23)
- [ ] Review in CMS (0/23)
```

### With ingest-content-skill

Complementary web content:

- **CMS skills**: Authenticated CMS content
- **ingest-content-skill**: Public web content
- Both store in `/sources/` for Kurt analysis

## File Organization

```
sources/
└── cms/
    └── sanity/
        ├── article/
        │   ├── quickstart-tutorial.md
        │   └── advanced-guide.md
        ├── blogPost/
        │   └── my-blog-post.md
        └── page/
            └── about.md

projects/
└── tutorial-refresh/
    ├── project.md
    ├── sources/          # Links to CMS content
    └── assets/
        ├── quickstart-v2-outline.md
        └── quickstart-v2-draft.md
```

## Infrastructure

### Adapters

CMS-specific implementations in `adapters/`:

- **base.py** - Common interface
- **sanity/** - Sanity.io adapter (fully implemented)
- **contentful/** - Coming soon
- **wordpress/** - Coming soon

### Scripts

CLI tools in `scripts/`:

- **cms_onboard.py** - Interactive onboarding
- **cms_search.py** - Search content
- **cms_fetch.py** - Download content
- **cms_import.py** - Import to Kurt
- **cms_publish.py** - Publish drafts

All scripts support `--help` for usage.

## Troubleshooting

### "No configuration found"

**Fix:**
```bash
# Run onboarding
python scripts/cms_onboard.py --cms sanity

# Or create config manually
cp adapters/sanity/config.json.example .claude/scripts/cms-config.json
```

### "Field not found"

**Cause:** Field mapping incorrect or schema changed

**Fix:**
```bash
# Re-run onboarding
python scripts/cms_onboard.py --cms sanity

# Reconfigure affected content type
```

### "Connection failed"

**Fix:**
```bash
# Test connection
python scripts/cms_search.py --cms sanity --test-connection

# Verify credentials in cms-config.json
# Check token permissions in CMS dashboard
```

### "Import failed"

**Fix:**
```bash
# Verify Kurt installed
which kurt

# Check import script
ls -la .claude/scripts/import_markdown.py

# Re-run import
python scripts/cms_import.py --cms sanity --file <file>
```

## Best Practices

1. **Always onboard first** - Don't skip schema mapping
2. **Use version control** - Commit fetched content and config
3. **Test on staging** - Validate workflow before production
4. **Review drafts** - Never blindly publish to production
5. **Backup regularly** - Fetch all content periodically
6. **Track in projects** - Use project-management-skill
7. **Document conventions** - Note schema mappings in project.md

## Security

**Configuration:**
- `cms-config.json` is gitignored
- Separate read and write tokens
- Write token only for draft creation (not publishing)

**Tokens:**
- Read token: `Viewer` role minimum
- Write token: `Editor` role (for drafts)
- Rotate tokens regularly

**Workflow:**
- Draft-only publishing (safe)
- Manual review required (user publishes)
- No destructive operations

## Quick Reference

```bash
# Onboard (first time)
python scripts/cms_onboard.py --cms sanity

# Search
python scripts/cms_search.py --cms sanity --query "text"

# Fetch
python scripts/cms_fetch.py --cms sanity --document-id abc-123

# Import
python scripts/cms_import.py --cms sanity --source-dir sources/cms/sanity/

# Publish
python scripts/cms_publish.py --cms sanity --file draft.md --document-id abc-123

# Complete workflow
cms_search.py --cms sanity --query "tutorial" --output json | \
cms_fetch.py --cms sanity --from-stdin && \
cms_import.py --cms sanity --source-dir sources/cms/sanity/
```

## Documentation

- **[Onboarding](skills/onboard/SKILL.md)** - Schema mapping setup
- **[Search](skills/search/SKILL.md)** - Query CMS content
- **[Fetch](skills/fetch/SKILL.md)** - Download as markdown
- **[Import](skills/import/SKILL.md)** - Load into Kurt database
- **[Publish](skills/publish/SKILL.md)** - Push drafts to CMS
- **[Sanity Adapter](adapters/sanity/README.md)** - Sanity-specific features
- **[Infrastructure README](README.md)** - Architecture and extending

## Support

For detailed operation guides, see individual SKILL.md files in `skills/`.

For CMS-specific questions, see adapter README files in `adapters/`.

For adding new CMSs, see [README.md](README.md) for extension guide.
