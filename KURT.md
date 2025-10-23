# Kurt: Document Intelligence System

## Overview

Kurt is a document intelligence CLI that helps teams manage, analyze, and create content. It fetches web content, stores it in a local SQLite database with extracted metadata, and provides tools for organizing projects around content creation and updates.

## Core Concepts

### Document Management

Kurt maintains two types of storage:

1. **Database (SQLite)**: Metadata about documents (title, URL, author, dates, content fingerprints)
2. **Filesystem (`/sources/`)**: Actual content as markdown files

Documents are fetched from the web using trafilatura for clean markdown extraction.

### Projects

Projects organize content creation workflows. Each project has:

- **Goal**: What you're trying to accomplish
- **Sources**: Ground truth content (working FROM)
- **Targets**: Content to update or create (working ON)
- **Style Guidelines**: Voice, tone, format patterns (future)
- **Structure Templates**: Document patterns and templates (future)

## File Structure

```
kurt-demo/
├── sources/                        # Organizational knowledge base (Kurt-managed)
│   ├── docs.getdbt.com/           # Your docs
│   ├── blog.company.com/          # Your blog
│   └── competitor.com/            # Competitor/reference content
├── rules/                          # Extracted rules for content creation
│   ├── style/                      # Writing voice/tone patterns
│   │   ├── technical-documentation.md
│   │   └── conversational-blog.md
│   ├── structure/                  # Document format templates
│   │   ├── quickstart-tutorial.md
│   │   └── api-reference.md
│   ├── personas/                   # Audience targeting profiles
│   │   ├── technical-implementer.md
│   │   └── enterprise-decision-maker.md
│   └── publisher/                  # Organizational context
│       └── publisher-profile.md    # Single company profile
├── projects/                       # Individual projects
│   └── project-name/
│       ├── project.md             # Project manifest
│       ├── sources/               # Project-specific sources only
│       │   ├── internal-spec.pdf
│       │   └── notes.md
│       └── targets/               # Work in progress
│           └── drafts/
└── .kurt/                          # Kurt database and config
    ├── kurt.sqlite
    └── config (hidden file)
```

### Content Organization Philosophy

**Top-level folders (Shared/Reusable):**
- `/sources/` - All web content ingested by Kurt (organizational knowledge base)
- `/rules/style/` - Style guides, voice/tone patterns extracted from content
- `/rules/structure/` - Document templates and format patterns extracted from content
- `/rules/personas/` - Audience targeting profiles extracted from content
- `/rules/publisher/` - Organizational context and brand profile

**Project folders (Project-specific):**
- `projects/name/sources/` - One-off files only for this project (PDFs, internal docs)
- `projects/name/targets/` - Drafts and work-in-progress content

### Why This Separation?

1. **No duplication** - Organizational content lives once in `/sources/`
2. **Reusability** - Multiple projects reference same org content and rules
3. **Clear ownership** - Easy to see what's org-wide vs project-specific
4. **Kurt compatibility** - Works with Kurt's existing ingest system
5. **Rule-based consistency** - Extracted rules ensure consistent content creation

## Project Lifecycle

### 1. Create Project

```bash
# User runs slash command
/create-project
```

Claude will:
1. Ask about project intent (positioning, marketing assets, docs updates, etc.)
2. Get project name (kebab-case) and goal description
3. Collect ground truth sources (skippable)
4. Identify target content (skippable)
5. Create project structure and project.md

### 2. Add Content to Project

**Organizational content (from web):**
```bash
# Ingest to /sources/ (org knowledge base)
kurt ingest map https://example.com
# Or with date discovery (extracts publish dates from blogrolls/changelogs)
kurt ingest map https://example.com --discover-dates

kurt ingest fetch --url-prefix https://example.com/

# Reference in project.md
```

**Project-specific content:**
```bash
# User adds file directly
cp ~/file.pdf projects/project-name/sources/

# Update project.md to reference it
```

### 3. Work on Project

Claude uses:
- **Sources**: Ground truth to work FROM
- **Targets**: Content to update or create (working ON)
- **Style** (future): Voice/tone guidelines
- **Structure** (future): Templates and patterns

### 4. Resume Project

```bash
/resume-project project-name
```

Claude will:
1. Load project.md context
2. Check for missing sources or targets
3. Recommend next actions based on project status
4. Offer to update project notes

## project.md Format

