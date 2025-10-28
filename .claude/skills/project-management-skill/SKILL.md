---
name: project-management
description: Manage Kurt projects - add sources/targets, update project.md, detect missing content, track progress.
---

# Project Management

## Overview

This skill helps manage Kurt projects by tracking sources (ground truth), targets (content to update/create), and project progress. It handles updating project.md, detecting missing content, and organizing project structure.

For core concepts about projects, see `KURT.md`.

## Quick Start

```bash
# Create a new project
/create-project

# Resume existing project
/resume-project

# Claude automatically invokes this skill when you:
# - Say "add this to my project"
# - Say "add source to project"
# - Say "what sources do we have?"
```

## Project Structure

```
projects/project-name/
├── project.md              # Project manifest (sources, targets, progress)
├── sources/                # Project-specific sources only
│   ├── internal-spec.pdf
│   └── notes.md
└── targets/                # Work in progress
    └── drafts/
        └── draft-content.md
```

**Note**: Web content lives in top-level `/sources/` (org knowledge base), not in project folders.

## Core Operations

### Add Source to Project

Sources are ground truth content you're working FROM.

**For web content:**

1. Ingest to organizational KB first:
   ```bash
   # Map URLs (add --discover-dates if publish dates are important)
   kurt ingest map https://example.com
   kurt ingest map https://example.com --discover-dates  # Extracts dates from blogrolls

   # Fetch content
   kurt ingest fetch --url-prefix https://example.com/
   ```

2. Update project.md to reference it:
   ```markdown
   ## Sources (Ground Truth)

   ### From Organizational Knowledge Base
   - [x] Page title: `/sources/example.com/path/page.md` (fetched: 2025-01-15)
   ```

**For local files:**

1. Copy file to project sources:
   ```bash
   cp ~/file.pdf projects/project-name/sources/
   ```

2. Update project.md:
   ```markdown
   ### Project-Specific Sources
   - [x] Internal spec: `sources/file.pdf` (added: 2025-01-15)
   ```

### Add Target to Project

Targets are content you're working ON (updating or creating).

**For existing content to update:**

Update project.md to reference content in `/sources/`:
```markdown
## Targets (Content to Update/Create)

### Existing Content to Update
- [ ] Tutorial: `/sources/docs.company.com/tutorial.md`
- [ ] Guide: `/sources/docs.company.com/guide.md`
```

**For new content to create:**

Update project.md with planned location:
```markdown
### New Content to Create
- [ ] New tutorial: `targets/drafts/new-tutorial.md` (planned)
- [ ] Blog post: `targets/drafts/blog-post.md` (planned)
```

### List Project Sources and Targets

Read project.md and display:
- Sources count (org KB vs project-specific)
- Targets count (to update vs to create)
- Completion status (checked vs unchecked)

Example output:
```
Sources: 5 total
  - 3 from organizational KB
  - 2 project-specific
  ✓ 4 fetched
  ☐ 1 pending

Targets: 4 total
  - 2 existing (to update)
  - 2 new (to create)
  ☐ 0 completed
  ☐ 4 pending
```

### Detect Missing Content

When resuming a project, check for gaps:

**No sources?**
```
⚠️ No ground truth sources found.

Do you have source material to add?
- Product specs or documentation
- Reference materials
- Internal docs or notes
```

**No targets?**
```
⚠️ No target content identified.

What do you want to create or update?
- Existing docs to update
- New content to create
```

### Update Project Progress

Update the Progress section in project.md:

```markdown
## Progress
- [x] Sources collected (2025-01-15)
- [x] Style guide identified (2025-01-16)
- [x] First draft: New tutorial (2025-01-17)
- [ ] Review and revisions
- [ ] Update existing tutorials
```

## Common Workflows

### Workflow 1: Add Web Content as Source

User: "Add https://example.com/docs to my project as ground truth"

Claude should:
1. Determine current project (from context or ask)
2. Ingest content:
   ```bash
   kurt ingest fetch https://example.com/docs
   ```
3. Find the file path in `/sources/`
4. Update project.md Sources section
5. Confirm: "Added example.com/docs as source to project-name"

### Workflow 2: Add Local File as Source

User: "Add this PDF to my project" (with file path)

