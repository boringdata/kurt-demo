# Gap Analysis Project Template

## Goal

Identify content gaps by comparing our documentation against [COMPETITOR] to find topics they cover that we don't. Prioritize gaps by estimated traffic opportunity and strategic value.

This template finds missing content opportunities through competitive analysis.

## Intent Category

**Content Type:** Analysis / Strategy
**Primary Goal:** Identify high-value content gaps to fill
**Audience:** Internal (content strategy planning)
**Analytics-driven:** Yes (traffic opportunity estimation)

## Sources (Ground Truth)

### From Organizational Knowledge Base

*Our existing content:*
- /sources/[our-domain]/

*For comparison and context:*
- Our sitemap/content inventory
- Product roadmap (what we should be covering)
- Customer requests for documentation

### Project-Specific Sources

*Competitor content (must be indexed first):*
```bash
# Index competitor content first
kurt map url [competitor-url]
kurt fetch --url-prefix "[competitor-domain]/"
kurt cluster-urls --url-prefix "[competitor-domain]/"
```

*Add to project:*
- Competitor sitemaps
- Topic cluster analysis
- Customer pain points (support tickets, forums)
- Keyword research data (if available)

## Targets (Content to Update/Create)

### How These Were Identified

**Analysis used:** Topic comparison + traffic estimation

**Step 1: Identify competitor topics**
```bash
# Get competitor content clusters
kurt cluster-urls --url-prefix "[competitor-domain]/" --format table

# List competitor content by topic
kurt content list --url-prefix "[competitor-domain]/[topic]/"
```

**Step 2: Check if we have equivalent content**
```bash
# Search our content for similar topics
kurt content list --url-prefix "[our-domain]/[topic]/"

# Check for semantic matches (if available)
kurt search --query "[topic]" --url-prefix "[our-domain]/"
```

**Step 3: Prioritize gaps**
Estimate value using:
- Competitor's traffic (if available via SEO tools)
- Search volume for topic (if available)
- Strategic importance (core to our product)
- Customer requests

### Content Gaps Identified

**HIGH Priority Gaps** (Strategic + High opportunity)
- [ ] [Topic 1] - Why important: [Core feature, competitor has detailed guide, customer requests]
  - Competitor has: /competitor/path/to/topic1
  - We need: [Type of content - tutorial, reference, guide]
  - Estimated opportunity: [HIGH/MEDIUM/LOW traffic potential]

- [ ] [Topic 2] - Why important: [Reason]
  - Competitor has: /competitor/path/to/topic2
  - We need: [Content type needed]
  - Estimated opportunity: [Traffic potential]

**MEDIUM Priority Gaps** (Good opportunity)
- [ ] [Topic 3] - Why important: [Reason]
  - Competitor has: [path]
  - We need: [Content type]
  - Estimated opportunity: [Traffic potential]

**LOW Priority Gaps** (Nice to have)
- [ ] [Topic 4] - Why important: [Reason]
  - Competitor has: [path]
  - We need: [Content type]
  - Estimated opportunity: [Traffic potential]

### New Content to Create

*Follow-up deliverable:*
- Gap analysis report (this project.md)
- Prioritized content roadmap
- Individual projects for top 3-5 gaps

## Rules Configuration

### Style

*For future gap-filling content:*
- Use rules/style/[appropriate-voice].md based on content type
- Match style to our existing similar content

### Structure

*For gap-filling content:*
- Use rules/structure/[appropriate-type].md
- Study competitor's structure for inspiration (but don't copy)

### Personas

*Target audiences for gap content:*
- Use rules/personas/ matching the topic
- Consider competitor's target audience

### Publisher Profile

*Organizational context:*
- Use rules/publisher/publisher-profile.md
- Ensure new content aligns with our positioning

## Progress

- [ ] Competitor content indexed
- [ ] Topic clusters identified
- [ ] Gaps identified and categorized
- [ ] Traffic opportunity estimated
- [ ] Strategic value assessed
- [ ] Gaps prioritized (HIGH → MEDIUM → LOW)
- [ ] Content roadmap created
- [ ] Follow-up projects created for top gaps

## Next Steps

**Workflow for gap analysis:**

1. **Prerequisites** (One-time setup)
   - Index competitor content using kurt CLI
   - Cluster competitor URLs by topic
   - Get analytics baseline (if available)

2. **Identify Gaps** (3-4 hours)
   - Review competitor topic clusters
   - For each cluster: Check if we have equivalent
   - List topics competitor has that we don't
   - Group by content type (tutorial, reference, guide, etc.)

3. **Estimate Impact** (2-3 hours)
   - For each gap, estimate traffic opportunity:
     - Check SEO tools for search volume
     - Look at competitor's traffic (if available)
     - Consider strategic importance
   - Categorize: HIGH / MEDIUM / LOW opportunity

4. **Prioritize Gaps** (1-2 hours)
   - Score gaps on two dimensions:
     - **Strategic value** (core product feature?)
     - **Traffic opportunity** (high search volume?)
   - **HIGH = Strategic + High traffic**
   - **MEDIUM = Either strategic OR high traffic**
   - **LOW = Neither (but still worth considering)**

5. **Create Content Plan** (1 hour)
   - Select top 3-5 gaps to fill
   - For each: Define content type needed
   - Create timeline for gap-filling
   - Create individual projects for each gap

6. **Execute** (Ongoing)
   - Create projects for top-priority gaps
   - Track: Does new content perform as expected?
   - Monitor: Are we closing the competitive gap?

---

**Prioritization Framework:**

```
           │ High Traffic  │ Med Traffic   │ Low Traffic
           │ Opportunity   │ Opportunity   │ Opportunity
───────────┼───────────────┼───────────────┼─────────────
Strategic  │  🔴 CRITICAL  │  🟡 HIGH      │  🔵 MEDIUM
(core to   │  (Do first)   │               │
product)   │               │               │
───────────┼───────────────┼───────────────┼─────────────
Nice to    │  🟡 HIGH      │  🔵 MEDIUM    │  ⚪ LOW
have       │               │               │
───────────┼───────────────┼───────────────┼─────────────
Not        │  🔵 MEDIUM    │  ⚪ LOW       │  ⚪ LOW
relevant   │  (Question:   │               │ (Skip)
           │   Why do they │               │
           │   have it?)   │               │
```

---

**To use this template:**
1. Clone with `/clone-project gap-analysis`
2. Index competitor content first (prerequisite)
3. Run gap identification process
4. Fill in Targets section with found gaps
5. Prioritize using framework above
6. Create follow-up projects for top 3-5 gaps
