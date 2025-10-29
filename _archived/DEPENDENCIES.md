# Kurt Commands & Skills Dependency Map

This document maps all dependencies and references between commands, skills, and other system components.

**Last Updated:** 2025-10-28

---

## Quick Reference

**Commands:** 2
- `/create-project`
- `/resume-project`

**Skills:** 9 (active)
- cms-interaction-skill
- content-writing-skill
- document-indexing-skill
- document-management-skill
- import-content-skill
- ingest-content-skill
- project-management-skill
- research-skill
- writing-rules-skill

**Deprecated:** 1
- ~~onboard-user-skill~~ (archived - functionality covered by `/create-project`)

---

## Issues Found

### ✅ All Issues Resolved

1. **document-indexing-skill** → Fixed `content-ingestion-skill` → `ingest-content-skill` ✅

2. **onboard-user-skill** → Deprecated and moved to `_archived/` ✅
   - Reason: Functionality fully covered by `/create-project` command
   - Had outdated references to old extraction skill names
   - Not referenced or used anywhere in codebase
   - Topic clustering feature preserved for potential future use

---

## Command Dependencies

### `/create-project`

**Purpose:** Create a new Kurt project with goals and structure

**Dependencies:**
- **Skills Called:**
  - `writing-rules-skill` (multiple operations: publisher, style, structure, persona)
  - `content-writing-skill` (outline, draft)
  - `ingest-content-skill` (for fetching sources)
  - `import-content-skill` (for importing content)
  - `project-management-skill` (for rule validation)
  - `research-skill` (setup-monitoring for project monitoring)

**Files Referenced:**
- `rules/rules-config.yaml` - Rule type registry
- `projects/<name>/project.md` - Project configuration
- `projects/<name>/monitoring-config.yaml` - Monitoring config

**Workflow:**
1. Get project intent and name from user
2. Create project directory structure
3. Offer to ingest company content (→ ingest-content-skill)
4. Extract publisher rules (→ writing-rules-skill publisher)
5. Extract style rules (→ writing-rules-skill style)
6. Optionally extract custom rule types
7. Set up project monitoring (→ research-skill setup-monitoring)
8. Create initial content (→ content-writing-skill)

---

### `/resume-project`

**Purpose:** Resume work on an existing Kurt project

**Dependencies:**
- **Skills Called:**
  - `writing-rules-skill` (for missing rules)
  - `content-writing-skill` (for target content)
  - `ingest-content-skill` (if sources missing)
  - `import-content-skill` (if not indexed)
  - `document-indexing-skill` (if not indexed)
  - `project-management-skill` (for rule checking)

**Files Referenced:**
- `projects/<name>/project.md` - Project configuration
- `rules/rules-config.yaml` - Rule type registry
- `rules/*/*.md` - Extracted rules

**Workflow:**
1. Load project context from project.md
2. Check sources status
3. Check rules status (→ project-management-skill)
4. Recommend missing extractions (→ writing-rules-skill)
5. Recommend content work (→ content-writing-skill)

---

## Skill Dependencies

### cms-interaction-skill

**Purpose:** Complete CMS integration (Sanity, Contentful, WordPress)

**Dependencies:**
- **Configuration:** `.kurt/cms-config.json`
- **Commands:** `kurt cms` (onboard, search, fetch, import, publish)
- **Skills Called:** None (leaf skill)

**Subskills:**
- `subskills/onboard.md` - Interactive CMS setup
- `subskills/search.md` - Search CMS content
- `subskills/fetch.md` - Download content as markdown
- `subskills/import.md` - Import to Kurt database
- `subskills/publish.md` - Publish drafts to CMS

**Called By:**
- None directly (user invokes via skill command)

---

### content-writing-skill

**Purpose:** Create outlines, drafts, and edited content with lineage tracking

**Dependencies:**
- **Configuration:** `rules/rules-config.yaml`
- **Rules Files:**
  - `rules/style/*.md`
  - `rules/structure/*.md`
  - `rules/personas/*.md`
  - `rules/publisher/*.md`
  - Custom rule directories (dynamically discovered)
- **Skills Called:**
  - `writing-rules-skill` (indirectly - checks for rules)
  - `document-management-skill` (for source content)

**Subskills:**
- `subskills/outline-content.md` - Create content outline
- `subskills/draft-content.md` - Generate draft from outline
- `subskills/edit-content.md` - Edit existing content

