---
description: Create comprehensive project brief for marketing writing projects
argument-hint: [project-topic] [optional: --research-mode] [optional: project-type]
---

# Project Brief Generator

## Step 1: Initial Project Scoping
Project topic/goal: $ARGUMENTS

Parse arguments for:
- Project topic or objective (required)
- `--research-mode` flag (triggers enhanced research workflow)
- Project type hint (product-launch, campaign, seo-content, thought-leadership, etc.)

## Step 2: Challenge and Clarify Thinking
Before proceeding, challenge the user to clarify their project vision:

❓ **Project Clarification Questions:**

**Primary Objective:**
- What specific business outcome are you trying to achieve with this project?
- How will you measure success? (leads, awareness, engagement, sales, etc.)
- What's the timeline for this project?

**Audience & Context:**
- Who is the primary audience for this content?
- What's the competitive landscape around this topic?
- What's your unique angle or perspective?

**Scope & Resources:**
- Is this a one-time project or recurring content series?
- What's the content distribution strategy? (blog, email, social, paid, etc.)
- Are there any constraints or requirements I should know about?

**Wait for responses before proceeding to Step 3.**

## Step 3: Research Gap Analysis
Based on the clarified project vision, identify research needs:

**Check Available Rule Files:**
1. **Publisher Profile:** Read `rules/publisher/publisher-profile.md` for organizational context
2. **Style Guides:** Review all files in `rules/style/` directory:
   - Look for project-appropriate style (e.g., technically-writing-style.md)
   - Note available voice/tone options for asset assignment
3. **Personas:** Review all files in `rules/personas/` directory:
   - Identify target audience matches (e.g., ai-curious-professional.md)
   - Consider multiple personas if targeting diverse audiences
4. **Structure Templates:** Review all files in `rules/structure/` directory:
   - Match content types to templates (e.g., glossary-faq-enhanced.md, blog-post-deep-dive.md)
   - Note specialized formats for different asset types
5. **Existing Content Library:** Analyze `/cms/` folder and CMS integrations (Sanity, etc.)

**Identify Research Gaps:**
❓ **Research Assessment:**
- Do we have sufficient audience insight for this project?
- Is competitive/market research needed?
- Should we do keyword research for SEO optimization?
- Are there industry trends or data points we need?
- Do we need additional company positioning context?
- **What existing content relates to this project topic?**
- **Are there content gaps we can fill or successful pieces to build upon?**
- **What internal content can we reference, link to, or expand on?**

**If research gaps identified:**
"I've identified some research areas that would strengthen this brief. Would you like me to:
- 🔍 **Keyword Research** (using SEMrush MCP for search volume and competition)
- 🌐 **Market Research** (using web search for trends and competitive analysis)
- 📊 **Industry Data** (using Perplexity for current statistics and insights)
- 🎯 **Audience Research** (additional persona development if needed)
- 📚 **Content Audit** (analyze existing content in /cms and CMS platforms)
- 🔗 **Content Mapping** (identify linking opportunities and content relationships)

Which research areas should I focus on?"

## Step 4: Enhanced Research Execution
**If `--research-mode` or research requested:**

### Keyword Research (if applicable)
Use SEMrush MCP to research:
- Primary keyword opportunities and difficulty
- Related keywords and search intent
- Competitor content gaps
- SERP analysis for content format insights

### Market & Competitive Research
Use web search and Perplexity to gather:
- Current industry trends and news
- Competitor content strategies
- Market data and statistics
- Expert opinions and thought leadership angles

### Content Gap Analysis
- What content exists on this topic?
- What perspectives are missing?
- Where can we add unique value?

### Existing Content Analysis
**Local Content Review** (scan `/cms/` directory):
- Identify related existing content by topic/keyword similarity
- Find high-performing pieces that could inform new content strategy
- Locate content gaps where this project fills missing pieces
- Map potential internal linking opportunities

**CMS Integration Analysis** (if Sanity or other CMS MCP available):
- Query CMS for content related to project topic/keywords
- Analyze content performance data if available
- Identify content series or themes to build upon
- Find successful content formats and structures to replicate

