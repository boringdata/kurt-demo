---
name: cms-onboard
description: Configure CMS schema mappings for your specific content types and fields
---

# CMS Onboard Skill

Interactive setup to discover your CMS schemas and map them to Kurt's format. Handles custom content types, field names, and nested structures.

## Overview

Every CMS instance has unique schemas. This skill:
- **Discovers** all content types in your CMS
- **Maps** custom fields to standard roles (content, title, metadata)
- **Validates** configuration with real data
- **Generates** config file for other CMS skills

**Use this skill when:**
- First time setup (before using other CMS skills)
- Adding new content types
- CMS schema changed
- Fetch/import not working correctly

## Quick Start

```bash
# Run interactive onboarding
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# Or invoke as skill in Claude Code
Skill(cms-onboard-skill)
```

## Prerequisites

**1. Basic CMS configuration**

Create `.claude/scripts/cms-config.json` with connection details:

```json
{
  "sanity": {
    "project_id": "your-project-id",
    "dataset": "production",
    "token": "your-read-token",
    "write_token": "your-write-token",
    "base_url": "https://yoursite.com"
  }
}
```

**2. CMS access**

Token needs permission to read schema and documents.

## Onboarding Workflow

### Phase 1: Discovery

Script connects and discovers available content types:

```
Connecting to Sanity CMS...
✓ Connected to project: your-project-name
✓ Dataset: production

Discovering content types...

Found 8 content types:

  ID  Type           Documents  Description
  --  ----           ---------  -----------
  1   article        123
  2   blogPost       45
  3   page           12
  4   author         8
  5   category       15
  6   product        200
  7   landingPage    25
  8   pressRelease   30

Which content types contain content you want to work with?
(Enter numbers separated by commas, e.g., 1,2,7)
Or type 'preview X' to see example of type X

Your selection:
```

**User:** `preview 1`

```
Example "article" document:

{
  "_id": "abc-123",
  "_type": "article",
  "title": "Getting Started with PostgreSQL",
  "headline": "Quick PostgreSQL Guide",
  "body": [
    {
      "_type": "block",
      "children": [{"text": "Welcome to PostgreSQL..."}]
    }
  ],
  "slug": {
    "_type": "slug",
    "current": "getting-started-postgresql"
  },
  "author": {
    "_ref": "author-456"
  },
  "publishedAt": "2024-01-15T10:30:00Z",
  "_updatedAt": "2024-10-20T15:45:00Z",
  "tags": ["tutorial", "database", "postgres"],
  "categories": [
    {"_ref": "cat-1", "_type": "reference"}
  ],
  "featured": true,
  "viewCount": 1250,
  "internalNotes": "Updated for v2"
}

Type 'select 1' to configure this type, or 'back' to return to list
```

**User:** `select 1,2`

### Phase 2: Field Mapping (per type)

For each selected content type:

```
=== Configuring: article ===

I'll ask about key fields. Example document shown above.

1. CONTENT FIELD
   Which field contains the main content to extract?

   Detected rich text fields:
   - body (Portable Text blocks)

   Detected text fields:
   - title
   - headline
   - internalNotes

   Which field? [body]:
```

**User:** `body` (or press Enter for default)

```
2. TITLE FIELD
   Which field should be used as the document title?

   Options:
   - title: "Getting Started with PostgreSQL"
   - headline: "Quick PostgreSQL Guide"

   Which field? [title]:
```

**User:** `title`

```
3. SLUG FIELD
   Which field contains the URL slug?

   Options:
   - slug.current: "getting-started-postgresql"

   Which field? [slug.current]:
```

**User:** `slug.current`

```
4. METADATA FIELDS
   Select which fields to include as metadata.
   These will be imported to Kurt and used in publishing.

   Available fields:

   [ ] author (reference to author)
   [ ] publishedAt (datetime)
   [ ] _updatedAt (datetime)
   [ ] tags (array of strings)
   [ ] categories (array of references)
   [ ] featured (boolean)
   [ ] viewCount (number)
   [ ] internalNotes (string)

   Enter field names to include (comma-separated):
   Or 'all' for all fields, 'none' for no metadata

   Fields to include:
```

**User:** `author, publishedAt, tags, categories`

```
5. REFERENCE RESOLUTION
   How should reference fields be resolved?

   author (reference):
     a) Include reference ID only
     b) Resolve to: author->name
     c) Resolve to: author->email
     d) Custom path: ___

   Choice [b]:
```

**User:** `b`

```
   categories (array of references):
     a) Include reference IDs only
     b) Resolve to: categories[]->title
     c) Resolve to: categories[]->slug.current
     d) Custom path: ___

   Choice [b]:
```

**User:** `b`

