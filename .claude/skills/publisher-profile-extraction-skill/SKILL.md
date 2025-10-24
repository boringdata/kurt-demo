# Publisher Profile Extraction Skill

Extract organizational context from company web pages and content to create a publisher profile for brand-consistent content creation.

## Purpose

Analyze company websites, marketing materials, and product documentation to build comprehensive organizational context (identity, products, target market, messaging, thought leadership) and save as a publisher profile in `/rules/publisher/publisher-profile.md`.

## When to Use

- **During project setup**: After collecting organizational content sources
- **Brand consistency needed**: Ensure content aligns with company messaging
- **New team members**: Build understanding of organizational voice and positioning
- **Messaging updates**: Refresh profile after rebrand or positioning change

## Prerequisites
## Content Discovery Method

> **⚠️ This skill uses file-based content maps (not Kurt CLI database)**
>
> All document discovery uses content map queries:
> - Query: `cat sources/<domain>/_content-map.json | jq ...`
> - Fetch: Use WebFetch tool (hooks auto-save + index)
> - Reference: See `.claude/docs/CONTENT-MAP-QUERIES.md` for query patterns


- Company web pages (About, Products, Pricing, etc.) OR
- Local marketing/product documentation
- Access to public company information

## Usage

### Discovery Mode (Recommended)

Ask user upfront: **Auto-discover or manual selection?**

**Option A: Auto-discover key pages (recommended)**
```bash
# Skill will discover key company pages from content map and propose them
invoke publisher-profile-extraction-skill --auto-discover

# Process:
# 1. Search content map for key marketing pages
# 2. Show discovered pages to user
# 3. User approves or refines list
# 4. Fetch (if needed) and extract
```

**Option B: Manual selection**
```bash
# User provides specific URLs or file paths
invoke publisher-profile-extraction-skill with sources: <URLs-and-file-paths>
```

**Option C: Hybrid (auto-discover + user refinement)**
```bash
# Discover + user adds/removes specific pages
invoke publisher-profile-extraction-skill --auto-discover --include <additional-url> --exclude <url-pattern>
```

### Auto-Discovery Process

When user chooses auto-discover, use Kurt's content map to find key pages:

**Step 1: Search for key page types**

```bash
# Homepage (root domain)
kurt document list --url-prefix https://company.com/ | grep -E "^https://[^/]+/?$"

# About/Company pages
kurt document list --url-contains /about
kurt document list --url-contains /company
kurt document list --url-contains /team
kurt document list --url-contains /leadership

# Product/Features pages
kurt document list --url-contains /product
kurt document list --url-contains /features
kurt document list --url-contains /pricing
kurt document list --url-contains /solutions

# Customer/Case study pages (for ICP insights)
kurt document list --url-contains /customer
kurt document list --url-contains /case-stud
kurt document list --url-contains /success-stor

# Blog homepage (for content strategy insights)
kurt document list --url-contains /blog/ | head -1
```

**Step 2: Show proposed list to user**

```
Found key company pages in content map:

✓ Homepage: https://company.com/
✓ About: https://company.com/about
✓ Products: https://company.com/products
✓ Pricing: https://company.com/pricing
✓ Case Studies: https://company.com/customers/case-studies
✓ Blog: https://company.com/blog/

Would you like to:
a) Use these pages (recommended)
b) Add/remove specific pages
c) Start over with manual selection
```

**Step 3: Fetch if needed**

```bash
# Check which pages are already fetched
cat sources/<domain>/_content-map.json | jq -r '.sitemap["<url>"] | select(.status == "FETCHED")'

# Fetch missing pages
for url in <proposed-urls>; do
  status=$(kurt document list --url $url | grep "status:")
  if [[ $status == *"NOT_FETCHED"* ]]; then
    # Use WebFetch tool for $url (hooks auto-save + index)
  fi
done
```

**Step 4: Extract from fetched content**

```bash
# Read content from /sources/
# Run extraction analysis
# Create/update publisher profile
```

### Initial Profile Creation
```bash
# Analyze sources and create new publisher profile
invoke publisher-profile-extraction-skill with sources: <URLs-and-file-paths>

# Or use auto-discovery
invoke publisher-profile-extraction-skill --auto-discover
```

### Incremental Update (Default - Recommended)
```bash
# Add new findings to existing profile
invoke publisher-profile-extraction-skill with sources: <URLs-and-file-paths>
```

