---
name: cms-import
description: Import CMS content into Kurt database for analysis and querying
---

# CMS Import Skill

Import CMS content from markdown files into Kurt's database for metadata extraction, analysis, and querying.

## Overview

Load CMS content into Kurt to:
- Extract AI-powered metadata (topics, tools, content types)
- Make content searchable and queryable
- Track content in projects
- Enable lineage tracking in content-writing-skill

**Use this skill when:**
- After fetching content with cms-fetch-skill
- Creating source material for projects
- Building organizational knowledge base
- Enabling Kurt's document intelligence features

## Quick Start

```bash
# Import all files from directory
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/

# Import specific file
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --file sources/cms/sanity/article/quickstart.md

# Verify import
kurt document list --url-prefix sanity://
kurt document get <doc-id>
```

## Prerequisites

**1. Run Onboarding (Recommended)**

Configure your CMS schema mappings first:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_onboard.py --cms sanity
```

See [cms-onboard-skill](../cms-onboard-skill/SKILL.md) for details.

**2. Kurt CLI installed:**
```bash
pip install kurt-cli
which kurt
```

**3. CMS content fetched:**

Use [cms-fetch-skill](../cms-fetch-skill/SKILL.md) first:
```bash
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123
```

## Import Operations

### Import Directory

Import all markdown files from a directory:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/
```

**What happens:**
1. Scans directory for `.md` files
2. Parses YAML frontmatter from each file
3. Creates Kurt document record with CMS URL
4. Links file to database record
5. Runs metadata extraction (AI-powered)
6. Reports success/failure for each file

**Output:**
```
============================================================
Importing: sources/cms/sanity/article/quickstart.md
============================================================
Creating Kurt document for: sanity://abc-123
Importing content to document abc-123...
✓ Content imported
Extracting metadata...
✓ Metadata extracted
✓ Success: abc-123

============================================================
Import Summary
============================================================
Total files: 23
Successful: 23
Failed: 0
```

### Import Single File

Import one specific file:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --file sources/cms/sanity/article/quickstart.md
```

**Use when:**
- Testing import process
- Importing newly fetched content
- Re-importing after manual edits

### Update Existing Only

Import without creating new documents:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/ \
  --no-create
```

**Use when:**
- Refreshing existing content
- Avoiding duplicate records
- Re-running metadata extraction

### Dry Run

Preview what would be imported:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/ \
  --dry-run
```

**Output:**
```
Found 23 file(s) to import

Dry run - would import:
  - Quickstart Tutorial (CMS ID: abc-123)
  - Advanced Guide (CMS ID: def-456)
  - Integration Guide (CMS ID: ghi-789)
  ...
```

## How It Works

### Step-by-Step Process

**1. Parse Frontmatter**
```yaml
---
title: "Quickstart Tutorial"
cms_id: abc-123
cms_type: article
url: https://yoursite.com/quickstart
author: Jane Doe
published_date: "2024-01-15"
cms_metadata:
  tags: [tutorial, beginner]
---
```

**2. Construct Kurt URL**
- Format: `{cms-name}://{cms-id}`
- Example: `sanity://abc-123`
- Or uses `cms_url` from frontmatter if available

**3. Check for Existing Document**
```bash
kurt document list --url-contains sanity://abc-123
```

**4a. Create New Document (if needed)**
```bash
kurt ingest add sanity://abc-123
```

**4b. Or Use Existing Document**
- If document already exists, uses that record
- With `--no-create`, skips if not exists

**5. Import Content**
```bash
python .claude/scripts/import_markdown.py \
  --document-id abc-123 \
  --file-path sources/cms/sanity/article/quickstart.md
```

- Links file to database
- Populates metadata from frontmatter
- Updates status to `FETCHED`

**6. Extract Metadata**
```bash
kurt index abc-123
```

- AI-powered analysis
- Extracts: topics, tools, content types
- Populates database fields

### Kurt Document Record

After import, Kurt stores:

```
ID: abc-123
Title: Quickstart Tutorial
Status: FETCHED
URL: sanity://abc-123
Author: Jane Doe
Published: 2024-01-15
Content Path: cms/sanity/article/quickstart.md
Content Hash: sha256:...
Topics: ["getting started", "tutorials", "quickstart"]
Tools: ["platform", "sdk"]
Content Type: tutorial
```