```markdown
# Project Name

## Goal
What you want to accomplish

## Intent Category
a/b/c/d/e from project creation

## Sources (Ground Truth)

### From Organizational Knowledge Base
- [x] Page title: `/sources/domain.com/path/page.md` (fetched: YYYY-MM-DD)
- [ ] Another page: https://example.com/page (not fetched)

### Project-Specific Sources
- [x] Internal doc: `sources/filename.pdf` (added: YYYY-MM-DD)
- [x] Notes: `sources/notes.md`

## Targets (Content to Update/Create)

### Existing Content to Update
- [ ] Tutorial: `/sources/docs.company.com/tutorial.md`
- [ ] Guide: `/sources/docs.company.com/guide.md`

### New Content to Create
- [ ] New tutorial: `targets/drafts/new-tutorial.md`
- [ ] Blog post: `targets/drafts/blog-post.md`

## Style Guidelines

*Extracted writing patterns applicable to this project's content:*
- Technical documentation style: `/rules/style/technical-documentation.md`
- Conversational blog style: `/rules/style/conversational-blog.md`

## Structure Templates

*Document format templates applicable to this project's content:*
- Quickstart tutorial: `/rules/structure/quickstart-tutorial.md`
- API reference: `/rules/structure/api-reference.md`

## Target Personas

*Audience profiles for this project's target content:*
- Developer persona: `/rules/personas/technical-implementer.md`
- Business decision-maker: `/rules/personas/enterprise-decision-maker.md`

## Publisher Profile

*Organizational context for brand consistency:*
- Company profile: `/rules/publisher/publisher-profile.md`

## Progress
- [x] Task completed (YYYY-MM-DD)
- [ ] Task pending

## Next Steps
<Updated as work progresses>
```

**Note on Rules Sections:**
- List only the rules that apply to **this specific project**
- Reference rules from `/rules/` directories
- Leave empty if no rules have been extracted yet
- Update as new rules are extracted or identified

## Key Patterns for Claude

### When User Says "Add to Project"

1. Determine if source or target
2. Determine if web content or local file
3. **If web content:**
   - Ingest to `/sources/` using Kurt CLI
   - Update project.md to reference it
4. **If local file:**
   - Copy to `projects/name/sources/`
   - Update project.md to reference it

### Detecting Missing Content

When resuming a project:
- **No sources?** → Warn: "No ground truth found. Do you have source material to add?"
- **No targets?** → Warn: "No target content identified. What do you want to create/update?"

### Project.md is the Map, Not the Storage

- project.md **references** content locations
- Content lives in `/sources/` (org-wide) or `projects/name/sources/` (project-specific)
- Don't duplicate content; reference it

## Rules Extraction System

Kurt includes a comprehensive rules extraction system that learns from existing content to create reusable guidelines for content creation.

### What Are Rules?

Rules are extracted patterns from existing content that guide consistent content creation:
- **Style guides** - Voice, tone, sentence structure, word choice
- **Structure templates** - Document organization, section flow, formatting
- **Personas** - Audience targeting patterns and communication preferences
- **Publisher profile** - Organizational context, messaging, brand positioning

### How Rules Are Created

Rules are **extracted FROM content** using AI analysis, not manually written:

```bash
# Extract style patterns from documentation
invoke style-extraction-skill with documents: /sources/docs.company.com/guides/*.md

# Extract structure templates from tutorials
invoke structure-extraction-skill with documents: /sources/docs.company.com/tutorials/*.md

# Extract audience personas from blog posts
invoke persona-extraction-skill with documents: /sources/blog.company.com/*.md

# Extract company profile from website
invoke publisher-profile-extraction-skill with sources: https://company.com/about https://company.com/products
```

### Extraction Modes

**Incremental (Default - Recommended):**
- Analyzes documents and compares with existing rules
- Creates new rule files only if distinct patterns found
- Keeps existing rules untouched
- Safe, additive approach

**Overwrite (Nuclear Option):**
- Deletes all existing rules in category
- Performs fresh analysis
- Creates completely new rule library
- Use when rules are outdated or incorrect

### Rule Matching for Content Work

When working on target content, Kurt automatically:

1. **Inspects target** - Determines content type, purpose, audience, tone
2. **Searches rules** - Looks for matching style/structure/persona in `/rules/`
3. **Flags missing rules** - Warns if no appropriate rules exist
4. **Recommends action** - Extract from similar content OR ask user for examples

