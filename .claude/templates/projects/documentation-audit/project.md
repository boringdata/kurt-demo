# Documentation Audit Project Template

## Goal

Conduct comprehensive traffic audit of [DOMAIN] documentation to identify content issues: stale high-traffic pages, declining traffic, and zero-traffic orphaned content.

This template uses analytics to find systemic documentation health issues.

## Intent Category

**Content Type:** Audit / Analysis
**Primary Goal:** Identify documentation health issues and create action plan
**Audience:** Internal (content team planning)
**Analytics-driven:** Yes (comprehensive traffic analysis)

## Sources (Ground Truth)

### From Organizational Knowledge Base

*Documentation being audited:*
- /sources/[domain]/docs/

*Context for analysis:*
- Sitemap or URL structure
- Content inventory
- Previous audit reports (if any)

### Project-Specific Sources

*Add to this audit:*
- Product changelog (to identify stale content)
- Support ticket data (common issues not in docs)
- Customer feedback on documentation
- Competitor documentation analysis

## Targets (Content to Update/Create)

### How These Were Identified

**Analysis used:** Comprehensive traffic audit

Run:
```bash
# Get traffic overview for domain
kurt content stats \
  --url-prefix "[domain]/" \
  --show-analytics

# Find high-traffic stale content
kurt content list \
  --url-prefix "[domain]/" \
  --with-analytics \
  --pageviews-30d-min MEDIUM \
  --order-by last_modified asc

# Find declining traffic
kurt content list \
  --url-prefix "[domain]/" \
  --with-analytics \
  --pageviews-trend decreasing \
  --order-by pageviews_30d desc

# Find zero-traffic content
kurt content list \
  --url-prefix "[domain]/" \
  --with-analytics \
  --pageviews-30d-max 0
```

### Audit Findings

**Issue Category 1: High-Traffic Stale Content**
*Content with high traffic but outdated (needs refresh)*

- [ ] /docs/page1 - Last updated: [DATE], Traffic: HIGH, Issue: [Outdated API version]
- [ ] /docs/page2 - Last updated: [DATE], Traffic: HIGH, Issue: [Deprecated approach]

**Issue Category 2: Declining Traffic**
*Content losing traffic (needs investigation)*

- [ ] /docs/page3 - Traffic trend: ↓ 45% last 30d, Potential cause: [New competing page? Outdated?]
- [ ] /docs/page4 - Traffic trend: ↓ 30% last 30d, Potential cause: [Product change?]

**Issue Category 3: Zero Traffic (Orphaned)**
*Content with no traffic (deprecated or poor discoverability)*

- [ ] /docs/page5 - 0 pageviews, Decision needed: Archive or improve discoverability?
- [ ] /docs/page6 - 0 pageviews, Decision needed: Remove or update?

**Issue Category 4: Missing Content**
*Gaps identified (high-value topics without documentation)*

- [ ] [Topic] - Identified from: [Support tickets, customer requests, competitor has it]

### New Content to Create

*Audit report deliverable:*
- Comprehensive audit report (this project.md serves as the report)
- Action plan with prioritized fixes
- Recommendations for content strategy

## Rules Configuration

### Style

*For follow-up content updates:*
- Use rules/style/technical-docs.md
- Maintain consistency with existing documentation voice

### Structure

*For documentation pages:*
- Use rules/structure/api-docs.md or appropriate doc type
- Follow established documentation patterns

### Personas

*Documentation audience:*
- Use rules/personas/developer.md or your technical personas
- Consider different experience levels

### Publisher Profile

*Organizational context:*
- Use rules/publisher/publisher-profile.md
- Ensure updated docs use current terminology

## Progress

- [ ] Traffic audit completed
- [ ] Issues categorized
- [ ] Findings prioritized
- [ ] Action plan created
- [ ] Follow-up projects created (if needed)

## Next Steps

**Workflow for documentation audit:**

1. **Run Traffic Audit** (1-2 hours)
   - Run analytics queries for domain
   - Export findings to categories:
     - High-traffic stale
     - Declining traffic
     - Zero traffic
     - Missing content gaps
   - Calculate traffic distribution (percentiles)

2. **Categorize Issues** (2-3 hours)
   - Review each finding
   - Determine root cause
   - Assign priority based on:
     - Traffic volume (impact)
     - Urgency (declining trend)
     - Business importance
   - Document in Targets section above

3. **Create Action Plan** (1 hour)
   - **Immediate actions** (CRITICAL items)
     - High-traffic stale content
     - Rapidly declining pages
   - **Short-term** (HIGH priority)
     - Medium-traffic issues
     - Steady declining pages
   - **Long-term** (MEDIUM/LOW priority)
     - Zero-traffic decisions
     - Content gaps

4. **Create Follow-Up Projects**
   - For major updates: Create dedicated update project
   - For content gaps: Create new content project
   - For archival: Document deprecation plan

5. **Report & Track**
   - Share audit findings with team
   - Create follow-up projects
   - Schedule next audit (quarterly recommended)
   - Track metrics after fixes

---

**Common Audit Findings:**

**High-traffic stale** = Quick wins (update high-impact pages)
**Declining traffic** = Investigate cause (product change? competitor? search ranking?)
**Zero traffic** = Discoverability issue or truly deprecated?
**Missing content** = Opportunity (fill gaps competitors don't have)

---

**To use this template:**
1. Clone with `/clone-project documentation-audit`
2. Specify domain in goal
3. Run traffic analysis queries
4. Categorize findings in Targets section
5. Prioritize: Traffic impact × Urgency
6. Create follow-up projects for major work
