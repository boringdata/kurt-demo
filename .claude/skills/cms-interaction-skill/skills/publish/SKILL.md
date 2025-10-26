---
name: cms-publish
description: Publish updated content to CMS as drafts for review (Sanity, Contentful, WordPress)
---

# CMS Publish Skill

Push updated content from Kurt projects back to your CMS as drafts for review and publication.

## Overview

Publish content to CMS with:
- **Draft-only mode** - Never auto-publishes to production
- Full metadata support (tags, categories, SEO)
- Update existing content or create new
- Returns draft URL for manual review

**Use this skill when:**
- Publishing updated content from content-writing-skill
- Creating new content in CMS
- Pushing bulk updates
- Syncing local changes back to CMS

**Safety:** This skill creates DRAFTS only. User must review and publish from CMS interface.

## Quick Start

```bash
# Update existing document as draft
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/my-project/assets/article-draft.md \
  --document-id abc-123

# Create new document as draft
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/my-project/assets/new-article.md \
  --create-new \
  --content-type article \
  --slug "new-article-slug"
```

## Prerequisites

**1. Run Onboarding (Recommended)**

Configure your CMS schema mappings first:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity
```

See [cms-onboard-skill](../cms-onboard-skill/SKILL.md) for details.

**2. CMS Write Token**

Configure with write permissions:

```json
{
  "sanity": {
    "project_id": "...",
    "dataset": "production",
    "token": "read-token",
    "write_token": "write-token-with-editor-role"
  }
}
```

**3. Content File**

Markdown file with YAML frontmatter:
```markdown
---
title: "Updated Tutorial"
cms_id: abc-123
cms_type: article
slug: updated-tutorial
tags: [tutorial, quickstart, v2]
---

# Updated Tutorial

Your updated content here...
```

## Publish Operations

### Update Existing Document

Update a document as draft:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/tutorial-refresh/assets/quickstart-v2-draft.md \
  --document-id abc-123
```

**What happens:**
1. Parses markdown + frontmatter
2. Converts markdown to CMS format (Portable Text for Sanity)
3. Creates draft version in CMS (`drafts.abc-123`)
4. Returns draft URL for review
5. **Does NOT publish** - waits for user approval

**Output:**
```
Reading: projects/tutorial-refresh/assets/quickstart-v2-draft.md

Publishing to sanity...

✓ Draft created successfully!

Draft ID: drafts.abc-123
Draft URL: https://www.sanity.io/manage/personal/project123/desk/article;abc-123

IMPORTANT: Review and publish from CMS interface
```

### Create New Document

Create entirely new content as draft:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/new-content/assets/postgres-guide.md \
  --create-new \
  --content-type article \
  --slug "postgres-integration-guide" \
  --tags "tutorial,postgres,integration"
```

**Required:**
- `--create-new` - Flag to create new document
- `--content-type` - CMS content type (e.g., article, post, page)

**Optional:**
- `--slug` - URL slug (auto-generated if not provided)
- `--tags` - Comma-separated tags
- `--categories` - Comma-separated category IDs
- `--author` - Author reference ID

### Publish with Metadata

Add/override metadata during publish:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file draft.md \
  --document-id abc-123 \
  --tags "tutorial,quickstart,v2" \
  --categories "cat-id-1,cat-id-2" \
  --slug "updated-quickstart-v2"
```

**Metadata priority:**
1. CLI arguments (highest priority)
2. Frontmatter in file
3. Existing CMS values (for updates)

### Dry Run

Preview what would be published:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file draft.md \
  --document-id abc-123 \
  --dry-run
```

**Output:**
```
Dry run - would publish:
  CMS: sanity
  Title: Updated Quickstart Tutorial
  Content Type: article
  Update Document: abc-123
  Metadata: {'slug': 'quickstart', 'tags': ['tutorial', 'v2']}
  Content Length: 3521 chars
```

## File Format

### Markdown with Frontmatter

The script reads standard markdown files:

```markdown
---
title: "Tutorial Title"
cms_id: abc-123
cms_type: article
slug: tutorial-slug
tags:
  - tutorial
  - quickstart
  - beginner
categories:
  - getting-started
author_id: author-ref-123
seo:
  meta_description: "Quick tutorial description"
  meta_title: "Tutorial Title | Site Name"
---

# Tutorial Title

Introduction paragraph...

## Section 1

Content here...

## Section 2

