# Persona Extraction Skill

Extract audience targeting patterns from existing content to create audience persona profiles.

## Purpose

Analyze content to identify who it's written for - inferred roles, technical level, pain points, goals, and communication preferences - and save them as persona profiles in `/rules/personas/` for use in content creation projects.

## When to Use

- **During project setup**: After collecting ground truth sources
- **When rule matching fails**: No appropriate persona exists for target audience
- **For content updates**: Need to match existing audience targeting
- **New content creation**: Building persona foundation from target examples

## Prerequisites
## Content Discovery Method

> **⚠️ This skill uses file-based content maps (not Kurt CLI database)**
>
> All document discovery uses content map queries:
> - Query: `cat sources/<domain>/_content-map.json | jq ...`
> - Fetch: Use WebFetch tool (hooks auto-save + index)
> - Reference: See `.claude/docs/CONTENT-MAP-QUERIES.md` for query patterns


- Minimum 3-5 substantial documents for reliable extraction
- Documents should target consistent audience(s)
- Content stored in `/sources/` or accessible file paths

## Usage

### Discovery Mode (Recommended)

Ask user upfront: **Auto-discover or manual selection?**

**Option A: Auto-discover by audience type**
```bash
# Extract personas for distinct audience segments
invoke persona-extraction-skill --audience-type all --auto-discover

# Or target specific audience segments
invoke persona-extraction-skill --audience-type technical --auto-discover
invoke persona-extraction-skill --audience-type business --auto-discover
invoke persona-extraction-skill --audience-type customer --auto-discover
```

**Option B: Manual selection**
```bash
# User provides specific documents
invoke persona-extraction-skill with documents: <file-paths>
```

**Option C: Hybrid (auto-discover + user refinement)**
```bash
# Discover + user adds/removes specific documents
invoke persona-extraction-skill --audience-type all --auto-discover --include <path> --exclude <pattern>
```

### Auto-Discovery Process

**Key Principle:** Persona extraction requires **diverse sampling** across content targeting different audiences.

**For Technical/Developer Personas:**

```bash
# Step 1: Discover technical content
docs=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "guide" and .value.status == "FETCHED") | .key')
api_refs=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "reference" and .value.status == "FETCHED") | .key')
guides=$(kurt document list --url-contains /guide --status FETCHED)
tutorials=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "tutorial" and .value.status == "FETCHED") | .key')

# Step 2: Sample technical content (5-10 for pattern detection)
sample=$(echo "$docs $api_refs $guides $tutorials" | head -10)

# Step 3: Show proposed list
echo "Found technical content for developer persona extraction:"
echo "✓ 4 documentation pages"
echo "✓ 2 API references"
echo "✓ 4 guides/tutorials"
echo "Total: 10 pages (technical audience)"

# Step 4: User approves or refines

# Step 5: Extract technical persona
# Create: /rules/personas/technical-implementer.md or /rules/personas/developer.md
```

**For Business/Executive Personas:**

```bash
# Discover business-focused content
product_pages=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "product_page" and .value.status == "FETCHED") | .key')
solutions=$(kurt document list --url-contains /solution --status FETCHED)
case_studies=$(kurt document list --url-contains /case-stud --status FETCHED)
pricing=$(kurt document list --url-contains /pricing --status FETCHED)
blog_business=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "blog" and .value.status == "FETCHED") | .key' | grep -E "(roi|business|strategy|leadership)")

# Sample business content (5-10 for pattern)
sample=$(echo "$product_pages $solutions $case_studies $pricing $blog_business" | head -10)
```

**For Customer/End-User Personas:**

```bash
# Discover customer-facing content
support=$(kurt document list --url-contains /support --status FETCHED)
help=$(kurt document list --url-contains /help --status FETCHED)
faq=$(kurt document list --url-contains /faq --status FETCHED)
getting_started=$(kurt document list --url-contains /getting-started --status FETCHED)

# Sample customer content (5-10 for pattern)
sample=$(echo "$support $help $faq $getting_started" | head -10)
```

**For All Personas (Discover Multiple):**