Claude should:
1. Determine current project
2. Copy file to `projects/project-name/sources/`
3. Update project.md Sources section
4. Confirm: "Added filename.pdf to project-name sources"

### Workflow 3: Identify Target Content

User: "I need to update the getting started tutorial"

Claude should:
1. Search for "getting started" in `/sources/`
2. Show matches
3. Ask user to confirm which one(s)
4. Update project.md Targets section
5. Mark as "to update"

### Workflow 4: Check Project Status

User: "What's the status of my project?"

Claude should:
1. Read project.md
2. Count sources (checked vs unchecked)
3. Count targets (checked vs unchecked)
4. Check Progress section
5. Display summary
6. Recommend next actions if applicable

### Workflow 5: Create or Update Target Content

User: "Let's update the BigQuery quickstart" or "Create a new blog post"

Claude should:
1. **Check if rules are extracted:**
   - Read project.md to see if style, structure, persona, publisher rules are listed
   - If missing → Recommend extraction first (see "Rule Matching and Validation" section)
   - If present → Proceed to content creation

2. **Verify target is in project.md:**
   - Check if target content is listed in Targets section
   - If not → Add it first, then proceed

3. **Recommend content-writing-skill workflow:**
   ```
   Great! I see we have the necessary rules for this content:
   - Style: technical-documentation-style.md
   - Structure: tutorial-structure-template.md
   - Persona: analytics-engineer-persona.md
   - Publisher: publisher-profile.md

   Let's use the content-writing-skill to create this with full lineage tracking:

   Step 1: Create outline
   content-writing-skill outline <project-name> <asset-name>

   This will map sources to sections and identify update patterns to apply.
   ```

4. **After outline is created:**
   ```
   The outline is ready. Let's generate a draft:

   content-writing-skill draft <project-name> <asset-name>

   This will create a draft with:
   - Section-level source attribution in YAML frontmatter
   - Inline HTML comments explaining reasoning
   - Update pattern applications documented
   ```

5. **After draft is created:**
   ```
   Draft complete! You can now:
   - Review the draft content
   - Edit if needed: content-writing-skill edit projects/<project-name>/assets/<asset-name>-draft.md --instructions "..."
   - Check lineage: grep "<!-- SECTION:" <draft-file>
   ```

6. **Update project.md Progress section:**
   - Mark outline as complete
   - Mark draft as complete (if done)
   - Add next steps (review, editing, publishing)

**Important**: Always check for rules before recommending content creation. If rules are missing, suggest extraction first.

## Updating project.md

### Sources Section Format

```markdown
## Sources (Ground Truth)

### From Organizational Knowledge Base
- [x] Page title: `/sources/domain.com/path/page.md` (fetched: YYYY-MM-DD)
- [ ] Another page: https://example.com/page (not fetched)

### Project-Specific Sources
- [x] Internal doc: `sources/filename.pdf` (added: YYYY-MM-DD)
- [ ] Notes: `sources/notes.md` (pending)
```

**Format rules:**
- Use `[x]` for fetched/added content
- Use `[ ]` for pending content
- Include date when content was added
- Use relative paths for project-specific sources
- Use absolute paths (`/sources/...`) for org KB content

### Targets Section Format

```markdown
## Targets (Content to Update/Create)

### Existing Content to Update
- [ ] Tutorial: `/sources/docs.company.com/tutorial.md`
- [x] Guide: `/sources/docs.company.com/guide.md` (updated: YYYY-MM-DD)

### New Content to Create
- [ ] New tutorial: `targets/drafts/new-tutorial.md` (planned)
- [x] Blog post: `targets/drafts/blog-post.md` (drafted: YYYY-MM-DD)
```

**Format rules:**
- Use `[ ]` for pending work
- Use `[x]` for completed work
- Include completion date when done
- Separate existing (to update) from new (to create)

## Rule Matching and Validation

When working on target content, ensure appropriate rules exist. The system dynamically discovers available rule types from `rules/rules-config.yaml`.

### Check for Required Rules

Before content work begins:

1. **Load available rule types from registry:**
   ```bash
   # Dynamically discover all enabled rule types
   registry="rules/rules-config.yaml"
   enabled_types=$(yq '.rule_types | to_entries | .[] | select(.value.enabled == true) | .key' "$registry")

   # Get directory for each type
   for type in $enabled_types; do
     directory=$(yq ".rule_types.${type}.directory" "$registry")
     echo "$type → rules/$directory/"
   done
   ```

