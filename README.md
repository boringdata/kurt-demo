# Kurt Plugin for Claude Code

AI-powered content creation system for B2B tech companies.

## What does this plugin do?

The Kurt Plugin helps tech companies create consistent, high-quality content faster by:

- **Creating marketing content** - Landing pages, blog posts, case studies, product messaging
- **Maintaining technical documentation** - Tutorials, guides, API docs, onboarding materials
- **Ensuring consistency** - Extracts and applies style, structure, and voice patterns from existing content
- **Tracking lineage** - Every piece of content tracks which sources informed it and why

**Target use case:** B2B tech companies that need to create lots of content while maintaining brand voice, technical accuracy, and quality.

---

## Quick Start

### 1. First Time Setup

Run `/start` in Claude Code to set up your team profile:

```
/start
```

This interactive wizard (10-15 minutes) will:
- Capture your company, team, and content goals
- Map your website and content sources
- Optionally configure analytics for traffic-based prioritization (PostHog)
- Extract your writing style, company profile, and target personas
- Create `.kurt/profile.md` with your team setup

**You can skip any question** - Kurt adapts to what you know.

**Analytics integration:** During onboarding, you'll be offered the option to connect PostHog analytics. This enables traffic-based content prioritization, helping you focus on high-impact updates. Analytics setup is optional and can be added later via `/start --update`.

### 2. Define Workflows (Optional)

If you have recurring project patterns, codify them as reusable workflows:

```
workflow-skill add
```

Examples:
- "Weekly tutorial publication"
- "Product launch campaigns"
- "Quarterly docs refresh"

**Workflows are optional** - projects can be created without them.

### 3. Create Projects

Create content projects using your profile and workflows:

```
# With workflow (recurring pattern)
/create-project --workflow weekly-tutorial

# Without workflow (one-off project)
/create-project
```

Projects automatically use your team profile (rules, personas, sources).

### 4. Create Content

Use the content-writing-skill to create outlines and drafts:

```
content-writing-skill outline <project> <asset>
content-writing-skill draft <project> <asset>
content-writing-skill edit <file> --instructions "..."
```

---

## What is kurt-core?

This plugin wraps **kurt-core**, a CLI tool that provides document intelligence capabilities:

- Fetches and indexes web content
- Stores documents in local SQLite database
- Extracts metadata using AI
- Manages content analysis and rule extraction

The plugin adds Claude Code workflows on top of kurt-core to orchestrate content creation projects.

---

## Prerequisites & Installation

### 1. Install kurt-core CLI

The plugin requires the kurt-core CLI to be installed:

```bash
# Install via pip (or your preferred method)
pip install kurt-core

# Verify installation
kurt --version
```

**Note:** The kurt-core CLI handles all document fetching, storage, and indexing. The plugin orchestrates workflows using Claude Code.

### 2. Initialize Kurt Database

Create a Kurt database in your project directory:

```bash
# Create database
kurt init

# Apply migrations if needed
kurt migrate apply
```

This creates a `.kurt/` directory with the SQLite database.

### 3. Install the Kurt Plugin

Install this plugin in Claude Code (instructions will vary based on plugin distribution method).

---

## Kurt CLI Workflows

The plugin uses a **2-step workflow** for ingesting organizational content:

### Step 1: Map (Discovery + Clustering)

Discover content from websites or CMS platforms and automatically organize them into topic clusters:

#### Map from Website

```bash
# Map a website and cluster its content (recommended)
kurt map url https://docs.example.com --cluster-urls

# Options:
kurt map url https://example.com --cluster-urls --sitemap-path /custom-sitemap.xml
kurt map url https://example.com --cluster-urls --include "*/docs/*"
kurt map url https://example.com --cluster-urls --exclude "*/api/*"
```

**What this does:**
- Discovers all URLs from sitemap (or crawls if no sitemap)
- Creates NOT_FETCHED document records in database
- **Organizes URLs into 5-10 topic clusters** (e.g., "Getting Started", "API Reference")
- **Classifies rough content types** (tutorial, guide, reference, blog, etc.)
- All in a single LLM call - no content downloads yet

#### Map from CMS