**Called By:**
- `/create-project` - For initial content creation
- `/resume-project` - For target content work
- `project-management-skill` - Recommends when rules ready

**Output:**
- `projects/<name>/assets/<asset>-outline.md`
- `projects/<name>/assets/<asset>-draft.md`

---

### document-indexing-skill

**Purpose:** Extract structured metadata from documents using AI

**Dependencies:**
- **Kurt Database:** `.kurt/kurt.sqlite`
- **Skills Called:**
  - ❌ `content-ingestion-skill` (BROKEN - should be `ingest-content-skill`)

**Called By:**
- `/resume-project` - If sources not indexed
- User directly for metadata extraction

**Output:**
- Metadata in Kurt database

---

### document-management-skill

**Purpose:** Query and manage documents in Kurt database

**Dependencies:**
- **Kurt Database:** `.kurt/kurt.sqlite`
- **Skills Called:** None (leaf skill)

**Called By:**
- `content-writing-skill` - For source content retrieval
- User directly for document queries

---

### import-content-skill

**Purpose:** Import markdown files into Kurt database

**Dependencies:**
- **Kurt Database:** `.kurt/kurt.sqlite`
- **Script:** `.claude/scripts/import_markdown.py`
- **Skills Called:** None (leaf skill)

**Called By:**
- `/create-project` - After ingesting content
- `/resume-project` - If sources fetched but not imported

---

### ingest-content-skill

**Purpose:** Ingest web content into Kurt (sitemap mapping + fetching)

**Dependencies:**
- **Scripts:**
  - `.claude/scripts/map_sitemap.py`
  - `.claude/scripts/advanced_fetch_custom_extraction.py`
- **Kurt Database:** `.kurt/kurt.sqlite`
- **Skills Called:** None (leaf skill)

**Called By:**
- `/create-project` - For company content ingestion
- `/resume-project` - If sources missing
- `document-indexing-skill` - ❌ Referenced as wrong name

**Output:**
- `sources/<domain>/**/*.md` - Fetched content

---

### ~~onboard-user-skill~~ (DEPRECATED)

**Status:** Archived in `.claude/skills/_archived/onboard-user-skill/`

**Reason for Deprecation:**
- Functionality fully covered by `/create-project` command
- Had outdated references to old extraction skill names
- Not referenced or used anywhere in active codebase
- Overlapping workflow with newer, better-maintained `/create-project`

**Unique Feature Preserved:**
- Topic clustering functionality (`kurt cluster compute`) preserved in archived version for potential future use

**Replacement:** Use `/create-project` command instead

---

### project-management-skill

**Purpose:** Manage Kurt projects - track sources, targets, rules

**Dependencies:**
- **Configuration:** `rules/rules-config.yaml`
- **Rules Files:** `rules/*/*.md`
- **Skills Called:**
  - `writing-rules-skill` - For missing rules
  - `content-writing-skill` - When rules ready

**Called By:**
- `/create-project` - For rule validation
- `/resume-project` - For rule checking

**Functions:**
- Check which rules exist
- Recommend missing rule extractions
- Validate rule coverage for targets
- Recommend content creation when ready

---

### research-skill

**Purpose:** Research API integration (Perplexity) + project monitoring

**Dependencies:**
- **Configuration:**
  - `.kurt/research-config.json` - Perplexity API key
  - `projects/<name>/monitoring-config.yaml` - Per-project monitoring
- **Kurt Commands:** `kurt research` (search, monitor)
- **Skills Called:** None (leaf skill)

**Workflows:**
1. **Search** - Query Perplexity API and save research
2. **Monitor** - Track Reddit, HN, RSS for project topics
3. **Setup Monitoring** - Interactive config creation

**Called By:**
- `/create-project` - Setup monitoring workflow
- User directly for research

**Output:**
- `sources/research/<date>-<topic>.md` - Research findings
- `projects/<name>/research/signals/<date>-signals.json` - Monitoring signals

---

### writing-rules-skill

**Purpose:** Extract and manage writing rules (style, structure, persona, publisher, custom)

**Dependencies:**
- **Configuration:** `rules/rules-config.yaml` - Rule type registry
- **Source Content:** `sources/**/*.md` (must be fetched + indexed)
- **Kurt Database:** `.kurt/kurt.sqlite`
- **Skills Called:**
  - `document-management-skill` - For source content
  - Self-referential (management operations reference extraction operations)

**Subskills:**

