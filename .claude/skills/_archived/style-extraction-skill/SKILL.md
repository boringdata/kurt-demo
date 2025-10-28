# Style Extraction Skill

Extract writing voice, tone, and style patterns from existing content to create reusable style guides.

## Purpose

Analyze content to identify consistent writing patterns (voice, tone, sentence structure, word choice) and save them as style guides in `rules/style/` for use in content creation projects.

## When to Use

- **During project setup**: After collecting ground truth sources
- **When rule matching fails**: No appropriate style guide exists for target content
- **For content updates**: Need to match existing content style
- **New content creation**: Building style foundation from examples

## Prerequisites

- Minimum 3-5 substantial documents for reliable extraction
- Documents should represent consistent writing style
- Content stored in `/sources/` or accessible file paths

## Style Extraction Philosophy

**Layered Approach:**
1. **Corporate Voice (Priority 1)** - The company's brand voice used on marketing pages
   - Most important to extract first
   - Used on homepage, product pages, about pages
   - Represents official brand communication

2. **Content Type Voices (Priority 2)** - Distinct voices for different content types
   - Technical documentation voice
   - Blog post voice (may be more casual than corporate)
   - Support/help content voice

3. **Individual Author Voices (Optional)** - Personal voices of specific authors
   - Blog posts by individual authors
   - Thought leadership pieces
   - Only extract if project requires matching individual author style

**Recommendation:** Always extract corporate voice first, then extract content-type voices, then individual voices if needed.

## Usage

### Discovery Mode (Recommended)

Ask user upfront: **Auto-discover or manual selection?**

**Option A: Auto-discover by style type**
```bash
# Extract corporate voice (always recommended first)
invoke style-extraction-skill --type corporate --auto-discover

# Extract content-type voice
invoke style-extraction-skill --type technical-docs --auto-discover
invoke style-extraction-skill --type blog --auto-discover

# Extract individual author voice (if needed)
invoke style-extraction-skill --type author --author-name "John Doe" --auto-discover
```

**Option B: Manual selection**
```bash
# User provides specific documents
invoke style-extraction-skill with documents: <file-paths>
```

**Option C: Hybrid (auto-discover + user refinement)**
```bash
# Discover + user adds/removes specific documents
invoke style-extraction-skill --type corporate --auto-discover --include <path> --exclude <pattern>
```

### Auto-Discovery Process

**For Corporate Voice (Priority 1):**

```bash
# Step 1: Discover key corporate/marketing pages
# Homepage
kurt document list --url-prefix https://company.com/ | grep -E "^https://[^/]+/?$"

# Product/Feature pages (marketing copy)
kurt document list --url-contains /product
kurt document list --url-contains /features
kurt document list --url-contains /solutions

# About/Company pages
kurt document list --url-contains /about
kurt document list --url-contains /company

# Landing pages (marketing campaigns)
kurt document list --url-contains /landing
kurt document list --url-contains /campaign

# Step 2: Show proposed list
echo "Found corporate/marketing pages for brand voice extraction:"
echo "- Homepage: ✓"
echo "- 5 product pages: ✓"
echo "- 2 about pages: ✓"
echo "Total: 8 pages"

# Step 3: User approves or refines

# Step 4: Fetch if needed, extract corporate voice style
```

**For Technical Documentation Voice:**

```bash
# Discover documentation pages
kurt document list --url-contains /docs/
kurt document list --url-contains /documentation
kurt document list --url-contains /guide
kurt document list --url-contains /tutorial
kurt document list --url-contains /reference

# Sample diverse doc types for comprehensive style
# (Not all docs, just representative sample of 5-10)
```

**For Blog Voice:**

```bash
# Discover blog posts
kurt document list --url-contains /blog/ --url-contains -v /blog/?$

# Sample recent blog posts (5-10 for general blog voice)
kurt document list --url-contains /blog/ | head -10

# Filter by specific author if extracting individual voice
kurt document list --url-contains /blog/ | grep "author: John Doe"
```

**For Individual Author Voice:**

```bash
# Search by author name in metadata or URL
kurt document list --author "John Doe"
# Or by URL pattern if author has dedicated path
kurt document list --url-contains /blog/john-doe/
kurt document list --url-contains /author/john-doe/
```