```bash
# Map CMS content and cluster (recommended)
kurt map cms --platform sanity --cluster-urls

# Options:
kurt map cms --platform sanity --instance prod --cluster-urls
kurt map cms --platform sanity --content-type article --cluster-urls
kurt map cms --platform sanity --status published --limit 100
```

**What this does:**
- Discovers all documents from CMS via API
- Creates NOT_FETCHED document records with semantic URLs like `sanity/prod/article/vibe-coding-guide`
- Stores CMS document ID separately for API fetching
- **Organizes documents into topic clusters** based on schema, slug, and description
- **Auto-infers content types** from schema names (e.g., "article" → article content type)
- No content downloads yet - just metadata discovery

**Why cluster during mapping?**
- See topics before downloading (fetch selectively)
- Query what content exists: `kurt content list --in-cluster "Tutorials"`
- Fetch by cluster: `kurt fetch --in-cluster "Tutorials"`
- Works across both web and CMS content sources

### Step 2: Fetch (Download + Index)

Download and index content selectively (works for both web and CMS content):

```bash
# Fetch specific cluster (works for web + CMS mixed)
kurt fetch --in-cluster "Getting Started"

# Fetch by content type (requires clustering first)
kurt fetch --with-content-type tutorial
kurt fetch --with-content-type guide

# Fetch by URL/identifier pattern
kurt fetch --include "*/docs/*"                          # Web URLs
kurt fetch --include "sanity/prod/*"                     # CMS content
kurt fetch --include "*tutorial*"                        # Both

# Fetch with exclusions
kurt fetch --include "*/docs/*" --exclude "*/api/*"

# Combine filters
kurt fetch --with-content-type tutorial --include "*/docs/*"
kurt fetch --with-content-type article --include "sanity/*"

# Options:
kurt fetch --in-cluster "Tutorials" --concurrency 10     # Parallel downloads
kurt fetch --include "*/docs/*" --skip-index             # Download only, skip LLM indexing
kurt fetch --with-status ERROR --refetch                 # Retry failed fetches
```

**What this does:**
- **Web content**: Downloads to `sources/{domain}/{path}.md`
- **CMS content**: Downloads to `sources/cms/{platform}/{instance}/{id}.md`
- Extracts detailed metadata via LLM (topics, tools, code examples, structure)
- Updates database status to FETCHED

### Query & Verify

```bash
# List documents
kurt content list                                        # All documents
kurt content list --with-status NOT_FETCHED              # Not yet downloaded
kurt content list --in-cluster "Tutorials"               # Specific cluster
kurt content list --include "*/docs/*"                   # By URL pattern

# View clusters
kurt cluster-urls --format table                         # Show all clusters

# Get document details
kurt content get <document-id>                           # Full metadata

# Statistics
kurt content stats                                       # Overview
```

### Re-clustering

Refine clusters as content grows:

```bash
# Refine existing clusters (incremental - keeps existing clusters)
kurt cluster-urls

# Force fresh clustering (ignores existing clusters)
kurt cluster-urls --force

# Cluster specific subset
kurt cluster-urls --include "*/blog/*"
```

### Common Patterns

**Ingest organizational website:**
```bash
# 1. Map + cluster (discovers URLs + organizes + classifies content types)
kurt map url https://docs.yourcompany.com --cluster-urls

# 2. Review clusters and content types
kurt cluster-urls --format table
kurt content list --with-content-type tutorial

# 3. Fetch selectively
kurt fetch --in-cluster "Getting Started"
kurt fetch --with-content-type tutorial
kurt fetch --with-content-type guide --include "*/docs/*"
```

**Ingest from CMS:**
```bash
# 1. Map CMS content + cluster
kurt map cms --platform sanity --cluster-urls

# 2. Review clusters
kurt cluster-urls --format table
kurt content list --include "sanity/*"

# 3. Fetch selectively
kurt fetch --in-cluster "Tutorials"
kurt fetch --with-content-type article --include "sanity/*"
```

**Mixed web + CMS ingestion:**
```bash
# Map both sources
kurt map url https://docs.example.com --cluster-urls
kurt map cms --platform sanity --cluster-urls

# Fetch all content (web + CMS) by cluster
kurt fetch --in-cluster "Getting Started"

# Or fetch separately
kurt fetch --include "docs.example.com/*"
kurt fetch --include "sanity/*"
```