**Extraction:**
- `subskills/extract-style.md` - Extract writing style
- `subskills/extract-structure.md` - Extract document structure
- `subskills/extract-persona.md` - Extract target personas
- `subskills/extract-publisher-profile.md` - Extract company profile

**Management:**
- `subskills/manage-list.md` - List rule types
- `subskills/manage-show.md` - Show rule type details
- `subskills/manage-add.md` - Add custom rule type
- `subskills/manage-validate.md` - Validate registry
- `subskills/manage-generate-subskill.md` - Generate extraction subskill
- `subskills/manage-onboard.md` - Onboarding wizard

**Called By:**
- `/create-project` - Extract foundation rules
- `/resume-project` - Extract missing rules
- `content-writing-skill` - Checks for rules
- `project-management-skill` - Rule validation
- ❌ `onboard-user-skill` - Via old skill names (broken)

**Output:**
- `rules/style/*.md`
- `rules/structure/*.md`
- `rules/personas/*.md`
- `rules/publisher/publisher-profile.md`
- Custom rule directories (if configured)

---

## Dependency Graph

### High-Level Flow

```
User Commands
    ↓
/create-project OR /resume-project
    ↓
project-management-skill (orchestrates)
    ↓
    ├─→ ingest-content-skill (fetch sources)
    ├─→ import-content-skill (import to DB)
    ├─→ document-indexing-skill (extract metadata)
    ├─→ writing-rules-skill (extract rules)
    │       ↓
    │   [uses document-management-skill]
    ├─→ research-skill (setup monitoring)
    └─→ content-writing-skill (create content)
            ↓
        [uses rules from writing-rules-skill]
        [uses sources from document-management-skill]
```

### Leaf Skills (No Dependencies on Other Skills)

- **cms-interaction-skill** - CMS operations only
- **document-management-skill** - Database queries only
- **import-content-skill** - Database writes only
- **ingest-content-skill** - Web fetching only
- **research-skill** - API calls only

### Orchestrator Skills (Call Other Skills)

- **project-management-skill** - Primary orchestrator
- **content-writing-skill** - Calls document-management-skill
- **writing-rules-skill** - Calls document-management-skill

### Command-Level Orchestrators

- **/create-project** - Highest level, calls multiple skills
- **/resume-project** - Highest level, calls multiple skills

---

## Configuration File Dependencies

### `.kurt/cms-config.json`
**Used By:**
- cms-interaction-skill

### `.kurt/research-config.json`
**Used By:**
- research-skill

### `.kurt/monitoring-config-template.yaml`
**Used By:**
- research-skill (template for project configs)

### `rules/rules-config.yaml`
**Used By:**
- writing-rules-skill
- content-writing-skill
- project-management-skill
- /create-project
- /resume-project

### `projects/<name>/monitoring-config.yaml`
**Used By:**
- research-skill (project-specific monitoring)

### `projects/<name>/project.md`
**Used By:**
- /create-project
- /resume-project
- All skills (context)

---

## System Health

### ✅ All Systems Green

1. **All broken references fixed** ✅
   - document-indexing-skill uses correct skill name
   - No references to old extraction skill names

2. **Deprecated skills properly archived** ✅
   - onboard-user-skill moved to `_archived/`
   - Functionality covered by `/create-project`

3. **All paths use relative references** ✅
   - Changed from `/rules/` to `rules/`
   - All configuration paths verified

4. **Dependency graph is clean** ✅
   - No circular dependencies
   - Clear orchestration hierarchy
   - All referenced skills exist

---

## Skill Invocation Patterns

### How to Call Skills

Skills are invoked using the `Skill` function in Claude Code:

```
Skill(skill-name)
```

### Common Patterns

**Check before calling:**
```bash
if [ -f "rules/publisher/publisher-profile.md" ]; then
  echo "Publisher profile already exists"
else
  writing-rules-skill publisher --auto-discover
fi
```

**Chain operations:**
```bash
# 1. Fetch content
ingest-content-skill map https://example.com/sitemap.xml

# 2. Import to database
import-content-skill --source-dir sources/example.com/

# 3. Extract rules
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type corporate --auto-discover

# 4. Create content
content-writing-skill outline my-project article-name
content-writing-skill draft my-project article-name
```

---

## See Also

- **Configuration Guide:** `CONFIG.md`
- **System Overview:** `KURT.md`
- **User Guide:** `CLAUDE.md`
- **Skill Documentation:** `.claude/skills/*/SKILL.md`
