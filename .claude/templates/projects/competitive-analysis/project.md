# Competitive Analysis Project Template

## Goal

Compare our documentation coverage and quality against [COMPETITOR] across shared topics. Identify where we're weaker and create improvement plan to match or exceed competitive quality.

This template analyzes competitive strengths/weaknesses across existing content.

## Intent Category

**Content Type:** Analysis / Quality Benchmark
**Primary Goal:** Identify quality gaps and improvement opportunities
**Audience:** Internal (content quality planning)
**Analytics-driven:** Partially (traffic data helps prioritize)

## Sources (Ground Truth)

### From Organizational Knowledge Base

*Our content for comparison:*
- /sources/[our-domain]/

*Context:*
- Our content strategy and goals
- Product documentation standards
- User feedback on our docs

### Project-Specific Sources

*Competitor content (must be indexed):*
```bash
# Index both our content and competitor's
kurt map url [our-url]
kurt map url [competitor-url]

# Fetch both
kurt fetch --url-prefix "[our-domain]/"
kurt fetch --url-prefix "[competitor-domain]/"

# Cluster to identify topic overlap
kurt cluster-urls --url-prefix "[our-domain]/"
kurt cluster-urls --url-prefix "[competitor-domain]/"
```

*Add to project:*
- Competitor content analysis
- User feedback comparing docs
- SEO performance data (if available)
- Support ticket data (where do users struggle?)

## Targets (Content to Update/Create)

### How These Were Identified

**Analysis used:** Topic-by-topic quality comparison

**Step 1: Identify shared topics**
```bash
# Find topics both we and competitor cover
# Compare cluster names/topics between our-domain and competitor-domain
```

**Step 2: For each shared topic, compare:**
- **Coverage breadth** - How many subtopics covered?
- **Content depth** - How detailed is the explanation?
- **Code examples** - Quality and quantity
- **Visual aids** - Screenshots, diagrams
- **Freshness** - Last updated dates
- **Structure** - Organization and discoverability
- **Completeness** - Missing pieces?

**Step 3: Rate each topic:**
- ✅ **We're stronger** - Our content is more comprehensive/helpful
- 🟡 **Roughly equal** - Similar quality
- ❌ **They're stronger** - Competitor's content is better

### Quality Gaps Identified

**CRITICAL Improvements** (High-traffic topics where we're weaker)
- [ ] [Topic 1] - [Why they're better: More examples, better structure, etc.]
  - Our page: /our-domain/path
  - Their page: /competitor-domain/path
  - Traffic: HIGH (important topic)
  - Gap: [Specific improvements needed]

- [ ] [Topic 2] - [Why they're better]
  - Our page: [path]
  - Their page: [path]
  - Traffic: HIGH
  - Gap: [Improvements needed]

**HIGH Priority Improvements** (Important topics, quality gap)
- [ ] [Topic 3] - [Why they're better]
  - Our page: [path]
  - Their page: [path]
  - Traffic: MEDIUM
  - Gap: [Improvements needed]

**MEDIUM Priority** (Less critical or smaller gaps)
- [ ] [Topic 4] - [Minor improvements]
  - Our page: [path]
  - Their page: [path]
  - Gap: [Improvements needed]

### Our Strengths (No action needed)

*Topics where we're already competitive or better:*
- ✅ [Topic X] - We have better examples
- ✅ [Topic Y] - We cover more edge cases
- ✅ [Topic Z] - Our structure is clearer

### Existing Content to Update

*Pages to improve (pulled from CRITICAL/HIGH above):*
- [ ] /our-domain/topic1 - Improvements: [Add 3 more examples, add diagram, restructure intro]
- [ ] /our-domain/topic2 - Improvements: [Add troubleshooting section, update code examples]
- [ ] /our-domain/topic3 - Improvements: [Add advanced use cases, improve navigation]

### New Content to Create

*Analysis deliverable:*
- Competitive analysis report (this project.md)
- Quality improvement roadmap
- Individual improvement projects for top items

## Rules Configuration

### Style

*For content improvements:*
- Use rules/style/technical-docs.md
- Maintain our voice (don't copy competitor's style)
- Focus on clarity and helpfulness

### Structure

*For content improvements:*
- Use rules/structure/[appropriate-type].md
- Learn from competitor's structure (what works?)
- Maintain our information architecture

### Personas

*Target audiences:*
- Use rules/personas/ for our audience
- Consider if competitor targets different sophistication level

### Publisher Profile

*Organizational context:*
- Use rules/publisher/publisher-profile.md
- Differentiate where appropriate (our unique value)

## Progress

- [ ] Both our and competitor content indexed
- [ ] Shared topics identified
- [ ] Quality comparison completed (topic by topic)
- [ ] Gaps categorized by priority
- [ ] Strengths identified (where we excel)
- [ ] Improvement roadmap created
- [ ] Top 3-5 improvement projects created

## Next Steps

**Workflow for competitive analysis:**

1. **Prerequisites** (One-time setup)
   - Index both our content and competitor's
   - Cluster both by topic
   - Get analytics for traffic prioritization

2. **Coverage Analysis** (2-3 hours)
   - List all topics competitor covers
   - Check which ones we also cover
   - Note: Topics only they cover → Gap Analysis project
   - Focus here on: Shared topics where we might be weaker

3. **Quality Comparison** (4-6 hours, most time-intensive)
   - For each shared topic, compare side-by-side:
     - **Breadth:** Do we cover all the subtopics?
     - **Depth:** Is our explanation as thorough?
     - **Examples:** Do we have enough code examples?
     - **Visuals:** Do they have diagrams we lack?
     - **Structure:** Is their organization clearer?
     - **Completeness:** Are we missing troubleshooting, FAQs, etc.?
   - Rate: ✅ We're better | 🟡 Equal | ❌ They're better

4. **Prioritize Improvements** (1-2 hours)
   - Focus on topics where: ❌ They're better
   - Prioritize by traffic/importance
   - **CRITICAL = High traffic + They're better**
   - **HIGH = Medium traffic + They're better**
   - **MEDIUM = Lower priority improvements**

5. **Create Improvement Plan** (1 hour)
   - For top 3-5 weak topics: Define specific improvements
   - Example: "Add 3 more code examples, create architecture diagram, add troubleshooting section"
   - Create timeline and effort estimates
   - Create individual projects for each improvement

6. **Execute & Monitor** (Ongoing)
   - Implement improvements
   - Track: Did quality improve measurably?
   - Monitor: Did user satisfaction / traffic improve?
   - Re-run analysis quarterly to track progress

---

**Quality Comparison Framework:**

For each shared topic, rate on 1-5 scale:

| Dimension | Us | Them | Gap? | Priority |
|-----------|----|----|------|----------|
| Breadth (subtopics covered) | 3 | 5 | Yes | High |
| Depth (detail level) | 4 | 4 | No | - |
| Code examples | 2 | 5 | Yes | Critical |
| Visual aids | 1 | 4 | Yes | Medium |
| Structure (clarity) | 4 | 3 | No (we're better) | - |
| Freshness | 3 | 5 | Yes | High |

**Overall:** They're stronger → ❌ Needs improvement

---

**To use this template:**
1. Clone with `/clone-project competitive-analysis`
2. Index both our and competitor content (prerequisite)
3. Identify shared topics
4. Complete quality comparison for each
5. Fill in Targets section with gaps found
6. Prioritize: Traffic × Quality gap
7. Create improvement projects for top 3-5 items
