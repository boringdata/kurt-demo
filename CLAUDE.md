# Kurt Demo Project

This is a **Kurt** project - a document intelligence system that helps teams manage, analyze, and create content.

## Quick Links

- **Core Concepts**: See `KURT.md` for project structure, sources vs targets, and file organization
- **Workflows**: See available skills in `.claude/skills/`
- **Commands**: `/create-project` or `/resume-project` to get started

## Project Organization

- `/sources/` - Organizational knowledge base (all web content)
- `/rules/` - Extracted rules for content creation
  - `/rules/style/` - Writing voice/tone patterns
  - `/rules/structure/` - Document format templates
  - `/rules/personas/` - Audience targeting profiles
  - `/rules/publisher/` - Company/brand profile
- `/projects/` - Individual content projects

---

## Content Creation Workflow

When working on content creation or updates for a Kurt project, use the **content-writing-skill** to ensure comprehensive lineage tracking.

### When to Use Content-Writing-Skill

✅ **Use this skill when:**
- Creating outlines for new content
- Generating drafts from outlines
- Editing existing content
- Updating documentation with new information
- Need to track which sources informed which sections
- Want full edit history and reasoning

❌ **Don't use for:**
- Simple one-line edits (use Edit tool directly)
- Exploring or reading content (use Read tool)
- Extracting rules (use extraction skills)

### Standard Content Creation Workflow

**Step 1: Extract Rules (if not done)**
```bash
# Extract publisher profile (foundation)
writing-rules-skill publisher --auto-discover

# Extract corporate style
writing-rules-skill style --type corporate --auto-discover

# Extract content-specific rules based on what you're creating:
# For technical docs:
writing-rules-skill style --type technical-docs --auto-discover
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover

# For marketing content:
writing-rules-skill structure --type landing-page --auto-discover
writing-rules-skill persona --audience-type business --auto-discover
```

**Step 2: Create Outline**
```bash
content-writing-skill outline <project-name> <asset-name>
```

**Output:** `/projects/<project-name>/assets/<asset-name>-outline.md`

**Contains:**
- YAML frontmatter with source documents listed
- Section-to-source mapping
- Update patterns (if project-specific)
- Rule files to apply

**Step 3: Generate Draft**
```bash
content-writing-skill draft <project-name> <asset-name>
```

**Output:** `/projects/<project-name>/assets/<asset-name>-draft.md`

**Contains:**
- Enhanced YAML frontmatter with section sources
- Inline HTML comments at sections citing sources
- Update pattern applications documented
- Rule compliance tracked

**Step 4: Edit as Needed**
```bash
content-writing-skill edit projects/<project-name>/assets/<asset-name>-draft.md --instructions "specific edit instructions"
```

**Updates:**
- Adds edit session to YAML history
- Increments version number
- Adds inline edit comments at changes
- Tracks which sections were modified

### Lineage Tracking

**Every piece of content created with this workflow tracks:**

1. **Sources** - Which documents informed which sections
2. **Reasoning** - Why content was written this way
3. **Rules Applied** - Style, structure, persona, publisher compliance
4. **Update Patterns** - Project-specific transformation patterns (if applicable)
5. **Edit History** - All changes with session IDs, instructions, timestamps

**Query lineage:**
```bash
# See section sources
grep "<!-- SECTION:" <draft-file>.md

# Find update patterns applied
grep "UPDATE PATTERN:" <draft-file>.md

# View edit history
head -100 <draft-file>.md | grep "edit_sessions:" -A 20

# Check rule compliance
head -100 <draft-file>.md | grep "rule_compliance:" -A 10
```

### Example: Tutorial Update Project

**Scenario:** Updating 23 tutorials to include new feature instructions

```bash
# 1. Create outline (maps sources to sections, identifies patterns)
content-writing-skill outline tutorial-refresh-fusion bigquery-quickstart

# 2. Review outline - verify source mapping and patterns

# 3. Generate draft (applies patterns, cites sources inline)
content-writing-skill draft tutorial-refresh-fusion bigquery-quickstart

# 4. Review draft for accuracy

# 5. Edit to add missing content
content-writing-skill edit projects/tutorial-refresh-fusion/assets/bigquery-quickstart-draft.md --instructions "Add limitations callout per Type 5 pattern"

# 6. Validate pattern application
grep "UPDATE PATTERN:" projects/tutorial-refresh-fusion/assets/bigquery-quickstart-draft.md

# 7. Check which tutorials use which patterns (across all tutorials)
for pattern in type_{1..7}; do
  echo "=== $pattern ==="
  grep -r "$pattern" projects/tutorial-refresh-fusion/assets/
done
```

### Integration with Project Management

**When resuming a project:**