### Incremental Mode (Default - Recommended)
```bash
# Analyze documents and add new styles if found
# Keeps existing style guides untouched
invoke style-extraction-skill with documents: <file-paths>

# Or use auto-discovery
invoke style-extraction-skill --type corporate --auto-discover
```

**Behavior:**
1. Reads existing style guides in `rules/style/`
2. Analyzes provided documents for style patterns
3. Compares findings with existing guides
4. Creates new style guide only if distinct pattern found
5. Reports "No new styles detected" if patterns already captured

### Overwrite Mode (Nuclear Option)
```bash
# Delete all existing style guides and create fresh analysis
invoke style-extraction-skill with documents: <file-paths> --overwrite
```

**Behavior:**
1. Deletes all files in `rules/style/`
2. Performs fresh analysis on all provided documents
3. Creates completely new style guide library

## What Gets Extracted

### Style Characteristics
- **Voice & Tone**: Conversational, authoritative, technical, friendly
- **Sentence Structure**: Length, complexity, active vs passive
- **Word Choice**: Technical terminology, jargon level, formality
- **Common Patterns**: Recurring phrases, transitions, expressions
- **Paragraph Structure**: Length and organization patterns

### Metadata Tracked
- Documents analyzed (count and file paths)
- Extraction date and command used
- Content types and target audiences
- Voice type, tone type, complexity level

## Auto-Naming Logic

Style guides get descriptive names based on:
- **Content type**: blog, landing-page, technical-doc, tutorial
- **Tone**: conversational, formal, authoritative, casual
- **Audience**: executive, developer, customer, general

**Example outputs:**
- `conversational-marketing.md`
- `technical-documentation.md`
- `executive-blog-posts.md`
- `friendly-support-content.md`

## Multi-Pattern Detection

Single analysis can identify multiple distinct styles:
```
✅ Analysis complete
📝 Created 2 new style guides:
   - technical-tutorial-style.md
   - conversational-blog-style.md
```

## Output Format

Each style guide includes:
- **YAML frontmatter**: Metadata for tracking and searchability
- **Voice & Tone**: Core writing personality
- **Sentence Structure**: How sentences are constructed
- **Word Choice**: Vocabulary and terminology patterns
- **Common Patterns**: Recurring expressions and transitions
- **Example Sentences**: Representative samples from analyzed content
- **Usage Notes**: When and how to apply this style

## Discovery Workflow Examples

### Example 1: Extract Corporate Voice (Recommended First Step)

```bash
# User wants to extract corporate brand voice

# 1. Ask user: Auto-discover or manual?
# User chooses: Auto-discover

# 2. Discover corporate/marketing pages from content map
homepage=$(kurt document list --url-prefix https://company.com/ | grep -E "^https://company\.com/?$")
products=$(kurt document list --url-contains /product --status FETCHED | head -5)
about=$(kurt document list --url-contains /about --status FETCHED)
features=$(kurt document list --url-contains /features --status FETCHED | head -3)

# 3. Show discovered pages
echo "Found 9 corporate/marketing pages:"
echo "✓ Homepage"
echo "✓ 5 product pages"
echo "✓ 1 about page"
echo "✓ 3 feature pages"

# 4. User approves: "Yes, use these"

# 5. Check fetch status and fetch if needed
for url in $products; do
  status=$(kurt document list --url $url | grep "status:")
  if [[ $status == *"NOT_FETCHED"* ]]; then
    kurt ingest fetch $url
  fi
done

# 6. Extract corporate voice style
# Read documents from /sources/company.com/...
# Analyze for voice, tone, sentence structure, word choice
# Create: rules/style/corporate-brand-voice.md
```

### Example 2: Extract Technical Documentation Voice

```bash
# User wants to extract technical docs style after corporate voice is done

# 1. Discover documentation pages
docs=$(kurt document list --url-contains /docs/ --status FETCHED)
guides=$(kurt document list --url-contains /guide --status FETCHED)
tutorials=$(kurt document list --url-contains /tutorial --status FETCHED)

# 2. Sample diverse doc types (5-10 representative docs)
sample_docs=$(echo "$docs $guides $tutorials" | shuf | head -8)

# 3. Show proposed list
echo "Found technical documentation for style extraction:"
echo "✓ 4 API reference pages"
echo "✓ 2 guides"
echo "✓ 2 tutorials"
echo "Total: 8 pages (diverse sample)"

# 4. User approves or adds specific docs

# 5. Extract technical documentation style
# Create: rules/style/technical-documentation.md
```

