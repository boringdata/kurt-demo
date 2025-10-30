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

# CMS integration
kurt cms onboard
kurt cms search --query "..."
kurt cms fetch --id <id> --output-dir sources/cms/
kurt cms publish --file <file> --content-type <type>
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