**Behavior:**
1. Checks if `/rules/publisher/publisher-profile.md` exists
2. If exists: Adds "Recent Analysis" section with new findings and date
3. If not: Creates comprehensive new profile

### Overwrite Mode (Nuclear Option)
```bash
# Delete existing profile and create fresh analysis
invoke publisher-profile-extraction-skill with sources: <URLs-and-file-paths> --overwrite
```

**Behavior:**
1. Deletes existing publisher profile
2. Performs fresh analysis of all sources
3. Creates completely new publisher profile

## Discovery Patterns for Key Pages

### Standard URL Patterns by Page Type

**Homepage (always highest priority):**
```bash
# Root domain URLs
kurt document list --url-prefix https://company.com/ | grep -E "^https://[^/]+/?$"
```

**About/Company:**
```bash
kurt document list --url-contains /about
kurt document list --url-contains /company
kurt document list --url-contains /who-we-are
kurt document list --url-contains /our-story
kurt document list --url-contains /team
kurt document list --url-contains /leadership
```

**Products/Services:**
```bash
kurt document list --url-contains /product
kurt document list --url-contains /features
kurt document list --url-contains /platform
kurt document list --url-contains /solutions
```

**Business Model:**
```bash
kurt document list --url-contains /pricing
kurt document list --url-contains /plans
```

**Customer/ICP:**
```bash
kurt document list --url-contains /customer
kurt document list --url-contains /case-stud
kurt document list --url-contains /success-stor
kurt document list --url-contains /testimonial
```

**Content Strategy:**
```bash
# Blog homepage (not individual posts)
kurt document list --url-contains /blog/ | grep -E "blog/?$"
# Resources/content hub
kurt document list --url-contains /resource
kurt document list --url-contains /content
```

### Discovery Priority Order

1. **Must have** (fail if missing):
   - Homepage

2. **Should have** (warn if missing):
   - About/Company page
   - At least 1 product/service page

3. **Nice to have**:
   - Pricing page
   - Customer stories
   - Blog homepage
   - Team/leadership

### Example Discovery Workflow

```bash
# 1. Discover all company URLs in content map
kurt document list --url-prefix https://company.com/ --status NOT_FETCHED

# 2. Filter for key page types
# Homepage
homepage=$(kurt document list --url-prefix https://company.com/ | grep -E "^https://company\.com/?$")

# About pages
about_pages=$(kurt document list --url-prefix https://company.com/ --url-contains /about)

# Product pages
product_pages=$(kurt document list --url-prefix https://company.com/ --url-contains /product)

# 3. Show proposed list
echo "Found key pages:"
echo "Homepage: $homepage"
echo "About: $about_pages"
echo "Products: $product_pages"

# 4. Get user approval
# 5. Fetch if needed
# 6. Extract from /sources/
```

## Input Types

### Web Sources (from Content Map)
**Priority pages to analyze (via auto-discovery):**
1. **Homepage** - Overall positioning and primary messaging
2. **About/Company page** - Mission, vision, company story
3. **Products/Services** - Offerings and value propositions
4. **Pricing** - Business model and target segments
5. **Case Studies/Customers** - ICP and success stories
6. **Blog/Resources** - Thought leadership and content strategy
7. **Team/Leadership** - Company culture and expertise

**Discovery Strategy:**
- Use `kurt document list` to search content map
- Filter by URL patterns for each page type
- Check fetch status and fetch if needed
- Read from `/sources/` for analysis

### Local Files
- Marketing materials
- Product documentation
- Sales decks and collateral
- Internal brand guidelines
- Customer-facing content

## What Gets Extracted

### Organizational Identity
- Company type and stage (startup, enterprise, agency, etc.)
- Mission, vision, and core values
- Industry and market focus
- Market position (leader, challenger, niche specialist)

### Products & Services
- Core offerings and product lines
- Target use cases and applications
- Pricing models and packaging
- Competitive differentiators

### Target Market & ICP
- Customer segments and verticals
- Company sizes served
- User personas and decision makers
- Geographic markets

### Messaging & Positioning
- Key value propositions
- Brand personality and tone
- Competitive positioning
- Proof points and credibility markers

### Content Strategy
- Topics and themes covered
- Content types and formats used
- Thought leadership areas
- Industry expertise claimed

