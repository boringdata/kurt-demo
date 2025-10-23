---
description: Interactive inline content editing with grouped changes
argument-hint: [content-file-path] [optional: --mode=interactive/batch/review] [optional: --focus=style/flow/clarity/all]
---

# Interactive Content Editor

## Step 1: Process Arguments & Mode Selection
Content to edit: $ARGUMENTS

Parse arguments for:
- Content file path to edit (required)
- `--mode` (interactive [default], batch, review)
- `--focus` (style, flow, clarity, seo, all [default])

**Mode Explanations:**
- **Interactive**: Present changes one group at a time for approval
- **Batch**: Show all suggested changes, apply approved ones at once
- **Review**: Analysis only, no changes made

## Step 2: Content Analysis & Change Detection
**Read and analyze existing content:**
- Parse content structure and identify improvement opportunities
- Load applicable style guides, personas, and company profile
- Categorize potential improvements by type and priority

**Generate improvement suggestions:**
- **Style & Voice Issues**: Brand alignment, tone consistency, word choice
- **Clarity & Flow Issues**: Sentence structure, transitions, readability
- **Content Quality Issues**: Message strength, value delivery, engagement
- **Technical Issues**: SEO, internal links, CTAs, formatting

## Step 3: Change Grouping & Prioritization
**Group changes by category and proximity:**
```markdown
## Detected Improvement Opportunities

### Group 1: Opening Hook (Lines 1-8)
**Category:** Engagement & Clarity
**Priority:** High
**Issues:** Weak opening, unclear value proposition
**Estimated Impact:** +25% engagement

### Group 2: Technical Terminology (Lines 15-23, 34-41)
**Category:** Style & Audience Alignment
**Priority:** Medium
**Issues:** Too technical for target persona, jargon heavy
**Estimated Impact:** +15% comprehension

### Group 3: Call-to-Action (Lines 67-71)
**Category:** Conversion Optimization
**Priority:** High
**Issues:** Weak CTA, poor placement, unclear value
**Estimated Impact:** +30% click-through
```

## Step 4: Interactive Change Presentation

### For Interactive Mode:
❓ **Change Group Review Process:**
"I've identified [X] groups of improvements. Let's review them one at a time.

**Group 1 of [X]: [Category] ([Priority] Priority)**
**Location:** [Line numbers or section]
**Issue:** [Specific problem identified]
**Impact:** [Expected improvement]

**Current Text:**
```
[Original text block with line numbers]
15: Lorem ipsum dolor sit amet, consectetur
16: adipiscing elit, sed do eiusmod tempor
17: incididunt ut labore et dolore magna aliqua.
```

**Suggested Revision:**
```
[Proposed text with changes highlighted]
15: Our platform transforms how teams collaborate,
16: reducing project timelines by 40% while
17: improving communication clarity.
```

**Changes Made:**
- Replaced generic lorem ipsum with specific value proposition
- Added concrete benefit (40% faster)
- Simplified language for target audience
- Strengthened brand messaging

**Actions:**
A) **Accept** - Apply this change
B) **Modify** - Let me refine the suggestion
C) **Reject** - Skip this change
D) **Explain** - Tell me more about why this improves the content

Your choice (A/B/C/D):"

### Change Application Process:
**If user selects 'Accept':**
- Apply changes immediately to content
- Mark group as complete
- Show updated line numbers
- Move to next group

**If user selects 'Modify':**
- Ask for specific guidance on refinement
- Generate alternative version
- Present refined option for approval

**If user selects 'Explain':**
- Provide detailed rationale for changes
- Reference style guide/persona alignment
- Show expected impact on content effectiveness
- Return to choice menu

## Step 5: Real-Time Content Updates
**After each accepted change:**
```markdown
✅ **Group [X] Applied**
**Changes:** [Brief summary]
**Lines Updated:** [X-Y]
**Content Status:** [X] of [Y] groups reviewed

**Current Progress:**
- Groups Complete: [X]
- Groups Remaining: [Y]
- Overall Improvement: [estimated %]
- Word Count: [original] → [current]
```

## Step 6: Advanced Interactive Features