**Example workflow:**
```
User: "Update the getting started tutorial"

Kurt checks:
✓ Found: rules/structure/quickstart-tutorial.md
✓ Found: rules/personas/technical-implementer.md
✗ Missing: Tutorial-specific style guide

Kurt recommends:
"Extract style from existing tutorials? Or use general technical documentation style?"
```

### Auto-Naming

Extracted rules get descriptive filenames automatically:
- **Style**: `technical-documentation.md`, `conversational-blog.md`
- **Structure**: `quickstart-tutorial.md`, `api-reference.md`
- **Personas**: `technical-implementer.md`, `enterprise-decision-maker.md`
- **Publisher**: `publisher-profile.md` (single file)

### Quality Requirements

For reliable extraction:
- **Minimum 3-5 documents** per extraction
- **Consistent patterns** in analyzed content
- **Same content type** for focused results

## Skills That Work with Projects

### Content Ingestion

- **ingest-content-skill** - Map/fetch web content to `/sources/`
- **document-management-skill** - List, query, manage documents
- **document-indexing-skill** - Extract metadata with AI
- **import-content-skill** - Import existing markdown files, fix ERROR records

### Project Management

- **project-management-skill** - Add sources/targets, rule matching, detect gaps, update project.md

### Rules Extraction

- **style-extraction-skill** - Extract writing voice/tone patterns from content
- **structure-extraction-skill** - Extract document format templates from content
- **persona-extraction-skill** - Extract audience targeting profiles from content
- **publisher-profile-extraction-skill** - Extract organizational context from company web pages/docs

## Auto-Import Workflow

Kurt includes an automatic import system that seamlessly integrates WebFetch content into the database.

### How It Works

When Claude writes markdown files to `/sources/` or `projects/*/sources/`, a PostToolUse hook automatically:

1. **Detects the write** - Triggers on any .md file in sources directories
2. **Maps path to URL** - Converts file path to original URL
3. **Finds ERROR record** - Searches Kurt DB for failed fetch record
4. **Updates database** - Changes status from ERROR to FETCHED
5. **Links content** - Sets content_path and calculates content_hash
6. **Extracts metadata** - Runs `kurt index` to extract topics, content type
7. **Confirms** - Shows brief success message

### Configuration

**Hook location:** `.claude/settings.json`
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{
          "type": "command",
          "command": "bash .claude/scripts/auto-import-source.sh"
        }]
      }
    ]
  }
}
```

**Script:** `.claude/scripts/auto-import-source.sh`
**Helper:** `.claude/scripts/import_markdown.py`
**Logs:** `.claude/logs/auto-import.log`

### When WebFetch is Used

If `kurt ingest fetch` fails (anti-bot protection), Claude automatically:

1. Falls back to WebFetch to retrieve content
2. Saves markdown file to `/sources/`
3. Auto-import hook triggers
4. File gets properly indexed in Kurt database
5. Content becomes queryable via Kurt commands

This happens transparently - no manual intervention needed.

### Manual Import (Fallback)

If auto-import fails or for bulk operations, use **import-content-skill**:

```bash
# Fix single ERROR record
python .claude/scripts/import_markdown.py \
  --document-id <doc-id> \
  --file-path <file-path>

# Extract metadata
kurt index <doc-id>

# Verify
kurt document get <doc-id>
```

### Troubleshooting

**Check auto-import logs:**
```bash
cat .claude/logs/auto-import.log
```

**Common issues:**

- **No confirmation message** - Check logs, file might not match ERROR record
- **Import failed** - Database locked or Kurt not installed
- **Metadata missing** - Run `kurt index <doc-id>` manually
- **No ERROR record** - File is new, not from failed fetch (this is OK)

### Benefits

- ✅ Transparent fallback from `kurt ingest` to WebFetch
- ✅ Automatic database integration
- ✅ No manual import steps needed
- ✅ Files are queryable and indexed
- ✅ Works for both org-wide and project-specific sources

## Tagging Strategy (Future)

When Kurt adds database support for projects, we'll use:

```sql
-- Projects table
CREATE TABLE projects (id, name, goal, intent_category, ...);

-- Many-to-many relationship
CREATE TABLE project_documents (
  project_id,
  document_id,
  role  -- 'source' | 'target'
);
```

For now, project.md is the source of truth. We'll validate file-based workflow before adding database integration.

## Next Steps

As the system evolves:
1. ✅ Project management with sources/targets (current)
2. ⏳ Style extraction and validation
3. ⏳ Structure templates and patterns
4. ⏳ Content generation using all components
5. ⏳ Database integration for project metadata
