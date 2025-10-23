---
description: Extract content structures and formats from documents
argument-hint: [document-paths...] [optional: --overwrite] [optional: filter-criteria]
---

# Structure Extraction

## Step 1: Process Arguments
Documents to analyze: $ARGUMENTS

Parse for:
- Document paths (required)
- `--overwrite` flag (optional)
- Filter criteria (content-type, author, date range, etc.)

## Step 2: Analysis Mode
**Default behavior (incremental):**
- Analyze documents for structural patterns
- Compare with existing files in `rules/structure/`
- Add new structures if found, leave existing ones untouched

**With `--overwrite` flag:**
- Delete all existing files in `rules/structure/`
- Perform fresh analysis of all documents
- Create completely new structure library

## Step 3: Apply Filters & Validate Content
If filtering criteria provided, search within the documents for:
- Content types (blog-post, landing-page, case-study, etc.)
- Specific author bylines
- Date ranges
- Keyword matches
- File name patterns

Show which documents will be analyzed after filtering.

**If less than 3 substantial documents found:**
❓ "I only found [X] documents to analyze. Structure extraction works best with at least 3-5 substantial pieces. Would you like to:
- Add more documents to the analysis?
- Proceed with limited analysis (results may be less reliable)?"

## Step 4: Incremental Analysis (Default)
1. **Read existing structure files** in `rules/structure/`
2. **Analyze new documents** for structural patterns
3. **Compare findings**:
   - New structure pattern found → Create new structure file
   - No new patterns → Report "No new structures detected"

**Output:**
```
✅ Analysis complete
📁 Existing structures: 4 files (unchanged)
📝 New structures created: 2 files
   - product-comparison-page.md (new pattern detected)
   - customer-success-story.md (new pattern detected)
```

## Step 5: Overwrite Mode
1. **Clear `rules/structure/` directory**
2. **Perform fresh analysis** on all documents
3. **Create new structure library** from scratch

**Output:**
```
🗑️  Removed 4 existing structure files
✅ Fresh analysis complete
📝 Created 6 new structure files:
   - blog-post-template.md
   - landing-page-template.md
   - case-study-template.md
   - product-announcement-template.md
   - help-article-template.md
   - email-newsletter-template.md
```

## Step 6: Structure Pattern Detection & Auto-Naming
Read through all documents and analyze for structural consistency:

**Look for patterns in:**
- Document organization and section flow
- Headline and subheading structures
- Introduction and conclusion patterns
- Call-to-action placement and style
- Content depth and detail levels
- Visual/formatting elements

**If single consistent structure:**
Create: `rules/structure/[auto-generated-name].md`
Examples: `blog-post-template.md`, `landing-page-template.md`, `case-study-template.md`

**If multiple distinct structures detected:**
❓ "Found [X] distinct content structures. Creating [X] structure files:
- [auto-name-1].md - [brief description]
- [auto-name-2].md - [brief description]
- [auto-name-3].md - [brief description]

Proceed?"

## Step 7: Create Structure Template(s)
For each structure identified, read the structure template from `.claude/system-prompts/structure-template.md` and follow its format to create the structure files.

Auto-generate descriptive names based on:
- Content purpose (blog-post, landing-page, case-study, announcement, etc.)
- Target outcome (lead-generation, education, conversion, support, etc.)
- Content depth (overview, deep-dive, quick-reference, comprehensive, etc.)

Save each file as `rules/structure/[auto-generated-name].md`

## Usage Examples

```bash
# Default: incremental (add new, keep existing)
/extract-structure @docs/marketing-pages/*.md

# Fresh start: delete existing, analyze everything
/extract-structure @docs/all-content/*.md --overwrite

# Incremental with filtering by content type
/extract-structure @docs/2025/*.md content-type:blog-post

# Analyze specific content category
/extract-structure @docs/case-studies/*.md --overwrite
```

## Behavior Summary
- **Default**: Always incremental (safe, additive)
- **--overwrite**: Nuclear option (complete replacement)
- **No session context dependency** (predictable behavior)
- **Always re-analyze documents** (fresh perspective each time)
- **Focus on reusable patterns** (templates for future content creation)