2. **Inspect target content** to determine requirements:
   - Content type (tutorial, blog, landing page, docs)
   - Content purpose (educational, lead-gen, reference)
   - Target audience (technical, business, general)
   - Tone and complexity level
   - Industry/vertical (if applicable)
   - Channel (if applicable)
   - Any other custom dimensions configured

3. **Search for matching rules across ALL rule types:**
   ```bash
   # Dynamically check each enabled rule type
   for type in $enabled_types; do
     directory=$(yq ".rule_types.${type}.directory" "$registry")
     name=$(yq ".rule_types.${type}.name" "$registry")

     echo "Checking $name:"
     ls -la "rules/$directory/" 2>/dev/null || echo "  (no rules extracted yet)"
   done
   ```

4. **Match requirements to available rules:**
   - **Built-in types** (always checked):
     - **Style**: Voice, tone, complexity match target needs?
     - **Structure**: Document format matches target type?
     - **Persona**: Audience profile matches target audience?
     - **Publisher**: Organizational context available?

   - **Custom types** (if configured):
     - **Verticals**: Does industry-specific content exist for target vertical?
     - **Use-cases**: Does problem/solution pattern exist for target use case?
     - **Channels**: Does channel-specific formatting exist for target channel?
     - **[Any other custom types]**: Check if rules exist for target's custom dimensions

### Handle Missing Rules

**Scenario 1: Target Content Exists (Updating Existing)**
```
Target: Update technical tutorial
Required: Technical writing style, tutorial structure, developer persona

Check: Do we have matching rules?
✓ Technical style → rules/style/technical-documentation.md
✗ Tutorial structure → NOT FOUND
✓ Developer persona → rules/personas/technical-implementer.md

Action: Extract tutorial structure from existing targets
writing-rules-skill structure with documents: /sources/docs.company.com/tutorials/*.md
# Or auto-discover
writing-rules-skill structure --type tutorial --auto-discover
```

**Scenario 2: No Target Content (Creating New)**
```
Target: Create new blog post series
Required: Blog style, blog structure, target persona

Check: Do we have matching rules?
✗ Blog style → NOT FOUND
✗ Blog structure → NOT FOUND
✗ Target persona → NOT FOUND

Options:
1. Extract from similar content (if available in sources)
2. Ask user to provide example/template
3. Proceed with general guidelines (not recommended)

Recommended: "I don't have rules for blog content. Can you provide:
- Example blog post to extract style/structure from, OR
- Style guidelines document, OR
- Description of desired tone and structure?"
```

**Scenario 3: Partial Match**
```
Target: Create case study
Required: Case study style, case study structure, customer persona

Check: Do we have matching rules?
✗ Case study style → NOT FOUND
✗ Case study structure → NOT FOUND
✓ General company style → rules/style/conversational-marketing.md
✓ Publisher profile → rules/publisher/publisher-profile.md

Action: Extract case study specifics, use general rules for foundation
writing-rules-skill structure with documents: /sources/company.com/case-studies/*.md
# Or auto-discover
writing-rules-skill structure --type case-study --auto-discover
```

### Rule Matching Algorithm (Dynamic)

```
FOR each target content item:
  1. Load rule types from registry:
     enabled_types = load_enabled_rule_types("rules/rules-config.yaml")

  2. Inspect target properties:
     - content_type: tutorial | blog | landing-page | docs | case-study | etc.
     - content_purpose: educational | lead-gen | reference | support | etc.
     - target_audience: technical | business | general | executive | etc.
     - complexity_level: beginner | intermediate | advanced
     - tone_required: professional | conversational | authoritative | casual
     - industry_vertical: [if verticals configured] healthcare | finance | etc.
     - use_case: [if use-cases configured] migration | optimization | etc.
     - channel: [if channels configured] email | web | social | etc.
     - [any other custom dimensions]

  3. Search rules directories dynamically:
     FOR each enabled rule type:
       directory = get_directory(rule_type)
       rules = list_rules("rules/$directory/")

       IF rules found:
         check_for_match(rules, target_properties)

  4. Evaluate matches per rule type:
     FOR each rule type:
       IF perfect match found → Use existing rule
       IF partial match found → Use partial + extract specifics
       IF no match found → Flag as missing

  5. Flag missing rules dynamically:
     FOR each rule type with no match:
       ⚠️ No {rule_type_name} for [target_properties]

     Examples:
       ⚠️ No style guide for technical tutorials
       ⚠️ No structure template for case studies
       ⚠️ No persona for business decision-makers
       ⚠️ No vertical rules for healthcare content
       ⚠️ No channel guidelines for email format

  6. Recommend action:
     - "Extract {rule_type} from these similar documents: [list]"
     - "Please provide example for {rule_type} extraction"
     - "Proceed with general guidelines? (not recommended)"
```