### Company Culture & Team
- Leadership background and credentials
- Team expertise and specialization
- Industry recognition
- Work style and values in action

## Single Profile Pattern

Unlike other extraction skills (which create multiple files), this skill maintains **one canonical publisher profile**:
- **File location**: `/rules/publisher/publisher-profile.md`
- **Update pattern**: Incremental additions with dated "Recent Analysis" sections
- **Overwrite option**: Complete replacement when organizational context changes significantly

## Output Format

Publisher profile includes:
- **YAML frontmatter**: Metadata for tracking and searchability
- **Sources Analyzed**: Web pages and local files used
- **Organizational Identity**: Company type, mission, vision, industry focus
- **Products & Services**: Core offerings, business model, differentiation
- **Target Market & ICP**: Customer segments, company sizes, personas
- **Messaging & Positioning**: Value props, brand personality, competitive positioning
- **Content & Thought Leadership Strategy**: Topics, formats, expertise areas
- **Company Culture & Team**: Leadership, expertise, recognition
- **Usage Guidelines**: How to apply profile in content creation
- **Content Avoid List**: What doesn't align with company positioning

## Workflow Integration

### Pattern 1: Project Setup with Publisher Profile
```
1. Create project → 2. Extract publisher profile → 3. Use for brand consistency → 4. Work on content
```

### Pattern 2: Profile Update During Project
```
1. Working on content → 2. New positioning discovered → 3. Update publisher profile → 4. Apply to content
```

### Pattern 3: Brand Guidelines Reference
```
1. Creating content → 2. Check publisher profile → 3. Ensure messaging alignment → 4. Publish
```

## Validation

**Sufficient Sources Check:**
- Works best with About/Company pages, product descriptions, marketing materials
- Warns if limited organizational context found
- Prompts to add more sources for comprehensive profile

**Quality Indicators:**
- More diverse sources = more complete profile
- Company web pages = current positioning
- Marketing materials = active messaging themes
- Customer content = real-world value delivery

## Directory Management

**Automatic Directory Creation:**
- Skill creates `/rules/publisher/` if it doesn't exist
- No manual setup required
- Works on first use

## Usage in Content Creation

When creating or updating content:
1. **Check publisher profile**: Review messaging, tone, positioning
2. **Align value props**: Use consistent value propositions
3. **Match brand personality**: Apply tone and voice guidelines
4. **Reference differentiators**: Emphasize competitive advantages
5. **Use proof points**: Include credibility markers and evidence

## Output Example

```
✅ Publisher profile extraction complete

📊 Sources analyzed:
   - 5 web pages fetched:
     • Homepage
     • About page
     • Products page
     • Customer stories
     • Blog posts
   - 3 local documents processed:
     • Product positioning deck
     • Sales collateral
     • Brand guidelines

📝 Profile action: Created new profile
   Location: /rules/publisher/publisher-profile.md

🔍 Key findings:
   - Organization: B2B SaaS, Series B growth stage
   - Primary market: Enterprise data teams
   - Core differentiation: AI-powered automation + reliability
   - Brand tone: Expert yet approachable, innovation-focused
   - Thought leadership: Data engineering best practices
```

## Related Skills

- **style-extraction-skill**: Extract writing voice and tone patterns (complements publisher tone)
- **persona-extraction-skill**: Extract audience targeting (complements ICP definition)
- **project-management-skill**: Uses publisher profile for brand consistency checks

## Template Reference

Uses: `.claude/system-prompts/publisher-profile-template.md`

## Best Practices

1. **Start with company website**: Homepage, About, Products pages provide strong foundation
2. **Include customer content**: Case studies and testimonials reveal real value delivery
3. **Update incrementally**: Add new findings as company evolves
4. **Review regularly**: Keep profile current with company positioning
5. **Use for onboarding**: New team members get comprehensive company context
6. **Reference during creation**: Check profile before creating customer-facing content

## Key Insight

The publisher profile is the **organizational voice and context layer** that ensures all content:
- Aligns with company messaging and positioning
- Uses consistent value propositions
- Matches brand personality and tone
- Emphasizes appropriate differentiators
- Reflects current product/market focus

This complements style guides (how to write), structure templates (how to organize), and personas (who to write for) with **what the company stands for and how it positions itself**.