## Common Workflows

### Workflow 1: Import After Fetch

Standard search → fetch → import:

```bash
# 1. Search
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --filter "tags=[tutorial]" --output json > tutorials.json

# 2. Fetch
cat tutorials.json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin

# 3. Import
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --source-dir sources/cms/sanity/

# 4. Verify
kurt document list --url-prefix sanity://
```

### Workflow 2: Project Setup

Import CMS content for a project:

```bash
# 1. Fetch to project directory
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity \
  --document-ids abc-123,def-456 \
  --output projects/tutorial-refresh/sources/

# 2. Import
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir projects/tutorial-refresh/sources/sanity/

# 3. Query in Kurt
kurt document list --url-prefix sanity:// --status FETCHED

# 4. Use in content creation
content-writing-skill draft tutorial-refresh updated-guide
# (Kurt automatically finds and uses imported sources)
```

### Workflow 3: Bulk Import

Import large amounts of content:

```bash
# 1. Fetch all content
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity --output json | \
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --from-stdin

# 2. Count files
find sources/cms/sanity/ -name "*.md" | wc -l

# 3. Import (dry run first)
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/ \
  --dry-run

# 4. Import for real
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --source-dir sources/cms/sanity/

# 5. Query results
kurt document list --status FETCHED | grep sanity:// | wc -l
```

### Workflow 4: Re-import After Edits

Re-import content after manual edits:

```bash
# 1. Edit file locally
vim sources/cms/sanity/article/quickstart.md

# 2. Re-import (updates existing record)
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity \
  --file sources/cms/sanity/article/quickstart.md

# 3. Verify changes
kurt document get <doc-id>
```

## Metadata Extraction

After import, Kurt runs AI-powered metadata extraction.

### Extracted Fields

| Field | Description | Example |
|-------|-------------|---------|
| `topics` | Main subjects | ["authentication", "oauth"] |
| `tools` | Technologies mentioned | ["postgres", "python", "react"] |
| `content_type` | Document category | tutorial, guide, reference |
| `complexity` | Technical level | beginner, intermediate, advanced |
| `prerequisites` | Requirements | Prior knowledge needed |

### Query by Metadata

```bash
# Find all tutorials
kurt document query --content-type tutorial

# Find content about specific tool
kurt document query --tool postgres

# Find beginner content
kurt document query --complexity beginner

# Complex queries (SQL)
sqlite3 .kurt/kurt.sqlite "
  SELECT title, topics, tools
  FROM documents
  WHERE url LIKE 'sanity://%'
  AND topics LIKE '%authentication%'
"
```

## Integration with Other Skills

### With cms-fetch-skill

Fetch then import:

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123

python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --file sources/cms/sanity/article/quickstart.md
```

### With content-writing-skill

Imported content becomes source material:

```bash
# 1. Import CMS content
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --source-dir sources/cms/sanity/

# 2. Create project with CMS sources
/create-project
# Name: tutorial-refresh
# Sources: sources/cms/sanity/article/

# 3. Create outline (Kurt finds CMS sources)
content-writing-skill outline tutorial-refresh updated-quickstart

# 4. Check lineage in outline
cat projects/tutorial-refresh/assets/updated-quickstart-outline.md
# Shows: sources/cms/sanity/article/quickstart.md as source
```

### With document-management-skill

Query imported content:

```bash
# List all CMS content
kurt document list --url-prefix sanity://

# Get specific document
kurt document get <doc-id>

# Query by attributes
kurt document query --content-type tutorial --tool postgres

# Find related documents
kurt document related <doc-id>
```

### With project-management-skill

Track CMS content in projects:

```markdown
## project.md

### Sources

**CMS Content (Existing Tutorials)**
- sources/cms/sanity/article/ (23 tutorials)
- Imported to Kurt: ✓
- Metadata extracted: ✓

**Reference Docs**
- sources/docs.getdbt.com/features/ (12 guides)

### Tasks
- [ ] Review all 23 tutorials in CMS
- [ ] Identify update patterns
- [ ] Create updated drafts
- [ ] Publish back to CMS
```

## Troubleshooting

### "kurt: command not found"

**Cause:** Kurt CLI not installed

**Fix:**
```bash
pip install kurt-cli
which kurt
kurt --version
```

### "import_markdown.py not found"

**Cause:** Script not at expected location

**Fix:**
```bash
# Verify script exists
ls -la .claude/scripts/import_markdown.py