```
✓ Configuration for "article" complete!

Summary:
  Content field: body
  Title field: title
  Slug field: slug.current
  Metadata:
    - author → author->name
    - publishedAt → publishedAt
    - tags → tags[]
    - categories → categories[]->title

Repeating configuration for: blogPost
```

### Phase 3: Validation

After configuring all types:

```
=== Validating Configuration ===

Test 1: Content type filtering
  ✓ Search limited to: article, blogPost
  ✓ Found 168 total documents

Test 2: Field access (article)
  ✓ Fetching sample article...
  ✓ Content field "body" exists and populated
  ✓ Title field "title" exists
  ✓ Slug field "slug.current" exists
  ✓ Metadata field "author->name" resolved
  ✓ Metadata field "publishedAt" exists
  ✓ Metadata field "tags[]" exists (3 items)
  ✓ Metadata field "categories[]->title" resolved (1 item)

Test 3: Field access (blogPost)
  ✓ Fetching sample blogPost...
  ✓ Content field "richText" exists and populated
  ✓ Title field "headline" exists
  ⚠ Warning: Slug field "urlSlug" is null in 2/5 test documents
  ✓ Metadata field "author.displayName" exists
  ⚠ Warning: "postTags[]" is empty in 3/5 test documents

Test 4: Conversion test
  ✓ Portable Text → Markdown conversion working
  ✓ Sample output: 823 characters

=== Configuration Complete ===

Configuration saved to: .claude/scripts/cms-config.json

Generated mappings for:
  ✓ article (123 documents)
  ✓ blogPost (45 documents)

You can now use:
  - cms-search-skill (searches configured types only)
  - cms-fetch-skill (extracts using field mappings)
  - cms-import-skill (imports with mapped metadata)
  - cms-publish-skill (publishes to mapped fields)

To reconfigure or add content types, run this script again.
```

## Configuration Format

### Generated Config

The script adds `content_type_mappings` to your cms-config.json:

```json
{
  "sanity": {
    "project_id": "abc123",
    "dataset": "production",
    "token": "sk...",
    "write_token": "sk...",
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
          "last_modified": "_updatedAt",
          "tags": "tags[]",
          "categories": "categories[]->title"
        }
      },
      "blogPost": {
        "enabled": true,
        "content_field": "richText",
        "title_field": "headline",
        "slug_field": "urlSlug",
        "metadata_fields": {
          "author": "author.displayName",
          "published_date": "publishDate",
          "tags": "postTags[]"
        }
      },
      "page": {
        "enabled": false
      }
    }
  }
}
```

### Field Path Syntax

**Simple fields:**
```json
"title_field": "title"
```

**Nested objects:**
```json
"slug_field": "slug.current"
"author": "author.name"
```

**References (Sanity):**
```json
"author": "author->name"           // Single reference
"categories": "categories[]->title" // Array of references
```

**Arrays:**
```json
"tags": "tags[]"                   // Array of strings
"authors": "authors[]->name"       // Array of references
```

## Manual Configuration

You can also edit cms-config.json manually:

### Add New Content Type

```json
"content_type_mappings": {
  "newType": {
    "enabled": true,
    "content_field": "mainContent",
    "title_field": "heading",
    "slug_field": "url",
    "metadata_fields": {
      "custom_field": "myCustomField"
    }
  }
}
```

### Disable Content Type

```json
"article": {
  "enabled": false,  // Won't appear in searches
  ...
}
```

### Update Field Mapping

```json
"article": {
  ...
  "content_field": "newBodyField",  // Changed field name
  ...
}
```

## Common Workflows

### Workflow 1: First Time Setup

```bash
# 1. Create basic config
cp .claude/skills/cms-interaction-skill/adapters/sanity/config.json.example \
   .claude/scripts/cms-config.json

# Edit with credentials

# 2. Run onboarding
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# 3. Follow prompts to configure content types

# 4. Test with search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --limit 5
```

### Workflow 2: Add New Content Type

```bash
# Run onboarding again
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# When prompted, select existing types + new type
# Example: "1,2,5" (existing: 1,2 | new: 5)

# Configure only the new type
# Existing configs preserved
```

### Workflow 3: Fix Incorrect Mapping

If fetch/import isn't working:

```bash
# Re-run onboarding
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# Select the problematic content type
# Reconfigure field mappings

# Validation will show if it works now
```

### Workflow 4: Explore Unknown Schema

```bash
# Run onboarding
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# Use 'preview X' to see example documents
# Understand structure before configuring
```

## Advanced Features

### Complex Field Paths

**Multiple levels of nesting:**
```json
"author_email": "author.contact.email"
```

**Conditional fields (future):**
```json
"content_field": "body || mainContent || content"  // Fallback chain
```