More content...
```

### Metadata Fields

| Frontmatter Field | CMS Field | Notes |
|-------------------|-----------|-------|
| `title` | title | Required |
| `slug` | slug | Optional, auto-generated if missing |
| `tags` | tags | Array of strings |
| `category_ids` | categories | Array of category reference IDs |
| `author_id` | author | Author reference ID |
| `seo` | seo | SEO metadata object |
| `cms_id` | Used for updates | Not sent to CMS |
| `cms_type` | _type | CMS content type |

### Content Conversion

Markdown is converted to CMS-specific format:

**Sanity:** Markdown → Portable Text blocks

**Supported:**
- ✅ Headings (h1-h6)
- ✅ Paragraphs
- ✅ Bold, italic, code (inline)
- ✅ Code blocks
- ✅ Blockquotes
- ✅ Lists (basic)

**Limitations:**
- Complex nested structures may need CMS review
- Custom components not supported
- Images as placeholders only

## Common Workflows

### Workflow 1: Update CMS Content

Complete update workflow:

```bash
# 1. Fetch existing content
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123

# 2. Import to Kurt
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --file sources/cms/sanity/article/quickstart.md

# 3. Create update project
/create-project
# Name: tutorial-refresh
# Sources: sources/cms/sanity/article/quickstart.md

# 4. Create updated draft
content-writing-skill draft tutorial-refresh quickstart-v2

# 5. Publish draft to CMS
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/tutorial-refresh/assets/quickstart-v2-draft.md \
  --document-id abc-123

# 6. Review in CMS (open draft URL)

# 7. Publish from CMS when ready
```

### Workflow 2: Bulk Updates

Update multiple documents:

```bash
# Prepare: Create drafts for all tutorials
for tutorial in quickstart advanced integration; do
  content-writing-skill draft tutorial-refresh $tutorial
done