```bash
/resume-project tutorial-refresh-fusion
```

Claude will:
1. Load project.md context
2. Check if rules are extracted
3. Check if target content exists
4. **Recommend content-writing-skill** if targets need work
5. Suggest next steps in workflow

**Project-management-skill** knows about content-writing-skill and will recommend it when appropriate.

---

## CMS Integration

Kurt integrates with CMS platforms (Sanity, Contentful, WordPress) via the `kurt cms` CLI commands.

### Setup

**Configuration is stored in `.kurt/cms-config.json`** (gitignored).

```json
{
  "sanity": {
    "project_id": "your-project-id",
    "dataset": "production",
    "token": "sk...your-read-token",
    "write_token": "sk...your-write-token",
    "base_url": "https://yoursite.com"
  }
}
```

### Onboarding

First-time setup to discover content types and configure field mappings:

```bash
kurt cms onboard
```

This will:
1. Test your CMS connection
2. Discover all content types (with document counts)
3. Guide you through selecting types to work with
4. Map custom fields to standard roles (content, title, slug, metadata)

### Common Workflows

**1. Browse CMS Content**
```bash
# List content types
kurt cms types

# Search all content
kurt cms search --query "tutorial"

# Search specific type
kurt cms search --content-type article --limit 20
```

**2. Fetch CMS Content to Local**
```bash
# Fetch single document as markdown
kurt cms fetch --id abc123 --output-dir sources/cms/sanity/

# Output shows: title, type, status, character count
# Creates markdown file with YAML frontmatter
```

**3. Import to Kurt Database**
```bash
# Import fetched markdown files
kurt cms import --source-dir sources/cms/sanity/

# Documents added to Kurt DB with CMS metadata preserved
# Can then index, cluster, extract rules, etc.
```

**4. Publish Drafts to CMS**
```bash
# Update existing document
kurt cms publish --file draft.md --id abc123

# Create new document
kurt cms publish --file new-article.md --content-type article

# Publishes as draft in CMS for review
```

### Integration with Other Workflows

**CMS → Kurt → Content Creation:**
```bash
# 1. Fetch existing articles from CMS
kurt cms search --content-type article
kurt cms fetch --id <id> --output-dir sources/cms/sanity/
kurt cms import --source-dir sources/cms/sanity/

# 2. Extract rules from CMS content
writing-rules-skill style --type corporate --auto-discover
writing-rules-skill structure --type article --auto-discover

# 3. Create new content using learned patterns
content-writing-skill outline my-project new-article
content-writing-skill draft my-project new-article

# 4. Publish back to CMS
kurt cms publish --file projects/my-project/assets/new-article-draft.md --content-type article
```

**Benefits:**
- ✅ Pull existing content from CMS for analysis
- ✅ Learn writing patterns from published content
- ✅ Create new content matching CMS style
- ✅ Round-trip: CMS → Kurt → CMS

### Supported Platforms

- **Sanity** - Full support (search, fetch, import, publish)
- **Contentful** - Coming soon
- **WordPress** - Coming soon

---

## Research Integration

Kurt integrates with AI research platforms (Perplexity) for daily news monitoring and topic discovery via `kurt research` CLI commands.

### Setup

**Configuration is stored in `.kurt/research-config.json`** (gitignored).

```json
{
  "perplexity": {
    "api_key": "pplx-...",
    "default_model": "sonar-reasoning",
    "default_recency": "day",
    "max_tokens": 4000,
    "temperature": 0.2
  }
}
```

Get your API key at: https://www.perplexity.ai/settings/api

### Models and Recency

**Available models:**
- `sonar-reasoning` - Best for comprehensive research (default)
- `sonar` - Faster, good for quick queries
- `sonar-pro` - Most powerful, higher cost

**Recency filters:**
- `hour` - Last hour (breaking news)
- `day` - Last 24 hours (daily monitoring)
- `week` - Last 7 days (weekly trends)
- `month` - Last 30 days (broader research)

### Basic Usage

**Execute research query:**
```bash
# Basic query
kurt research search "latest AI coding assistant news"

# With recency filter
kurt research search "latest AI coding assistant news" --recency day

# Save results to markdown
kurt research search "latest AI coding assistant news" --recency day --save
```

Research results are saved to `sources/research/YYYY-MM-DD-query.md` with:
- YAML frontmatter (query, citations, metadata)
- Comprehensive answer with inline citations
- Full source list

**Browse research history:**
```bash
# List recent research
kurt research list

# View specific result
kurt research get 2025-10-27-latest-ai-coding-assistant-news
```

### Research Workflows (research-skill)

For orchestrated workflows, use the **research-skill**:

**1. Daily News Digest**
```bash
research-skill daily
```
Monitors saved topics, generates time-appropriate queries, presents key insights.

