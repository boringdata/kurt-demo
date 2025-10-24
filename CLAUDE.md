# Kurt Demo Project

This is a **Kurt** project - a document intelligence system that helps teams manage, analyze, and create content.

## Quick Links

- **Core Concepts**: See `KURT.md` for project structure, sources vs targets, and file organization
- **Workflows**: See available skills in `.claude/skills/`
- **Commands**: `/create-project` or `/resume-project` to get started

## Project Organization

- `/sources/` - Organizational knowledge base (all web content)
- `/rules/` - Extracted rules for content creation
  - `/rules/style/` - Writing voice/tone patterns
  - `/rules/structure/` - Document format templates
  - `/rules/personas/` - Audience targeting profiles
  - `/rules/publisher/` - Company/brand profile
- `/projects/` - Individual content projects

---

## Content Creation Workflow

When working on content creation or updates for a Kurt project, use the **content-writing-skill** to ensure comprehensive lineage tracking.

### When to Use Content-Writing-Skill

✅ **Use this skill when:**
- Creating outlines for new content
- Generating drafts from outlines
- Editing existing content
- Updating documentation with new information
- Need to track which sources informed which sections
- Want full edit history and reasoning

❌ **Don't use for:**
- Simple one-line edits (use Edit tool directly)
- Exploring or reading content (use Read tool)
- Extracting rules (use extraction skills)

### Standard Content Creation Workflow

**Step 1: Extract Rules (if not done)**
```bash
# Extract style from existing content
invoke style-extraction-skill

# Extract structure templates
invoke structure-extraction-skill

# Extract personas
invoke persona-extraction-skill

# Extract publisher profile
invoke publisher-profile-extraction-skill
```

**Step 2: Create Outline**
```bash
content-writing-skill outline <project-name> <asset-name>
```

**Output:** `/projects/<project-name>/assets/<asset-name>-outline.md`

**Contains:**
- YAML frontmatter with source documents listed
- Section-to-source mapping
- Update patterns (if project-specific)
- Rule files to apply

**Step 3: Generate Draft**
```bash
content-writing-skill draft <project-name> <asset-name>
```

**Output:** `/projects/<project-name>/assets/<asset-name>-draft.md`

**Contains:**
- Enhanced YAML frontmatter with section sources
- Inline HTML comments at sections citing sources
- Update pattern applications documented
- Rule compliance tracked

**Step 4: Edit as Needed**
```bash
content-writing-skill edit projects/<project-name>/assets/<asset-name>-draft.md --instructions "specific edit instructions"
```

**Updates:**
- Adds edit session to YAML history
- Increments version number
- Adds inline edit comments at changes
- Tracks which sections were modified

### Lineage Tracking

**Every piece of content created with this workflow tracks:**

1. **Sources** - Which documents informed which sections
2. **Reasoning** - Why content was written this way
3. **Rules Applied** - Style, structure, persona, publisher compliance
4. **Update Patterns** - Project-specific transformation patterns (if applicable)
5. **Edit History** - All changes with session IDs, instructions, timestamps

**Query lineage:**
```bash
# See section sources
grep "<!-- SECTION:" <draft-file>.md

# Find update patterns applied
grep "UPDATE PATTERN:" <draft-file>.md

# View edit history
head -100 <draft-file>.md | grep "edit_sessions:" -A 20

# Check rule compliance
head -100 <draft-file>.md | grep "rule_compliance:" -A 10
```

### Example: Tutorial Update Project

**Scenario:** Updating 23 tutorials to include new feature instructions

```bash
# 1. Create outline (maps sources to sections, identifies patterns)
content-writing-skill outline tutorial-refresh-fusion bigquery-quickstart

# 2. Review outline - verify source mapping and patterns

# 3. Generate draft (applies patterns, cites sources inline)
content-writing-skill draft tutorial-refresh-fusion bigquery-quickstart

# 4. Review draft for accuracy

# 5. Edit to add missing content
content-writing-skill edit projects/tutorial-refresh-fusion/assets/bigquery-quickstart-draft.md --instructions "Add limitations callout per Type 5 pattern"

# 6. Validate pattern application
grep "UPDATE PATTERN:" projects/tutorial-refresh-fusion/assets/bigquery-quickstart-draft.md

# 7. Check which tutorials use which patterns (across all tutorials)
for pattern in type_{1..7}; do
  echo "=== $pattern ==="
  grep -r "$pattern" projects/tutorial-refresh-fusion/assets/
done
```

### Integration with Project Management

**When resuming a project:**

```bash
/resume-project tutorial-refresh-fusion
```

Claude will:
1. Load project.md context
2. Check if rules are extracted
3. Check if target content exists
4. **Recommend content-writing-skill** if targets need work
5. Suggest next steps in workflow

**Project-management-skill** knows about content-writing-skill and will recommend it when appropriate.

---

## Best Practices

### For Outline Creation

✅ **DO:**
- List ALL source documents used (even "for inspiration")
- Document WHY each source matters
- Map sources to specific sections
- Identify project-specific update patterns

### For Draft Generation

✅ **DO:**
- Review inline HTML comments for source attribution
- Check that update patterns were applied correctly
- Validate rule compliance scores in YAML
- Ensure section sources are complete

### For Editing

✅ **DO:**
- Provide specific, actionable edit instructions
- Review changes before accepting
- Check that edit comments were added
- Verify version history is tracked

❌ **DON'T:**
- Use vague instructions ("make it better")
- Accept all changes without review
- Edit without understanding original rationale

---

## Files Created by Content-Writing-Skill

**Location:** `/projects/<project-name>/assets/`

**File types:**
- `<asset-name>-outline.md` - Outline with source mapping
- `<asset-name>-draft.md` - Draft with inline lineage
- `<asset-name>-draft.md` (edited) - Same file with version history

**Metadata in files:**
- **YAML frontmatter** - High-level, queryable metadata
- **Inline HTML comments** - Granular, contextual attribution

---

## See Also

- **Skill documentation:** `.claude/skills/content-writing-skill/README.md`
- **Metadata schemas:** `.claude/skills/content-writing-skill/templates/`
- **Comment patterns:** `.claude/skills/content-writing-skill/templates/inline-comment-patterns.md`
- **KURT.md:** Full system documentation
- **Project example:** `/projects/tutorial-refresh-fusion/project.md` (see "Using Content Writing Skill" section)
