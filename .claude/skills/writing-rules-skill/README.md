# Writing Rules Skill

**Purpose:** Unified skill for extracting reusable writing rules from existing content
**Location:** `.claude/skills/writing-rules-skill/`
**Output:** Rule files in `/rules/` directories

---

## Overview

The writing-rules-skill consolidates all rule extraction operations into a single entry point with four subskills:

- **style** - Extract writing voice, tone, and style patterns
- **structure** - Extract document organization and format templates
- **persona** - Extract audience targeting patterns
- **publisher** - Extract organizational context and brand profile

Rules extracted by this skill are used by **content-writing-skill** to ensure consistency when creating or updating content.

---

## Quick Start

```bash
# Extract all foundation rules for a new project
writing-rules-skill publisher --auto-discover     # Company context
writing-rules-skill style --type corporate --auto-discover  # Brand voice
writing-rules-skill structure --type tutorial --auto-discover  # Doc format
writing-rules-skill persona --audience-type technical --auto-discover  # Audience
```

---

## Subskills

### style - Extract Writing Patterns

Extract voice, tone, sentence structure, and word choice patterns from existing content.

**Usage:**
```bash
# Auto-discover corporate voice from marketing pages
writing-rules-skill style --type corporate --auto-discover

# Auto-discover technical docs style
writing-rules-skill style --type technical-docs --auto-discover

# Auto-discover blog voice
writing-rules-skill style --type blog --auto-discover

# Manual document selection
writing-rules-skill style with documents: /sources/example.com/page1.md /sources/example.com/page2.md
```

**Output:** `/rules/style/<name>.md`

**Modes:**
- Incremental (default) - Adds new styles if patterns differ from existing
- Overwrite (`--overwrite`) - Replaces all existing style guides

---

### structure - Extract Document Templates

Extract document organization, section flow, and format patterns from existing content.

**Usage:**
```bash
# Auto-discover tutorial structure
writing-rules-skill structure --type tutorial --auto-discover

# Auto-discover landing page structure
writing-rules-skill structure --type landing-page --auto-discover

# Auto-discover API reference structure
writing-rules-skill structure --type api-reference --auto-discover

# Manual document selection
writing-rules-skill structure with documents: /sources/docs.com/tutorial1.md /sources/docs.com/tutorial2.md
```

**Output:** `/rules/structure/<name>.md`

**Modes:**
- Incremental (default) - Adds new structures if patterns differ from existing
- Overwrite (`--overwrite`) - Replaces all existing structure templates

---

### persona - Extract Audience Profiles

Extract audience targeting patterns from content to understand who content is written for.

**Usage:**
```bash
# Auto-discover all personas from diverse content
writing-rules-skill persona --audience-type all --auto-discover

# Auto-discover technical/developer personas
writing-rules-skill persona --audience-type technical --auto-discover

# Auto-discover business/executive personas
writing-rules-skill persona --audience-type business --auto-discover

# Auto-discover customer/end-user personas
writing-rules-skill persona --audience-type customer --auto-discover

# Manual document selection
writing-rules-skill persona with documents: /sources/docs.com/technical-guide.md
```

**Output:** `/rules/personas/<name>.md`

**Modes:**
- Incremental (default) - Adds new personas if audiences differ from existing
- Overwrite (`--overwrite`) - Replaces all existing persona profiles

---

### publisher - Extract Company Profile

Extract organizational identity, messaging, positioning, and brand context from company web pages and marketing materials.

**Usage:**
```bash
# Auto-discover key company pages and extract profile
writing-rules-skill publisher --auto-discover

# Manual source selection (URLs or local files)
writing-rules-skill publisher with sources: https://company.com/ https://company.com/about /path/to/brand-guide.pdf

# Update existing profile (incremental)
writing-rules-skill publisher --auto-discover

# Replace existing profile (overwrite)
writing-rules-skill publisher --auto-discover --overwrite
```

**Output:** `/rules/publisher/publisher-profile.md` (single canonical file)

**Modes:**
- Incremental (default) - Adds "Recent Analysis" section to existing profile
- Overwrite (`--overwrite`) - Replaces entire publisher profile

---

## Prerequisites

All rule extraction requires content to be **fetched + indexed**:

1. **Fetch content** - Download to `/sources/`:
   ```bash
   kurt ingest fetch --url-prefix <url>
   ```

2. **Index content** - Extract metadata:
   ```bash
   kurt index --url-prefix <url>
   ```

3. **Verify readiness**:
   ```bash
   kurt document list --url-prefix <url> --status FETCHED
   kurt document get <url>  # Should show topics, entities
   ```