```bash
# Step 1: Sample diverse content types
technical=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "guide" and .value.status == "FETCHED") | .key' | head -5)
business=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "product_page" and .value.status == "FETCHED") | .key' | head -5)
customer=$(kurt document list --url-contains /support --status FETCHED | head -5)
blog=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "blog" and .value.status == "FETCHED") | .key' | head -5)

# Step 2: Combine samples
all_content=$(echo "$technical $business $customer $blog")

# Step 3: Show proposed list
echo "Found diverse content for persona extraction:"
echo "✓ 5 technical docs (developer persona)"
echo "✓ 5 product pages (business persona)"
echo "✓ 5 support pages (customer persona)"
echo "✓ 5 blog posts (mixed personas)"
echo "Total: 20 pages (diverse audience targeting)"

# Step 4: User approves

# Step 5: Extract multiple personas
# May create: /rules/personas/technical-implementer.md
#            /rules/personas/business-decision-maker.md
#            /rules/personas/end-user.md
```

### Discovery Patterns by Audience Type

| Audience Type | Content Sources | URL Patterns | Sample Size |
|---------------|----------------|--------------|-------------|
| Technical/Developer | Docs, API, Guides, Tutorials | `/docs/`, `/api/`, `/guide`, `/tutorial`, `/reference` | 5-10 docs |
| Business/Executive | Product, Solutions, Case Studies | `/product`, `/solution`, `/case-stud`, `/pricing`, `/roi` | 5-10 pages |
| Customer/End-User | Support, Help, FAQ, Getting Started | `/support`, `/help`, `/faq`, `/getting-started` | 5-10 pages |
| Marketing/Prospects | Landing, Campaign, Blog | `/landing`, `/campaign`, `/blog/` | 5-10 pages |
| Enterprise | Enterprise features, Security, Compliance | `/enterprise`, `/security`, `/compliance` | 5-10 pages |
| SMB/Startup | Pricing, Simple guides, Quick starts | `/pricing`, `/quick`, `/simple` | 5-10 pages |

### Incremental Mode (Default - Recommended)
```bash
# Analyze documents and add new personas if found
# Keeps existing persona profiles untouched
invoke persona-extraction-skill with documents: <file-paths>

# Or use auto-discovery
invoke persona-extraction-skill --audience-type all --auto-discover
```

**Behavior:**
1. Reads existing persona profiles in `/rules/personas/`
2. Analyzes provided documents for audience targeting patterns
3. Compares findings with existing personas
4. Creates new persona profile only if distinct audience found
5. Reports "No new personas detected" if audiences already captured

### Overwrite Mode (Nuclear Option)
```bash
# Delete all existing persona profiles and create fresh analysis
invoke persona-extraction-skill with documents: <file-paths> --overwrite
```

**Behavior:**
1. Deletes all files in `/rules/personas/`
2. Performs fresh analysis on all provided documents
3. Creates completely new persona library

## What Gets Extracted

### Audience Characteristics (Inferred from Content)
- **Language Complexity**: Technical depth and vocabulary used
- **Problems Addressed**: Pain points and challenges content targets
- **Solutions Emphasized**: Benefits and outcomes highlighted
- **Objections Handled**: Concerns content addresses
- **Industry References**: Context and terminology used
- **Role-Specific Terms**: Job titles and responsibilities mentioned
- **Knowledge Assumptions**: What content assumes audience knows

### Persona Attributes
- **Likely Job Roles**: Inferred from content focus and terminology
- **Company Size**: Based on scale of problems discussed
- **Technical Level**: Beginner, intermediate, expert
- **Decision Authority**: Individual contributor, influencer, decision-maker

### Metadata Tracked
- Documents analyzed (count and file paths)
- Extraction date and command used
- Job roles, company size, technical level, decision authority

## Auto-Naming Logic

Persona profiles get descriptive names based on:
- **Job role/title**: ceo, developer, marketer, analyst
- **Company size**: enterprise, mid-market, small-business, startup
- **User type**: decision-maker, implementer, end-user, influencer
- **Industry context**: saas, ecommerce, healthcare, finance

