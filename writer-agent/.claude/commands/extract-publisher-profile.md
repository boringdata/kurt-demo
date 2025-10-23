---
description: Extract publisher profile from files and URLs
argument-hint: [document-paths-and-urls...] [optional: --overwrite] [optional: filter-criteria]
---

# Publisher Profile Extraction

## Step 1: Process Arguments
Sources to analyze: $ARGUMENTS

Parse for:
- Local document paths (files)
- URLs (websites to fetch and analyze)
- `--overwrite` flag (optional)
- Filter criteria (content-type, page-type, etc.)

## Step 2: Analysis Mode
**Default behavior (incremental):**
- Analyze sources for organizational context
- Compare with existing file in `rules/publisher/`
- Update existing profile or create new one if none exists

**With `--overwrite` flag:**
- Delete existing company profile
- Perform fresh analysis of all sources
- Create completely new company profile

## Step 3: Fetch URLs & Validate Content
**For URLs provided:**
- Use web fetching capability to retrieve content
- Focus on key pages: About, Products/Services, Homepage, Case Studies
- Extract text content for analysis

**For local files:**
- Read and process document content
- Focus on company-facing content, marketing materials, product docs

Show which sources will be analyzed after fetching/filtering.

**If insufficient content found:**
❓ "I found limited organizational context in these sources. Company profile extraction works best with:
- About/Company pages
- Product/Service descriptions
- Marketing materials
- Case studies or customer content

Would you like to:
- Add more sources (URLs or files)?
- Proceed with limited analysis?
- Focus on specific types of content?"

## Step 4: Company Profile Analysis
Analyze all sources for organizational patterns and extract:

**Organizational Identity:**
- Company type (startup, enterprise, agency, publication, etc.)
- Mission and vision statements
- Core values and positioning
- Industry and market focus

**Products & Services:**
- Main offerings and product lines
- Target use cases and applications
- Pricing models and packaging
- Competitive differentiators

**Target Market (ICP):**
- Customer segments and verticals
- Company sizes served
- User personas and decision makers
- Geographic markets

**Messaging & Positioning:**
- Key value propositions
- Brand personality and tone
- Competitive positioning
- Proof points and credibility markers

**Content Strategy:**
- Topics and themes covered
- Content types and formats used
- Thought leadership areas
- Industry expertise claimed

## Step 5: Profile Management
**If publisher profile exists (`rules/publisher/publisher-profile.md`):**
❓ "Found existing publisher profile. How should I proceed:
1. **Update existing profile** with new findings (recommended)
2. **Replace entire profile** with fresh analysis
3. **Create comparison report** showing changes"

**If no profile exists:**
Create new profile at `rules/publisher/publisher-profile.md`

## Step 6: Create/Update Publisher Profile
Read the publisher profile template from `.claude/system-prompts/publisher-profile-template.md` and follow its format.

**For updates:** Add "Recent Analysis" section with new findings and date
**For new profiles:** Create comprehensive profile from scratch

Save as `rules/publisher/publisher-profile.md`

## Usage Examples

```bash
# Analyze company website and local marketing materials
/extract-company-profile https://company.com/about https://company.com/products @docs/marketing/*.md

# Fresh analysis of key company pages
/extract-company-profile https://company.com https://company.com/about https://company.com/pricing --overwrite

# Add case studies and customer content to existing profile
/extract-company-profile @docs/case-studies/*.md @docs/customer-stories/*.md

# Comprehensive analysis combining web and local content
/extract-company-profile https://company.com/about @docs/product-docs/*.md @docs/sales-materials/*.md

# Focus on specific URL types
/extract-company-profile https://company.com/about https://company.com/team content-type:company-info
```

## Web Fetching Strategy
**Priority pages to analyze (if URLs provided):**
1. **Homepage** - Overall positioning and primary messaging
2. **About/Company page** - Mission, vision, company story
3. **Products/Services** - Offerings and value propositions
4. **Pricing** - Business model and target segments
5. **Case Studies/Customers** - ICP and success stories
6. **Blog/Resources** - Thought leadership and content strategy
7. **Team/Leadership** - Company culture and expertise

**Content extraction focus:**
- Headlines and primary messaging
- Product descriptions and benefits
- Customer testimonials and case studies
- Company background and history
- Team expertise and thought leadership

## Output Summary
**Analysis complete report:**
```
✅ Company profile analysis complete
📊 Sources analyzed:
   - 3 web pages fetched
   - 12 local documents processed
📝 Profile action: Updated existing profile
🔍 Key findings:
   - Product portfolio expanded (3 new offerings identified)
   - ICP refined (added mid-market segment)
   - New messaging themes around AI/automation
```

## Behavior Summary
- **Handles both URLs and local files** (flexible input)
- **Web fetching for live company data** (current website content)
- **Default incremental updates** (safe, preserves existing insights)
- **--overwrite for fresh start** (complete replacement when needed)
- **Single company profile** (one source of truth for organizational context)
