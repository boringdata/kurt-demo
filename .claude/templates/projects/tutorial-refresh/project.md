# Tutorial Refresh Project Template

## Goal

Update outdated tutorials on [TOPIC AREA] prioritized by traffic data. Focus on high-traffic pages that are stale or declining to maximize impact.

This template uses analytics to identify which tutorials need updating most urgently.

## Intent Category

**Content Type:** Content update / Refresh
**Primary Goal:** Improve accuracy and relevance of existing tutorials
**Audience:** Technical (developers using our tutorials)
**Analytics-driven:** Yes (uses traffic data for prioritization)

## Sources (Ground Truth)

### From Organizational Knowledge Base

*Existing tutorials to potentially update:*
- /sources/tutorials/[topic-area]/

*Related documentation for context:*
- Latest API documentation
- Product documentation for current features
- Recent changelog entries

### Project-Specific Sources

*Add research for updates:*
- Latest best practices for [topic]
- Updated code examples
- New tool versions or dependencies
- Customer feedback or common issues
- Competitive tutorials (what others are doing better)

## Targets (Content to Update/Create)

### How These Were Identified

**Analysis used:** Traffic-based prioritization

Run:
```bash
# Find tutorials on topic with analytics
kurt content list \
  --url-prefix "/tutorials/[topic]/" \
  --with-analytics \
  --order-by pageviews_30d desc
```

**Prioritization matrix:**
- **CRITICAL** = High traffic (>75th percentile) + Declining trend
- **HIGH** = High traffic (>75th percentile) + Any trend
- **MEDIUM** = Medium traffic (25th-75th percentile) + Declining
- **LOW** = Lower priority updates

Focus on CRITICAL and HIGH priority items first for maximum impact.

### Existing Content to Update

*Tutorials identified for update (add after running analysis):*

**CRITICAL Priority** (High traffic + declining)
- [ ] /tutorials/[topic]/page1.md - [Brief reason: outdated API, deprecated approach, etc.]
- [ ] /tutorials/[topic]/page2.md - [Brief reason]

**HIGH Priority** (High traffic)
- [ ] /tutorials/[topic]/page3.md - [Brief reason]
- [ ] /tutorials/[topic]/page4.md - [Brief reason]

**MEDIUM Priority** (Medium traffic + declining)
- [ ] /tutorials/[topic]/page5.md - [Brief reason]

## Rules Configuration

### Style

*Tutorial voice:*
- Use rules/style/technical-voice.md or your tutorial style guide
- Maintain consistency with existing tutorial voice

### Structure

*Tutorial structure:*
- Use rules/structure/tutorial.md if extracted
- Follow existing tutorial format for consistency

### Personas

*Target audience:*
- Use rules/personas/developer.md or your technical persona
- Match sophistication level of original tutorials

### Publisher Profile

*Organizational context:*
- Use rules/publisher/publisher-profile.md
- Ensure updated content matches current product terminology

## Progress

- [ ] Traffic analysis completed
- [ ] Tutorials prioritized (CRITICAL → HIGH → MEDIUM)
- [ ] For each tutorial being updated:
  - [ ] Current version reviewed
  - [ ] Outdated sections identified
  - [ ] New code examples tested
  - [ ] Screenshots updated (if needed)
  - [ ] Technical review completed
  - [ ] Published

## Next Steps

**Workflow for traffic-driven tutorial refresh:**

1. **Identify Content** (30-60 min)
   - Run traffic analysis on tutorial section
   - Generate prioritization matrix
   - Select 3-5 top-priority tutorials to update

2. **Prioritize** (15-30 min per tutorial)
   - Review each CRITICAL item
   - Assess: What's outdated? Why is traffic declining?
   - Decide: Quick fix or major rewrite?
   - Plan: What needs updating?

3. **Update Content** (2-3 hours per tutorial)
   - Update outdated information
   - Refresh code examples with current syntax
   - Test all code examples
   - Update screenshots if UI changed
   - Add troubleshooting for new common issues
   - Update "Next steps" or "Further reading"

4. **Technical Review** (Per tutorial)
   - Verify accuracy of updates
   - Test all code examples
   - Check for any new best practices

5. **Publish & Monitor**
   - Publish updated tutorials
   - Monitor traffic trend after update
   - Check if declining trend reverses

---

**To use this template:**
1. Clone with `/clone-project tutorial-refresh`
2. Specify topic area in goal
3. Run traffic analysis to identify tutorials
4. Add identified tutorials to Targets section
5. Prioritize CRITICAL and HIGH items
6. Update tutorials in priority order