**Example outputs:**
- `enterprise-decision-maker.md`
- `technical-implementer.md`
- `small-business-owner.md`
- `developer-end-user.md`

## Multi-Pattern Detection

Single analysis can identify multiple distinct personas:
```
✅ Analysis complete
📝 Created 3 new persona profiles:
   - enterprise-decision-maker.md
   - technical-implementer.md
   - end-user-practitioner.md
```

## Output Format

Each persona profile includes:
- **YAML frontmatter**: Metadata for tracking and searchability
- **Documents Analyzed**: Source files used for extraction
- **Persona Overview**: Clear summary of who this represents
- **Inferred Role & Context**: Job title, company size, technical level, authority
- **Pain Points Addressed**: Primary challenges and concerns
- **Goals & Motivations**: What persona wants to achieve
- **Language & Communication Style**: How content speaks to them
- **Objections & Concerns Addressed**: Hesitations content handles
- **Content Focus Areas**: Topics and angles emphasized
- **Communication Preferences**: How they like to receive information
- **Usage Guidelines**: How to apply this persona in content creation

## Workflow Integration

### Pattern 1: Project Setup with Persona Extraction
```
1. Create project → 2. Collect sources → 3. Extract personas → 4. Work on targets
```

### Pattern 2: Persona Discovery During Content Work
```
1. Working on target → 2. No matching persona found → 3. Extract from similar targets → 4. Apply extracted persona
```

### Pattern 3: User Provides Example
```
1. No existing content → 2. User provides audience example → 3. Extract persona → 4. Apply to new content
```

## Validation

**Minimum Document Check:**
- Requires at least 3 substantial documents
- Warns if insufficient content provided
- Prompts to add more sources or proceed with caveat

**Quality Indicators:**
- More documents = more reliable patterns
- Consistent targeting = clearer persona profile
- Explicit pain points = better persona definition

## Directory Management

**Automatic Directory Creation:**
- Skill creates `/rules/personas/` if it doesn't exist
- No manual setup required
- Works on first use

## Rule Matching (for Content Work)

When working on target content:
1. **Inspect target**: Identify intended audience, technical level, context
2. **Search rules**: Look for matching persona in `/rules/personas/`
3. **Match or extract**:
   - Match found → Use existing persona profile
   - No match → Extract from targets OR ask user for audience description
4. **Flag missing rules**: Warn if no appropriate persona exists

## Output Example

```
✅ Persona extraction complete

📊 Analysis:
   - 8 documents analyzed
   - 2 distinct audience personas identified

📝 Persona profiles created:
   - technical-implementer.md
   - business-decision-maker.md

🔍 Persona characteristics:

   Technical Implementer:
   - Role: Developer, Data Engineer, DevOps
   - Technical level: Intermediate to Expert
   - Focus: Implementation details, best practices, troubleshooting

   Business Decision Maker:
   - Role: VP Engineering, CTO, Technical Leader
   - Technical level: Intermediate (strategic understanding)
   - Focus: ROI, team efficiency, strategic value
```

## Related Skills

- **style-extraction-skill**: Extract writing voice and tone patterns
- **structure-extraction-skill**: Extract document format templates
- **project-management-skill**: Uses persona matching for content work

## Template Reference

Uses: `.claude/system-prompts/persona-template.md`

## Best Practices

1. **Start incremental**: Default mode is safe and additive
2. **Group similar audience content**: Analyze content targeting same audience together
3. **Minimum 3-5 docs**: Better patterns with more examples
4. **Review auto-naming**: Check generated names reflect audience accurately
5. **Update regularly**: Extract as audience strategy evolves
6. **Focus on targeting**: Best results from content with clear audience focus

## Key Insight

Personas are extracted FROM content, not FROM user research. They represent "who the content is written for" based on:
- Language complexity and terminology used
- Problems and solutions emphasized
- Assumptions about audience knowledge
- Objections and concerns addressed
- Tone and communication style

This is different from marketing personas created through user research. These are **content targeting personas** that help maintain consistency in audience approach.
