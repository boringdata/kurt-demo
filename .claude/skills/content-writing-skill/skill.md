---
name: content-writing
description: Create outlines, drafts, and edited content with comprehensive lineage tracking (project)
---

# Content Writing Skill

**Purpose:** Unified content creation workflow with comprehensive lineage tracking
**Subskills:** outline, draft, edit
**Lineage:** Tracks sources, reasoning, rule compliance, and edit history through YAML frontmatter + inline HTML comments

---

## Usage

```bash
# Create outline
content-writing-skill outline <project-name> <asset-name> [--interactive]

# Generate draft
content-writing-skill draft <project-name> <asset-name> [--section "Section Name"]

# Edit content
content-writing-skill edit <file-path> --instructions "Edit instructions" [--section "Section Name"]
```

---

## Routing Logic

This skill routes to the appropriate subskill based on the first argument:

- `outline` → subskills/outline-content.md
- `draft` → subskills/draft-content.md
- `edit` → subskills/edit-content.md

---

## Step 1: Parse Arguments

Extract subskill and arguments: $ARGUMENTS

**Expected format:**
- First argument: `outline`, `draft`, or `edit`
- Remaining arguments: passed to subskill

**If no arguments or invalid subskill:**
Show usage help and available subskills.

---

## Step 2: Load Shared Context

### Project Context (for outline/draft)
If subskill is `outline` or `draft`:
- Project name from arguments
- Locate project directory: `/projects/<project-name>/`
- Read project.md or project-brief.md for context
- Check for task-breakdown.md

### Rule Files Context
Load rule file paths from project directory:
- Publisher profile: `/rules/publisher/publisher-profile.md`
- Available style guides: `/rules/style/`
- Available structure templates: `/rules/structure/`
- Available personas: `/rules/personas/`

### Validation
- Confirm project directory exists
- Confirm referenced rule files exist
- Log any missing files as warnings

---

## Step 3: Route to Subskill

**For `outline`:**
Invoke subskills/outline-content.md with arguments:
- Project name
- Asset name
- Optional flags (--interactive, --template-override)
- Loaded context (project, rules)

**For `draft`:**
Invoke subskills/draft-content.md with arguments:
- Project name
- Asset name
- Optional flags (--section)
- Loaded context (project, rules, outline path)

**For `edit`:**
Invoke subskills/edit-content.md with arguments:
- File path to edit
- Edit instructions (--instructions flag)
- Optional flags (--section, --mode, --focus)
- Loaded context (project if derivable, rules)

---

## Step 4: Context Handoff

Pass the following to subskills:

**Shared Context:**
```
PROJECT_NAME: <name>
PROJECT_PATH: /projects/<name>/
PROJECT_BRIEF: /projects/<name>/project.md
RULES_PUBLISHER: /rules/publisher/publisher-profile.md
RULES_STYLE_DIR: /rules/style/
RULES_STRUCTURE_DIR: /rules/structure/
RULES_PERSONAS_DIR: /rules/personas/
```

**Asset-Specific Context (outline/draft):**
```
ASSET_NAME: <name>
ASSET_OUTPUT_DIR: /projects/<name>/assets/
OUTLINE_PATH: /projects/<name>/assets/<name>-outline.md (if exists)
DRAFT_PATH: /projects/<name>/assets/<name>-draft.md (if exists)
```

---

## Step 5: Lineage Tracking Standards

All subskills must follow these lineage tracking conventions:

### YAML Frontmatter (High-Level)
- Track rule files applied
- Track source documents used
- Track update patterns applied (project-specific)
- Track quality metrics and compliance
- Track edit sessions and version history

### Inline HTML Comments (Granular)
- Section-level source attribution
- Reasoning for additions/changes
- Update pattern application notes
- Rule compliance notes

### Metadata Templates
Use templates from `/skills/content-writing-skill/templates/`:
- `outline-metadata-schema.yaml`
- `draft-metadata-schema.yaml`
- `inline-comment-patterns.md`

---

## Error Handling

**If project not found:**
```
Error: Project '<name>' not found in /projects/

Available projects:
  - project-1
  - project-2

Create a new project with: /create-project "<name>"
```

**If rule files missing:**
```
Warning: Some rule files not found:
  - /rules/personas/data-engineer.md

Continue anyway? (Y/n)
```

**If subskill invalid:**
```
Error: Unknown subskill '<name>'

Available subskills:
  - outline  : Create detailed content outline
  - draft    : Generate content draft from outline
  - edit     : Interactive content editing

Usage: content-writing-skill <subskill> [arguments]
```

---

## Success Indicators

✅ **Skill invoked successfully** when:
- Subskill identified and routed correctly
- Shared context loaded and validated
- Subskill execution completes
- Output includes proper lineage metadata

✅ **Lineage tracking complete** when:
- YAML frontmatter includes all required fields
- Section-level inline comments present
- Source documents referenced
- Rule compliance documented
- Edit history tracked (for edits)

---

## Integration with Existing Workflow

This skill replaces the following slash commands:
- `/outline-content` → `content-writing-skill outline`
- `/write-content` → `content-writing-skill draft`
- `/edit-content` → `content-writing-skill edit`

**Advantages over commands:**
- Unified entry point with consistent context loading
- Enhanced lineage tracking built-in
- Reusable metadata templates
- Better error handling and validation
- Skill can be invoked by other skills

---

## Next Steps After Invocation

After successful subskill execution, suggest next steps:

**After outline:**
```
✅ Outline created: /projects/<name>/assets/<name>-outline.md

Next steps:
  1. Review outline structure and section flow
  2. Generate draft: content-writing-skill draft <project> <asset>
  3. Or edit outline: content-writing-skill edit <outline-path> --instructions "..."
```

**After draft:**
```
✅ Draft created: /projects/<name>/assets/<name>-draft.md
   Word count: X words
   Rule compliance: Y%

Next steps:
  1. Review draft for accuracy and completeness
  2. Edit draft: content-writing-skill edit <draft-path> --instructions "..."
  3. Or check lineage: grep "SECTION:" <draft-path>
```

**After edit:**
```
✅ Edit session complete: <file-path>
   Version: X.Y
   Sections modified: [list]
   Session ID: <id>

Next steps:
  1. Review changes in file
  2. Further edits: content-writing-skill edit <file-path> --instructions "..."
  3. Check edit history: head -100 <file-path> | grep "edit_sessions:"
```

---

*This is the main entry point for the content-writing-skill. It provides unified routing to outline, draft, and edit subskills with comprehensive lineage tracking capabilities.*