**Key difference from hardcoded approach:**
- System discovers rule types from registry (not hardcoded to 4 types)
- Checks ALL enabled rule types (built-in + custom)
- Error messages reflect actual configured rule types
- Fully extensible as teams add custom dimensions

### Add Rules to project.md

Track which rules apply to the project. The format is **dynamic** based on enabled rule types in the registry:

```markdown
## Rules Configuration

[Dynamically generated sections for each enabled rule type]

### Style Guidelines
- Technical documentation style: `rules/style/technical-documentation.md`
- Conversational blog style: `rules/style/conversational-blog.md`

### Structure Templates
- Tutorial structure: `rules/structure/quickstart-tutorial.md`
- API reference structure: `rules/structure/api-reference.md`

### Target Personas
- Developer persona: `rules/personas/technical-implementer.md`
- Business decision-maker: `rules/personas/enterprise-decision-maker.md`

### Publisher Profile
- Company profile: `rules/publisher/publisher-profile.md` (always applicable)

[If custom rule types are configured:]

### Industry Verticals
- Healthcare vertical: `rules/verticals/healthcare-vertical.md`
- Finance vertical: `rules/verticals/finance-vertical.md`

### Use Case Patterns
- Migration pattern: `rules/use-cases/migration-patterns.md`

### Channel Guidelines
- Email guidelines: `rules/channels/email-guidelines.md`
- Social guidelines: `rules/channels/social-guidelines.md`
```

**Dynamic section generation:**
```bash
# Generate project.md rules sections from registry
for type in $(yq '.rule_types | to_entries | .[] | select(.value.enabled == true) | .key' rules/rules-config.yaml); do
  name=$(yq ".rule_types.${type}.name" rules/rules-config.yaml)
  directory=$(yq ".rule_types.${type}.directory" rules/rules-config.yaml)

  echo "### $name"

  # List rules in this directory
  for rule_file in rules/$directory/*.md; do
    if [ -f "$rule_file" ]; then
      rule_name=$(basename "$rule_file" .md | sed 's/-/ /g')
      echo "- ${rule_name^}: \`$rule_file\`"
    fi
  done

  echo ""
done
```

### Workflow: Content Work with Rule Validation

```
1. User: "Let's update the getting started tutorial"

2. Check project.md targets:
   - Target: /sources/docs.company.com/getting-started.md

3. Inspect target content:
   - Content type: Tutorial
   - Purpose: Educational quickstart
   - Audience: Developers (beginner to intermediate)
   - Tone: Friendly, supportive, clear

4. Check for matching rules:
   ls rules/style/ | grep -i tutorial
   ls rules/structure/ | grep -i tutorial
   ls rules/personas/ | grep -i developer

5. Report findings:
   ✓ Found: rules/structure/quickstart-tutorial.md
   ✓ Found: rules/personas/technical-implementer.md
   ✗ Missing: Tutorial-specific style guide

6. Recommend:
   "I found structure and persona rules for tutorials, but no tutorial-specific style guide.

   Options:
   - Extract style from existing tutorials in sources
   - Use general technical documentation style
   - Provide example of desired tutorial tone

   What would you prefer?"

7. User chooses → Extract or proceed

8. Once rules are confirmed/extracted:
   "Rules are ready! Let's use content-writing-skill to create this update with full lineage tracking:

   content-writing-skill outline <project-name> getting-started-tutorial

   This will create an outline mapping sources to sections, then we can generate the draft."
```

## Integration with Other Skills

### With writing-rules-skill (extraction)

