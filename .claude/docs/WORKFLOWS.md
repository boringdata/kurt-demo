# Kurt Content Engineering Workflows

**Purpose**: This document defines the ideal workflows Kurt should support, independent of current implementation. Use this as the design spec for CLI and skills architecture.

**Status**: Design document (not implementation)

---

## Table of Contents

1. [Workflow 1: Tutorial Refresh (Bulk Updates)](#workflow-1-tutorial-refresh-bulk-updates)
2. [Workflow 2: Competitive Gap Analysis](#workflow-2-competitive-gap-analysis)
3. [Workflow 3: Product Page Optimization](#workflow-3-product-page-optimization)
4. [Workflow 4: Documentation Audit](#workflow-4-documentation-audit)
5. [Workflow 5: Agency Brand Consistency](#workflow-5-agency-brand-consistency)
6. [Workflow 6: Research → Multi-format Content](#workflow-6-research--multi-format-content)
7. [System Design Summary](#system-design-summary)

---

## Workflow 1: Tutorial Refresh (Bulk Updates)

### User Goal
Update 20-50 tutorials that reference an outdated product feature with new instructions, maintaining consistent voice and structure.

### Ideal Experience

**Step 1: Create project**
```
User: /create-project

Claude: What type of project?
a) Create new content
b) Update existing content
c) Analyze content landscape

User: b) Update existing content

Claude: What are you updating?

User: All tutorials that mention BigQuery need to reference the new Python SDK

Claude: Got it. Let me help you identify which tutorials need updates.
```

**Step 2: Identify stale/affected content**
```
Claude runs:
- content-analysis-skill identify-affected --search-term "BigQuery" --content-type tutorial

Claude: Found 23 tutorials mentioning BigQuery:
- 15 published >365 days ago (likely outdated)
- 8 published <180 days ago (may need minor updates)

Priority groups:
📊 High Priority (365+ days, has code examples): 12 tutorials
🔧 Medium Priority (180-365 days): 3 tutorials
✅ Low Priority (<180 days): 8 tutorials

What should I add as targets?
a) All 23 tutorials
b) Just high priority (12 tutorials)
c) Let me select manually

User: b) Just high priority
```

**Step 3: Analyze update patterns**
```
Claude: Analyzing the 12 tutorials to identify update patterns...

Claude runs:
- content-analysis-skill identify-patterns --targets <12-tutorial-urls>

Claude: I found 3 distinct update patterns:

Pattern 1: "SDK Version Update" (8 tutorials)
- Old: from google.cloud import bigquery_v1
- New: from google.cloud.bigquery import Client
- Affects: import statements + client initialization

Pattern 2: "Query Syntax Change" (3 tutorials)
- Old: client.run_sync_query()
- New: client.query()
- Affects: query execution code blocks

Pattern 3: "Auth Flow Update" (1 tutorial)
- Old: Manual service account JSON
- New: Application Default Credentials
- Affects: setup instructions

Should I save these as update rules?

User: Yes
```

**Step 4: Gather reference sources**
```
Claude: To make these updates accurately, I need reference material. What sources should I use?

Suggested sources:
☐ BigQuery Python SDK docs (latest)
☐ Migration guide (old SDK → new SDK)
☐ Internal specs/notes (if any)

User: First two

Claude runs:
- kurt content add https://cloud.google.com/python/docs/reference/bigquery/latest
- kurt content add https://cloud.google.com/bigquery/docs/migration-guide

Claude: ✓ Fetched 15 pages from SDK docs
✓ Fetched 3 pages from migration guide
✓ Indexed all sources

Sources ready for reference during updates.
```

**Step 5: Extract rules (if needed)**
```
Claude: Before updating, let me check if we have writing rules...

Claude runs:
- project-management-skill check-foundation

Claude: ✓ Publisher profile exists
✓ Primary voice exists
✗ Tutorial structure template not found

I recommend extracting tutorial structure from your existing tutorials to ensure consistency.

Claude runs:
- writing-rules-skill structure --type tutorial --auto-discover

Claude: ✓ Extracted tutorial structure template from 5 high-quality tutorials

Key patterns:
- Introduction → Prerequisites → Step-by-step → Validation → Next steps
- Code blocks with explanations
- Validation checkpoints after each major step

Ready to begin updates?

User: Yes
```

**Step 6: Bulk content updates**
```
Claude: I'll update all 12 tutorials using the patterns and sources we've identified.

For each tutorial, I'll:
1. Create outline showing which sections need updates
2. Generate updated draft with pattern applications tracked
3. Mark which update patterns were applied where

Should I proceed tutorial-by-tutorial or batch process?

User: Batch process, but show me the first one for approval

Claude runs:
- content-writing-skill outline tutorial-refresh bigquery-quickstart

Claude: [Shows outline with marked sections needing updates]

This outline shows:
- Section 3 "Install SDK" → Apply Pattern 1 (SDK version update)
- Section 5 "Run query" → Apply Pattern 2 (Query syntax change)

Look good?

User: Yes, proceed with all

Claude runs (in loop for each tutorial):
- content-writing-skill outline tutorial-refresh <tutorial-name>
- content-writing-skill draft tutorial-refresh <tutorial-name>

Claude: ✓ Generated outlines for 12 tutorials
✓ Generated drafts for 12 tutorials
✓ Applied update patterns consistently

Summary:
- Pattern 1 applied: 8 tutorials
- Pattern 2 applied: 3 tutorials
- Pattern 3 applied: 1 tutorial

All drafts saved to projects/tutorial-refresh/drafts/

Next step: Review and publish?
```

**Step 7: Validate and publish**
```
Claude: Would you like to validate the updates before publishing?

a) Get persona-based feedback for all
b) Spot-check 3 tutorials manually
c) Skip validation, publish all

User: a) Get feedback

Claude runs (for each tutorial):
- content-writing-skill feedback tutorial-refresh <tutorial-name>

Claude: Feedback summary across 12 tutorials:

Developer Persona (primary audience):
- Average alignment: 88%
- Common issues: 2 tutorials missing validation steps (high priority fix)
- Positive: All code examples test correctly

Data Analyst Persona (secondary audience):
- Average alignment: 72%
- Common issues: Jargon not explained in 4 tutorials
- Positive: Step-by-step clarity improved

Critical fixes needed on 2 tutorials. Should I apply them?

User: Yes

Claude runs:
- content-writing-skill edit <tutorial-1> --instructions "Apply critical fixes from feedback"
- content-writing-skill edit <tutorial-2> --instructions "Apply critical fixes from feedback"

Claude: ✓ Applied fixes
All tutorials now >85% aligned with target personas

Ready to publish?

User: Yes

Claude runs:
- content-operations-skill publish --project tutorial-refresh --all

Claude: ✓ Published 12 tutorials
✓ Updated project.md with completion status

Project complete! Summary:
- Updated: 12 tutorials
- Patterns applied: 3 distinct patterns tracked
- Sources referenced: 18 docs
- Average persona alignment: 88%
- Time saved vs manual: ~15 hours
```

### Skills Needed

**content-analysis-skill**
- `identify-affected --search-term <term> --content-type <type>`
- `identify-patterns --targets <urls>`

**content-writing-skill** (already exists)
- `outline <project> <asset>`
- `draft <project> <asset>`
- `feedback <project> <asset>`
- `edit <file> --instructions <text>`

**content-operations-skill** (NEW)
- `publish --project <name> --all`
- `publish --project <name> --targets <list>`

**project-management-skill** (already exists)
- `check-foundation`

**writing-rules-skill** (already exists)
- `structure --type <mode> --auto-discover`

### CLI Commands Needed

**Content querying**
```bash
# Find content by keyword
kurt content search "BigQuery" --content-type tutorial

# Filter by metadata
kurt content list --content-type tutorial --published-before 2024-01-01

# Filter by structural features
kurt content list --has-code-examples true --content-type tutorial
```

**Pattern analysis** (Could be skill-only, not CLI)
```bash
# Analyze differences between versions
kurt content compare <old-url> <new-url> --extract-changes
```

### Data Requirements

**Essential**:
- ✅ `content_type` filter (TUTORIAL)
- ✅ `published_date` range queries
- ✅ `primary_topics` keyword search
- ✅ `has_code_examples` boolean filter
- ✅ Full-text search across content

**Nice-to-have**:
- Content versioning (track before/after)
- Change tracking (what was updated)
- Pattern storage (reusable update patterns)

---

## Workflow 2: Competitive Gap Analysis

### User Goal
Identify topics, content types, and messaging where competitors have strong coverage but we don't.

### Ideal Experience

**Step 1: Create analysis project**
```
User: /create-project

Claude: What type of project?
c) Analyze content landscape

User: c

Claude: What kind of analysis?
☑ Compare topics vs competitor
☑ Compare content quality vs competitor
☐ Identify stale content
☐ Audit documentation completeness

User: [Selects first two]

Claude: Which competitor should I analyze?

User: fivetran.com

Claude: Got it. Let me start by gathering their content.
```

**Step 2: Ingest competitor content**
```
Claude runs:
- kurt content add https://fivetran.com --url-contains /blog/
- kurt content add https://fivetran.com --url-contains /docs/

Claude: ✓ Discovered 145 pages from fivetran.com
✓ Fetched 145 pages
✓ Indexed 145 pages

Content breakdown:
- 67 blog posts
- 45 documentation pages
- 23 guides/tutorials
- 10 product pages

Ready to analyze vs our content?

User: Yes
```

**Step 3: Topic gap analysis**
```
Claude runs:
- content-analysis-skill compare-topics --own docs.ourcompany.com --competitor fivetran.com

Claude: Topic Gap Analysis Complete

Our content: 89 docs analyzed
Their content: 145 docs analyzed

MISSING TOPICS (0 our docs, 5+ their docs):
1. Real-time CDC (0 vs 12) - High opportunity
2. Data governance (0 vs 8) - Medium opportunity
3. Reverse ETL (0 vs 7) - Medium opportunity

UNDERSERVED TOPICS (few our docs, many their docs):
1. Schema migration (2 vs 15) - 7.5x coverage gap
2. Data quality (1 vs 9) - 9x coverage gap
3. API integration (3 vs 12) - 4x coverage gap

WELL-COVERED (competitive parity):
- Data warehouse setup (8 vs 9)
- SQL transformations (12 vs 14)

Saved detailed report to: projects/competitor-analysis/analysis/topic-gap-fivetran.md

What should we do with these findings?
a) Add missing topics as content targets
b) Add their content as learning sources
c) Both

User: c) Both
```

**Step 4: Content quality analysis**
```
Claude runs:
- content-analysis-skill compare-quality --own docs.ourcompany.com --competitor fivetran.com

Claude: Content Quality Comparison

CONTENT TYPE DISTRIBUTION:
Ours:
- Tutorials: 23 (26%)
- Guides: 34 (38%)
- Blogs: 22 (25%)
- Reference: 10 (11%)

Theirs:
- Tutorials: 45 (31%)
- Guides: 45 (31%)
- Blogs: 45 (31%)
- Reference: 10 (7%)

Finding: They have balanced content mix; we're guide-heavy

TUTORIAL QUALITY METRICS:
Our tutorials:
- With code examples: 45% (10/23)
- With step-by-step: 78% (18/23)
- With narrative: 30% (7/23)

Their tutorials:
- With code examples: 82% (37/45)
- With step-by-step: 91% (41/45)
- With narrative: 67% (30/45)

Finding: Quality gap - our tutorials less actionable (code examples) and less engaging (narrative)

BLOG POST ANALYSIS:
Our blogs:
- Avg topics covered: 2.3
- With code examples: 18%
- With narrative: 77%

Their blogs:
- Avg topics covered: 3.1
- With code examples: 42%
- With narrative: 89%

Finding: Their blogs more technical and narrative-driven

Saved detailed report to: projects/competitor-analysis/analysis/quality-comparison-fivetran.md

Recommendations:
1. Add code examples to tutorials (priority: high)
2. Incorporate narrative structure in tutorials (priority: medium)
3. Create content for missing topics (priority: high)

Should I create targets based on these recommendations?

User: Yes, focus on high priority items
```

**Step 5: Create content plan from analysis**
```
Claude: Based on the gap analysis, I recommend:

NEW CONTENT (missing topics):
- 12 pieces on Real-time CDC
- 8 pieces on Data governance
- 7 pieces on Reverse ETL

QUALITY IMPROVEMENTS (existing tutorials):
- Add code examples to 13 tutorials (no examples currently)
- Add narrative structure to 16 tutorials

Total work: 27 new pieces + 29 tutorial updates = 56 content items

This is a large project. How should we prioritize?

User: Start with quality improvements to existing tutorials

Claude: Got it. I'll create a project for tutorial improvements.

Claude runs:
- Create project: tutorial-quality-improvements
- Add 13 tutorials needing code examples as targets
- Add 16 tutorials needing narrative as targets
- Add competitor tutorials as reference sources

Project created: tutorial-quality-improvements

Next steps:
1. Extract structure patterns from competitor tutorials
2. Create improvement plan for each target
3. Begin updates

Ready to continue or should we pause here?

User: Continue

[Project proceeds like Workflow 1]
```

### Skills Needed

**content-analysis-skill** (NEW)
- `compare-topics --own <domain> --competitor <domain>`
- `compare-quality --own <domain> --competitor <domain>`
- `compare-positioning --own <domain> --competitor <domain>`
- `generate-recommendations --analysis-results <results>`

**content-writing-skill** (already exists)
- Used downstream for creating/improving content

**project-management-skill** (already exists)
- Orchestrates the workflow

### CLI Commands Needed

**Aggregation and grouping**
```bash
# Group by content type
kurt content stats --group-by content_type --url-starts-with <domain>

# Group by topic
kurt content stats --group-by topics --url-starts-with <domain>

# Aggregate structural features
kurt content stats --structural-features --url-starts-with <domain>
```

**Filtering**
```bash
# Multi-filter queries
kurt content list \
  --content-type tutorial \
  --has-code-examples false \
  --url-starts-with docs.ourcompany.com
```

**Comparison** (Could be skill-only)
```bash
# Compare two domains
kurt content compare \
  --domain-a docs.ourcompany.com \
  --domain-b fivetran.com \
  --dimensions topics,quality,types
```

### Data Requirements

**Essential**:
- ✅ `content_type` distribution counts
- ✅ `has_code_examples`, `has_step_by_step_procedures`, `has_narrative_structure` boolean filters and aggregations
- ✅ `primary_topics` aggregation (topic → doc count)
- ✅ `tools_technologies` aggregation
- ✅ URL prefix filtering (separate domains)

**Nice-to-have**:
- Content length (word count)
- Reading level
- Semantic similarity clustering (beyond topics)

---

## Workflow 3: Product Page Optimization

### User Goal
Analyze competitor product pages to improve our own positioning, messaging, and conversion.

### Ideal Experience

**Step 1: Gather competitive product pages**
```
User: /create-project

Claude: What type of project?
c) Analyze content landscape

User: c

Claude: What kind of analysis?
☐ Compare topics vs competitor
☑ Analyze product page positioning
☐ Identify stale content

User: Analyze product page positioning

Claude: Which competitors? (You can list multiple)

User: fivetran.com, airbyte.com, stitch.com

Claude: I'll gather their product/landing pages for analysis.

Claude runs:
- kurt content add https://fivetran.com --content-type product_page,landing_page,homepage
- kurt content add https://airbyte.com --content-type product_page,landing_page,homepage
- kurt content add https://stitch.com --content-type product_page,landing_page,homepage

Claude: ✓ Gathered 47 product/landing pages:
- Fivetran: 18 pages
- Airbyte: 16 pages
- Stitch: 13 pages

Now gathering our own product pages...

Claude runs:
- kurt content add https://ourcompany.com --content-type product_page,landing_page,homepage

Claude: ✓ Gathered 12 of our product/landing pages

Ready to analyze?

User: Yes
```

**Step 2: Positioning analysis**
```
Claude runs:
- content-analysis-skill compare-positioning \
    --own ourcompany.com \
    --competitors fivetran.com,airbyte.com,stitch.com

Claude: Positioning Analysis Complete

COMPETITOR POSITIONING THEMES:

Fivetran:
- Value prop: "Zero maintenance data pipelines"
- Target persona: Data engineers tired of pipeline maintenance
- Key differentiators: Fully managed, automated schema migration
- Messaging focus: Reliability (99.9% uptime), hands-off operation

Airbyte:
- Value prop: "Open-source data integration"
- Target persona: Engineers who want control + flexibility
- Key differentiators: 300+ connectors, open-source, customizable
- Messaging focus: Flexibility, community, no vendor lock-in

Stitch:
- Value prop: "Simple data integration"
- Target persona: Analysts who need quick setup
- Key differentiators: Easy UI, quick setup, affordable
- Messaging focus: Simplicity, speed to value

OUR POSITIONING (from publisher profile + product pages):
- Value prop: "Modern data integration platform"
- Target persona: [Currently unclear - mixed messaging]
- Key differentiators: [Not clearly stated]
- Messaging focus: Feature lists (not benefit-driven)

GAPS & OPPORTUNITIES:

1. **Unclear positioning** (HIGH PRIORITY)
   - We don't clearly state WHO we're for
   - Competitors have sharp persona targeting (engineers vs analysts)
   - Recommendation: Choose positioning lane (reliability, flexibility, or simplicity)

2. **Feature-focused vs benefit-focused** (HIGH PRIORITY)
   - Our pages list features ("300 connectors", "real-time sync")
   - Competitors lead with benefits ("Save 20 hours/week", "Zero maintenance")
   - Recommendation: Rewrite with benefit-first messaging

3. **Missing differentiation** (MEDIUM PRIORITY)
   - Competitors clearly state what makes them different
   - We say "modern" but don't explain what that means
   - Recommendation: Identify 2-3 unique differentiators

4. **Narrative structure gap** (MEDIUM PRIORITY)
   - Competitor pages: 67% use narrative structure
   - Our pages: 25% use narrative structure
   - Recommendation: Add customer stories, problem → solution narratives

Saved detailed report to: projects/product-page-optimization/analysis/positioning-comparison.md

What would you like to do?
a) Rewrite our product pages with clearer positioning
b) Extract positioning patterns from top competitor pages
c) Both

User: c) Both
```

**Step 3: Extract competitor patterns**
```
Claude runs:
- writing-rules-skill structure --type landing-page --from-sources <competitor-pages>

Claude: ✓ Extracted landing page structure patterns

Pattern 1: "Problem → Solution → Proof" (Fivetran style)
- Hero: Problem statement (pain point)
- Section 1: Solution overview (how it solves)
- Section 2: Key benefits (specific outcomes)
- Section 3: Social proof (logos, testimonials)
- Section 4: How it works (simple 3-step)
- CTA: Strong action-oriented

Pattern 2: "Feature → Benefit → Use Case" (Airbyte style)
- Hero: Core feature (open-source, 300+ connectors)
- Section 1: Why it matters (control, flexibility)
- Section 2: Use cases (by role/industry)
- Section 3: Technical depth (for engineers)
- Section 4: Community proof (GitHub stars, contributors)
- CTA: Try it free / Get started

Pattern 3: "Quick Win → Easy Process" (Stitch style)
- Hero: Speed promise ("Setup in 5 minutes")
- Section 1: Simple 3-step process
- Section 2: What you can do immediately
- Section 3: Pricing transparency
- Section 4: Support + resources
- CTA: Start free trial

Saved structure patterns to: rules/structure/landing-page-competitor-patterns.md

Which pattern aligns best with our positioning?

User: We should position like Fivetran - reliability and automation

Claude: Good choice. I'll use Pattern 1 (Problem → Solution → Proof) for rewrites.
```

**Step 4: Rewrite product pages**
```
Claude: I'll rewrite our 12 product pages using:
- Fivetran's structure pattern (Problem → Solution → Proof)
- Benefit-first messaging
- Clearer positioning for data engineers

Should I create drafts for all 12 pages?

User: Yes

Claude runs (for each page):
- content-writing-skill outline product-page-optimization <page-name>
- content-writing-skill draft product-page-optimization <page-name>

Claude: ✓ Created outlines for 12 product pages
✓ Generated drafts for 12 product pages

Key improvements:
- All pages now lead with pain point (not features)
- Benefit-driven headlines ("Save 20 hours/week" vs "Automated pipelines")
- Narrative structure throughout (67% → 100%)
- Clear CTA (specific action, not vague "Learn more")

Example before/after:

BEFORE:
"Modern Data Integration Platform
- 300+ connectors
- Real-time sync
- Learn more →"

AFTER:
"Stop Babysitting Data Pipelines
Your data engineers shouldn't spend 20 hours/week fixing broken pipelines.
Our fully automated platform keeps data flowing while your team builds what matters.
See how it works →"

All drafts saved to: projects/product-page-optimization/drafts/

Ready to review?

User: Show me 3 examples

[Claude shows 3 drafts, user approves]

User: Looks great, publish all

Claude runs:
- content-operations-skill publish --project product-page-optimization --all

Claude: ✓ Published 12 product pages
Project complete!
```

### Skills Needed

**content-analysis-skill** (NEW)
- `compare-positioning --own <domain> --competitors <domains>`
- `analyze-messaging --pages <urls>`

**writing-rules-skill** (already exists)
- `structure --type landing-page --from-sources <urls>`

**content-writing-skill** (already exists)
- `outline`, `draft`, `feedback`, `edit`

**content-operations-skill** (NEW)
- `publish --project <name> --all`

### CLI Commands Needed

**Content type filtering**
```bash
# Get only product/landing pages
kurt content list --content-type product_page,landing_page,homepage

# Get pages with narrative structure
kurt content list --content-type landing_page --has-narrative-structure true
```

**Metadata extraction**
```bash
# Get descriptions for SEO analysis
kurt content list --format json --fields url,title,description

# Get structural features for quality analysis
kurt content list --format json --fields url,has_narrative_structure,has_code_examples
```

### Data Requirements

**Essential**:
- ✅ `content_type` filter (PRODUCT_PAGE, LANDING_PAGE, HOMEPAGE)
- ✅ `has_narrative_structure` boolean filter
- ✅ `description` field (for meta description analysis)
- ✅ Full-text search for messaging analysis

**Nice-to-have**:
- Conversion metrics (if integrated with analytics)
- A/B test tracking
- Message theme extraction (LLM-based)

---

## Workflow 4: Documentation Audit

### User Goal
Identify gaps, inconsistencies, and quality issues across an entire documentation site.

### Ideal Experience

**Step 1: Ingest all documentation**
```
User: /create-project

Claude: What type of project?
c) Analyze content landscape

User: c

Claude: What kind of analysis?
☐ Compare topics vs competitor
☐ Analyze product page positioning
☑ Audit documentation completeness

User: Audit documentation completeness

Claude: What's your documentation domain?

User: docs.ourcompany.com

Claude: I'll gather all documentation for analysis.

Claude runs:
- kurt content add https://docs.ourcompany.com

Claude: ✓ Discovered 234 documentation pages
✓ Fetched 234 pages
✓ Indexed 234 pages

Content breakdown:
- 89 tutorials
- 67 guides
- 45 reference docs
- 33 conceptual explanations

Ready to audit?

User: Yes
```

**Step 2: Completeness audit**
```
Claude runs:
- content-analysis-skill audit-completeness --domain docs.ourcompany.com

Claude: Documentation Completeness Audit

TOPIC COVERAGE ANALYSIS:
✓ Analyzed 234 docs across 47 primary topics

Well-covered topics (5+ docs each):
- Authentication (12 docs)
- Data connectors (23 docs)
- Transformations (15 docs)

Underserved topics (1-2 docs each):
- Security (2 docs) - Critical gap!
- Monitoring (1 doc) - Critical gap!
- Disaster recovery (0 docs) - MISSING!

CONTENT TYPE GAPS:
For each major topic, ideal mix is:
- Tutorial (hands-on)
- Guide (how-to)
- Reference (API/config)
- Concept (explainer)

Topics with gaps:
1. Security: Has 1 reference, 1 concept. MISSING: Tutorial, Guide
2. Monitoring: Has 1 guide. MISSING: Tutorial, Reference, Concept
3. Data quality: Has 3 tutorials. MISSING: Reference, Concept

STRUCTURAL QUALITY ISSUES:

Tutorials without code examples (26 found):
- "Getting Started with Connectors" (should have code!)
- "Query Optimization Tutorial" (should have code!)
[... 24 more]

Guides without step-by-step procedures (12 found):
- "How to Configure Alerts" (needs steps!)
- "How to Set Up Monitoring" (needs steps!)
[... 10 more]

Reference docs without... references (API specs, config options):
- "Configuration Reference" (only has 3 options listed, incomplete)
- "REST API Reference" (missing error codes section)

CONSISTENCY ISSUES:

Inconsistent terminology:
- "Data pipeline" vs "Pipeline" vs "Integration" (used interchangeably)
- "Sync" vs "Replication" vs "Transfer" (same concept, 3 names)

Recommendation: Create terminology guide

Saved detailed audit to: projects/documentation-audit/analysis/completeness-audit.md

What should we tackle first?
a) Fill critical topic gaps (Security, Monitoring)
b) Fix quality issues (add code examples, procedures)
c) Create missing content types
d) All of the above (create prioritized plan)

User: d) All of the above
```

**Step 3: Create prioritized improvement plan**
```
Claude: I'll create a prioritized plan based on:
- Criticality (security > features)
- User impact (high-traffic pages first)
- Effort (quick wins vs large projects)

PRIORITY 1 - Critical Gaps (2-3 weeks):
- [ ] Create Security Tutorial (hands-on setup)
- [ ] Create Security Guide (best practices)
- [ ] Create Monitoring Tutorial (setup walkthrough)
- [ ] Create Disaster Recovery Guide

PRIORITY 2 - Quality Fixes (1-2 weeks):
- [ ] Add code examples to 26 tutorials
- [ ] Add step-by-step procedures to 12 guides
- [ ] Complete Configuration Reference (missing options)

PRIORITY 3 - Content Type Gaps (3-4 weeks):
- [ ] Create 15 missing reference docs
- [ ] Create 8 missing concept explainers
- [ ] Create 12 missing tutorials

Total: 78 content items across 3 priority levels

Should I create projects for each priority level?

User: Yes, start with Priority 1

Claude: Creating project: docs-audit-priority-1

Claude runs:
- Create project with 4 content items as targets
- Check if relevant sources exist (product specs, internal docs)
- Extract rules for security/ops content (may differ from feature content)

Project created. Let's gather sources for these topics.

What sources should we use for Security and Monitoring content?
a) Our internal security specs
b) Industry best practices (gather from web)
c) Both

User: c) Both

[Project continues with content creation workflow]
```

**Step 4: Cluster-based navigation audit** (Optional advanced feature)
```
Claude: One more thing - I can analyze your documentation structure using topic clustering.

This helps identify:
- Related docs that aren't cross-linked
- Topics that should be grouped but aren't
- Navigation hierarchy issues

Should I run this analysis?

User: Yes

Claude runs:
- kurt content cluster --url-starts-with docs.ourcompany.com

Claude: ✓ Identified 12 topic clusters across 234 docs

Cluster Analysis:

Cluster: "Data Connectors" (45 docs)
- Well-structured
- Clear hierarchy: Overview → Individual connector docs → Troubleshooting

Cluster: "Authentication & Security" (14 docs)
- ISSUE: Scattered across 3 different navigation sections
- Recommendation: Group under single "Security" section

Cluster: "SQL Transformations" (23 docs)
- ISSUE: Related docs not cross-linked
  - "Writing SQL Queries" and "Query Optimization" should link to each other
  - "Testing Transformations" should link from all SQL docs

Cluster: "API Reference" (12 docs)
- ISSUE: Alphabetically organized, not by use case
- Recommendation: Group by workflow (Setup APIs, Data APIs, Admin APIs)

Saved detailed cluster report to: projects/documentation-audit/analysis/cluster-navigation.md

Should I add navigation improvements to the project plan?

User: Yes, as Priority 4

Claude: ✓ Added 15 navigation/cross-linking tasks to project

Updated plan now includes:
- P1: Critical content gaps (4 items)
- P2: Quality fixes (38 items)
- P3: Content type gaps (35 items)
- P4: Navigation improvements (15 items)

Total: 92 items

Ready to start on Priority 1?

User: Yes

[Proceeds with content creation]
```

### Skills Needed

**content-analysis-skill** (NEW)
- `audit-completeness --domain <domain>`
- `audit-quality --domain <domain>`
- `audit-consistency --domain <domain>`
- `identify-gaps --domain <domain> --framework <framework>`

**content-writing-skill** (already exists)
- Used for creating missing content

**project-management-skill** (already exists)
- Orchestrates multi-phase audit → fix workflow

### CLI Commands Needed

**Topic and content type analysis**
```bash
# Topics with doc counts
kurt content stats --group-by topics --url-starts-with docs.ourcompany.com

# Content types per topic
kurt content stats --group-by topics,content_type --url-starts-with docs.ourcompany.com

# Find structural issues
kurt content list --content-type tutorial --has-code-examples false
kurt content list --content-type guide --has-step-by-step-procedures false
```

**Clustering**
```bash
# Already exists
kurt content cluster --url-starts-with docs.ourcompany.com
```

**Cross-referencing** (Advanced)
```bash
# Find related but not linked docs
kurt content find-related --url <url> --not-linked-from <url>
```

### Data Requirements

**Essential**:
- ✅ `primary_topics` aggregation (topics → doc counts)
- ✅ `content_type` + `primary_topics` cross-tabulation
- ✅ `has_code_examples`, `has_step_by_step_procedures` filters
- ✅ Topic clustering (already exists)

**Nice-to-have**:
- Content freshness (last updated date)
- Internal linking analysis (which docs link to each other)
- Terminology extraction (inconsistent terms used)
- Reading level analysis

---

## Workflow 5: Agency Brand Consistency

### User Goal
Ensure multiple writers/clients maintain consistent voice, style, and quality across all content.

### Ideal Experience

**Step 1: Establish baseline**
```
User: /create-project

Claude: What type of project?
a) Create new content

User: a) Create new content

Claude: For which client/brand?

User: Acme Analytics (new client)

Claude: Is this your first project for Acme Analytics?

User: Yes

Claude: Great! For a new client, I recommend setting up their foundation first:
1. Gather sample content (their existing blog/docs)
2. Extract their brand voice and style
3. Extract their target personas
4. Create their publisher profile

This ensures all content matches their brand. Should we do this now?

User: Yes

Claude: Let's start by gathering their existing content.

What content sources should I analyze?
a) Their existing blog
b) Their existing documentation
c) Their marketing pages
d) All of the above

User: d) All of the above

Claude runs:
- kurt content add https://acmeanalytics.com/blog
- kurt content add https://acmeanalytics.com/docs
- kurt content add https://acmeanalytics.com --content-type product_page,landing_page

Claude: ✓ Gathered 87 pieces of Acme Analytics content:
- 34 blog posts
- 31 documentation pages
- 22 marketing pages

Now I'll extract their brand patterns...

Claude runs:
- writing-rules-skill publisher --auto-discover --source acmeanalytics.com
- writing-rules-skill style --type primary --auto-discover --source acmeanalytics.com
- writing-rules-skill persona --audience-type all --auto-discover --source acmeanalytics.com

Claude: ✓ Extracted brand foundation

Publisher Profile (Acme Analytics):
- Company identity: B2B analytics platform for healthcare
- Value proposition: "Simplify patient data analysis"
- Tone: Professional but approachable, empathetic
- Key themes: Patient outcomes, regulatory compliance, ease of use

Primary Voice:
- Sentence structure: Medium length (15-20 words avg)
- Vocabulary: Technical terms explained simply
- POV: Mix of "we" (platform) and "you" (user)
- Formality: Professional with occasional warmth

Target Personas (3 identified):
1. Healthcare Data Analyst (primary)
   - Technical level: Intermediate
   - Pain points: Regulatory complexity, data silos
   - Communication style: Prefers step-by-step, visual aids

2. Hospital IT Director (secondary)
   - Technical level: High-level
   - Pain points: Security, integration complexity
   - Communication style: Bottom-line focused, ROI-driven

3. Clinical Researcher (tertiary)
   - Technical level: Domain expert, not technical
   - Pain points: Data access, statistical rigor
   - Communication style: Evidence-based, peer-reviewed sources

Saved brand foundation to:
- rules/publisher/acme-analytics-profile.md
- rules/style/acme-analytics-primary-voice.md
- rules/personas/healthcare-data-analyst.md
- rules/personas/hospital-it-director.md
- rules/personas/clinical-researcher.md

Foundation complete! Now when we create content for Acme Analytics, it will match their brand.

What content do you need to create for them?

User: 10 blog posts about new analytics features
```

**Step 2: Create content with brand consistency**
```
Claude: Creating 10 blog posts for Acme Analytics.

I'll ensure each post:
- Matches their professional-but-approachable voice
- Targets the right persona (Data Analyst primary, IT Director secondary)
- Follows their blog structure patterns
- Uses their terminology and style

But first, let me check if we have their blog structure pattern...

Claude runs:
- writing-rules-skill structure --type blog --auto-discover --source acmeanalytics.com

Claude: ✓ Extracted blog post structure

Acme Analytics Blog Structure:
- Title: Benefit-driven, includes use case
- Opening: Problem statement (1-2 sentences)
- Section 1: Context/background (why this matters)
- Section 2: Feature explanation (how it works)
- Section 3: Use case example (real scenario)
- Section 4: Getting started (3 simple steps)
- Closing: CTA to documentation or trial

Ready to create blog posts. What are the topics?

User: [Lists 10 feature topics]

Claude runs (for each post):
- content-writing-skill outline blog-acme-features <post-name>
- content-writing-skill draft blog-acme-features <post-name>
- content-writing-skill feedback blog-acme-features <post-name>

Claude: ✓ Created 10 blog post drafts

Persona alignment scores:
- Healthcare Data Analyst: 91% avg (excellent!)
- Hospital IT Director: 84% avg (good)
- Clinical Researcher: 78% avg (acceptable for secondary audience)

Brand consistency check:
- Voice match: 94% (all posts match primary voice)
- Structure compliance: 100% (all posts follow blog template)
- Terminology: 96% (using Acme's preferred terms)

All posts saved to: projects/blog-acme-features/drafts/

Ready for client review?

User: Yes
```

**Step 3: Quality gates before client delivery**
```
Claude: Before sending to the client, let me run final quality checks:

Claude runs:
- content-analysis-skill check-consistency --project blog-acme-features

Claude: Consistency Check Results:

VOICE CONSISTENCY: ✓ Pass
- All 10 posts use similar sentence structure
- Tone is uniform across posts
- Vocabulary level consistent

STRUCTURAL CONSISTENCY: ✓ Pass
- All posts follow blog structure template
- Section lengths similar (±20%)
- CTA placement consistent

TERMINOLOGY CONSISTENCY: ⚠ Review needed
- Post 3 uses "EHR integration" (good - Acme's term)
- Post 7 uses "Electronic Health Record integration" (inconsistent - too formal)
- Recommendation: Edit Post 7 to use "EHR integration"

PERSONA TARGETING: ✓ Pass
- All posts appropriate for Healthcare Data Analyst
- Technical depth consistent
- Pain points addressed uniformly

Should I fix the terminology issue in Post 7?

User: Yes

Claude runs:
- content-writing-skill edit projects/blog-acme-features/drafts/post-7.md \
    --instructions "Replace 'Electronic Health Record integration' with 'EHR integration' to match brand terminology"

Claude: ✓ Fixed terminology in Post 7

All quality checks now passing. Content is ready for client delivery!

Summary for client:
- 10 blog posts created
- 94% brand voice match
- 91% primary persona alignment
- 100% structure compliance
- All terminology standardized

Shall I export these for client review?

User: Yes

Claude runs:
- content-operations-skill export --project blog-acme-features --format docx --include-metadata

Claude: ✓ Exported 10 blog posts to: projects/blog-acme-features/exports/
Each file includes:
- Draft content
- Metadata (word count, reading level, persona scores)
- Sources referenced
- Brand compliance scores

Ready to send to client!
```

**Step 4: Handle client feedback**
```
[One week later, client provides feedback]

User: Client reviewed posts. They want:
1. Post 3: More emphasis on HIPAA compliance
2. Posts 5, 7: Add real customer examples
3. Overall: Slightly more technical depth

Claude: Got it. Let me update the posts with that feedback.

For the HIPAA emphasis and customer examples, I'll need sources. Do you have:
- HIPAA compliance documentation?
- Customer case studies I can reference?

User: Yes [provides internal docs]

Claude runs:
- kurt content add ./acme-hipaa-compliance.pdf
- kurt content add ./acme-case-studies.pdf

Claude: ✓ Added sources

Now applying client feedback...

Claude runs:
- content-writing-skill edit projects/blog-acme-features/drafts/post-3.md \
    --instructions "Add section on HIPAA compliance, reference acme-hipaa-compliance.pdf"
- content-writing-skill edit projects/blog-acme-features/drafts/post-5.md \
    --instructions "Add customer example from case studies"
- content-writing-skill edit projects/blog-acme-features/drafts/post-7.md \
    --instructions "Add customer example from case studies"
- content-writing-skill edit-batch projects/blog-acme-features/drafts/*.md \
    --instructions "Increase technical depth slightly - add 1-2 more technical details per section"

Claude: ✓ Applied all feedback

Re-running quality checks...

Claude runs:
- content-analysis-skill check-consistency --project blog-acme-features

Claude: Updated consistency check:

VOICE CONSISTENCY: ✓ Pass (still 94%)
- Technical depth increased but voice maintained

PERSONA ALIGNMENT:
- Healthcare Data Analyst: 93% avg (improved!)
- Hospital IT Director: 89% avg (improved with more technical depth)

All edits tracked in version history. Ready for final client approval?

User: Yes

[Content approved and published]
```

### Skills Needed

**writing-rules-skill** (already exists)
- `publisher --auto-discover --source <domain>`
- `style --type primary --auto-discover --source <domain>`
- `structure --type <type> --auto-discover --source <domain>`
- `persona --audience-type all --auto-discover --source <domain>`

**content-writing-skill** (already exists)
- `outline`, `draft`, `feedback`, `edit`
- `edit-batch` (NEW - apply same edit to multiple files)

**content-analysis-skill** (NEW)
- `check-consistency --project <name>`
- `check-brand-compliance --project <name> --brand <brand-name>`

**content-operations-skill** (NEW)
- `export --project <name> --format <format> --include-metadata`

### CLI Commands Needed

**Brand/source filtering**
```bash
# List content by domain for rule extraction
kurt content list --url-starts-with acmeanalytics.com

# Filter by content type for structure extraction
kurt content list --url-starts-with acmeanalytics.com --content-type blog
```

**Metadata for quality checks**
```bash
# Get author attribution (who wrote what)
kurt content list --format json --fields url,author,published_date

# Useful for finding style variations by author
kurt content stats --group-by author --url-starts-with acmeanalytics.com
```

### Data Requirements

**Essential**:
- ✅ URL prefix filtering (separate clients/brands)
- ✅ `content_type` filtering
- ✅ `primary_topics`, `tools_technologies` for rule extraction
- ✅ Structural features for quality checking

**Nice-to-have**:
- `author` field (track who writes what style)
- Content versioning (track edits over time)
- Reading level scores
- Sentiment/tone analysis

---

## Workflow 6: Research → Multi-format Content

### User Goal
Take research findings and create multiple content formats (blog, tutorial, guide, case study, product page) from the same source material.

### Ideal Experience

**Step 1: Conduct research**
```
User: I need to create content about the latest trends in real-time data streaming

Claude: Let me start with research to gather current information.

Claude runs:
- research-skill query "latest trends in real-time data streaming 2025" --recency month

Claude: ✓ Research complete

Key findings:
- Apache Kafka 4.0 introduces major improvements to exactly-once semantics
- Serverless streaming platforms gaining adoption (AWS Kinesis, Google Pub/Sub)
- Real-time CDC (Change Data Capture) becoming standard practice
- Schema evolution and registry management critical for production

Sources:
- 8 technical blogs (Apache, Confluent, AWS)
- 4 vendor announcements
- 2 conference talks (Kafka Summit, DataEngConf)

Full research saved to: sources/research/2025-10-30-real-time-streaming-trends.md

This is rich material. What content formats do you want to create from this?

User: Multiple formats - blog post, tutorial, guide, and case study

Claude: Great! Let me help you create all four formats from this research.
```

**Step 2: Create content strategy**
```
Claude: For "Real-time Data Streaming Trends", here's my recommended content mix:

1. **Blog Post** (800-1200 words)
   - Audience: Data engineers, architects
   - Purpose: Awareness, thought leadership
   - Angle: "5 Real-Time Streaming Trends Transforming Data Engineering in 2025"
   - Key points: Kafka 4.0, serverless, CDC, schema management
   - Tone: Forward-looking, industry insights

2. **Tutorial** (2000-3000 words)
   - Audience: Hands-on data engineers
   - Purpose: Skill building
   - Angle: "Implementing Exactly-Once Semantics with Kafka 4.0"
   - Key points: Step-by-step setup, code examples, validation
   - Tone: Instructional, detailed

3. **Guide** (1500-2500 words)
   - Audience: Platform teams, architects
   - Purpose: Decision-making
   - Angle: "Choosing Between Kafka and Serverless Streaming: A Practical Guide"
   - Key points: Comparison framework, use cases, tradeoffs
   - Tone: Analytical, balanced

4. **Case Study** (1000-1500 words)
   - Audience: Business stakeholders, senior engineers
   - Purpose: Proof of concept
   - Angle: "How [Company] Achieved Sub-Second Data Freshness with Real-Time CDC"
   - Key points: Problem, solution, results (metrics)
   - Tone: Narrative, results-focused

Does this content mix look good?

User: Yes, but we don't have a real case study. Can we create a hypothetical one?

Claude: Absolutely. I'll create a realistic hypothetical case study based on common patterns from the research.

Creating project: real-time-streaming-content
```

**Step 3: Create multi-format content**
```
Claude: I'll create all 4 formats from the same research foundation.

But first, let me check what rules we have...

Claude runs:
- project-management-skill check-foundation

Claude: Foundation check:
✓ Publisher profile exists
✓ Primary voice exists
✓ Developer persona exists
✗ Blog structure not found
✗ Tutorial structure not found
✗ Guide structure not found
✗ Case study structure not found

I need structure templates for these content types. Should I:
a) Extract from our existing content
b) Use industry best practices
c) Skip (I'll create free-form)

User: a) Extract from our existing content

Claude runs:
- writing-rules-skill structure --type blog --auto-discover
- writing-rules-skill structure --type tutorial --auto-discover
- writing-rules-skill structure --type guide --auto-discover
- writing-rules-skill structure --type case-study --auto-discover

Claude: ✓ Extracted 4 structure templates

Now creating content...

Claude runs:
- content-writing-skill outline real-time-streaming-content blog-streaming-trends
- content-writing-skill draft real-time-streaming-content blog-streaming-trends

- content-writing-skill outline real-time-streaming-content tutorial-kafka-exactly-once
- content-writing-skill draft real-time-streaming-content tutorial-kafka-exactly-once

- content-writing-skill outline real-time-streaming-content guide-kafka-vs-serverless
- content-writing-skill draft real-time-streaming-content guide-kafka-vs-serverless

- content-writing-skill outline real-time-streaming-content case-study-realtime-cdc
- content-writing-skill draft real-time-streaming-content case-study-realtime-cdc

Claude: ✓ Created 4 content pieces from research

Summary:

1. Blog Post: "5 Real-Time Streaming Trends Transforming Data Engineering in 2025"
   - 1,150 words
   - Cites 8 research sources
   - Forward-looking tone ✓
   - Developer persona: 89% aligned

2. Tutorial: "Implementing Exactly-Once Semantics with Kafka 4.0"
   - 2,650 words
   - 7 code examples
   - Step-by-step procedures ✓
   - Developer persona: 94% aligned

3. Guide: "Choosing Between Kafka and Serverless Streaming"
   - 2,100 words
   - Comparison framework with decision tree
   - Analytical tone ✓
   - Developer persona: 87% aligned

4. Case Study: "How HealthTech Corp Achieved Sub-Second Data Freshness"
   - 1,400 words
   - Narrative structure ✓
   - Results-focused with metrics
   - Developer persona: 82% aligned (slightly technical for business stakeholders)

All drafts saved to: projects/real-time-streaming-content/drafts/

Issues found:
- Case study may be too technical for business stakeholders
- Should I adjust for mixed audience (business + technical)?

User: Yes, make case study accessible to business stakeholders too

Claude runs:
- content-writing-skill edit projects/real-time-streaming-content/drafts/case-study-realtime-cdc.md \
    --instructions "Adjust for business stakeholders: less technical jargon, focus on business outcomes (cost savings, time to insight), add executive summary"

Claude: ✓ Updated case study

Re-checked persona alignment:
- Developer persona: 78% (slightly less technical, as intended)
- Business persona: 91% (much improved!)
- Mixed audience goal achieved

All 4 pieces now ready!
```

**Step 4: Cross-link and package**
```
Claude: These 4 pieces work together. Should I add cross-links between them?

Suggested cross-links:
- Blog → Tutorial ("Want hands-on practice? See our tutorial")
- Blog → Guide ("Not sure which platform? Read our guide")
- Tutorial → Guide ("Choosing a platform first? Read our guide")
- Case Study → Tutorial ("See how to implement this yourself")

User: Yes, add those links

Claude runs:
- content-writing-skill add-cross-references --project real-time-streaming-content

Claude: ✓ Added 6 cross-references between pieces

Content package complete!

Publishing plan:
- Week 1: Publish blog post (awareness)
- Week 2: Publish guide (decision-making)
- Week 3: Publish tutorial (skill-building)
- Week 4: Publish case study (social proof)

This creates a content funnel:
Blog (awareness) → Guide (consideration) → Tutorial (activation) → Case Study (validation)

Should I create this publishing schedule?

User: Yes

Claude: ✓ Created publishing schedule in project.md

All 4 pieces ready to publish on schedule!
```

### Skills Needed

**research-skill** (already exists)
- `query <question> --recency <timeframe>`

**writing-rules-skill** (already exists)
- `structure --type <type> --auto-discover`

**content-writing-skill** (already exists)
- `outline`, `draft`, `edit`
- `add-cross-references --project <name>` (NEW)

**project-management-skill** (already exists)
- Orchestrates multi-format workflow

**content-operations-skill** (NEW)
- `schedule-publish --project <name> --timeline <timeline>`

### CLI Commands Needed

**Research management**
```bash
# Already exists via research-skill
kurt research search "<query>" --recency <timeframe> --save
kurt research list
```

**Content querying** (for finding existing structures to extract)
```bash
kurt content list --content-type blog,tutorial,guide,case_study
```

### Data Requirements

**Essential**:
- ✅ `content_type` filtering (to extract different structure templates)
- ✅ Research storage (already exists - not in Kurt DB)
- ✅ Structure rules for each content type

**Nice-to-have**:
- Content relationship tracking (which pieces link to which)
- Publishing schedule metadata
- Content funnel analytics (awareness → consideration → activation)

---

## System Design Summary

### Skills Matrix

| Skill | Operations | Used In Workflows |
|-------|-----------|-------------------|
| **content-analysis-skill** (NEW) | identify-affected<br>identify-patterns<br>compare-topics<br>compare-quality<br>compare-positioning<br>audit-completeness<br>check-consistency | 1, 2, 3, 4, 5 |
| **content-writing-skill** (exists) | outline<br>draft<br>feedback<br>edit<br>edit-batch (NEW)<br>add-cross-references (NEW) | 1, 2, 3, 4, 5, 6 |
| **content-operations-skill** (NEW) | publish<br>export<br>schedule-publish | 1, 3, 5, 6 |
| **writing-rules-skill** (exists) | publisher<br>style<br>structure<br>persona | 1, 3, 4, 5, 6 |
| **research-skill** (exists) | query<br>daily<br>discover | 6 |
| **project-management-skill** (exists) | create-project<br>resume-project<br>check-foundation | All |

### CLI Commands Matrix

| Command Category | Commands Needed | Priority | Notes |
|-----------------|----------------|----------|-------|
| **Content Querying** | `kurt content list`<br>`kurt content search` | P0 | Add filters: content_type, published_before/after, has_code_examples, has_step_by_step_procedures, has_narrative_structure |
| **Content Stats** | `kurt content stats --group-by <field>` | P1 | Aggregate by: topics, content_type, domain, author |
| **Content Clustering** | `kurt content cluster` | P0 | Already exists |
| **Content Addition** | `kurt content add` | P0 | Already exists |
| **Content Indexing** | `kurt content index` | P0 | Already exists |
| **Research** | `kurt research search`<br>`kurt research list` | P0 | Already exists |

### Metadata Requirements

| Field | Currently Exists? | Populated By | Used In Workflows | Priority |
|-------|------------------|--------------|-------------------|----------|
| `content_type` | ✅ Yes | Indexing (LLM) | All | P0 |
| `published_date` | ✅ Yes | Fetch (HTML meta) | 1, 2, 4 | P0 |
| `primary_topics` | ✅ Yes | Indexing (LLM) | All | P0 |
| `tools_technologies` | ✅ Yes | Indexing (LLM) | 2, 4 | P1 |
| `has_code_examples` | ✅ Yes | Indexing (LLM) | 1, 2, 4 | P0 |
| `has_step_by_step_procedures` | ✅ Yes | Indexing (LLM) | 1, 2, 4 | P0 |
| `has_narrative_structure` | ✅ Yes | Indexing (LLM) | 2, 3, 5 | P1 |
| `description` | ✅ Yes | Fetch (HTML meta) | 3, 4 | P1 |
| `author` | ✅ Yes | Fetch (HTML meta) | 5 | P2 |
| `title` | ✅ Yes | Fetch (HTML meta) | All | P0 |
| `is_chronological` | ✅ Yes | Discovery | 4 | P2 |
| `discovery_method` | ✅ Yes | Discovery | N/A | P3 |
| `discovery_url` | ✅ Yes | Discovery | N/A | P3 |

### Data Operations Needed

| Operation | Description | Implement Where? | Priority |
|-----------|-------------|------------------|----------|
| **Filter by content_type** | `--content-type tutorial,guide` | CLI + document.py | P0 |
| **Filter by date range** | `--published-before/after` | CLI + document.py | P0 |
| **Filter by boolean flags** | `--has-code-examples true` | CLI + document.py | P0 |
| **Full-text search** | Search within content | CLI + new module | P1 |
| **Aggregate by field** | Group by topics, content_type, etc. | CLI + document.py | P1 |
| **Topic search** | Find docs about specific topic | CLI + document.py | P1 |

### Skills Architecture

**Tier 1: Orchestration Skills** (coordinate workflows)
- project-management-skill
- research-skill

**Tier 2: Domain Skills** (specialized operations)
- content-analysis-skill (NEW)
- content-writing-skill (exists)
- writing-rules-skill (exists)
- content-operations-skill (NEW)

**Tier 3: CLI Tool** (data layer)
- kurt-core (document storage, retrieval, indexing)

**Pattern**: Orchestration skills call domain skills, domain skills call CLI tool

---

## Implementation Priorities

### Phase 1: Foundation (Current + Minor Extensions)
**Goal**: Support Workflow 1 (Tutorial Refresh) and Workflow 5 (Brand Consistency)

**CLI Changes**:
- Add `--content-type` filter to `list` command
- Add `--published-before/after` filters to `list` command
- Add `--has-code-examples/step-by-step/narrative` filters to `list` command

**Skills Changes**:
- Create `content-analysis-skill` with:
  - `identify-affected` operation
  - `identify-patterns` operation
  - `check-consistency` operation
- Extend `content-writing-skill` with:
  - `edit-batch` operation

**Estimated effort**: 1-2 weeks

### Phase 2: Competitive Analysis (Extensions)
**Goal**: Support Workflow 2 (Competitive Gap) and Workflow 3 (Product Page Optimization)

**CLI Changes**:
- Add `kurt content stats --group-by <field>` command
- Add topic aggregation to stats

**Skills Changes**:
- Extend `content-analysis-skill` with:
  - `compare-topics` operation
  - `compare-quality` operation
  - `compare-positioning` operation
- Create `content-operations-skill` with:
  - `publish` operation
  - `export` operation

**Estimated effort**: 2-3 weeks

### Phase 3: Documentation Audit (Advanced)
**Goal**: Support Workflow 4 (Documentation Audit)

**CLI Changes**:
- Add `kurt content search` command (full-text)
- Add cross-tabulation to stats (e.g., topics × content_type)

**Skills Changes**:
- Extend `content-analysis-skill` with:
  - `audit-completeness` operation
  - `audit-quality` operation

**Estimated effort**: 2-3 weeks

### Phase 4: Multi-format Content (Polish)
**Goal**: Support Workflow 6 (Research → Multi-format)

**Skills Changes**:
- Extend `content-writing-skill` with:
  - `add-cross-references` operation
- Extend `content-operations-skill` with:
  - `schedule-publish` operation

**Estimated effort**: 1 week

---

## Open Questions

1. **Content versioning**: Should kurt-core track content versions over time?
   - Use case: Track before/after for bulk updates
   - Alternative: Git handles this at file level

2. **Publishing integration**: Should kurt-core integrate with CMS platforms for publishing?
   - Already exists via `kurt cms` commands
   - May need deeper integration for scheduling

3. **Analytics integration**: Should we track content performance metrics?
   - Use case: Prioritize updates based on traffic
   - Probably out of scope for v1

4. **Pattern storage**: Should update patterns be stored in DB or as files?
   - Patterns identified in Workflow 1 could be reusable
   - Lean toward files (like rules) for simplicity

5. **Full-text search**: How sophisticated should content search be?
   - Simple keyword search (SQLite FTS)?
   - Vector search (requires embeddings)?
   - Start simple, evolve based on need

---

## Next Steps

1. Review this design document
2. Identify any missing workflows or use cases
3. Prioritize which workflows to implement first
4. Design kurt-core CLI changes needed for Phase 1
5. Design content-analysis-skill architecture
6. Begin implementation

