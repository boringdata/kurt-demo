# AI Writing Agent System

This Claude Code project implements a comprehensive content creation and management system that helps writers and content teams produce consistent, high-quality content at scale while maintaining strategic alignment and brand consistency.

## Project Overview

### Purpose
Transform content creation from ad-hoc writing to systematic, rule-based content production that learns from existing content, plans strategically, and executes with consistency.

### Core Capabilities
- **Learn**: Extract writing rules from existing content (style, structure, personas, publisher profile)
- **Plan**: Create strategic project briefs with research integration and task breakdowns
- **Execute**: Generate outlines, drafts, and polished content following established guidelines
- **Edit**: Interactive inline editing with instruction-based improvements
- **Track**: Complete traceability from strategy to published content with YAML metadata

## System Architecture

### Content Creation Workflow
```
1. EXTRACTION → Learn from existing content to create rules
2. PLANNING → Strategic briefs with research and task breakdown
3. EXECUTION → Outline → Draft → Edit → Publish
4. TRACKING → YAML frontmatter enables search and traceability
```

### File Organization
```
/
├── .claude/
│   ├── commands/           # 11 slash commands for content workflow
│   └── system-prompts/     # 11 templates ensuring consistency
├── rules/                  # Extracted knowledge base
│   ├── style/             # Writing voice and tone guides
│   ├── structure/         # Content format templates
│   ├── personas/          # Audience targeting profiles
│   └── publisher/         # Organizational context
├── projects/              # Active content projects
│   └── [project-name]/
│       ├── project-brief.md      # Strategic planning
│       ├── task-breakdown.md     # Operational tasks
│       ├── research-findings.md  # Supporting research
│       └── assets/               # Content files
└── cms/                   # Existing content for analysis
```

## Available Commands

### Extraction Commands (Learn from Existing Content)
- `/extract-style [docs...] [--overwrite]` - Extract writing voice and tone patterns
- `/extract-structure [docs...] [--overwrite]` - Identify content format templates
- `/extract-personas [docs...] [--overwrite]` - Extract audience targeting patterns
- `/extract-publisher-profile [docs/URLs...] [--overwrite]` - Build organizational context

### Planning Commands (Strategic Foundation)
- `/create-project-brief "[topic]" [--research-mode]` - Create strategic project plan
- `/generate-tasks [brief-path] [--detailed] [--assign]` - Break brief into actionable tasks

### Execution Commands (Content Production)
- `/execute-task [task-breakdown] [task-id]` - Universal task executor with smart routing
- `/outline-content [task-breakdown] [task-id] [--interactive]` - Create detailed content outlines
- `/write-content [task-breakdown] [task-id] [--section]` - Generate drafts from outlines
- `/edit-content [file] "[instructions]" [--section] [--across-files]` - Interactive inline editing

## MCP Tool Integration

### Research & SEO Tools
Configure these MCP servers for enhanced research capabilities:
```bash
# SEMrush for keyword research
claude mcp add semrush -e SEMRUSH_API_KEY=your_key -- npx -y @semrush/mcp-server

# Perplexity for industry research
claude mcp add perplexity -e PERPLEXITY_API_KEY=your_key -- npx -y @perplexity/mcp-server
```

### Content Management
```bash
# Sanity CMS integration
claude mcp add sanity -e SANITY_PROJECT_ID=your_id -e SANITY_TOKEN=your_token -- npx -y @sanity/mcp-server
```

## Content Quality Standards

### Rule-Based Consistency
Every piece of content follows established rules:
- **Style Guide**: Voice, tone, and writing patterns from `rules/style/`
- **Structure Template**: Content format and flow from `rules/structure/`
- **Target Persona**: Audience-specific communication from `rules/personas/`
- **Publisher Profile**: Brand context and messaging from `rules/publisher/`

