---
name: writing-rules
description: Extract style, structure, persona, and publisher rules from content (project)
---

# Writing Rules Skill

**Purpose:** Unified rule extraction workflow for creating reusable writing guidelines
**Subskills:** style, structure, persona, publisher
**Output:** Rule files in `/rules/` directories for use in content creation

---

## Usage

```bash
# Extract style patterns
writing-rules-skill style --type corporate --auto-discover
writing-rules-skill style --type technical-docs --auto-discover
writing-rules-skill style with documents: <file-paths>

# Extract structure templates
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill structure --type landing-page --auto-discover
writing-rules-skill structure with documents: <file-paths>

# Extract audience personas
writing-rules-skill persona --audience-type all --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover
writing-rules-skill persona with documents: <file-paths>

# Extract publisher profile
writing-rules-skill publisher --auto-discover
writing-rules-skill publisher with sources: <URLs-and-file-paths>
```

---

## Routing Logic

This skill routes to the appropriate subskill based on the first argument:

- `style` → subskills/extract-style.md
- `structure` → subskills/extract-structure.md
- `persona` → subskills/extract-persona.md
- `publisher` → subskills/extract-publisher-profile.md

---

## Step 1: Parse Arguments

Extract subskill and arguments: $ARGUMENTS

**Expected format:**
- First argument: `style`, `structure`, `persona`, or `publisher`
- Remaining arguments: passed to subskill

**If no arguments or invalid subskill:**
Show usage help and available subskills.

---

## Step 2: Load Shared Context

### Project Context (if applicable)
- Check if we're in a project context
- Locate current project directory (if exists)
- Read project.md for context about sources and targets

### Source Content Status
Check if content is ready for extraction:
- Are sources fetched? (files in `/sources/`)
- Are sources indexed? (metadata extracted via `kurt index`)

### Existing Rules
Load existing rule file paths to understand what's already extracted:
- Publisher profile: `/rules/publisher/publisher-profile.md`
- Available style guides: `/rules/style/`
- Available structure templates: `/rules/structure/`
- Available personas: `/rules/personas/`

### Validation
- Log which rules already exist
- Warn if sources not fetched/indexed (required for extraction)
- Note any gaps in rule coverage

---

## Step 3: Route to Subskill

**For `style`:**
Invoke subskills/extract-style.md with arguments:
- Type flag (--type corporate, technical-docs, blog, etc.)
- Auto-discovery flag (--auto-discover)
- Manual document selection (with documents: <paths>)
- Optional overwrite flag (--overwrite)
- Loaded context (project, sources, existing styles)

**For `structure`:**
Invoke subskills/extract-structure.md with arguments:
- Type flag (--type tutorial, landing-page, api-reference, etc.)
- Auto-discovery flag (--auto-discover)
- Manual document selection (with documents: <paths>)
- Optional overwrite flag (--overwrite)
- Loaded context (project, sources, existing structures)

**For `persona`:**
Invoke subskills/extract-persona.md with arguments:
- Audience type flag (--audience-type all, technical, business, customer)
- Auto-discovery flag (--auto-discover)
- Manual document selection (with documents: <paths>)
- Optional overwrite flag (--overwrite)
- Loaded context (project, sources, existing personas)

**For `publisher`:**
Invoke subskills/extract-publisher-profile.md with arguments:
- Auto-discovery flag (--auto-discover)
- Manual source selection (with sources: <URLs-and-paths>)
- Optional overwrite flag (--overwrite)
- Loaded context (project, sources, existing profile)

---

## Step 4: Context Handoff

Pass the following to subskills:

**Shared Context:**
```
PROJECT_NAME: <name> (if in project context)
PROJECT_PATH: /projects/<name>/ (if applicable)
PROJECT_BRIEF: /projects/<name>/project.md (if applicable)
RULES_PUBLISHER: /rules/publisher/publisher-profile.md (if exists)
RULES_STYLE_DIR: /rules/style/
RULES_STRUCTURE_DIR: /rules/structure/
RULES_PERSONAS_DIR: /rules/personas/
SOURCES_STATUS: fetched|not_fetched|indexed|not_indexed
EXISTING_RULES: <list of existing rule files>
```

**Content Paths:**
```
SOURCES_PATH: /sources/ (organizational knowledge base)
PROJECT_SOURCES_PATH: /projects/<name>/sources/ (if applicable)
```

---

## Step 5: Prerequisites Validation

All rule extraction requires content to be **fetched + indexed**:

### Check Fetch Status
```bash
# Verify sources are downloaded to /sources/
kurt document list --url-prefix <url> --status FETCHED
```

### Check Index Status
```bash
# Verify metadata has been extracted
kurt document get <url>
# Should show: title, topics, entities, indexed_at
```