```bash
# Extract style patterns
writing-rules-skill style with documents: <similar-content-files>
# Or auto-discover
writing-rules-skill style --type corporate --auto-discover

# Extract structure templates
writing-rules-skill structure with documents: <similar-content-files>
# Or auto-discover
writing-rules-skill structure --type tutorial --auto-discover

# Extract audience personas
writing-rules-skill persona with documents: <target-audience-content>
# Or auto-discover
writing-rules-skill persona --audience-type all --auto-discover

# Extract publisher profile
writing-rules-skill publisher with sources: <company-web-pages-and-docs>
# Or auto-discover
writing-rules-skill publisher --auto-discover
```

### With ingest-content-skill

```bash
# Ingest content first
kurt ingest map https://example.com
# Or with date discovery for blogs/docs (recommended for projects tracking content freshness)
kurt ingest map https://example.com --discover-dates

kurt ingest fetch --url-prefix https://example.com/

# Then add to project (this skill)
# Updates project.md to reference ingested content
```

### With document-management-skill

```bash
# List what's available in org KB
kurt document list --url-prefix https://example.com

# Search for specific content
kurt document list --url-contains "tutorial"

# Then add relevant docs to project
```

### With content-writing-skill

```bash
# Use content-writing-skill for target content work
# Provides comprehensive lineage tracking from sources to drafts

# Step 1: Create outline with source mapping
content-writing-skill outline <project-name> <asset-name>

# Step 2: Generate draft with inline attribution
content-writing-skill draft <project-name> <asset-name>

# Step 3: Edit with session history tracking
content-writing-skill edit projects/<project-name>/assets/<asset-name>-draft.md --instructions "..."
```

**When to recommend content-writing-skill:**
- User says "let's update [target content]" or "create [new content]"
- Target content needs drafting or editing
- User wants to track lineage (which sources informed which sections)
- Project has rules extracted (style, structure, persona, publisher)

**What it provides:**
- YAML frontmatter with section-level source attribution
- Inline HTML comments documenting reasoning and sources
- Update pattern tracking (project-specific transformations)
- Version history and edit session tracking
- Complete traceability from project plan to draft

**Example integration:**
```
User: "Let's update the BigQuery tutorial"

Project-management-skill:
1. Checks project.md for target
2. Validates rules exist (style, structure, persona)
3. If rules exist → Recommend: "Use content-writing-skill outline tutorial-refresh-fusion bigquery-quickstart"
4. If rules missing → Recommend extraction first, then content-writing-skill
```

## Quick Reference

| Task | Action |
|------|--------|
| Add web source | Ingest → Update project.md Sources |
| Add local source | Copy to project/sources/ → Update project.md |
| Add target | Update project.md Targets section |
| List sources | Read & parse project.md Sources |
| List targets | Read & parse project.md Targets |
| Check status | Count checked vs unchecked items |
| Detect gaps | Check for empty Sources or Targets |
| Update progress | Add entry to Progress section |

## Detection Patterns

Claude should invoke this skill when user says:

- "Add [URL/file] to my project"
- "Add this as ground truth"
- "What sources do we have?"
- "What do we need to update?"
- "Add target content"
- "Project status"
- "What's missing from the project?"

**When to recommend content-writing-skill** (from project-management-skill):

- "Let's update [content name]"
- "Create [new content]"
- "Write a draft for [content]"
- "Start working on [target content]"
- Any request to work on target content listed in project.md

**Flow**: project-management-skill checks for rules → if rules exist, recommend content-writing-skill → if rules missing, recommend extraction first

## Important Notes

- **project.md is the source of truth** for project metadata (for now)
- **Web content goes to /sources/** (org KB), not project folders
- **Project sources folder** is only for project-specific files (PDFs, notes, etc.)
- **Always update project.md** when adding sources or targets
- **Use relative paths** for project-specific content
- **Use absolute paths** (`/sources/...`) for org KB content

## Next Steps

- For content ingestion, see **ingest-content-skill**
- For document queries, see **document-management-skill**
- For rules extraction, see **writing-rules-skill** (consolidates style, structure, persona, and publisher extraction)
- For content creation (outline/draft/edit), see **content-writing-skill**
- For project creation, use `/create-project`
- For resuming work, use `/resume-project`