**2. Topic Discovery**
```bash
research-skill discover "AI coding tools"
```
Broad exploration → Extract topics → Deep dive on selected topics.

**3. Direct Research**
```bash
research-skill query "What are the latest developments in Claude Code?"
```
Research specific question with appropriate recency.

**4. Browse History**
```bash
research-skill browse
```
Review past research, organized by date.

**5. Kickoff Content Project**
```bash
research-skill kickoff <research-file> <project-name>
```
Use research as foundation for new content project.

### Integration with Content Creation

**Research → Content Workflow:**
```bash
# 1. Research topic
kurt research search "Latest trends in AI coding assistants" --recency day --save

# 2. Kickoff project from research
research-skill kickoff 2025-10-27-latest-trends-in-ai-coding-assistants ai-coding-guide

# 3. Extract rules (if needed)
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type technical-docs --auto-discover

# 4. Create outline (references research file as source)
content-writing-skill outline ai-coding-guide intro-to-ai-coding

# 5. Generate draft (with research citations)
content-writing-skill draft ai-coding-guide intro-to-ai-coding
```

**Benefits:**
- ✅ Stay current with industry trends
- ✅ Discover content topics backed by research
- ✅ Track all citations and sources
- ✅ Feed research into content creation workflow
- ✅ Maintain lineage from research → outline → draft

### Key Differences: Research vs Documents

**Research files are NOT imported to Kurt database:**
- Research is ephemeral (news, trends, time-sensitive)
- Saved as markdown in `sources/research/`
- Can be referenced as sources in content creation
- Use `kurt research list` to browse (not `kurt document list`)

**CMS/Web content IS imported:**
- Documentation, articles, reference material
- Stable content that updates over time
- Imported to Kurt DB for indexing and clustering
- Use `kurt document list` to browse

### Example: Daily Monitoring Workflow

```bash
# Morning: Check yesterday's news
research-skill daily

# If interesting topic found:
kurt research search "Detailed query about topic" --recency day --save

# Kickoff content project if worth writing about:
research-skill kickoff 2025-10-27-topic-name new-article-project

# Create content:
content-writing-skill outline new-article-project article
content-writing-skill draft new-article-project article

# Publish to CMS:
kurt cms publish --file projects/new-article-project/assets/article-draft.md --content-type article
```

**Complete cycle:** Monitor → Research → Create → Publish

---

## Best Practices

### For Outline Creation

✅ **DO:**
- List ALL source documents used (even "for inspiration")
- Document WHY each source matters
- Map sources to specific sections
- Identify project-specific update patterns

### For Draft Generation

✅ **DO:**
- Review inline HTML comments for source attribution
- Check that update patterns were applied correctly
- Validate rule compliance scores in YAML
- Ensure section sources are complete

### For Editing

✅ **DO:**
- Provide specific, actionable edit instructions
- Review changes before accepting
- Check that edit comments were added
- Verify version history is tracked

❌ **DON'T:**
- Use vague instructions ("make it better")
- Accept all changes without review
- Edit without understanding original rationale

---

## Files Created by Content-Writing-Skill

**Location:** `/projects/<project-name>/assets/`

**File types:**
- `<asset-name>-outline.md` - Outline with source mapping
- `<asset-name>-draft.md` - Draft with inline lineage
- `<asset-name>-draft.md` (edited) - Same file with version history

**Metadata in files:**
- **YAML frontmatter** - High-level, queryable metadata
- **Inline HTML comments** - Granular, contextual attribution

---

## See Also

- **Skill documentation:** `.claude/skills/content-writing-skill/README.md`
- **Metadata schemas:** `.claude/skills/content-writing-skill/templates/`
- **Comment patterns:** `.claude/skills/content-writing-skill/templates/inline-comment-patterns.md`
- **KURT.md:** Full system documentation
- **Project example:** `/projects/tutorial-refresh-fusion/project.md` (see "Using Content Writing Skill" section)

---

## Rules System

Kurt has an **extensible rules system**. See `KURT.md` for full details on how rules work.

### Quick Reference for Claude

**Extract rules:**
```bash
# Built-in types (always available)
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type corporate --auto-discover
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover

# Custom types (if configured by user)
writing-rules-skill <custom-type> --type <mode> --auto-discover
```

**Manage rule types:**
```bash
writing-rules-skill list              # See what's configured
writing-rules-skill add               # Add custom type (wizard)
writing-rules-skill validate          # Check system health
```

**Key points:**
- Rules system is dynamic - check registry for available types
- System adapts to custom rule types automatically
- Use `writing-rules-skill list` to see current configuration
- Point users to `KURT.md` for comprehensive rules documentation