**Selective ingestion:**
```bash
# Map everything, fetch only tutorials
kurt map url https://docs.example.com --cluster-urls
kurt fetch --include "*/tutorials/*"
```

**Retry failed fetches:**
```bash
# Check failures
kurt content list --with-status ERROR

# Retry
kurt fetch --with-status ERROR --refetch
```

---

## CMS Integration Setup (Optional)

If you want to ingest content from a CMS (Sanity, Contentful, WordPress), follow these steps:

### 1. Configure CMS Connection

Create `.kurt/cms-config.json` with your CMS credentials:

```json
{
  "sanity": {
    "prod": {
      "project_id": "your-project-id",
      "dataset": "production",
      "token": "sk...your-read-token",
      "write_token": "sk...your-write-token",
      "base_url": "https://yoursite.com",
      "content_type_mappings": {
        "article": {
          "enabled": true,
          "content_field": "content_body_portable",
          "title_field": "title",
          "slug_field": "slug.current",
          "description_field": "excerpt",
          "inferred_content_type": "article",
          "metadata_fields": {}
        },
        "universeItem": {
          "enabled": true,
          "content_field": "description",
          "title_field": "title",
          "slug_field": "slug.current",
          "description_field": "description",
          "inferred_content_type": "reference",
          "metadata_fields": {}
        }
      }
    }
  }
}
```

**Key fields explained:**
- `slug_field`: Field containing URL slug - used in semantic URLs for clustering
- `description_field`: Field containing summary/excerpt - provides context for topic clustering
- `inferred_content_type`: Auto-assigned content type from schema name - skips LLM classification
- `content_type_mappings`: Per-schema field mappings discovered during onboarding

**Note:** The `.kurt/` directory is already gitignored, so credentials are safe.

### 2. Run Onboarding

Discover content types and map custom field names:

```bash
cms-interaction-skill onboard
```

### 3. Use the Unified Workflow

Once configured, CMS content works just like web content:

```bash
# Map CMS content
kurt map cms --platform sanity --cluster-urls

# Fetch CMS content
kurt fetch --include "sanity/*"

# Mix with web content in the same workflow
kurt map url https://docs.example.com --cluster-urls
kurt fetch --in-cluster "Tutorials"  # Fetches both web + CMS content
```

See the [CMS Interaction Skill documentation](.claude/skills/cms-interaction-skill/SKILL.md) for details.

---

## Quick Start

### Create Your First Project

```bash
# In Claude Code, run:
/create-project
```

You'll be guided through:
1. **Project intent** - What are you creating? (marketing, docs, positioning)
2. **Project name** - Kebab-case name for your project
3. **Organizational foundation** - Content map + core rules (first-time setup)
4. **Sources** - Ground truth content to work FROM (optional)
5. **Targets** - Content to create or update (optional)
6. **Rules** - Extract patterns from existing content (optional)

**Result:** A project structure in `projects/<name>/` with a `project.md` manifest tracking your work.

### Resume an Existing Project

```bash
/resume-project <project-name>
```

The plugin will:
- Load your project context
- Check what's missing (sources, targets, rules)
- Recommend next steps based on your project intent
- Validate rule coverage before content work

---

## File Structure

```
your-project/
├── sources/                    # Organizational knowledge base (web content)
│   ├── docs.company.com/
│   ├── blog.company.com/
│   └── research/               # Research results (not in DB)
├── rules/                      # Extracted patterns
│   ├── rules-config.yaml       # Rule type registry
│   ├── style/                  # Voice and tone patterns
│   ├── structure/              # Document templates
│   ├── personas/               # Audience profiles
│   └── publisher/              # Company profile
├── projects/                   # Individual projects
│   └── my-project/
│       ├── project.md         # Project manifest
│       ├── sources/           # Project-specific files (PDFs, notes)
│       └── drafts/            # Work in progress
└── .kurt/                      # Kurt database
    └── kurt.sqlite
```

---

## Key Concepts

### Sources vs Targets

**Sources** are ground truth content you're working FROM:
- Reference materials
- Competitive analysis
- Internal specs
- Research findings
- Existing documentation

**Targets** are content you're working ON:
- Documentation to update
- New content to create
- Blog posts to write
- Tutorials to refresh

### Rules

Rules are extracted patterns from existing content that guide consistent content creation:

