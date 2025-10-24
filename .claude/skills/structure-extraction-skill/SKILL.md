# Structure Extraction Skill

Extract document organization patterns and content templates from existing content to create reusable structure guides.

## Purpose

Analyze content to identify consistent document structures (section flow, headline patterns, content organization) and save them as structure templates in `/rules/structure/` for use in content creation projects.

## When to Use

- **During project setup**: After collecting ground truth sources
- **When rule matching fails**: No appropriate structure template exists for target content
- **For content updates**: Need to match existing document formats
- **New content creation**: Building structure foundation from examples

## Prerequisites
## Content Discovery Method

> **⚠️ This skill uses file-based content maps (not Kurt CLI database)**
>
> All document discovery uses content map queries:
> - Query: `cat sources/<domain>/_content-map.json | jq ...`
> - Fetch: Use WebFetch tool (hooks auto-save + index)
> - Reference: See `.claude/docs/CONTENT-MAP-QUERIES.md` for query patterns


- Minimum 3-5 substantial documents for reliable extraction
- Documents should represent consistent structural patterns
- Content stored in `/sources/` or accessible file paths

## Usage

### Discovery Mode (Recommended)

Ask user upfront: **Auto-discover or manual selection?**

**Option A: Auto-discover by content type**
```bash
# Extract structure for specific content type
invoke structure-extraction-skill --type tutorial --auto-discover
invoke structure-extraction-skill --type api-reference --auto-discover
invoke structure-extraction-skill --type landing-page --auto-discover
invoke structure-extraction-skill --type blog-post --auto-discover
```

**Option B: Manual selection**
```bash
# User provides specific documents
invoke structure-extraction-skill with documents: <file-paths>
```

**Option C: Hybrid (auto-discover + user refinement)**
```bash
# Discover + user adds/removes specific documents
invoke structure-extraction-skill --type tutorial --auto-discover --include <path> --exclude <pattern>
```

### Auto-Discovery Process

**Key Principle:** Structure extraction requires **focused sampling** - analyze same content type for consistent patterns.

**For Tutorial/Quickstart Structure:**

```bash
# Step 1: Discover tutorial/quickstart pages
tutorials=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "tutorial" and .value.status == "FETCHED") | .key')
quickstarts=$(kurt document list --url-contains /quickstart --status FETCHED)
getting_started=$(kurt document list --url-contains /getting-started --status FETCHED)
get_started=$(kurt document list --url-contains /get-started --status FETCHED)

# Step 2: Sample representative tutorials (5-8 for pattern detection)
sample=$(echo "$tutorials $quickstarts $getting_started $get_started" | head -8)

# Step 3: Show proposed list
echo "Found tutorial/quickstart pages for structure extraction:"
echo "✓ 5 tutorials"
echo "✓ 3 quickstart guides"
echo "Total: 8 pages (focused sample)"

# Step 4: User approves or refines

# Step 5: Extract tutorial structure template
# Create: /rules/structure/quickstart-tutorial.md
```

**For API Reference Structure:**

```bash
# Discover API reference pages
api_refs=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "reference" and .value.status == "FETCHED") | .key')
reference=$(kurt document list --url-contains /reference --status FETCHED)
endpoints=$(kurt document list --url-contains /endpoint --status FETCHED)

# Sample diverse API docs (5-8 endpoints/resources)
sample=$(echo "$api_refs $reference $endpoints" | head -8)
```

**For Landing Page Structure:**

```bash
# Discover landing/product pages
landing=$(kurt document list --url-contains /landing --status FETCHED)
product=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "product_page" and .value.status == "FETCHED") | .key' | grep -v "/products/?$")

# Sample product/landing pages (5-8 for pattern)
sample=$(echo "$landing $product" | head -8)
```

**For Blog Post Structure:**

```bash
# Discover blog posts (exclude blog homepage)
blog_posts=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == "blog" and .value.status == "FETCHED") | .key' | grep -v "/blog/?$")

# Sample recent blog posts (5-8 for structure pattern)
sample=$(echo "$blog_posts" | head -8)
```

**For Guide/How-To Structure:**

```bash
# Discover guide/how-to pages
guides=$(kurt document list --url-contains /guide --status FETCHED)
howto=$(kurt document list --url-contains /how-to --status FETCHED)

# Sample guides (5-8 for pattern)
sample=$(echo "$guides $howto" | head -8)
```

### Discovery Patterns by Content Type

| Content Type | URL Patterns | Sample Size |
|--------------|--------------|-------------|
| Tutorial/Quickstart | `/tutorial`, `/quickstart`, `/getting-started`, `/get-started` | 5-8 docs |
| API Reference | `/api/`, `/reference`, `/endpoint` | 5-8 endpoints |
| Landing Page | `/landing`, `/product/[name]` | 5-8 pages |
| Blog Post | `/blog/[post]` (not `/blog/?$`) | 5-8 posts |
| Guide/How-To | `/guide`, `/how-to` | 5-8 guides |
| Case Study | `/case-stud`, `/customer/[name]`, `/success-stor` | 5-8 studies |
| Documentation | `/docs/` | 5-8 doc pages |

