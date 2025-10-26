---
name: cms-search
description: Search CMS content with text queries and filters (Sanity, Contentful, WordPress)
---

# CMS Search Skill

Search content in your CMS using text queries, filters, and CMS-specific query languages.

## Overview

Find content in your CMS before fetching or updating. Supports:
- Text search across titles and content
- Filtering by content type, tags, dates
- CMS-specific queries (GROQ for Sanity)
- JSON output for piping to other skills

**Use this skill when:**
- Finding content to update
- Auditing content by date/tags
- Discovering content types
- Building lists for batch operations

## Quick Start

```bash
# Basic search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial"

# Filter by content type
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --limit 50

# JSON output for piping
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "quickstart" \
  --output json > results.json
```

## Prerequisites

**1. Run Onboarding (Recommended)**

Configure your CMS schema mappings first:

```bash
# Interactive onboarding to map your content types and fields
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# Or invoke as skill
Skill(cms-onboard-skill)
```

See [cms-onboard-skill](../cms-onboard-skill/SKILL.md) for details.

**2. Manual Configuration (Alternative)**

If you skip onboarding, create basic config:

```bash
cp .claude/skills/cms-interaction-skill/adapters/sanity/config.json.example \
   .claude/scripts/cms-config.json
```

Edit with your credentials. Default field names (title, body, etc.) will be assumed.

**3. Test Connection**

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --test-connection
```

## Search Operations

### Text Search

Search across title and content fields:

```bash
# Simple text search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "getting started"

# Multiple keywords
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "postgres integration tutorial"
```

**What it searches:**
- Document titles
- Body content (full text)
- CMS-specific searchable fields

### Filter by Content Type

Limit results to specific content types:

```bash
# Articles only
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article

# Blog posts only
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type post
```

**Discover content types:**
```bash
# List all content types in CMS
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --limit 1
# (Then try different types based on your schema)
```

### Advanced Filters

Use CMS-specific filters for precise queries:

```bash
# By tags
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "tags=[tutorial,guide]"

# By date (published after)
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "publishedAt=>2024-01-01"

# By date (published before)
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "publishedAt=<2024-01-01"

# Multiple filters
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "quickstart" \
  --content-type article \
  --filter "tags=[tutorial]" \
  --filter "publishedAt=>2024-01-01" \
  --limit 20
```

**Filter syntax:**
- `key=[value1,value2]` - Array contains any value
- `key=>date` - Greater than (after date)
- `key=<date` - Less than (before date)
- `key=value` - Exact match

### Limit Results

Control result count:

```bash
# Default limit (100)
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial"

# Custom limit
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial" \
  --limit 500
```

### Output Formats

#### Human-Readable (default)

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial"
```

Output:
```
✓ Found 23 documents

ID: abc-123
Title: Quickstart Tutorial
Type: article
Status: published
URL: https://yoursite.com/quickstart
Author: Jane Doe
Published: 2024-01-15
Modified: 2024-10-20
Tags: tutorial, beginner, quickstart
Categories: Getting Started

ID: def-456
...
```

#### JSON Output

For piping to other tools or skills:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial" \
  --output json > results.json
```

Output:
```json
[
  {
    "id": "abc-123",
    "title": "Quickstart Tutorial",
    "content": "",
    "content_type": "article",
    "status": "published",
    "url": "https://yoursite.com/quickstart",
    "author": "Jane Doe",
    "published_date": "2024-01-15",
    "last_modified": "2024-10-20",
    "metadata": {
      "slug": "quickstart",
      "tags": ["tutorial", "beginner"],
      "categories": ["Getting Started"]
    }
  }
]
```

## Common Workflows

### Workflow 1: Find Outdated Content

Identify content that needs updating:

```bash
# Articles published before 2024
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --filter "publishedAt=<2024-01-01" \
  --output json > outdated-content.json

# Review results
cat outdated-content.json | jq '.[] | {title, published_date, url}'

# Count by year
cat outdated-content.json | jq -r '.[] | .published_date' | cut -d'-' -f1 | sort | uniq -c
```

### Workflow 2: Audit by Tags

Review content organization:

```bash
# All tutorials
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# All guides
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "tags=[guide]" \
  --output json > guides.json

# Compare counts
echo "Tutorials: $(cat tutorials.json | jq length)"
echo "Guides: $(cat guides.json | jq length)"
```

### Workflow 3: Search Then Fetch

Find content, then download it:

```bash
# Step 1: Search for tutorials
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# Step 2: Review results
cat tutorials.json | jq '.[] | {id, title, published_date}'

# Step 3: Fetch selected content (pipe to cms-fetch-skill)
cat tutorials.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --from-stdin
```

### Workflow 4: Build Update List

Create list of content to update:

```bash
# Find articles without specific tag
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --output json | \
jq '[.[] | select(.metadata.tags | contains(["v2"]) | not) | {id, title, url}]' \
  > needs-v2-tag.json