If content is not ready, the skill will warn you and show the required commands.

---

## Auto-Discovery Mode

Each subskill supports auto-discovery to intelligently find relevant content without manual selection:

**Style auto-discovery:**
- Corporate voice → Homepage, product pages, about pages
- Technical docs → Documentation, guides, tutorials
- Blog voice → Recent blog posts
- Author voice → Posts by specific author

**Structure auto-discovery:**
- Tutorial → Tutorial, quickstart, getting-started pages
- Landing page → Product, feature, campaign pages
- API reference → API docs, reference pages
- Blog post → Recent blog posts

**Persona auto-discovery:**
- Technical → Docs, API refs, guides, tutorials
- Business → Product pages, solutions, case studies, pricing
- Customer → Support, help, FAQ, getting-started
- All → Diverse sample across content types

**Publisher auto-discovery:**
- Homepage (required)
- About/company pages
- Product/feature pages
- Customer stories/case studies
- Pricing pages

---

## Integration with Project Workflow

### During Project Setup (`/create-project`)

Extract foundation rules after collecting sources:

1. **Publisher profile** (always) - Company context and brand voice
2. **Corporate style** (recommended) - Official brand writing style
3. **Content-specific rules** (based on targets):
   - Marketing: Landing page structure, marketing personas
   - Technical docs: Technical style, tutorial structure, developer personas

### When Resuming Projects (`/resume-project`)

Validate rule coverage before content work:

```
Checking rule coverage for target: quickstart-tutorial

Required rules:
✓ Style: Technical documentation style found
✗ Structure: Tutorial structure NOT FOUND
✓ Persona: Developer persona found
✓ Publisher: Company profile found

Missing: Tutorial structure template

Recommendation: Extract tutorial structure before starting work
```

### During Content Work (via `project-management-skill`)

Rules are automatically referenced when creating content via `content-writing-skill`.

---

## Output Directory Structure

```
/rules/
├── publisher/
│   └── publisher-profile.md          # Single canonical profile
├── style/
│   ├── corporate-brand-voice.md      # Corporate marketing voice
│   ├── technical-documentation.md    # Technical writing style
│   └── conversational-blog.md        # Blog post style
├── structure/
│   ├── quickstart-tutorial.md        # Tutorial format template
│   ├── landing-page-structure.md     # Landing page format
│   └── api-reference-structure.md    # API docs format
└── personas/
    ├── technical-implementer.md      # Developer persona
    ├── business-decision-maker.md    # Executive persona
    └── end-user.md                   # Customer persona
```

---

## Best Practices

### Extraction Order

1. **Start with publisher profile** - Provides foundational company context
2. **Extract corporate voice** - Establishes brand writing style
3. **Extract content-specific rules** - Based on what you're creating:
   - Technical content → Technical style + Tutorial structure + Developer persona
   - Marketing content → Marketing style + Landing page structure + Business persona

### Minimum Documents

- **Style extraction:** 3-5 documents with consistent voice
- **Structure extraction:** 3-5 documents with same format
- **Persona extraction:** 5-10 documents targeting same audience
- **Publisher extraction:** Homepage + 2-3 key pages minimum

### Incremental vs Overwrite

- **Use incremental (default)** when:
  - Adding new rule variations (blog style + technical style)
  - Extending existing rule library
  - Unsure if new patterns exist

- **Use overwrite** when:
  - Company rebrand (update publisher profile)
  - Complete style refresh (replace all styles)
  - Starting fresh after major content changes

---

## Troubleshooting

### "Sources not ready for extraction"

**Problem:** Content hasn't been fetched or indexed yet
**Solution:**
```bash
# Check status
kurt document list --url-prefix <url>

# Fetch if needed
kurt ingest fetch --url-prefix <url>

# Index if needed
kurt index --url-prefix <url>

# Retry extraction
writing-rules-skill <subskill> ...
```

### "No new patterns detected"

**Problem:** Patterns already captured in existing rules
**Solution:**
- Review existing rule files - may already have what you need
- Try different content types for distinct patterns
- Use `--overwrite` to refresh existing rules

### "Insufficient documents for reliable extraction"

**Problem:** Too few documents provided
**Solution:**
- Add more source documents (minimum 3-5 recommended)
- Use auto-discovery to find more content
- Proceed with caveat if necessary

---

## Related Documentation

- **SKILL.md** - Technical implementation and routing logic
- **subskills/** - Individual extraction subskill implementations
- **content-writing-skill** - Uses extracted rules for content creation
- **project-management-skill** - Validates rule coverage for projects
