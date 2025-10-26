---
name: cms-fetch
description: Download CMS content as markdown files with full metadata
---

# CMS Fetch Skill

Download content from your CMS and save as markdown files with YAML frontmatter containing all metadata.

## Overview

Retrieve full document content from CMS with:
- Complete markdown conversion
- YAML frontmatter with all metadata
- Single document or batch operations
- Organized file structure by content type

**Use this skill when:**
- Downloading content for local editing
- Creating backups of CMS content
- Importing to Kurt database (with cms-import-skill)
- Building source material for projects

## Quick Start

```bash
# Fetch single document
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-id abc-123

# Fetch multiple documents
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-ids abc-123,def-456,ghi-789

# Fetch from search results
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --query "tutorial" --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

## Prerequisites

**Run Onboarding First (Recommended)**

Configure your CMS schema mappings:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity
```

See [cms-onboard-skill](../cms-onboard-skill/SKILL.md) for details.

**Or see [cms-search-skill](../cms-search-skill/SKILL.md#prerequisites) for manual setup.**

## Fetch Operations

### Fetch Single Document

Download one document by ID:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-id abc-123
```

**Output:**
```
✓ Saved: sources/cms/sanity/article/quickstart-tutorial.md

✓ Fetched 1 document(s)
  Output: sources/cms/sanity/
```

### Fetch Multiple Documents

Download several documents by IDs:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-ids abc-123,def-456,ghi-789
```

**Performance:** Uses batch operations when possible (parallel downloads).

### Fetch from Search Results

Pipe search results directly:

```bash
# Search then fetch
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --query "tutorial" \
  --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --from-stdin
```

**Or save search results first:**
```bash
# Search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# Review
cat tutorials.json | jq '.[] | {id, title}'

# Fetch selected
cat tutorials.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

### Custom Output Directory

Control where files are saved:

```bash
# Save to custom location
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-id abc-123 \
  --output projects/my-project/sources/

# Result: projects/my-project/sources/sanity/article/quickstart.md
```

**Default:** `sources/cms/`

### Dry Run

Preview what would be fetched:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-ids abc-123,def-456 \
  --dry-run
```

Output:
```
Dry run - would fetch:
  - Quickstart Tutorial (abc-123)
  - Advanced Guide (def-456)
```

## File Format

### Directory Structure

Organized by CMS and content type:

```
sources/cms/
└── sanity/
    ├── article/
    │   ├── quickstart-tutorial.md
    │   └── advanced-guide.md
    ├── post/
    │   └── blog-post.md
    └── page/
        └── about.md
```

**Pattern:** `{output-dir}/{cms-name}/{content-type}/{slug-or-id}.md`

### Markdown File Format

Each file contains YAML frontmatter + content:

```markdown
---
title: "Quickstart Tutorial"
cms_id: abc-123
cms_type: article
status: published
url: https://yoursite.com/quickstart-tutorial
author: Jane Doe
published_date: "2024-01-15"
last_modified: "2024-10-20"
cms_metadata:
  slug: quickstart-tutorial
  tags:
    - tutorial
    - beginner
    - quickstart
  categories:
    - Getting Started
  seo:
    meta_description: "Get started quickly with our platform"
  created_at: "2024-01-15T10:30:00Z"
fetched_from: sanity
cms_url: https://yoursite.com/quickstart-tutorial
---

# Quickstart Tutorial

Welcome to our quickstart guide! This tutorial will help you...

## Prerequisites

Before starting, ensure you have:
- Item 1
- Item 2

## Step 1: Setup

Here's how to get started...
```

### Frontmatter Fields

| Field | Description | Source |
|-------|-------------|--------|
| `title` | Document title | CMS title field |
| `cms_id` | CMS document ID | CMS internal ID |
| `cms_type` | Content type | CMS schema type |
| `status` | Publication status | draft/published |
| `url` | Public URL | Constructed from slug |
| `author` | Author name | CMS author field |
| `published_date` | Publish date | CMS publish date |
| `last_modified` | Last update | CMS update timestamp |
| `cms_metadata` | CMS-specific data | Tags, categories, SEO, etc. |
| `fetched_from` | CMS name | Script metadata |
| `cms_url` | Document URL | CMS + document ID |

## Content Conversion

### Sanity: Portable Text → Markdown

Sanity's Portable Text is converted to markdown:

**Supported:**
- ✅ Headings (h1-h6)
- ✅ Paragraphs
- ✅ Bold, italic, code (inline)
- ✅ Code blocks with language
- ✅ Blockquotes
- ✅ Lists (basic)

**Limitations:**
- Complex nested structures may need adjustment
- Custom marks/annotations not fully supported
- Images preserved as placeholders

**Example conversion:**

Portable Text:
```json
{
  "_type": "block",
  "style": "h2",
  "children": [
    {"text": "Getting Started", "marks": ["strong"]}
  ]
}
```

Markdown:
```markdown
## **Getting Started**
```

### Other CMSs

- **Contentful** - Rich Text → Markdown (coming soon)
- **WordPress** - HTML → Markdown with html2text (coming soon)

## Common Workflows

### Workflow 1: Backup CMS Content

Download all content for backup:

```bash
# 1. Find all published content
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "status=published" \
  --output json > all-content.json

# 2. Count by type
cat all-content.json | jq -r '.[] | .content_type' | sort | uniq -c

# 3. Fetch everything
cat all-content.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin --output backups/$(date +%Y-%m-%d)/

# 4. Verify
ls -R backups/$(date +%Y-%m-%d)/
```

### Workflow 2: Selective Download

Fetch only specific content:

```bash
# 1. Search for tutorials
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --content-type article \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# 2. Review count
echo "Found: $(cat tutorials.json | jq length) tutorials"

# 3. Filter to outdated ones
cat tutorials.json | \
  jq '[.[] | select(.published_date < "2024-01-01")]' \
  > outdated-tutorials.json

echo "Outdated: $(cat outdated-tutorials.json | jq length)"

# 4. Fetch outdated tutorials
cat outdated-tutorials.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

### Workflow 3: Fetch for Project

Download sources for a content project:

```bash
# 1. Create project
/create-project
# Name: tutorial-refresh
# Goal: Update tutorials with new v2 features

# 2. Search for tutorials
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "tags=[tutorial]" \
  --output json > tutorials.json

# 3. Fetch to project directory
cat tutorials.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --from-stdin \
  --output projects/tutorial-refresh/sources/

# 4. Import to Kurt (next step - see cms-import-skill)
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir projects/tutorial-refresh/sources/sanity/
```

### Workflow 4: Incremental Updates

Fetch only recently updated content:

```bash
# 1. Search for recent updates
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --filter "last_modified=>2024-10-01" \
  --output json > recent-updates.json

# 2. Check what changed
cat recent-updates.json | jq '.[] | {title, last_modified}'

# 3. Fetch updates
cat recent-updates.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin

# 4. Compare with existing files (if any)
# Use git diff or file comparison tools
```

## Performance

### Batch Operations

Fetching multiple documents uses batch operations when possible:

**Sequential (one by one):**
```bash
# Slow: 3 separate API calls
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id def-456
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id ghi-789
```

**Batch (parallel):**
```bash
# Fast: 1 batched API call
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-ids abc-123,def-456,ghi-789
```

**Performance gains:**
- Sequential: ~2-3 seconds per document
- Batch: ~0.4-0.6 seconds per document
- Example: 50 documents = ~2 minutes batch vs ~2.5 hours sequential

### Large Batches

For very large batches (100+ documents):

```bash
# Option 1: Use stdin piping (handles batching automatically)
cat all-docs.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin

# Option 2: Split into chunks manually
cat all-docs.json | jq -r '.[0:50] | .[] | .id' | \
  paste -sd "," - | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-ids $(cat -)
```

## Integration with Other Skills

### With cms-search-skill

Search then fetch:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --query "tutorial" --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

### With cms-import-skill

Fetch then import to Kurt:

```bash
# 1. Fetch
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-ids abc-123,def-456

# 2. Import (see cms-import-skill)
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --source-dir sources/cms/sanity/
```

### With content-writing-skill

Use fetched content as sources:

```bash
# 1. Fetch existing tutorials
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-ids abc-123

# 2. Import to Kurt
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --file sources/cms/sanity/article/tutorial.md

# 3. Use in content creation
content-writing-skill draft my-project updated-tutorial
# Sources in project.md include: sources/cms/sanity/article/tutorial.md
```

## Troubleshooting

### "Document not found"

**Cause:** Invalid document ID or no access

**Fix:**
```bash
# Verify ID in CMS
# Try searching for it first
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --query "title keywords"

# Use ID from search results
```

### "Fetch failed: Permission denied"

**Cause:** Token lacks read permissions

**Fix:**
- Check token has `Viewer` role minimum
- Verify token in cms-config.json is correct
- Test token in CMS dashboard

### "Empty content"

**Cause:** Document has no body content or conversion failed

**Fix:**
- Check document in CMS has content
- Verify content field structure matches expectations
- Review CMS-specific conversion notes

### "Timeout error"

**Cause:** Large batch or slow network

**Fix:**
```bash
# Reduce batch size
# Instead of 100 IDs, try 10-20 at a time

# Or use search → fetch for auto-batching
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin
```

### "File already exists"

**Behavior:** Overwrites existing files by default

**To preserve:**
```bash
# Backup first
cp -r sources/cms/sanity/ backups/sanity-$(date +%Y%m%d)/

# Then fetch
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123
```

## Best Practices

1. **Dry run first** - Use `--dry-run` for large batches
2. **Use search → fetch** - More reliable than manual ID lists
3. **Save search results** - Review before fetching
4. **Batch operations** - Always prefer batch over sequential
5. **Organize by project** - Use `--output` for project-specific fetches
6. **Version control** - Commit fetched files to track changes
7. **Regular backups** - Schedule periodic full fetches
8. **Check file quality** - Review conversion results, especially for complex content

## Quick Reference

```bash
# Single document
cms_fetch.py --cms sanity --document-id abc-123

# Multiple documents
cms_fetch.py --cms sanity --document-ids id1,id2,id3

# From stdin (search results)
cms_search.py --cms sanity --query "text" --output json | \
  cms_fetch.py --cms sanity --from-stdin

# Custom output
cms_fetch.py --cms sanity --document-id abc-123 --output custom/dir/

# Dry run
cms_fetch.py --cms sanity --document-ids id1,id2 --dry-run

# Full workflow
cms_search.py --cms sanity --filter "tags=[tutorial]" --output json | \
  cms_fetch.py --cms sanity --from-stdin --output sources/cms/
```

## Related Skills

- **[cms-search-skill](../cms-search-skill/SKILL.md)** - Search CMS to find documents to fetch
- **[cms-import-skill](../cms-import-skill/SKILL.md)** - Import fetched content to Kurt database
- **[cms-publish-skill](../cms-publish-skill/SKILL.md)** - Publish updated content back to CMS

## Configuration

See [CMS Interaction README](../cms-interaction-skill/README.md) for adapter documentation and setup.