# Publish all drafts
for draft_file in projects/tutorial-refresh/assets/*-draft.md; do
  # Extract CMS ID from frontmatter
  cms_id=$(head -20 "$draft_file" | grep "cms_id:" | cut -d'"' -f2)

  echo "Publishing: $draft_file → $cms_id"

  python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
    --cms sanity \
    --file "$draft_file" \
    --document-id "$cms_id"

  echo "Draft URL opened. Review and publish before continuing."
  read -p "Press Enter when published..."
done
```

### Workflow 3: New Content Creation

Create new content with Kurt:

```bash
# 1. Fetch reference content
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --filter "tags=[tutorial]" --limit 5 --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin

# 2. Import references
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --source-dir sources/cms/sanity/

# 3. Create project
/create-project
# Name: new-postgres-tutorial
# Sources: sources/cms/sanity/article/ (reference tutorials)

# 4. Create outline and draft
content-writing-skill outline new-postgres-tutorial postgres-guide
content-writing-skill draft new-postgres-tutorial postgres-guide

# 5. Publish as new article
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/new-postgres-tutorial/assets/postgres-guide-draft.md \
  --create-new \
  --content-type article \
  --slug "postgres-integration-guide" \
  --tags "tutorial,postgres,database,integration"

# 6. Review draft in CMS
# 7. Publish from CMS
```

### Workflow 4: Metadata Updates

Update metadata without content changes:

```bash
# 1. Fetch current version
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123

# 2. Edit frontmatter only
vim sources/cms/sanity/article/tutorial.md
# Update tags, categories, SEO

# 3. Publish metadata changes
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file sources/cms/sanity/article/tutorial.md \
  --document-id abc-123 \
  --tags "tutorial,quickstart,v2,updated"

# 4. Review in CMS
# 5. Publish
```

## Draft System

### How Drafts Work

**Sanity:**
- Drafts have ID format: `drafts.{document-id}`
- Draft exists separately from published version
- Publishing replaces published version with draft
- Deleting draft leaves published version unchanged

**Draft lifecycle:**
1. Create draft via API
2. Review in Sanity Studio
3. Edit if needed (in CMS)
4. Click "Publish" button
5. Draft becomes new published version

### Draft URLs

Script returns CMS-specific draft URL:

**Sanity:**
```
https://www.sanity.io/manage/personal/{project-id}/desk/{content-type};{document-id}
```

**Opens:**
- Sanity Studio interface
- Split view: draft vs published
- Edit panel with all fields
- Publish button when ready

## Safety Features

### Never Auto-Publishes

**By design:**
- Only creates drafts
- Never calls publish API
- Requires manual review
- Prevents accidental overwrites

### Confirmation Workflow

```bash
# 1. Create draft
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity --file draft.md --document-id abc-123

# 2. Script output
# ✓ Draft created successfully!
# Draft URL: https://...
# IMPORTANT: Review and publish from CMS interface

# 3. User opens URL in browser
# 4. User reviews changes
# 5. User clicks Publish (or discards)
```

### Rollback

If draft has issues:

**Option 1: Delete draft in CMS**
- Open draft URL
- Click "Discard changes"
- Draft deleted, published version unchanged

**Option 2: Edit draft in CMS**
- Open draft URL
- Edit fields directly
- Publish when ready

**Option 3: Republish corrected version**
```bash
# Edit local file
vim draft.md

# Republish (overwrites draft)
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity --file draft.md --document-id abc-123
```

## Integration with Other Skills

### With content-writing-skill

Primary use case:

```bash
# 1. Create draft with content-writing-skill
content-writing-skill draft my-project updated-article

# 2. Publish to CMS
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file projects/my-project/assets/updated-article-draft.md \
  --document-id abc-123

# 3. Review lineage in CMS
# Draft includes all updates from content-writing-skill
# Lineage tracked in git history
```

### With cms-fetch-skill

Round-trip workflow:

```bash
# Fetch → Edit → Publish
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123

# (Edit file)

python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file sources/cms/sanity/article/tutorial.md \
  --document-id abc-123
```

### With project-management-skill

Track publishing in projects:

```markdown
## project.md

### Publishing Status

| Document | CMS ID | Draft Created | Published | Status |
|----------|--------|---------------|-----------|--------|
| quickstart-v2 | abc-123 | 2024-10-20 | 2024-10-21 | ✅ Live |
| advanced-v2 | def-456 | 2024-10-20 | - | 📝 In review |
| integration-v2 | ghi-789 | 2024-10-20 | - | 📝 In review |
```

## Troubleshooting

### "Write token not configured"

**Cause:** Missing `write_token` in cms-config.json

**Fix:**
```json
{
  "sanity": {
    ...
    "write_token": "sk...your-token-with-editor-role"
  }
}
```

Create write token:
1. Go to Sanity project settings
2. API → Tokens
3. Create token with `Editor` role
4. Copy to cms-config.json

### "Permission denied"

**Cause:** Token lacks write permissions

**Fix:**
- Verify token has `Editor` or `Admin` role
- Test token in Sanity dashboard
- Regenerate token if needed

### "Content type not found"

**Cause:** Invalid content type in `--content-type`

**Fix:**
```bash
# Check available types in your CMS schema
# For Sanity, check schema files or use Vision tool

# Common types:
--content-type article
--content-type post
--content-type page
```

### "Required field missing"

**Cause:** CMS schema requires field not provided

**Fix:**
```bash
# Add required fields to frontmatter or CLI

# Example: If author is required
python .claude/skills/cms-interaction-skill/scripts/cms_publish.py \
  --cms sanity \
  --file draft.md \
  --document-id abc-123 \
  --author "author-ref-id"
```

### "Conversion failed"

**Cause:** Markdown too complex for automatic conversion

**Fix:**
1. Publish simple version as draft
2. Edit complex formatting in CMS
3. Or simplify markdown locally

### "Draft not visible in CMS"

**Cause:** Draft created but not appearing

**Fix:**
- Refresh CMS interface
- Open draft URL directly
- Check document ID is correct
- Verify dataset (production vs staging)

## Best Practices

1. **Always dry run first** - Preview with `--dry-run` for new workflows
2. **Test on staging** - Use staging CMS before production
3. **Review in CMS** - Never blindly publish, always review drafts
4. **Track in version control** - Commit drafts before publishing
5. **Document publish log** - Keep record of what was published when
6. **Use references** - Author IDs, category IDs, not names
7. **Validate metadata** - Check tags/categories exist in CMS
8. **Batch carefully** - Review each draft individually for bulk updates

## Quick Reference

```bash
# Update existing as draft
cms_publish.py --cms sanity --file draft.md --document-id abc-123

# Create new as draft
cms_publish.py --cms sanity --file new.md --create-new --content-type article

# With metadata
cms_publish.py --cms sanity --file draft.md --document-id abc-123 \
  --tags "tag1,tag2" --slug "new-slug"

# Dry run
cms_publish.py --cms sanity --file draft.md --document-id abc-123 --dry-run

# Full workflow
cms_fetch.py --cms sanity --document-id abc-123
# (Edit file)
cms_publish.py --cms sanity --file sources/cms/sanity/article/doc.md --document-id abc-123
# (Review draft URL in browser)
# (Publish from CMS)
```

## Related Skills

- **[content-writing-skill](../../content-writing-skill/SKILL.md)** - Create drafts to publish
- **[cms-fetch-skill](../cms-fetch-skill/SKILL.md)** - Fetch existing content to update
- **[cms-search-skill](../cms-search-skill/SKILL.md)** - Find content to update
- **[project-management-skill](../../project-management-skill/SKILL.md)** - Track publishing workflow

## Configuration

See [CMS Interaction README](../cms-interaction-skill/README.md) for:
- Write token setup
- Adapter documentation
- CMS-specific features
