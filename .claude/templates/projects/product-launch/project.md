# Product Launch Campaign Template

## Goal

Launch [PRODUCT/FEATURE NAME] with comprehensive content across multiple formats: announcement blog post, documentation, tutorial, and marketing assets.

This template is for coordinated product launches that require multiple content deliverables.

## Intent Category

**Content Type:** Multi-format campaign (blog, docs, tutorial, marketing)
**Primary Goal:** Drive awareness and adoption of new product/feature
**Audience:** Mixed (technical users, decision-makers, general audience)

## Sources (Ground Truth)

### From Organizational Knowledge Base

*Reference existing organizational content:*
- Product documentation (existing features)
- API documentation
- Related tutorials
- Brand guidelines
- Previous launch announcements (for format/tone reference)

### Project-Specific Sources

*Add to `projects/[project-name]/sources/` for this launch:*
- Product requirements document (PRD)
- Engineering specifications
- Design mockups/prototypes
- Beta user feedback
- Competitive analysis
- Marketing positioning document
- Key messaging from product marketing

## Targets (Content to Update/Create)

### New Content to Create

*Launch deliverables:*

1. **Announcement Blog Post**
   - Format: Feature announcement with value proposition
   - Length: 800-1200 words
   - Includes: Hero image, feature highlights, CTA

2. **Product Documentation**
   - Format: Reference documentation
   - Sections: Overview, Getting Started, API Reference, Examples
   - Length: 2000-3000 words

3. **Tutorial**
   - Format: Step-by-step implementation guide
   - Length: 1500-2000 words
   - Includes: Code examples, screenshots

4. **Quick Start Guide**
   - Format: Concise getting-started
   - Length: 500-800 words
   - Focus: Fastest path to "Hello World"

### Existing Content to Update

*Update related content:*
- Main product overview page (add new feature)
- API reference (add new endpoints)
- Pricing page (if pricing changes)
- FAQ (add new feature questions)

## Rules Configuration

### Style

*Multiple voices needed:*
- **Blog post:** Marketing voice (enthusiastic, value-focused)
- **Documentation:** Technical voice (precise, instructional)
- **Tutorial:** Educational voice (patient, thorough)

Use:
- rules/style/marketing-voice.md for blog post
- rules/style/technical-docs.md for documentation
- rules/style/tutorial-voice.md for tutorials

### Structure

*Templates for each content type:*
- rules/structure/announcement-post.md
- rules/structure/api-documentation.md
- rules/structure/tutorial.md
- rules/structure/quick-start.md

If not extracted, use standard patterns for each content type.

### Personas

*Multiple audiences:*
- Decision-makers (for blog post - focus on business value)
- Developers (for docs/tutorial - focus on implementation)
- Product users (for quick start - focus on immediate value)

Use rules/personas/ for your specific audience profiles.

### Publisher Profile

*Organizational context:*
Use rules/publisher/publisher-profile.md for:
- Product name capitalization
- Company terminology
- Brand voice
- Approved messaging

## Progress

- [ ] Product research completed
- [ ] Messaging and positioning defined
- [ ] Blog post drafted
- [ ] Documentation drafted
- [ ] Tutorial drafted
- [ ] Quick start drafted
- [ ] All code examples tested
- [ ] Screenshots captured
- [ ] Marketing review completed
- [ ] Technical review completed
- [ ] Legal review completed (if needed)
- [ ] All content published
- [ ] Launch promoted (social, email, etc.)

## Next Steps

**Typical workflow for product launches:**

1. **Research & Planning** (1-2 days)
   - Review PRD and specs
   - Identify key features and benefits
   - Define messaging and positioning
   - Determine content deliverables needed

2. **Outlining** (Half day)
   - Create outlines for all deliverables
   - Map feature benefits to content pieces
   - Plan code examples and demos
   - Identify screenshots needed

3. **Content Creation** (1-2 weeks, can parallelize)
   - Draft blog post
   - Write documentation
   - Create tutorial
   - Write quick start guide
   - Test all code examples
   - Capture screenshots

4. **Review & Approval** (3-5 days)
   - Marketing review (messaging, positioning)
   - Technical review (accuracy, code examples)
   - Legal review (if making claims)
   - Product review (feature completeness)

5. **Publication** (1 day)
   - Publish in coordinated sequence
   - Update related existing content
   - Set up redirects if needed
   - Configure analytics tracking

6. **Promotion**
   - Share on social media
   - Send to email list
   - Internal announcement
   - Track engagement metrics

---

**To use this template:**
1. Clone with `/clone-project product-launch`
2. Customize product name and features
3. Add PRD and specs to sources
4. Adjust deliverables based on launch scope
5. Follow the progress checklist