# If missing, check import-content-skill is installed
```

### "No frontmatter found"

**Cause:** File missing YAML frontmatter

**Fix:**
```bash
# Check file format
head -20 sources/cms/sanity/article/quickstart.md

# Should start with:
# ---
# title: "..."
# cms_id: "..."
# ---

# Re-fetch if frontmatter is missing
python .claude/skills/cms-interaction-skill/scripts/cms_fetch.py \
  --cms sanity --document-id abc-123
```

### "Document already exists"

**Behavior:** Uses existing document (not an error)

**To force new record:**
```bash
# Delete old record first
kurt document delete <doc-id>

# Then re-import
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --file sources/cms/sanity/article/quickstart.md
```

### "Metadata extraction failed"

**Cause:** AI API timeout or rate limit

**Fix:**
```bash
# Re-run indexing manually
kurt index <doc-id>

# Or batch index all
kurt index --status FETCHED --url-prefix sanity://

# Check logs
cat .kurt/logs/indexing.log
```

### "Import failed: Database locked"

**Cause:** Another Kurt process has lock

**Fix:**
```bash
# Check for other Kurt processes
ps aux | grep kurt

# Wait and retry
sleep 2
python .claude/skills/cms-interaction-skill/scripts/cms_import.py \
  --cms sanity --file sources/cms/sanity/article/quickstart.md
```

## Verification

### Check Import Success

```bash
# List imported documents
kurt document list --url-prefix sanity://

# Get document details
kurt document get <doc-id>

# Verify metadata extraction
kurt document get <doc-id> | grep -E "(topics|tools|content_type)"

# Check file linking
kurt document get <doc-id> | grep "content_path"
```

### Query Imported Content

```bash
# Count by status
kurt document list --status FETCHED | grep sanity:// | wc -l

# List by content type
kurt document list --content-type tutorial

# Find by topic
kurt document query --topic authentication

# Check recent imports
kurt document list --status FETCHED --limit 10
```

## Best Practices

1. **Dry run first** - Always preview with `--dry-run` for large batches
2. **Import after fetch** - Don't manually create files, use cms-fetch-skill
3. **Verify frontmatter** - Ensure YAML is valid and complete
4. **Check metadata** - Review extracted topics/tools for accuracy
5. **Use version control** - Commit imported files to track changes
6. **Bulk operations** - Import directories, not individual files
7. **Monitor failures** - Check import summary for errors
8. **Re-index if needed** - Run `kurt index` if metadata extraction fails

## Performance

### Import Speed

- **Single file:** ~2-3 seconds (includes metadata extraction)
- **10 files:** ~20-30 seconds
- **100 files:** ~3-5 minutes
- **Bottleneck:** AI metadata extraction (most time-consuming)

### Optimization

```bash
# Skip metadata extraction during import (faster)
# Then batch index afterward
for file in sources/cms/sanity/**/*.md; do
  python .claude/scripts/import_markdown.py \
    --document-id $(grep "cms_id:" "$file" | cut -d'"' -f2) \
    --file-path "$file"
done

# Batch index all at once
kurt index --status FETCHED --url-prefix sanity://
```

## Quick Reference

```bash
# Import directory
cms_import.py --cms sanity --source-dir sources/cms/sanity/

# Import file
cms_import.py --cms sanity --file path/to/file.md

# Update existing only
cms_import.py --cms sanity --source-dir sources/cms/sanity/ --no-create

# Dry run
cms_import.py --cms sanity --source-dir sources/cms/sanity/ --dry-run

# Verify
kurt document list --url-prefix sanity://
kurt document get <doc-id>

# Re-index metadata
kurt index <doc-id>
```

## Related Skills

- **[cms-fetch-skill](../cms-fetch-skill/SKILL.md)** - Download CMS content first
- **[cms-search-skill](../cms-search-skill/SKILL.md)** - Find content to fetch/import
- **[document-management-skill](../../document-management-skill/SKILL.md)** - Query imported content
- **[content-writing-skill](../../content-writing-skill/SKILL.md)** - Use imported content as sources

## Configuration

See [CMS Interaction README](../cms-interaction-skill/README.md) for infrastructure documentation.