# Review
cat needs-v2-tag.json | jq '.[] | .title'
```

## CMS-Specific Features

### Sanity (GROQ Queries)

Sanity searches use GROQ query language internally.

**Supported filters:**
- Text search: `title match "*query*"` or `pt::text(body) match "*query*"`
- Content type: `_type == "article"`
- Tags: `"value" in tags[]`
- Dates: `publishedAt > "2024-01-01"`
- Draft status: Automatically detected

**Example filters:**
```bash
# Complex tag filter
--filter "tags=[tutorial,guide]"
# → Translates to: "tutorial" in tags[] || "guide" in tags[]

# Date range
--filter "publishedAt=>2024-01-01" --filter "publishedAt=<2024-12-31"
# → Translates to: publishedAt > "2024-01-01" && publishedAt < "2024-12-31"
```

See [Sanity adapter docs](../cms-interaction-skill/adapters/sanity/README.md) for GROQ details.

### Contentful

Coming soon.

### WordPress

Coming soon.

## Output Fields

Search results include:

| Field | Description | Always Present |
|-------|-------------|----------------|
| `id` | CMS document ID | ✅ |
| `title` | Document title | ✅ |
| `content_type` | CMS content type | ✅ |
| `status` | draft/published | ✅ |
| `url` | Public URL | If available |
| `author` | Author name | If available |
| `published_date` | Publish date | If available |
| `last_modified` | Last update | If available |
| `metadata.slug` | URL slug | If available |
| `metadata.tags` | Tags array | If available |
| `metadata.categories` | Categories | If available |

**Note:** `content` field is empty for search results (performance). Use **cms-fetch-skill** to get full content.

## Integration with Other Skills

### With cms-fetch-skill

Search, then fetch:

```bash
# Search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --query "tutorial" --output json > results.json

# Fetch
cat results.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

### With cms-import-skill

Search → Fetch → Import workflow:

```bash
# 1. Search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --filter "tags=[tutorial]" --output json | \

# 2. Fetch
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin --output sources/cms/

# 3. Import (see cms-import-skill)
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --source-dir sources/cms/sanity/
```

### With project-management-skill

Use search to scope projects:

```markdown
## Project: Tutorial Updates

### Discovery
Searched CMS for tutorials published before 2024:
- Found: 23 articles
- Tags: tutorial, beginner, quickstart
- Date range: 2022-2024

### Scope
Update all 23 tutorials with new v2 features.
```

## Troubleshooting

### "No configuration found for CMS"

**Cause:** Missing or invalid cms-config.json

**Fix:**
```bash
# Create config
cp .claude/skills/cms-interaction-skill/adapters/sanity/config.json.example \
   .claude/scripts/cms-config.json

# Edit with your credentials
# Add to .gitignore
echo ".claude/scripts/cms-config.json" >> .gitignore
```

### "Connection test failed"

**Cause:** Invalid credentials or network issue

**Fix:**
- Verify `project_id`, `dataset`, `token` in cms-config.json
- Check token has read permissions
- Test network/firewall
- Try in CMS dashboard to confirm credentials work

### "No results found"

**Cause:** Query too restrictive or no matching content

**Fix:**
```bash
# Try broader search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --limit 10  # Just get some results

# Check content types
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type page  # Try different types

# Remove filters
# Start simple, add filters incrementally
```

### "Invalid filter format"

**Cause:** Incorrect filter syntax

**Fix:**
- Use `key=value` format
- Arrays: `key=[value1,value2]`
- Dates: `key=>2024-01-01` or `key=<2024-01-01`
- Check spacing and quotes

## Best Practices

1. **Test connection first** - Always run `--test-connection` when setting up
2. **Start broad, filter down** - Begin with simple queries, add filters as needed
3. **Use JSON for piping** - `--output json` for integration with other tools
4. **Limit results** - Use `--limit` to avoid overwhelming output
5. **Save search results** - Redirect JSON to files for reuse
6. **Review before fetch** - Inspect search results before fetching content
7. **Document queries** - Save complex filters in project docs

## Quick Reference

```bash
# Test connection
cms_search.py --cms sanity --test-connection

# Basic search
cms_search.py --cms sanity --query "text"

# By type
cms_search.py --cms sanity --content-type article

# With filters
cms_search.py --cms sanity --filter "tags=[value]"

# Date filters
cms_search.py --cms sanity --filter "publishedAt=>2024-01-01"

# JSON output
cms_search.py --cms sanity --query "text" --output json

# Complex query
cms_search.py --cms sanity \
  --query "tutorial" \
  --content-type article \
  --filter "tags=[quickstart]" \
  --filter "publishedAt=>2024-01-01" \
  --limit 50 \
  --output json > results.json
```

## Related Skills

- **[cms-fetch-skill](../cms-fetch-skill/SKILL.md)** - Download content found via search
- **[cms-import-skill](../cms-import-skill/SKILL.md)** - Import fetched content to Kurt DB
- **[cms-publish-skill](../cms-publish-skill/SKILL.md)** - Publish updated content back to CMS

## Configuration

See [CMS Interaction README](../cms-interaction-skill/README.md) for:
- Adapter documentation
- Configuration templates
- Supported CMSs
- Adding new CMSs
