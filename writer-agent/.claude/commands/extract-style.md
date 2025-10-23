---
description: Extract writing style from documents
argument-hint: [document-paths...] [optional: --overwrite] [optional: filter-criteria]
---

# Style Extraction

## Step 1: Process Arguments
Documents to analyze: $ARGUMENTS

Parse for:
- Document paths (required)
- `--overwrite` flag (optional)
- Filter criteria (author, date range, etc.)

## Step 2: Analysis Mode
**Default behavior (incremental):**
- Analyze documents for style patterns
- Compare with existing files in `rules/style/`
- Add new styles if found, leave existing ones untouched

**With `--overwrite` flag:**
- Delete all existing files in `rules/style/`
- Perform fresh analysis of all documents
- Create completely new style library

## Step 3: Apply Filters & Validate Content
If filtering criteria provided, search within the documents for:
- Specific author bylines
- Date ranges
- Content types
- Keyword matches
- File name patterns

Show which documents will be analyzed after filtering.

**If less than 3 substantial documents found:**
❓ "I only found [X] documents to analyze. Style extraction works best with at least 3-5 substantial pieces. Would you like to:
- Add more documents to the analysis?
- Proceed with limited analysis (results may be less reliable)?"

## Step 4: Incremental Analysis (Default)
1. **Read existing style files** in `rules/style/`
2. **Analyze new documents** for patterns
3. **Compare findings**:
   - New pattern found → Create new style file
   - No new patterns → Report "No new styles detected"

**Output:**
```
✅ Analysis complete
📁 Existing styles: 3 files (unchanged)
📝 New styles created: 1 file
   - supportive-help-content.md (new pattern detected)
```

## Step 5: Overwrite Mode
1. **Clear `rules/style/` directory**
2. **Perform fresh analysis** on all documents
3. **Create new style library** from scratch

**Output:**
```
🗑️  Removed 3 existing style files
✅ Fresh analysis complete
📝 Created 4 new style files:
   - conversational-marketing.md
   - technical-documentation.md
   - executive-communications.md
   - supportive-help-content.md
```

## Step 6: Multi-Style Detection & Auto-Naming
Read through all documents and analyze for consistency:

**If single consistent style:**
Create: `rules/style/[auto-generated-name].md`
Examples: `conversational-marketing.md`, `technical-documentation.md`, `executive-communications.md`

**If multiple distinct styles detected:**
❓ "Found [X] distinct writing styles. Creating [X] style files:
- [auto-name-1].md - [brief description]
- [auto-name-2].md - [brief description]
- [auto-name-3].md - [brief description]

Proceed?"

## Step 7: Create Style Guide(s)
For each style identified, read the style guide template from `.claude/system-prompts/style-guide-template.md` and follow its format to create the style files.

Auto-generate descriptive names based on:
- Content type (blog, landing-page, technical, etc.)
- Tone (conversational, formal, authoritative, etc.)
- Audience (executive, developer, customer, etc.)

Save each file as `rules/style/[auto-generated-name].md`

## Usage Examples

```bash
# Default: incremental (add new, keep existing)
/extract-style @docs/recent-posts/*.md

# Fresh start: delete existing, analyze everything
/extract-style @docs/all-content/*.md --overwrite

# Incremental with filtering
/extract-style @docs/2025/*.md author:sarah

# Overwrite with specific content
/extract-style @docs/marketing/*.md --overwrite
```

## Behavior Summary
- **Default**: Always incremental (safe, additive)
- **--overwrite**: Nuclear option (complete replacement)
- **No session context dependency** (predictable behavior)
- **Always re-analyze documents** (fresh perspective each time)
