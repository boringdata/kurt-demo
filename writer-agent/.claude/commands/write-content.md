---
description: Generate content draft from outline and project requirements
argument-hint: [task-breakdown-path] [task-id] [optional: --section] [optional: --style-override]
---

# Content Writing Generator

## Step 1: Process Arguments & Task Context
Writing task to execute: $ARGUMENTS

Parse arguments for:
- Task breakdown file path (required)
- Specific writing task ID (required)
- `--section` flag with section name (write specific section only)
- `--style-override` (temporarily use different style guide)

## Step 2: Gather Writing Requirements
Read task breakdown and extract writing specifications:

**Asset Requirements:**
- Content type, purpose, and success metrics
- Target word count and scope
- Target audience and key objectives
- Quality standards and acceptance criteria

**Content Foundation:**
- Locate and read content outline (from outline task or asset directory)
- Review research findings and supporting materials
- Check for dependencies on other completed content

**Rule Files to Apply:**
- Style guide for voice, tone, and writing patterns (e.g., @rules/style/technically-writing-style.md)
- Persona file for audience targeting (e.g., @rules/personas/ai-curious-professional.md)
- Publisher profile for brand context (e.g., @rules/publisher/publisher-profile.md)
- Structure template if no outline exists (e.g., @rules/structure/glossary-faq-enhanced.md)

**Load and analyze each rule file:**
- Read style guide → Extract voice patterns, word choices, sentence structures
- Read persona → Understand pain points, goals, communication preferences
- Read publisher profile → Apply brand values and messaging
- Use structure template as fallback if outline missing

## Step 3: Content Preparation & Validation
**Outline Analysis:**
- Extract section structure and word count targets
- Identify key points, research, and supporting materials for each section
- Map internal links and call-to-action placements
- Understand content flow and transition requirements

**Requirements Validation:**
❓ **Content Readiness Check:**
"Preparing to write: [Asset Name]

**Foundation Status:**
- ✅ Outline: Found and analyzed
- ✅ Research: [X] findings available
- ✅ Style Guide: [style-name] loaded
- ✅ Persona: [persona-name] loaded
- ✅ Company Profile: Loaded

**Content Specifications:**
- Target Length: [X] words
- Primary Audience: [Persona description]
- Content Goal: [Asset purpose]
- Writing Style: [Style characteristics]

**If missing requirements:**
Missing foundation elements:
- ❌ [Missing element]: [What's needed and how to get it]

Proceed anyway or address missing elements first?"

## Step 4: Style & Voice Calibration
**Load and apply writing guidelines:**
- Extract voice and tone characteristics from style guide
- Understand sentence structure and word choice patterns
- Load common phrases and writing patterns to emulate
- Calibrate technical depth and complexity from persona requirements

**Style Application:**
- Adapt company messaging and positioning for this content type
- Apply persona-specific communication preferences
- Integrate brand personality and voice characteristics
- Ensure consistency with existing content examples

## Step 5: Content Generation by Section
Read the content draft template from `.claude/system-prompts/content-draft-template.md` and follow its structure for creating the draft.

### Section-by-Section Writing Process:
**For each section in the outline:**

1. **Section Setup:**
   - Read section purpose and key points from outline
   - Identify word count target for this section
   - Review supporting materials and research to integrate
   - Note transition requirements from previous section

2. **Content Creation:**
   - Write section following style guide voice and tone
   - Integrate planned research findings and supporting data
   - Include planned internal links and references
   - Maintain persona-appropriate depth and complexity
   - Follow outline structure while allowing natural flow

3. **Section Quality Check:**
   - Verify key points from outline are covered
   - Check word count alignment with targets
   - Ensure style consistency with guidelines
   - Validate audience appropriateness and clarity

## Step 6: Content Integration & Flow
**Ensure cohesive content:**
- Verify smooth transitions between sections
- Check that internal links flow naturally within content
- Ensure consistent voice and style throughout
- Validate that key messages and objectives are addressed

**Call-to-Action Integration:**
- Place primary and secondary CTAs according to outline strategy
- Ensure CTAs align with content goals and audience journey
- Make CTAs contextual and natural within content flow

## Step 7: Content Review & Optimization
**Quality Assurance:**
- Check adherence to style guide requirements
- Verify persona appropriateness and communication style
- Ensure company messaging and positioning alignment
- Validate that research and data are properly integrated

**Content Optimization:**
- Review for clarity, readability, and engagement
- Check for proper internal linking and reference integration
- Ensure call-to-actions are strategically placed and compelling
- Verify content meets outline objectives and success criteria

**If quality issues identified:**
❓ "Content draft complete but identified improvement areas:
- [Issue 1: specific problem and suggested fix]
- [Issue 2: specific problem and suggested fix]

Would you like me to:
- Revise automatically based on feedback
- Create revision notes for manual editing
- Proceed with current draft
- Focus improvements on specific sections"

## Step 8: Draft Finalization & Handoff
**Save completed draft:**
- Create content file using content draft template: `/projects/[project]/assets/[asset-name]-draft.md`
- Include complete YAML frontmatter for traceability
- Include metadata: word count, outline adherence, style guide used
- Update task status in task breakdown
- Mark editing/review tasks as ready to execute

**Draft Summary:**
```markdown
## Writing Completion Summary
**Draft Created:** `/projects/[project]/assets/[asset-name]-draft.md`
**Final Word Count:** [X] words (target: [Y] words)
**Outline Adherence:** [X]% of planned elements included
**Style Guide Applied:** [style-guide-name]
**Research Integration:** [X] findings and [Y] references included
**Internal Links:** [X] strategic links included
**Ready for Review Task:** [review-task-id]

## Content Quality Metrics
- **Readability:** [Assessment of clarity and flow]
- **Audience Alignment:** [How well it matches persona needs]
- **Brand Consistency:** [Adherence to company voice and messaging]
- **Objective Achievement:** [How well it meets content goals]

## Recommended Next Steps
- [Review task to execute next]
- [Any specific areas needing editorial attention]
```

## Usage Examples

```bash
# Write complete content from outline
/write-content @projects/launch/task-breakdown.md blog-write-01

# Write specific section only
/write-content @projects/guide/task-breakdown.md tutorial-write-01 --section "Getting Started"

# Override style for specific content piece
/write-content @projects/technical/task-breakdown.md docs-write-01 --style-override technical-detailed

# Write content with enhanced guidance
/write-content @projects/series/task-breakdown.md episode-write-03 --interactive
```

## Success Indicators
**A complete content draft should include:**
- ✅ All outline sections written with appropriate depth
- ✅ Target word count achieved (±10% of target acceptable)
- ✅ Style guide voice and tone consistently applied
- ✅ Persona-appropriate communication and complexity
- ✅ Research findings and data properly integrated
- ✅ Internal links placed strategically and naturally
- ✅ Call-to-actions aligned with content goals
- ✅ Company messaging and brand voice maintained
- ✅ Clear, engaging, and actionable content