### Per-Type Conversion Settings

```json
"article": {
  ...
  "conversion_settings": {
    "favor_precision": true,
    "include_tables": true,
    "image_handling": "preserve"
  }
}
```

### Custom Metadata Transformations

```json
"metadata_fields": {
  "published_date": "publishedAt",
  "year_published": "publishedAt.year"  // Extract year only
}
```

## How Other Skills Use Mappings

### cms-search-skill

```python
# Only searches enabled content types
enabled_types = [
  type_name
  for type_name, config in mappings.items()
  if config.get('enabled', True)
]

# Filters: _type in ['article', 'blogPost']
```

### cms-fetch-skill

```python
# Uses mapped fields
content_type = doc['_type']
mapping = mappings.get(content_type, {})

content = extract_field(doc, mapping.get('content_field', 'body'))
title = extract_field(doc, mapping.get('title_field', 'title'))
```

### cms-import-skill

```python
# Extracts configured metadata
metadata_mappings = mapping.get('metadata_fields', {})
for key, field_path in metadata_mappings.items():
  value = extract_field(doc, field_path)
  frontmatter[key] = value
```

### cms-publish-skill

```python
# Publishes to mapped fields
doc_data = {
  mapping['content_field']: content,
  mapping['title_field']: title,
  mapping['slug_field']: slug,
  # ... metadata fields
}
```

## Troubleshooting

### "No content types found"

**Cause:** Token lacks schema read permissions

**Fix:**
- Verify token has `Viewer` role minimum
- Check token is for correct project/dataset
- Test in CMS dashboard

### "Field not found" during validation

**Cause:** Selected field doesn't exist in test documents

**Fix:**
- Preview example document first
- Check field name spelling
- Verify field exists in schema
- Some documents may have null/empty fields (shows as warning)

### "Reference resolution failed"

**Cause:** Referenced document doesn't exist or isn't published

**Fix:**
- Use reference ID instead of resolution
- Check if references are published
- Some null references are expected (warnings only)

### Configuration not taking effect

**Cause:** Config file not in expected location

**Fix:**
```bash
# Verify config location
ls -la .claude/scripts/cms-config.json

# Check for syntax errors
python -m json.tool .claude/scripts/cms-config.json

# Re-run onboarding to regenerate
```

### Want to start over

```bash
# Backup current config
cp .claude/scripts/cms-config.json .claude/scripts/cms-config.json.backup

# Remove mappings section
# Edit .claude/scripts/cms-config.json
# Delete "content_type_mappings": {...}

# Re-run onboarding
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity
```

## Best Practices

1. **Preview before configuring** - Use `preview X` to see document structure
2. **Start with main types** - Configure primary content types first
3. **Test incrementally** - Configure one type, test, then add more
4. **Include essential metadata** - Author, dates, tags at minimum
5. **Document conventions** - Add comments to config (future enhancement)
6. **Version control config** - Commit cms-config.json to track changes
7. **Reconfigure after schema changes** - Re-run onboarding when CMS schema updates

## Integration with Other Skills

### Before onboarding:

```bash
# cms-search-skill assumes 'body' field
# cms-fetch-skill assumes 'title' field
# May fail with custom schemas
```

### After onboarding:

```bash
# cms-search-skill uses configured types only
# cms-fetch-skill extracts from mapped fields
# cms-import-skill preserves mapped metadata
# cms-publish-skill writes to mapped fields

# All skills work with your custom schema!
```

## Script Options

```bash
# Interactive mode (default)
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity

# Non-interactive (future)
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py \
  --cms sanity \
  --config preset-config.json

# Add single type (future)
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py \
  --cms sanity \
  --add-type article

# Validate existing config
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py \
  --cms sanity \
  --validate-only
```

## Quick Reference

```bash
# Run onboarding
cms_onboard.py --cms sanity

# Follow prompts:
# 1. Select content types (preview available)
# 2. Map fields for each type
# 3. Configure reference resolution
# 4. Validation tests

# Output: Updated cms-config.json with mappings

# Then use other skills normally:
cms_search.py --cms sanity --query "tutorial"
cms_fetch.py --cms sanity --document-id abc-123
# (Uses your configured field mappings)
```

## Related Skills

- **[cms-search-skill](../cms-search-skill/SKILL.md)** - Searches configured content types
- **[cms-fetch-skill](../cms-fetch-skill/SKILL.md)** - Fetches using field mappings
- **[cms-import-skill](../cms-import-skill/SKILL.md)** - Imports with mapped metadata
- **[cms-publish-skill](../cms-publish-skill/SKILL.md)** - Publishes to mapped fields

## Configuration Reference

See [CMS Interaction README](../cms-interaction-skill/README.md) for infrastructure documentation.
