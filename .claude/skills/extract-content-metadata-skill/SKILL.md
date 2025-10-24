# Extract Content Metadata Skill

Extract metadata from dynamically added content without using Kurt CLI.

## Purpose

When you add content on-the-fly during a Claude Code session (via WebFetch or manual creation), this skill extracts metadata and updates the content map so the content is immediately usable.

## When to Use

- After using WebFetch to fetch a new page
- After manually creating a source document
- When you need metadata for content not in main content map
- Before extracting rules from newly added content

## What It Does

1. **Analyzes content** using Claude API:
   - Extracts 3-5 main topics
   - Identifies entities (companies, products, technologies)
   - Generates 1-2 sentence summary
   - Determines content type (blog, docs, tutorial, etc.)

2. **Updates content map** (`_content-map.json`):
   - Adds entry with extracted metadata
   - Matches to existing cluster or creates new one
   - Marks as "basic" metadata level
   - Makes content immediately discoverable

3. **No Kurt CLI required**:
   - Pure file operations
   - Uses Claude API directly
   - Fast (1-2 seconds)

## Usage

### Basic Usage

```bash
invoke extract-content-metadata-skill with file: /sources/docs.company.com/new-page.md
```

### After WebFetch

```bash
# 1. Fetch content
WebFetch https://competitor.com/pricing

# 2. Content auto-imported to /sources/competitor.com/pricing.md

# 3. Extract metadata
invoke extract-content-metadata-skill with file: /sources/competitor.com/pricing.md
```

### Batch Processing

```bash
# Extract metadata for multiple files
invoke extract-content-metadata-skill with files: [
  "/sources/domain.com/page1.md",
  "/sources/domain.com/page2.md"
]
```

## Prerequisites

- File must exist in `/sources/` directory
- `ANTHROPIC_API_KEY` environment variable must be set
- Python 3 with anthropic package installed

## Output

The skill shows:

```
✅ Metadata extracted: /sources/competitor.com/pricing.md

📄 Title: Competitor Pricing Comparison
📊 Topics: pricing, tiers, features, comparison, enterprise
🏢 Entities: CompetitorCo, Product X, Enterprise Plan
📝 Summary: Detailed pricing comparison showing three tiers with feature breakdown and enterprise options.
📁 Content type: landing-page
🔗 Cluster: competitive-analysis

📂 Content map updated: /sources/competitor.com/_content-map.json
```

## Content Map Structure

Creates or updates `_content-map.json` in domain directory:

```json
{
  "domain": "competitor.com",
  "last_updated": "2025-01-24T15:30:00Z",
  "sitemap": {
    "https://competitor.com/pricing": {
      "status": "FETCHED",
      "file_path": "/sources/competitor.com/pricing.md",
      "title": "Pricing",
      "topics": ["pricing", "tiers", "features"],
      "entities": ["CompetitorCo", "Product X"],
      "summary": "Detailed pricing comparison...",
      "content_type": "landing-page",
      "cluster": "competitive-analysis",
      "metadata_level": "basic",
      "source": "dynamic_fetch",
      "indexed_at": "2025-01-24T15:30:00Z"
    }
  },
  "clusters": [
    {
      "name": "competitive-analysis",
      "description": "Content related to pricing, competition, features",
      "urls": ["https://competitor.com/pricing"],
      "topics": ["pricing", "tiers", "features", "comparison"]
    }
  ],
  "topics": {
    "pricing": 1,
    "tiers": 1,
    "features": 1
  }
}
```

## Metadata Levels

**Basic (this skill):**
- Fast (1-2 seconds)
- Good enough for immediate work
- Topics, entities, summary, cluster matching
- Extracted via Claude API inline

**Advanced (Kurt CLI offline):**
- Slower (batch processing)
- More sophisticated clustering
- Entity relationships
- Semantic similarity
- Run with `kurt prepare --refresh` later

## Workflow

### Dynamic Content Addition Flow

```
1. User needs competitor page
   ↓
2. WebFetch https://competitor.com/pricing
   ↓
3. Auto-import saves to /sources/competitor.com/pricing.md
   ↓
4. invoke extract-content-metadata-skill
   ↓
5. Metadata extracted + content map updated
   ↓
6. Content immediately usable with metadata
```

### Future Enhancement Flow

```
Later, run offline processing:

kurt prepare --refresh
  ↓
Upgrades "basic" → "advanced" metadata
Updates clusters with better analysis
```

## Implementation Details

**Scripts used:**
1. `.claude/scripts/extract_metadata.py`
   - Reads markdown file
   - Parses frontmatter
   - Uses Claude API to analyze content
   - Returns structured metadata

2. `.claude/scripts/update_content_map.py`
   - Loads existing content map
   - Simple cluster matching based on topics
   - Updates/creates sitemap entry
   - Writes back JSON

**Error Handling:**
- If file not found → clear error message
- If API key missing → instructions to set it
- If extraction fails → returns empty metadata, still updates map

## Example Session

```
User: "Fetch competitor pricing page for comparison"

Claude: "Fetching https://competitor.com/pricing..."
[Uses WebFetch tool]
✓ Content saved to /sources/competitor.com/pricing.md

Claude: "Extracting metadata..."
[Invokes extract-content-metadata-skill]

✅ Metadata extracted: /sources/competitor.com/pricing.md

📄 Title: Pricing Plans
📊 Topics: pricing, tiers, features, enterprise, comparison
🏢 Entities: CompetitorCo, Enterprise Plan, Pro Plan
📝 Summary: Three-tier pricing structure with feature comparison and enterprise options.
📁 Content type: landing-page
🔗 Cluster: competitive-analysis (matched to existing cluster)

📂 Content map updated: /sources/competitor.com/_content-map.json

Claude: "Content ready! You can now use this for your pricing comparison analysis. The page is automatically clustered with other competitive analysis content."
```

## Integration with Other Skills

**Works with:**
- **WebFetch** (after fetching new content)
- **import-content-skill** (after manual import)
- **style-extraction-skill** (provides metadata for auto-discovery)
- **structure-extraction-skill** (provides metadata for auto-discovery)

**Before extraction skills:**
- Run this skill to add new content to content map
- Extraction skills can then auto-discover from content map

## Best Practices

1. **Run after every dynamic fetch** to keep content map updated
2. **Check content map** before extraction to see what's available
3. **Batch process** if adding multiple pages at once
4. **Upgrade later** with `kurt prepare --refresh` for advanced features

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "ANTHROPIC_API_KEY not set" | Export env var: `export ANTHROPIC_API_KEY=sk-...` |
| "File not in /sources/" | File must be in `/sources/{domain}/` directory |
| "No topics extracted" | Content may be too short or unclear - check file |
| "Content map not found" | First run creates it automatically |

## Future Enhancements

**Optional post-hook (later):**
- Automatically run after Write tool creates file in `/sources/`
- Completely transparent to user
- No manual invocation needed

**For now:** Explicit skill invocation for reliability and debugging