### If Not Ready
```
⚠️ Content must be fetched + indexed before extraction

Sources not fetched:
  - https://example.com/page1
  - https://example.com/page2

Run: kurt ingest fetch --url-prefix <url>

Sources fetched but not indexed:
  - /sources/example.com/page3.md
  - /sources/example.com/page4.md

Run: kurt index --url-prefix <url>

Once complete, retry extraction.
```

---

## Error Handling

**If subskill invalid:**
```
Error: Unknown subskill '<name>'

Available subskills:
  - style      : Extract writing voice, tone, and style patterns
  - structure  : Extract document organization and format templates
  - persona    : Extract audience targeting patterns
  - publisher  : Extract organizational context and brand profile

Usage: writing-rules-skill <subskill> [arguments]

Examples:
  writing-rules-skill style --type corporate --auto-discover
  writing-rules-skill structure --type tutorial --auto-discover
  writing-rules-skill persona --audience-type technical --auto-discover
  writing-rules-skill publisher --auto-discover
```

**If sources not ready:**
```
Error: Sources not ready for extraction

Requirements:
  ✓ Content must be fetched (files in /sources/)
  ✓ Content must be indexed (metadata extracted)

Current status: <fetch status> / <index status>

Next steps:
  1. Fetch content: kurt ingest fetch --url-prefix <url>
  2. Index content: kurt index --url-prefix <url>
  3. Retry extraction: writing-rules-skill <subskill> ...
```

**If project context missing (when needed):**
```
Warning: No project context found

Rule extraction will create global rules in /rules/.
These will be available to all projects.

Continue? (Y/n)
```

---

## Success Indicators

✅ **Skill invoked successfully** when:
- Subskill identified and routed correctly
- Prerequisites validated (content fetched + indexed)
- Shared context loaded and validated
- Subskill execution completes
- Output includes rule files in `/rules/` directories

✅ **Rule extraction complete** when:
- New rule file(s) created in appropriate `/rules/` subdirectory
- Rule files include proper YAML frontmatter
- Source documents tracked in rule metadata
- Extraction date and method documented
- Rule characteristics clearly defined

---

## Integration with Other Skills

This skill is invoked by:
- **project-management-skill**: When validating rule coverage for content work
- **create-project command**: During project setup to extract foundation rules
- **resume-project command**: When gaps in rule coverage are detected

This skill creates rules used by:
- **content-writing-skill**: Applies rules during outline/draft/edit operations
- **project-management-skill**: Validates rule coverage before content work

---

## Next Steps After Invocation

After successful subskill execution, suggest next steps:

**After style extraction:**
```
✅ Style extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> style pattern(s) identified

📝 Style guide(s) created:
   - <filename>.md

Next steps:
  1. Review style guide characteristics
  2. Extract other rule types if needed (structure, persona, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After structure extraction:**
```
✅ Structure extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> structural pattern(s) identified

📝 Structure template(s) created:
   - <filename>.md

Next steps:
  1. Review structure template sections and flow
  2. Extract other rule types if needed (style, persona, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After persona extraction:**
```
✅ Persona extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> distinct persona(s) identified

📝 Persona profile(s) created:
   - <filename>.md

Next steps:
  1. Review persona characteristics and needs
  2. Extract other rule types if needed (style, structure, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After publisher extraction:**
```
✅ Publisher profile extraction complete

📊 Sources analyzed:
   - <count> web pages
   - <count> local documents

📝 Profile action: <Created new|Updated existing> profile
   Location: /rules/publisher/publisher-profile.md

Next steps:
  1. Review organizational identity and messaging
  2. Extract other rule types if needed (style, structure, persona)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

---

## Workflow Examples

### Example 1: Extract Foundation Rules for New Project

```bash
# Step 1: Extract publisher profile (company context)
writing-rules-skill publisher --auto-discover

# Step 2: Extract corporate voice (brand style)
writing-rules-skill style --type corporate --auto-discover

# Step 3: Extract content-specific rules based on targets
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover

# Now ready for content creation with full rule coverage
```

### Example 2: Extract Rules for Specific Content Type

```bash
# Need to create blog posts in new voice
writing-rules-skill style --type blog --auto-discover
writing-rules-skill structure --type blog-post --auto-discover
writing-rules-skill persona --audience-type business --auto-discover
```

### Example 3: Update Existing Rules

```bash
# Company rebrand - update publisher profile
writing-rules-skill publisher --auto-discover --overwrite

# New blog author - extract their voice
writing-rules-skill style --type author --author-name "Jane Smith" --auto-discover
```

---

*This is the main entry point for the writing-rules-skill. It provides unified routing to style, structure, persona, and publisher extraction subskills with comprehensive validation and context loading capabilities.*