### Incremental Mode (Default - Recommended)
```bash
# Analyze documents and add new structures if found
# Keeps existing structure templates untouched
invoke structure-extraction-skill with documents: <file-paths>

# Or use auto-discovery
invoke structure-extraction-skill --type tutorial --auto-discover
```

**Behavior:**
1. Reads existing structure templates in `/rules/structure/`
2. Analyzes provided documents for structural patterns
3. Compares findings with existing templates
4. Creates new structure template only if distinct pattern found
5. Reports "No new structures detected" if patterns already captured

### Overwrite Mode (Nuclear Option)
```bash
# Delete all existing structure templates and create fresh analysis
invoke structure-extraction-skill with documents: <file-paths> --overwrite
```

**Behavior:**
1. Deletes all files in `/rules/structure/`
2. Performs fresh analysis on all provided documents
3. Creates completely new structure template library

## What Gets Extracted

### Structural Elements
- **Document Organization**: Overall section flow and hierarchy
- **Headline Patterns**: Common headline and subheading formulas
- **Opening Hooks**: How content typically begins
- **Content Flow Logic**: How ideas progress through the piece
- **Call-to-Action Patterns**: CTA placement and style
- **Content Depth Guidelines**: Typical detail level and depth
- **Visual/Formatting Elements**: Lists, tables, code blocks, etc.

### Metadata Tracked
- Documents analyzed (count and file paths)
- Extraction date and command used
- Content purpose and target audiences
- Typical word count and section count

## Auto-Naming Logic

Structure templates get descriptive names based on:
- **Content purpose**: lead-generation, educational, case-study, tutorial
- **Content type**: blog-post, landing-page, documentation, guide
- **Audience**: enterprise, technical, general, customer

**Example outputs:**
- `tutorial-documentation.md`
- `lead-generation-landing-page.md`
- `technical-case-study.md`
- `educational-blog-post.md`

## Multi-Pattern Detection

Single analysis can identify multiple distinct structures:
```
✅ Analysis complete
📝 Created 2 new structure templates:
   - quickstart-tutorial-structure.md
   - api-reference-structure.md
```

## Output Format

Each structure template includes:
- **YAML frontmatter**: Metadata for tracking and searchability
- **Documents Analyzed**: Source files used for extraction
- **Content Purpose**: Primary goal and use case
- **Target Audience**: Who structure is designed for
- **Structural Outline**: Section-by-section breakdown with purpose and length
- **Headline Patterns**: Common headline formulas
- **Opening Hooks**: How content typically starts
- **Content Flow Logic**: How ideas progress
- **Call-to-Action Patterns**: CTA style and placement
- **Content Depth Guidelines**: Typical detail level
- **Visual/Formatting Elements**: Consistent formatting patterns
- **Typical Length**: Word count ranges
- **Success Metrics**: What success looks like
- **Usage Guidelines**: When and how to use this structure
- **Example Outline Template**: Ready-to-use markdown template

## Workflow Integration

### Pattern 1: Project Setup with Structure Extraction
```
1. Create project → 2. Collect sources → 3. Extract structure → 4. Work on targets
```

### Pattern 2: Structure Discovery During Content Work
```
1. Working on target → 2. No matching structure found → 3. Extract from similar targets → 4. Apply extracted structure
```

### Pattern 3: User Provides Example
```
1. No existing content → 2. User provides structure example → 3. Extract structure → 4. Apply to new content
```

## Validation

**Minimum Document Check:**
- Requires at least 3 substantial documents
- Warns if insufficient content provided
- Prompts to add more sources or proceed with caveat

**Quality Indicators:**
- More documents = more reliable patterns
- Same content type = more focused structure
- Consistent formatting = clearer template

## Directory Management

**Automatic Directory Creation:**
- Skill creates `/rules/structure/` if it doesn't exist
- No manual setup required
- Works on first use

## Rule Matching (for Content Work)

When working on target content:
1. **Inspect target**: Identify content purpose, type, audience
2. **Search rules**: Look for matching structure template in `/rules/structure/`
3. **Match or extract**:
   - Match found → Use existing structure template
   - No match → Extract from targets OR ask user for example
4. **Flag missing rules**: Warn if no appropriate structure exists

## Output Example

```
✅ Structure extraction complete

📊 Analysis:
   - 6 documents analyzed
   - 1 consistent structural pattern identified

📝 Structure template created:
   - quickstart-tutorial-structure.md

🔍 Structure characteristics:
   - Purpose: Educational quickstart guidance
   - Typical sections: 7 (Intro → Setup → First Task → Next Steps)
   - Typical length: 1200-1800 words
   - Opening: Problem statement + solution preview
   - CTAs: Embedded throughout + strong closing
```

## Related Skills

- **style-extraction-skill**: Extract writing voice and tone patterns
- **persona-extraction-skill**: Extract audience targeting patterns
- **project-management-skill**: Uses structure matching for content work

## Template Reference

Uses: `.claude/system-prompts/structure-template.md`

## Best Practices

1. **Start incremental**: Default mode is safe and additive
2. **Group similar content**: Analyze related document types together
3. **Minimum 3-5 docs**: Better patterns with more examples
4. **Review auto-naming**: Check generated names make sense
5. **Update regularly**: Extract as formats evolve
6. **Focus on consistency**: Best results from structurally similar documents