**Research Summary:**
Create `/projects/[project-name]/research-findings.md` with all research insights.

## Step 5: Project Brief Creation
Read the project brief template from `.claude/system-prompts/project-brief-template.md` and create a comprehensive brief.

**Brief Structure:**
1. **Project Overview** (objectives, success metrics, timeline)
2. **Audience & Messaging** (target personas, key messages, positioning)
3. **Content Strategy** (themes, angles, distribution channels)
4. **Asset Inventory** (detailed list of all content pieces to create)
5. **Production Guidelines** (style/structure/persona rules for each asset)
6. **Research Foundation** (key insights driving the strategy)
7. **Success Metrics** (how to measure project effectiveness)

## Step 6: Asset Planning & Rule Assignment
For each content asset in the project:

**Rule Assignment Process:**

1. **Scan available rules** in each directory:
   - `ls rules/style/` → Select appropriate writing style
   - `ls rules/personas/` → Match target audience
   - `ls rules/structure/` → Choose content format template
   - Always include `rules/publisher/publisher-profile.md`

2. **Match rules to content needs:**
   - **Content Type** → Structure template (e.g., glossary-faq-enhanced.md, blog-post-deep-dive.md)
   - **Target Audience** → Persona (e.g., ai-curious-professional.md)
   - **Voice/Tone** → Style guide (e.g., technically-writing-style.md)
   - **Company Context** → Publisher profile (always included)

3. **Validate rule selections:**
   - Ensure selected files exist in the rules directories
   - Verify compatibility between chosen style, persona, and structure
   - Note if new rules need to be extracted/created

**Asset Planning Format:**
```markdown
## Content Asset: [Asset Name]
- **Type:** [Blog post / Landing page / Glossary / Email / etc.]
- **Purpose:** [Specific goal for this asset]
- **Rule Assignments:**
  - **Persona:** @rules/personas/[specific-file.md] (e.g., ai-curious-professional.md)
  - **Style:** @rules/style/[specific-file.md] (e.g., technically-writing-style.md)
  - **Structure:** @rules/structure/[specific-file.md] (e.g., glossary-faq-enhanced.md)
  - **Publisher:** @rules/publisher/publisher-profile.md
- **Priority:** High / Medium / Low
- **Dependencies:** [Any assets this depends on]
- **Internal Links:** [Existing content to reference/link to]
- **Content Inspiration:** [Similar successful pieces to use as reference]
```

## Step 7: Project File Management
Create organized project structure:

```
/projects/[project-name]/
├── project-brief.md              # Master brief
├── research-findings.md          # Research insights
├── assets/                       # Individual content pieces
│   ├── [asset-1-name].md
│   ├── [asset-2-name].md
│   └── ...
└── working-files/               # Drafts, notes, iterations
    ├── asset-notes.md
    └── revision-log.md
```

## Step 8: Brief Review & Refinement
Present the completed brief for review:

❓ **Brief Review:**
"I've created a comprehensive project brief with [X] content assets planned. The brief includes:
- Clear objectives and success metrics
- [X] research insights incorporated
- Detailed asset inventory with rule assignments
- Content analysis and internal linking strategy
- Production timeline and dependencies

Would you like to:
- **Proceed with the brief as-is**
- **Modify specific assets or approach**
- **Add additional research or planning**
- **Begin content production**"

## Usage Examples

```bash
# Basic project brief
/create-project-brief "Q1 product launch campaign"

# With research mode enabled
/create-project-brief "AI industry thought leadership series" --research-mode

# Specific project type
/create-project-brief "SEO content hub for small business tools" seo-content

# Recurring content project
/create-project-brief "Weekly industry newsletter" recurring-content --research-mode
```

## Success Indicators
**A complete project brief should include:**
- ✅ Clear business objectives and success metrics
- ✅ Well-defined target audience and messaging
- ✅ Comprehensive asset inventory with production rules
- ✅ Research-backed content strategy
- ✅ Existing content analysis and linking strategy
- ✅ Realistic timeline and resource allocation
- ✅ Success measurement framework
