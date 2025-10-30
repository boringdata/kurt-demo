# Kurt Demo Project - Quick Reference

**For system architecture and concepts, see `KURT.md`.**

---

## Quick Links

- **Commands**: `/create-project` or `/resume-project` to get started
- **Architecture**: See `KURT.md` for project structure, sources vs targets, and file organization
- **Skills**: See `.claude/skills/` for detailed skill documentation

---

## Common Workflows

### Create a New Project

```bash
/create-project
```

You'll be guided through:
1. Project intent (positioning, marketing, docs, general)
2. Project name and goal
3. Organizational foundation check (content map + core rules)
4. Adding sources (optional)
5. Identifying targets (optional)
6. Extracting rules (optional)

**All steps except name/goal are optional - you can skip and return later.**

---

### Resume Existing Project

```bash
/resume-project my-project-name
```

Or without name for interactive selection:
```bash
/resume-project
```

The system will:
- Load your project context
- Check what's missing (sources, targets, rules)
- Recommend next steps based on your project intent
- Validate rule coverage before content work

---

### Content Creation Workflow

When creating or updating content, use **content-writing-skill** for full lineage tracking.

#### Step 1: Extract Rules (if not done)

```bash
# Foundation rules (for all projects)
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type primary --auto-discover

# Content-specific rules (based on what you're creating)
# For technical docs:
writing-rules-skill style --type technical-docs --auto-discover
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover

# For marketing content:
writing-rules-skill structure --type landing-page --auto-discover
writing-rules-skill persona --audience-type business --auto-discover
```

#### Step 2: Create Outline

```bash
content-writing-skill outline <project-name> <asset-name>
```

Output: `/projects/<project-name>/drafts/<asset-name>-outline.md`

Contains:
- YAML frontmatter with source documents listed
- Section-to-source mapping
- Update patterns (if project-specific)
- Rule files to apply

#### Step 3: Generate Draft

```bash
content-writing-skill draft <project-name> <asset-name>
```

Output: `/projects/<project-name>/drafts/<asset-name>-draft.md`

Contains:
- Enhanced YAML frontmatter with section sources
- Inline HTML comments at sections citing sources
- Update pattern applications documented
- Rule compliance tracked

#### Step 3.5: Get Persona-Based Feedback (Recommended)

```bash
content-writing-skill feedback <project-name> <asset-name>
```

Output: `/projects/<project-name>/feedback/<asset-name>-feedback.md`