### Batch Mode Option:
❓ **After reviewing individual groups:**
"You've reviewed [X] groups. Would you like to:
1. **Continue one-by-one** with remaining groups
2. **Batch apply** all remaining high-priority changes
3. **Preview all changes** together before deciding
4. **Save progress** and resume later"

### Change Preview:
**If user selects 'Preview all changes':**
```markdown
## Complete Edit Preview
**Total Changes:** [X] groups affecting [Y] lines
**Estimated Improvement:** [Z]% overall quality increase

### Summary by Category:
- **Style & Voice:** [X] changes → [improvement description]
- **Clarity & Flow:** [X] changes → [improvement description]
- **Content Quality:** [X] changes → [improvement description]
- **Technical:** [X] changes → [improvement description]

### Before/After Metrics:
- **Readability Score:** [X] → [Y]
- **Brand Alignment:** [X]% → [Y]%
- **Estimated Engagement:** +[X]%

**Actions:**
A) **Apply All** - Make all suggested changes
B) **Apply by Category** - Choose which categories to apply
C) **Return to Individual Review** - Go back to one-by-one
D) **Cancel Changes** - Keep original content
```

## Step 7: Focused Editing Modes

### Style Focus Mode (`--focus=style`):
- Only present style guide and brand voice improvements
- Skip structural and content changes
- Faster workflow for brand consistency cleanup

### Flow Focus Mode (`--focus=flow`):
- Focus on transitions, structure, and readability
- Ignore style issues, concentrate on logical progression
- Good for content that's on-brand but poorly organized

### Clarity Focus Mode (`--focus=clarity`):
- Target confusing sentences, unclear explanations
- Simplify complex ideas for target persona
- Improve comprehension without changing structure

## Step 8: Change Tracking & Documentation
**Real-time change log:**
```markdown
## Edit Session Log
**Started:** [timestamp]
**Mode:** Interactive
**Focus:** All improvements

### Changes Applied:
1. **Group 1 - Opening Hook** ✅
   - **Lines:** 1-8
   - **Type:** Engagement improvement
   - **Impact:** Stronger value proposition

2. **Group 2 - Technical Terms** ✅
   - **Lines:** 15-23, 34-41
   - **Type:** Audience alignment
   - **Impact:** Reduced complexity for persona

3. **Group 3 - CTA** ⏭️ Skipped
   - **Reason:** User prefers original version

### Session Summary:
- **Groups Reviewed:** 8
- **Changes Applied:** 6
- **Changes Rejected:** 2
- **Improvement Score:** +40% estimated
```

## Step 9: Final Review & Completion
**End of session summary:**
❓ **"Editing session complete! Here's what we accomplished:**

**Content Improvements:**
- **Word Count:** [original] → [final] ([+/-X] words)
- **Readability:** [score improvement]
- **Brand Alignment:** [percentage improvement]
- **Issues Resolved:** [X] of [Y] identified issues

**Quality Gains:**
- [Improvement 1: specific enhancement made]
- [Improvement 2: specific enhancement made]
- [Improvement 3: specific enhancement made]

**Next Steps:**
A) **Save and Finish** - Content ready for review/publishing
B) **Continue Editing** - Address remaining issues
C) **Undo Last Changes** - Revert recent modifications
D) **Export Change Report** - Generate detailed edit summary

Your choice (A/B/C/D)?"

## Usage Examples

```bash
# Interactive inline editing (default)
/edit-content @projects/launch/assets/blog-post-draft.md

# Focus on style issues only
/edit-content @projects/guide/assets/tutorial.md --focus=style

# Batch mode for faster editing
/edit-content @projects/campaign/assets/landing-page.md --mode=batch

# Review mode (analysis only, no changes)
/edit-content @projects/series/assets/episode-1.md --mode=review --focus=clarity
```

## Success Indicators
**An effective interactive editing session should:**
- ✅ Present changes in logical, manageable groups
- ✅ Allow granular accept/reject control
- ✅ Provide clear rationale for each suggested change
- ✅ Show real-time progress and impact
- ✅ Maintain content quality while respecting user preferences
- ✅ Complete faster than manual editing while achieving better results