- **Style Guidelines** - Voice, tone, sentence structure, word choice
- **Structure Templates** - Document organization, section flow, formatting
- **Target Personas** - Audience roles, pain points, communication preferences
- **Publisher Profile** - Company identity, messaging, brand positioning

The rules system is extensible - teams can add custom rule types via the registry.

### Projects

Projects organize content creation workflows. Each project has:

- **Goal** - What you're trying to accomplish
- **Sources** - Ground truth content (working FROM)
- **Targets** - Content to update or create (working ON)
- **Rules** - Applicable patterns for this project
- **Progress** - Task tracking and next steps

---

## Available Commands

### Project Management

- `/create-project` - Create a new content project
- `/resume-project [name]` - Resume existing project (interactive if no name)

### Direct Skill Invocation

All workflows are available as skills:

```bash
# Project workflows
project-management create-project
project-management resume-project [name]
project-management check-foundation
project-management gather-sources
project-management extract-rules

# Rule extraction
writing-rules-skill publisher --auto-discover
writing-rules-skill style --type primary --auto-discover
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover

# Content creation
content-writing-skill outline <project> <asset>
content-writing-skill draft <project> <asset>
content-writing-skill feedback <project> <asset>
content-writing-skill edit <file> --instructions "..."

# Research integration
research-skill daily [project]
research-skill discover "<topic>"
research-skill query "<question>"

# CMS integration (unified workflow)
kurt map cms --platform sanity --cluster-urls
kurt fetch --include "sanity/*"

# CMS ad-hoc operations (via skill)
cms-interaction-skill onboard
cms-interaction-skill search --query "..."
cms-interaction-skill publish --file <file> --document-id <id>
```

---

## project.md Format

Each project has a `project.md` file that serves as the project manifest:

```markdown
# Project Name

## Goal
Brief description of what you want to accomplish

## Intent Category
a) Update positioning
b) Marketing assets
c) Technical docs updates
d) General project
e) Custom

## Sources (Ground Truth)

### From Organizational Knowledge Base
- [x] Page title: `/sources/domain.com/path/page.md` (fetched: YYYY-MM-DD)
- [ ] Another page: https://example.com/page (not fetched)

### Project-Specific Sources
- [x] Internal doc: `sources/filename.pdf` (added: YYYY-MM-DD)

## Targets (Content to Update/Create)

### Existing Content to Update
- [ ] Tutorial: `/sources/docs.company.com/tutorial.md`

### New Content to Create
- [ ] New tutorial: `drafts/new-tutorial.md` (planned)

## Rules Configuration

### Style Guidelines
- Technical documentation style: `rules/style/technical-documentation.md`

### Structure Templates
- Tutorial structure: `rules/structure/quickstart-tutorial.md`

### Target Personas
- Developer persona: `rules/personas/technical-implementer.md`

### Publisher Profile
- Company profile: `rules/publisher/publisher-profile.md`

## Progress
- [x] Task completed (YYYY-MM-DD)
- [ ] Task pending

## Next Steps
<Updated as work progresses>
```

---

## Content Pipeline

The typical content creation flow:

```
1. Fetch sources → 2. Index content → 3. Extract rules → 4. Create content → 5. Publish
```

1. **Fetch**: Download content to `/sources/` as markdown
2. **Index**: Extract metadata (title, author, date, topics, entities)
3. **Extract Rules**: Learn patterns from indexed content
4. **Create Content**: Apply rules to targets with full lineage tracking
5. **Publish**: Push to CMS or export

**Lineage tracking** means every piece of content tracks:
- Which sources informed which sections
- Why content was written this way
- Which rules were applied
- Edit history with reasoning

---

## Where to Learn More

All skills in `.claude/skills/` are self-documenting with:
- What they do
- When to use them
- How they integrate with other skills
- Technical details

**Key skills:**
- `project-management-skill/` - Project workflows
- `writing-rules-skill/` - Rule extraction and management
- `content-writing-skill/` - Content creation with lineage
- `research-skill/` - AI-powered research integration
- `cms-interaction-skill/` - CMS platform integration

Skills are automatically indexed by Claude Code, so just describe what you want to do and Claude will use the appropriate skill.

---

## License

[Your license here]

## Contributing

[Contributing guidelines here]
