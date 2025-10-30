# Kurt: Document Intelligence System

## Overview

Kurt is a document intelligence CLI that helps teams manage, analyze, and create content. It fetches web content, stores it in a local SQLite database with extracted metadata, and provides tools for organizing projects around content creation and updates.

**For workflows and usage examples, see `CLAUDE.md`.**

---

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
- **Rules**: Extracted patterns (style, structure, personas, publisher profile)

---

## File Structure

```
kurt-demo/
├── sources/                        # Organizational knowledge base
│   ├── docs.getdbt.com/           # Fetched web content
│   ├── blog.company.com/
│   └── competitor.com/
├── rules/                          # Extracted rules for content creation
│   ├── rules-config.yaml           # Rule type registry (extensible)
│   ├── style/                      # Writing voice/tone patterns
│   ├── structure/                  # Document format templates
│   ├── personas/                   # Audience targeting profiles
│   ├── publisher/                  # Organizational context
│   └── [custom-types]/             # Optional custom rule types
├── projects/                       # Individual projects
│   └── project-name/
│       ├── project.md             # Project manifest
│       ├── sources/               # Project-specific sources only
│       └── drafts/                # Work in progress
└── .kurt/                          # Kurt database and config
    └── kurt.sqlite
```

### Content Organization Philosophy

**Top-level folders (Shared/Reusable):**
- `/sources/` - All web content ingested by Kurt (organizational knowledge base)
- `rules/` - Extracted patterns from content (style, structure, personas, publisher, custom)

**Project folders (Project-specific):**
- `projects/name/sources/` - One-off files only for this project (PDFs, internal docs)
- `projects/name/drafts/` - Drafts and work-in-progress content

### Why This Separation?

1. **No duplication** - Organizational content lives once in `/sources/`
2. **Reusability** - Multiple projects reference same org content and rules
3. **Clear ownership** - Easy to see what's org-wide vs project-specific
4. **Rule-based consistency** - Extracted rules ensure consistent content creation
5. **Single source of truth** - Registry (`rules-config.yaml`) defines available rule types

---

## project.md Format

Each project has a `project.md` file that serves as the project manifest:

```markdown
# Project Name

## Goal
Brief description of what you want to accomplish

## Intent Category
a) Update positioning
b) Marketing assets
c) Technical docs updates
d) General project
e) Custom

## Sources (Ground Truth)

### From Organizational Knowledge Base
- [x] Page title: `/sources/domain.com/path/page.md` (fetched: YYYY-MM-DD)
- [ ] Another page: https://example.com/page (not fetched)

### Project-Specific Sources
- [x] Internal doc: `sources/filename.pdf` (added: YYYY-MM-DD)

## Targets (Content to Update/Create)

### Existing Content to Update
- [ ] Tutorial: `/sources/docs.company.com/tutorial.md`

### New Content to Create
- [ ] New tutorial: `drafts/new-tutorial.md` (planned)

## Rules Configuration

### Style Guidelines
- Technical documentation style: `rules/style/technical-documentation.md`

### Structure Templates
- Tutorial structure: `rules/structure/quickstart-tutorial.md`

### Target Personas
- Developer persona: `rules/personas/technical-implementer.md`

### Publisher Profile
- Company profile: `rules/publisher/publisher-profile.md`

[Additional rule sections if custom types are configured]

## Progress
- [x] Task completed (YYYY-MM-DD)
- [ ] Task pending

## Next Steps
<Updated as work progresses>
```

**Note on Rules Sections:**
- List only the rules that apply to this specific project
- Reference rules from `rules/` directories
- Sections are dynamic based on enabled rule types in registry
- Leave empty if no rules have been extracted yet

---

## Rules System Architecture

Kurt includes an extensible rules system that learns from existing content to create reusable guidelines.

### What Are Rules?

Rules are extracted patterns from existing content that guide consistent content creation.

**Built-in rule types** (always available):
- **Style Guidelines** - Voice, tone, sentence structure, word choice
- **Structure Templates** - Document organization, section flow, formatting
- **Target Personas** - Audience roles, pain points, communication preferences
- **Publisher Profile** - Company identity, messaging, brand positioning

**Custom rule types** (optional, team-configurable):
- Teams can extend with custom types: verticals, use-cases, channels, etc.
- All types defined in `rules/rules-config.yaml` (the registry)

### Registry: Single Source of Truth

All rule types are defined in **`rules/rules-config.yaml`** - the central registry.

This file defines:
- Which rule types are enabled
- What each type extracts and governs
- How extraction works (discovery modes, sample size)
- Directory locations for each type

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

