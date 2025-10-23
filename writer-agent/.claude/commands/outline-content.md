---
description: Create detailed content outline following project requirements
argument-hint: [task-breakdown-path] [task-id] [optional: --interactive] [optional: --template-override]
---

# Content Outline Generator

## Step 1: Process Arguments & Task Context
Outline task to execute: $ARGUMENTS

Parse arguments for:
- Task breakdown file path (required)
- Specific outline task ID (required)
- `--interactive` flag (enables guided outline development)
- `--template-override` (allows custom structure template)

## Step 2: Gather Content Requirements
Read task breakdown and extract outline requirements:

**Asset Information:**
- Content type and purpose from task description
- Target word count and scope
- Success metrics and objectives
- Dependencies and content relationships

**Rule Files to Apply:**
- Structure template from asset specification (e.g., @rules/structure/glossary-faq-enhanced.md)
- Target persona from asset specification (e.g., @rules/personas/ai-curious-professional.md)
- Style guide from asset specification (e.g., @rules/style/technically-writing-style.md)
- Publisher profile for context (e.g., @rules/publisher/publisher-profile.md)

**Verify rule files exist:**
- Check that all referenced rule files are present
- Read each rule file to understand requirements
- Note any special instructions or guidelines

**Research Foundation:**
- Read project research findings
- Review related existing content for inspiration
- Identify key internal links and references

## Step 3: Structure Template Analysis
Load and analyze the specified structure template:

**Template Evaluation:**
- Extract structural outline and section purposes
- Understand content flow logic and progression
- Identify required elements and components
- Note typical length guidelines for each section

**Template Adaptation:**
- Adapt generic template to specific content topic
- Customize section purposes for this asset's objectives
- Adjust scope and depth based on word count target
- Consider audience needs from persona analysis

## Step 4: Interactive Outline Development
**If `--interactive` flag used:**

❓ **Content Focus Questions:**
"Let's develop a focused outline for: [Asset Name]

**Content Angle:**
- What's the primary angle or unique perspective for this piece?
- What key insight or takeaway should readers have?
- How does this connect to your broader content themes?

**Audience Consideration:**
- What level of prior knowledge should we assume?
- What are the main objections or questions to address?
- What action do you want readers to take after reading?

**Content Scope:**
- What topics are essential vs. nice-to-have?
- Are there specific examples or case studies to include?
- What internal content should we reference or link to?"

## Step 5: Research Integration & Content Mapping
**Integrate research findings:**
- Map research insights to appropriate outline sections
- Identify supporting data, statistics, and proof points
- Plan placement of expert quotes and references
- Note fact-checking requirements and source citations

**Content Relationship Mapping:**
- Plan internal linking strategy within outline
- Identify opportunities to reference existing content
- Map content inspirations to specific sections
- Plan cross-promotional elements

## Step 6: Detailed Outline Creation
Read the content outline template from `.claude/system-prompts/content-outline-template.md` and create comprehensive outline following the template structure.

Include YAML frontmatter with:
- Asset metadata and relationships
- Rule file references used
- Project context and dependencies
- Content specifications and requirements

## Step 7: Outline Validation & Refinement
**Structure Quality Check:**
- Verify logical flow and progression
- Ensure all template requirements are met
- Confirm audience needs are addressed
- Validate word count distribution across sections

**Content Completeness Check:**
- All key messages and objectives covered
- Research findings appropriately integrated
- Internal linking strategy comprehensive
- Call-to-action placement strategic

**If outline issues identified:**
❓ "I've identified some areas for outline improvement:
- [Issue 1: and suggested fix]
- [Issue 2: and suggested fix]

Would you like me to:
- Refine the outline automatically
- Work through improvements interactively
- Proceed with current outline
- Start over with different approach"

## Step 8: Outline Finalization & Handoff
**Save completed outline:**
- Create outline file: `/projects/[project]/assets/[asset-name]-outline.md`
- Include complete YAML frontmatter for traceability
- Update task status in task breakdown
- Mark writing task as ready to execute

**Handoff Package:**
```markdown
## Outline Completion Summary
**Outline Created:** `/projects/[project]/assets/[asset-name]-outline.md`
**Word Count Planned:** [X] words across [Y] sections
**Research Integrated:** [X] findings and [Y] references
**Internal Links Planned:** [X] strategic links
**Ready for Writing Task:** [writing-task-id]

**Writer Instructions:**
- Follow section structure and word count targets
- Integrate all planned research and references
- Maintain tone and style specified in outline
- Include all planned CTAs and internal links
```

## Usage Examples

```bash
# Create outline for specific task
/outline-content @projects/launch/task-breakdown.md blog-outline-01

# Interactive outline development
/outline-content @projects/seo-hub/task-breakdown.md guide-outline-01 --interactive

# Use custom structure template
/outline-content @projects/series/task-breakdown.md episode-outline-03 --template-override tutorial-deep-dive

# Quick outline for email content
/outline-content @projects/nurture/task-breakdown.md email-2-outline --interactive
```

## Success Indicators
**A complete content outline should include:**
- ✅ Detailed section breakdown with word count targets
- ✅ Clear purpose and key points for each section
- ✅ Research findings and supporting materials integrated
- ✅ Internal linking strategy planned
- ✅ Call-to-action placement optimized
- ✅ Logical flow aligned with structure template
- ✅ All project objectives and requirements addressed