### Example 3: Extract Individual Author Voice

```bash
# User wants to write blog post in John Doe's voice

# 1. Check if corporate + blog voice already extracted
ls rules/style/corporate*.md  # ✓ exists
ls rules/style/blog*.md  # ✓ exists

# 2. Ask: "Extract individual author voice or use general blog voice?"
# User: "Extract John's voice - I want to match his personal style"

# 3. Discover John's posts
john_posts=$(kurt document list --author "John Doe" --status FETCHED)
# Or by URL if author has dedicated path
john_posts=$(kurt document list --url-contains /blog/john-doe/ --status FETCHED)

# 4. Show discovered posts
echo "Found 12 blog posts by John Doe"
echo "Date range: 2023-01-15 to 2024-12-03"
echo "Topics: AI, product launches, company culture"

# 5. User approves: "Use the 6 most recent"

# 6. Extract individual author style
# Create: rules/style/john-doe-blog-voice.md
```

### Example 4: Diverse Sampling for General Style

```bash
# User wants general content style (mix of corporate, blog, docs)

# 1. Discover diverse content types
corp_pages=$(kurt document list --url-contains /product --status FETCHED | head -3)
blog_posts=$(kurt document list --url-contains /blog/ --status FETCHED | head -3)
docs_pages=$(kurt document list --url-contains /docs/ --status FETCHED | head -3)

# 2. Combine for diverse sample
all_content=$(echo "$corp_pages $blog_posts $docs_pages")

# 3. Show proposed mix
echo "Found diverse content for style extraction:"
echo "✓ 3 corporate/product pages"
echo "✓ 3 blog posts"
echo "✓ 3 documentation pages"
echo "Total: 9 pages (balanced mix)"

# 4. User approves

# 5. Extract general company style
# Create: rules/style/general-company-style.md
# Note: May identify multiple distinct styles in output
```

## Workflow Integration

### Pattern 1: Project Setup with Style Extraction
```
1. Create project → 2. Collect sources → 3. Extract style → 4. Work on targets
```

### Pattern 2: Style Discovery During Content Work
```
1. Working on target → 2. No matching style found → 3. Extract from similar targets → 4. Apply extracted style
```

### Pattern 3: User Provides Example
```
1. No existing content → 2. User provides style example → 3. Extract style → 4. Apply to new content
```

## Validation

**Minimum Document Check:**
- Requires at least 3 substantial documents
- Warns if insufficient content provided
- Prompts to add more sources or proceed with caveat

**Quality Indicators:**
- More documents = more reliable patterns
- Consistent authorship = clearer style voice
- Same content type = more focused style guide

## Directory Management

**Automatic Directory Creation:**
- Skill creates `rules/style/` if it doesn't exist
- No manual setup required
- Works on first use

## Rule Matching (for Content Work)

When working on target content:
1. **Inspect target**: Identify content type, tone, audience
2. **Search rules**: Look for matching style guide in `rules/style/`
3. **Match or extract**:
   - Match found → Use existing style guide
   - No match → Extract from targets OR ask user for example
4. **Flag missing rules**: Warn if no appropriate style exists

## Output Example

```
✅ Style extraction complete

📊 Analysis:
   - 8 documents analyzed
   - 1 consistent style pattern identified

📝 Style guide created:
   - technical-tutorial-style.md

🔍 Style characteristics:
   - Voice: Educational and supportive
   - Tone: Professional but approachable
   - Complexity: Intermediate technical level
   - Sentence structure: Clear, step-by-step instructions
```

## Related Skills

- **structure-extraction-skill**: Extract document format templates
- **persona-extraction-skill**: Extract audience targeting patterns
- **project-management-skill**: Uses style matching for content work

## Template Reference

Uses: `.claude/system-prompts/style-guide-template.md`

## Best Practices

1. **Start incremental**: Default mode is safe and additive
2. **Group similar content**: Analyze related documents together
3. **Minimum 3-5 docs**: Better patterns with more examples
4. **Review auto-naming**: Check generated names make sense
5. **Update regularly**: Extract as style evolves