### Quality Requirements

For reliable extraction:
- **Minimum 3-5 documents** per extraction
- **Consistent patterns** in analyzed content
- **Same content type** for focused results

---

## Skills Ecosystem

Kurt uses Claude Code skills for different operations:

### Content Ingestion
- **ingest-content-skill** - Map/fetch web content to `/sources/`
- **document-management-skill** - List, query, manage documents
- **document-indexing-skill** - Extract metadata with AI
- **import-content-skill** - Import existing markdown files, fix ERROR records

### Project Management
- **project-management-skill** - Orchestrates project workflows
  - Subskills: create-project, resume-project, check-foundation, gather-sources, extract-rules

### Rules Extraction
- **writing-rules-skill** - Extract and manage all rule types
  - Extraction: style, structure, persona, publisher, custom types
  - Management: list, show, add, validate, generate-subskill, onboard

### Content Creation
- **content-writing-skill** - Create outlines, drafts, edited content with lineage tracking
  - Subskills: outline (source mapping), draft (inline attribution), edit (session history), feedback (persona-based review)
  - Tracks: sources, reasoning, rule compliance, update patterns, edit history

### CMS Integration
- **cms-interaction-skill** - Work with CMS platforms (Sanity, Contentful, WordPress)
  - Subskills: onboard, search, fetch, import, publish

### Research Integration
- **research-skill** - AI-powered research via Perplexity
  - Operations: daily digest, topic discovery, direct research, browse history, kickoff projects

---

## Auto-Import Workflow

Kurt includes an automatic import system that seamlessly integrates WebFetch content into the database.

### How It Works

When Claude writes markdown files to `/sources/` or `projects/*/sources/`, a PostToolUse hook automatically:

1. **Detects the write** - Triggers on any .md file in sources directories
2. **Maps path to URL** - Converts file path to original URL
3. **Finds ERROR record** - Searches Kurt DB for failed fetch record
4. **Updates database** - Changes status from ERROR to FETCHED
5. **Links content** - Sets content_path and calculates content_hash
6. **Extracts metadata** - Runs `kurt content index` to extract topics, content type
7. **Confirms** - Shows brief success message

### Configuration

**Hook location:** `.claude/settings.json`
**Script:** `.claude/scripts/auto-import-source.sh`
**Helper:** `.claude/scripts/import_markdown.py`
**Logs:** `.claude/logs/auto-import.log`

### When WebFetch is Used

If `kurt content fetch` fails (anti-bot protection), Claude automatically:
1. Falls back to WebFetch to retrieve content
2. Saves markdown file to `/sources/`
3. Auto-import hook triggers
4. File gets properly indexed in Kurt database
5. Content becomes queryable via Kurt commands

This happens transparently - no manual intervention needed.

---

## Data Model Concepts

### Sources vs Targets

**Sources** are ground truth content you're working FROM:
- Reference materials
- Competitive analysis
- Internal specs
- Research findings
- Existing documentation

**Targets** are content you're working ON:
- Documentation to update
- New content to create
- Blog posts to write
- Tutorials to refresh

### Content Processing Pipeline

```
URL → Fetch → Index → Extract Rules → Create Content
```

1. **Fetch**: Download content to `/sources/` as markdown
2. **Index**: Extract metadata (title, author, date, topics, entities)
3. **Extract Rules**: Learn patterns from indexed content
4. **Create Content**: Apply rules to targets with lineage tracking

### Lineage Tracking

Content created with Kurt tracks:
- **Sources** - Which documents informed which sections
- **Reasoning** - Why content was written this way
- **Rules Applied** - Style, structure, persona, publisher compliance
- **Update Patterns** - Project-specific transformation patterns
- **Edit History** - All changes with session IDs, instructions, timestamps

Tracked in:
- **YAML frontmatter** - High-level, queryable metadata
- **Inline HTML comments** - Granular, contextual attribution

---

## Future Enhancements

### Tagging Strategy (Planned)

When Kurt adds database support for projects:

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

For now, project.md is the source of truth.

---

## Key Architectural Principles

1. **Separation of concerns** - Commands invoke → Skills orchestrate → Domain tools execute
2. **Single source of truth** - Registry for rules, /sources/ for content, project.md for projects
3. **Reusability** - Org-wide content and rules shared across projects
4. **Extensibility** - Custom rule types via registry
5. **Lineage tracking** - Full traceability from sources to drafts
6. **Batch operations** - Always prefer batched commands over loops
7. **Progressive disclosure** - Optional steps, users can skip and return

---

For usage examples, workflows, and integration guides, see **`CLAUDE.md`**.
