---
description: Extract audience personas from content targeting patterns
argument-hint: [document-paths...] [optional: --overwrite] [optional: filter-criteria]
---

# Persona Extraction

## Step 1: Process Arguments
Documents to analyze: $ARGUMENTS

Parse for:
- Document paths (required)
- `--overwrite` flag (optional)
- Filter criteria (content-type, author, date range, etc.)

## Step 2: Analysis Mode
**Default behavior (incremental):**
- Analyze documents for audience targeting patterns
- Compare with existing files in `rules/personas/`
- Add new personas if found, leave existing ones untouched

**With `--overwrite` flag:**
- Delete all existing files in `rules/personas/`
- Perform fresh analysis of all documents
- Create completely new persona library

## Step 3: Apply Filters & Validate Content
If filtering criteria provided, search within the documents for:
- Content types (marketing, sales, support, technical, etc.)
- Specific author bylines
- Date ranges
- Product categories
- Customer segments mentioned
- Keyword matches

Show which documents will be analyzed after filtering.

**If less than 3 substantial documents found:**
❓ "I only found [X] documents to analyze. Persona extraction works best with at least 3-5 substantial pieces. Would you like to:
- Add more documents to the analysis?
- Proceed with limited analysis (results may be less reliable)?"

## Step 4: Incremental Analysis (Default)
1. **Read existing persona files** in `rules/personas/`
2. **Analyze new documents** for audience targeting patterns
3. **Compare findings**:
   - New persona pattern found → Create new persona file
   - No new patterns → Report "No new personas detected"

**Output:**
```
✅ Analysis complete
📁 Existing personas: 3 files (unchanged)
📝 New personas created: 1 file
   - technical-implementer.md (new audience pattern detected)
```

## Step 5: Overwrite Mode
1. **Clear `rules/personas/` directory**
2. **Perform fresh analysis** on all documents
3. **Create new persona library** from scratch

**Output:**
```
🗑️  Removed 3 existing persona files
✅ Fresh analysis complete
📝 Created 4 new persona files:
   - enterprise-decision-maker.md
   - technical-implementer.md
   - small-business-owner.md
   - end-user-practitioner.md
```

## Step 6: Persona Pattern Detection & Auto-Naming
Read through all documents and analyze for audience targeting consistency:

**Look for patterns in:**
- Language complexity and technical depth used
- Problems and pain points addressed in content
- Solutions and benefits emphasized
- Objections and concerns that content addresses
- Industry references and context provided
- Role-specific terminology and job titles mentioned
- Assumptions about audience knowledge level

**If single consistent persona:**
Create: `rules/personas/[auto-generated-name].md`
Examples: `enterprise-decision-maker.md`, `technical-implementer.md`, `small-business-owner.md`

**If multiple distinct personas detected:**
❓ "Found [X] distinct audience personas. Creating [X] persona files:
- [auto-name-1].md - [brief description]
- [auto-name-2].md - [brief description]
- [auto-name-3].md - [brief description]

Proceed?"

## Step 7: Create Persona Profile(s)
For each persona identified, read the persona template from `.claude/system-prompts/persona-template.md` and follow its format to create the persona files.

Auto-generate descriptive names based on:
- Job role/title (ceo, developer, marketer, etc.)
- Company size (enterprise, mid-market, small-business, etc.)
- User type (decision-maker, implementer, end-user, influencer, etc.)
- Industry context (saas, ecommerce, healthcare, etc.)

Save each file as `rules/personas/[auto-generated-name].md`

## Usage Examples

```bash
# Default: incremental (add new, keep existing)
/extract-personas @docs/marketing-content/*.md

# Fresh start: delete existing, analyze everything
/extract-personas @docs/all-customer-content/*.md --overwrite

# Incremental with filtering by content type
/extract-personas @docs/2025/*.md content-type:case-study

# Analyze specific product documentation
/extract-personas @docs/product-docs/*.md

# Focus on sales materials
/extract-personas @docs/sales-materials/*.md --overwrite
```

## Behavior Summary
- **Default**: Always incremental (safe, additive)
- **--overwrite**: Nuclear option (complete replacement)
- **No session context dependency** (predictable behavior)
- **Always re-analyze documents** (fresh perspective each time)
- **Focus on audience patterns** (who content is written for, not just what it says)