### YAML Frontmatter Requirements
All content files include structured metadata for traceability:
```yaml
---
content_type: [style_guide/outline/draft/etc]
project: [project-name]
created_date: [YYYY-MM-DD]
style_guide: rules/style/[file].md
target_persona: rules/personas/[file].md
# ... additional metadata
---
```

## Workflow Examples

### Initial Setup (One-Time)
```bash
# Extract knowledge from existing content
/extract-company-profile https://company.com/about @docs/marketing/*.md
/extract-style @docs/blog-posts/*.md
/extract-structure @docs/landing-pages/*.md
/extract-personas @docs/customer-content/*.md
```

### Strategic Project Planning
```bash
# Create comprehensive project brief with research
/create-project-brief "Q2 Product Launch Campaign" --research-mode

# Break down into actionable tasks
/generate-tasks @projects/q2-launch/project-brief.md --detailed --assign
```

### Content Production
```bash
# Execute tasks in sequence
/outline-content @projects/q2-launch/task-breakdown.md blog-outline-01 --interactive
/write-content @projects/q2-launch/task-breakdown.md blog-write-01
/edit-content @projects/q2-launch/assets/blog-draft.md "Make more conversational and add concrete examples"
```

### Multi-File Operations
```bash
# Consistent changes across content series
/edit-content @projects/guide/assets/*.md "Simplify for small business owners" --across-files="*.md"

# Extract patterns from content series
/extract-structure @docs/tutorial-series/*.md
```

## Best Practices

### Content Planning
- Always start with project briefs for strategic alignment
- Use research mode for competitive and market insights
- Break complex projects into manageable task groups
- Plan internal linking strategy during outline phase

### Rule Management
- Extract rules incrementally (don't overwrite unless necessary)
- Use descriptive auto-generated names for rules
- Regular rule updates as content strategy evolves
- Archive outdated rules rather than deleting

### Quality Control
- Interactive editing mode for important content
- Section-specific editing for targeted improvements
- Batch mode for trusted, routine improvements
- Always specify clear editing instructions

### Project Organization
- One brief per strategic initiative
- Group related assets within projects
- Use YAML metadata for searchability
- Maintain clear file naming conventions

## Advanced Features

### Searchability
Use YAML frontmatter to find content across projects:
```bash
# Find all content using specific personas
grep -r "target_persona: rules/personas/enterprise-decision-maker.md" projects/

# Find content ready for review
grep -r "status: draft_complete" projects/

# Analyze content by project type
grep -r "project_type: campaign" projects/
```

### Content Portfolio Analysis
- Track rule usage across projects
- Identify high-performing content patterns
- Monitor brand consistency over time
- Analyze content effectiveness by persona

### Automation Opportunities
- Batch apply style updates across content library
- Automated content audits using rule compliance
- Performance tracking integration via YAML metadata
- Content calendar integration with project planning

## Troubleshooting

### Common Issues
- **Rules not applying**: Check file paths in asset specifications
- **MCP tools not working**: Verify API keys and server configuration
- **Inconsistent output**: Ensure proper template usage in system-prompts/
- **Search not finding content**: Check YAML frontmatter syntax

### Performance Optimization
- Use section-specific editing for large documents
- Batch operations for routine improvements
- Interactive mode only for high-stakes content
- Regular cleanup of completed projects

## Security & Compliance

### Content Safety
- Company profile extraction respects public information only
- No storage of external API responses beyond session
- YAML metadata contains no sensitive information
- All content generation follows established brand guidelines

### Data Management
- Local file storage for all extracted rules and content
- MCP integrations use read-only access where possible
- Project files organized for easy backup and versioning
- Clear audit trail through YAML frontmatter

---

## Getting Started

1. **Set up MCP tools** for research and content management
2. **Extract initial rules** from 10-20 existing content pieces
3. **Create your first project brief** with research mode enabled
4. **Generate tasks** and begin content production
5. **Iterate and improve** rules as you create more content

This system scales from individual content creators to enterprise content teams, maintaining quality and consistency while dramatically improving production efficiency.