Analyzes from each target persona's perspective:
- Comprehension issues (unexplained jargon, missing context)
- Technical depth (too advanced or too basic)
- Missing information (gaps they'd need filled)
- Tone/style mismatches
- Length issues
- Structure problems

Provides section-level issues with line numbers, concrete fix suggestions, and persona alignment scores.

#### Step 4: Edit as Needed

```bash
content-writing-skill edit projects/<project-name>/drafts/<asset-name>-draft.md --instructions "specific edit instructions"
```

Updates:
- Adds edit session to YAML history
- Increments version number
- Adds inline edit comments at changes
- Tracks which sections were modified

---

### Query Lineage

Every piece of content tracks its lineage. Query it with:

```bash
# See section sources
grep "<!-- SECTION:" <draft-file>.md

# Find update patterns applied
grep "UPDATE PATTERN:" <draft-file>.md

# View persona feedback sessions
head -100 <draft-file>.md | grep "feedback_sessions:" -A 30

# View edit history
head -100 <draft-file>.md | grep "edit_sessions:" -A 20

# Check rule compliance
head -100 <draft-file>.md | grep "rule_compliance:" -A 10
```

---

## CMS Integration

Kurt integrates with CMS platforms (Sanity, Contentful, WordPress) via the `kurt cms` CLI commands.

### Setup

Configuration is stored in `.kurt/cms-config.json` (gitignored).

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

First-time setup:

```bash
kurt cms onboard
```

This will:
1. Test your CMS connection
2. Discover all content types (with document counts)
3. Guide you through selecting types to work with
4. Map custom fields to standard roles

### Common Operations

**Browse CMS Content:**
```bash
kurt cms types                                        # List content types
kurt cms search --query "tutorial"                   # Search all content
kurt cms search --content-type article --limit 20    # Search specific type
```

**Fetch to Local:**
```bash
kurt cms fetch --id abc123 --output-dir sources/cms/sanity/
```

**Import to Kurt Database:**
```bash
kurt cms import --source-dir sources/cms/sanity/
```

**Publish Drafts to CMS:**
```bash
kurt cms publish --file draft.md --id abc123          # Update existing
kurt cms publish --file new-article.md --content-type article  # Create new
```

### Full CMS → Kurt → CMS Workflow

```bash
# 1. Fetch existing articles from CMS
kurt cms search --content-type article
kurt cms fetch --id <id> --output-dir sources/cms/sanity/
kurt cms import --source-dir sources/cms/sanity/

# 2. Extract rules from CMS content
writing-rules-skill style --type primary --auto-discover
writing-rules-skill structure --type article --auto-discover

# 3. Create new content using learned patterns
content-writing-skill outline my-project new-article
content-writing-skill draft my-project new-article

# 4. Publish back to CMS
kurt cms publish --file projects/my-project/drafts/new-article-draft.md --content-type article
```

---

## Research Integration

Kurt integrates with AI research platforms (Perplexity) for daily news monitoring and topic discovery via `kurt research` CLI commands.

### Setup

Configuration is stored in `.kurt/research-config.json` (gitignored).

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

**Models:**
- `sonar-reasoning` - Best for comprehensive research (default)
- `sonar` - Faster, good for quick queries
- `sonar-pro` - Most powerful, higher cost

**Recency filters:**
- `hour` - Last hour (breaking news)
- `day` - Last 24 hours (daily monitoring)
- `week` - Last 7 days (weekly trends)
- `month` - Last 30 days (broader research)

### Basic Usage

```bash
# Execute research query
kurt research search "latest AI coding assistant news" --recency day --save

# Browse research history
kurt research list

# View specific result
kurt research get 2025-10-27-latest-ai-coding-assistant-news
```

Results are saved to `sources/research/YYYY-MM-DD-query.md` with YAML frontmatter, comprehensive answer with inline citations, and full source list.

### Research Workflows (research-skill)

**Daily News Digest:**
```bash
research-skill daily
```

**Topic Discovery:**
```bash
research-skill discover "AI coding tools"
```

**Direct Research:**
```bash
research-skill query "What are the latest developments in Claude Code?"
```

**Kickoff Content Project from Research:**
```bash
research-skill kickoff <research-file> <project-name>
```

### Full Research → Content Workflow

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

### Example: Daily Monitoring Workflow

**Option 1: Project-Based Monitoring (Recommended)**

```bash
# Interactive setup
research-skill setup-monitoring data-tools-watch

# Daily: Run project monitoring
kurt research monitor projects/data-tools-watch

# Deep dive on interesting signal
kurt research search "topic from signal" --recency day --save
mv sources/research/[file].md projects/data-tools-watch/research/

# Create content
content-writing-skill outline data-tools-watch article-name
content-writing-skill draft data-tools-watch article-name

# Publish
kurt cms publish --file projects/data-tools-watch/drafts/article-draft.md --content-type article
```

**Benefits:**
- All research lives with the project
- Clear lineage: signals → research → content
- Configure once, run daily
- Track trends over time

---

## Best Practices

### For Content Creation

✅ **DO:**
- Extract rules before creating content (ensures consistency)
- Use content-writing-skill for full lineage tracking
- Review persona feedback before finalizing
- Check inline HTML comments for source attribution
- Validate rule compliance scores in YAML

❌ **DON'T:**
- Use vague edit instructions ("make it better")
- Skip rule extraction (leads to inconsistent content)
- Edit without understanding original rationale
- Accept all changes without review

### For Rules Extraction

✅ **DO:**
- Extract foundation rules first (publisher + primary voice)
- Extract content-specific rules based on what you're creating
- Use --auto-discover for automatic document selection
- Review sample documents before extraction

❌ **DON'T:**
- Extract rules from too few documents (need 3-5 minimum)
- Extract from mixed content types (dilutes patterns)
- Skip the preview step (may extract from wrong documents)

### For Project Organization

✅ **DO:**
- Keep web content in `/sources/` (organizational knowledge base)
- Keep project-specific files in `projects/<name>/sources/`
- Reference rules from `rules/` directories
- Use batch operations for multiple URLs

❌ **DON'T:**
- Duplicate content across projects
- Loop individual fetch/index commands (use --url-prefix)
- Skip indexing (required for rule extraction)

---

## Rules System Quick Reference

**List available rule types:**
```bash
writing-rules-skill list
```

**Extract built-in rules:**
```bash
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type <mode> --auto-discover
writing-rules-skill structure --type <mode> --auto-discover
writing-rules-skill persona --audience-type <type> --auto-discover
```

**Manage rule types:**
```bash
writing-rules-skill add       # Add custom type (wizard)
writing-rules-skill validate  # Check system health
```

**Key points:**
- Rules system is dynamic - check registry for available types
- System adapts to custom rule types automatically
- See `KURT.md` for comprehensive rules documentation

---

## When to Use Which Skill

| Task | Skill | Command |
|------|-------|---------|
| Create new project | project-management | `/create-project` |
| Resume existing project | project-management | `/resume-project` |
| Add sources to project | project-management | `project-management gather-sources` |
| Extract writing rules | writing-rules-skill | `writing-rules-skill <type> --auto-discover` |
| Create content outline | content-writing-skill | `content-writing-skill outline` |
| Generate draft | content-writing-skill | `content-writing-skill draft` |
| Get persona feedback | content-writing-skill | `content-writing-skill feedback` |
| Edit draft | content-writing-skill | `content-writing-skill edit` |
| Fetch web content | ingest-content-skill | `kurt content fetch` |
| Work with CMS | cms-interaction-skill | `kurt cms <operation>` |
| Research topics | research-skill | `kurt research search` or `research-skill` |

---

## Files Created by Workflows

**Content creation:**
- `/projects/<project-name>/drafts/<asset-name>-outline.md`
- `/projects/<project-name>/drafts/<asset-name>-draft.md`
- `/projects/<project-name>/feedback/<asset-name>-feedback.md`

**Rules extraction:**
- `rules/style/<style-name>.md`
- `rules/structure/<structure-name>.md`
- `rules/personas/<persona-name>.md`
- `rules/publisher/publisher-profile.md`

**Research:**
- `sources/research/YYYY-MM-DD-<query>.md`

---

## See Also

- **Architecture**: `KURT.md` - System concepts, data model, file structure
- **Skill docs**: `.claude/skills/` - Detailed documentation for each skill
- **Project example**: `/projects/tutorial-refresh-fusion/project.md` - Example project structure

---

For system architecture, data model, and core concepts, see **`KURT.md`**.
