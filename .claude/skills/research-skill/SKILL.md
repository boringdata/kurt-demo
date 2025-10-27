---
name: research
description: Daily news monitoring, topic discovery, and research for content creation
---

# Research Skill

**Purpose:** Help discover content topics through AI-powered research integration (Perplexity)
**Core workflow:** Daily monitoring → Topic discovery → Research reports → Content creation
**CLI integration:** Uses `kurt research` commands for API interaction

---

## Overview

This skill orchestrates research workflows for content creators:

1. **Daily News Monitoring** - Track industry trends and developments
2. **Topic Discovery** - Find interesting topics to write about or react to
3. **Research Reports** - Generate comprehensive reports with citations
4. **Content Integration** - Feed research into content creation workflow

**Key insight:** Research is separate from Kurt documents. Results are saved as markdown files in `sources/research/` for reference, not imported to the Kurt database.

---

## Usage Examples

```bash
# Daily news digest
research-skill daily

# Discover topics in a specific area
research-skill discover "AI coding tools"

# Research a specific question
research-skill query "What are the latest developments in Claude Code?"

# Browse recent research
research-skill browse

# Use research to kick off content project
research-skill kickoff <research-file> <project-name>
```

---

## Prerequisites Check

Before executing any research workflow, verify:

1. **Perplexity API configured**
```bash
# Check if config exists and has valid API key
if [ -f ".kurt/research-config.json" ]; then
  if grep -q "YOUR_PERPLEXITY_API_KEY_HERE" .kurt/research-config.json; then
    echo "ERROR: Perplexity API key not configured"
    echo "Edit .kurt/research-config.json and add your API key"
    echo "Get key at: https://www.perplexity.ai/settings/api"
    exit 1
  fi
else
  echo "ERROR: Research config not found"
  echo "Create .kurt/research-config.json with your Perplexity API key"
  echo "See .kurt/README.md for setup instructions"
  exit 1
fi
```

2. **Research directory exists**
```bash
mkdir -p sources/research
```

---

## Workflows

### Workflow 1: Daily News Digest

**Purpose:** Get daily digest of industry news and trends

**Steps:**

1. **Understand user's focus areas**
   - Check if `sources/research/topics.md` exists with saved topics
   - If not, ask user: "What areas should I monitor for you?"
   - Common examples:
     - "AI coding tools and assistants"
     - "Developer productivity tools"
     - "Cloud infrastructure trends"
     - "API development and integration"
   - Save topics to `sources/research/topics.md` for future reference

2. **Generate time-appropriate query**
   - Use current date/time to determine recency
   - Morning (6am-12pm): `--recency day` (yesterday's news)
   - Afternoon (12pm-6pm): `--recency day` (today's news)
   - Evening (6pm-12am): `--recency day` (today's summary)
   - Format query: "Latest news and developments in [topic] [timeframe]"

3. **Execute research**
```bash
# Example for AI coding tools
kurt research search "Latest AI coding assistant news and developments today" \
  --recency day \
  --save

# Note: This blocks for 10-30 seconds while Perplexity processes
```

4. **Present results**
   - Show key headlines and insights
   - List number of citations
   - Show saved file location
   - Offer to:
     - Research deeper on specific topics
     - Kick off content project based on findings
     - Schedule next digest

**Output:** Saved to `sources/research/YYYY-MM-DD-[topic].md`

---

### Workflow 2: Topic Discovery

**Purpose:** Find interesting topics to write about or react to

**Arguments:**
- `<area>` - Broad area to explore (e.g., "AI coding tools", "API development")

**Steps:**

1. **Broad exploration query**
   - Query format: "What are the most interesting developments and trends in [area] this week?"
   - Use `--recency week` for broader perspective
   - Save results

2. **Extract potential topics**
   - Parse the research results
   - Identify 5-7 specific topics worth exploring
   - For each topic, note:
     - Why it's interesting
     - Potential angle for content
     - Urgency (breaking news vs. ongoing trend)

3. **Present topic menu**
   - List topics with brief descriptions
   - Ask: "Which topic would you like to research deeper?"
   - Offer to research multiple topics

4. **Deep dive on selected topics**
   - For each selected topic, execute focused research
   - Use `--recency day` or `--week` based on topic freshness
   - Save each as separate research file

**Output:**
- Discovery file: `sources/research/YYYY-MM-DD-[area]-discovery.md`
- Deep dive files: `sources/research/YYYY-MM-DD-[specific-topic].md`

---

### Workflow 3: Direct Research Query

**Purpose:** Research a specific question or topic

**Arguments:**
- `<query>` - The research question

**Steps:**

1. **Validate query**
   - Ensure query is clear and specific
   - Suggest improvements if needed
   - Examples of good queries:
     - "What are the best practices for API rate limiting in 2025?"
     - "How does Claude Code compare to GitHub Copilot?"
     - "What are the latest developments in vector databases?"

2. **Determine recency**
   - Ask user or infer from query
   - "today" / "latest" → `--recency day`
   - "this week" → `--recency week`
   - "recently" / "current" → `--recency month`
   - No time indicator → `--recency month` (default)

3. **Execute research**
```bash
kurt research search "$query" --recency "$recency" --save
```

4. **Present results**
   - Display answer with citations
   - Show file location
   - Offer next steps:
     - Related queries to explore
     - Kick off content project
     - Save to content ideas list

---

### Workflow 4: Browse Research History

**Purpose:** Review past research and find useful reports

**Steps:**

1. **List recent research**
```bash
kurt research list --limit 20
```

2. **Present organized view**
   - Group by date
   - Highlight key topics
   - Show source counts
   - Note: Research files include YAML frontmatter with metadata

3. **Offer actions**
   - View specific research: `kurt research get <filename>`
   - Kick off content project from research
   - Delete old/irrelevant research
   - Export to different format

---

### Workflow 5: Kickoff Content Project from Research

**Purpose:** Use research as foundation for new content

**Arguments:**
- `<research-file>` - Research markdown file to use
- `<project-name>` - Name for new content project

**Steps:**

1. **Validate inputs**
   - Confirm research file exists in `sources/research/`
   - Check if project already exists
   - Get user confirmation

2. **Analyze research**
   - Read research markdown file
   - Extract key points and citations
   - Identify potential content angles

3. **Create project structure**
```bash
# Create project directory
mkdir -p projects/$project_name

# Create project.md with research context
cat > projects/$project_name/project.md <<EOF
# $project_name

## Research Foundation

Source: sources/research/$research_file
Research Date: [extracted from frontmatter]
Citations: [count from frontmatter]

## Key Findings

[Extract main points from research]

## Content Angles

[Suggest 3-5 potential angles based on research]

## Next Steps

1. Extract relevant writing rules (if not done)
2. Create content outline using content-writing-skill
3. Draft content with research citations
EOF
```

4. **Recommend next steps**
   - Extract publisher profile: `writing-rules-skill publisher --auto-discover`
   - Extract style rules: `writing-rules-skill style --type [type] --auto-discover`
   - Create outline: `content-writing-skill outline $project_name [asset-name]`

**Output:** New project in `projects/$project_name/` ready for content creation

---

## Integration Points

### With Content Writing Skill

Research files can be used as source documents in content creation:

```bash
# 1. Research topic
research-skill query "Latest trends in AI coding assistants"

# 2. Kickoff project
research-skill kickoff 2025-10-27-latest-ai-coding-assistant-news tutorial-ai-coding

# 3. Create outline (content-writing-skill reads sources/research/ files)
content-writing-skill outline tutorial-ai-coding intro-to-ai-coding

# 4. Generate draft
content-writing-skill draft tutorial-ai-coding intro-to-ai-coding
```

### With Project Management Skill

Research can inform project planning:

```bash
# Discovery phase
research-skill discover "API development trends"

# Review findings with project management
/resume-project api-best-practices

# Project management skill will see research files in sources/research/
```

---

## Configuration

### Perplexity API Settings

Located in `.kurt/research-config.json`:

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

**Models available:**
- `sonar-reasoning` - Best for comprehensive research (default)
- `sonar` - Faster, good for quick queries
- `sonar-pro` - Most powerful, higher cost

**Recency filters:**
- `hour` - Last hour (breaking news)
- `day` - Last 24 hours (daily monitoring)
- `week` - Last 7 days (weekly trends)
- `month` - Last 30 days (broader research)

### Saved Topics

Optional file `sources/research/topics.md` for daily monitoring:

```markdown
# Research Topics

Areas to monitor daily:
- AI coding tools and assistants
- Developer productivity tools
- Cloud infrastructure trends
- API development and integration

Last updated: 2025-10-27
```

---

## File Structure

```
sources/research/
├── topics.md                                    # Saved monitoring topics
├── 2025-10-27-latest-ai-coding-news.md         # Research results
├── 2025-10-27-api-trends-discovery.md          # Discovery report
└── 2025-10-26-vector-databases-deep-dive.md    # Deep dive research

projects/
└── tutorial-ai-coding/
    ├── project.md                               # Links to research source
    └── assets/
        └── intro-outline.md                     # Cites research file
```

---

## Error Handling

### API Key Issues

If Perplexity API key is missing or invalid:
```
ERROR: Perplexity not configured
Add your API key to .kurt/research-config.json
See .kurt/README.md for setup instructions
Get API key: https://www.perplexity.ai/settings/api
```

### API Rate Limits

If rate limited:
```
ERROR: Perplexity API rate limit exceeded
Please wait a few minutes and try again
Consider upgrading your API plan for higher limits
```

### Network Issues

If API request fails:
```
ERROR: Could not connect to Perplexity API
Check your internet connection
Verify API endpoint is accessible
```

---

## Advanced Usage

### Custom Queries with Specific Domains

Research only from specific domains:

```bash
# Research from specific sources (future enhancement)
kurt research search "API best practices" \
  --domains "docs.anthropic.com,developer.mozilla.org" \
  --save
```

### Research Series

Research multiple related topics:

```bash
# Create research series for comprehensive coverage
for topic in "AI coding" "API development" "Cloud infrastructure"; do
  kurt research search "Latest trends in $topic" --recency week --save
  sleep 5  # Rate limit friendly
done

# Then browse all results
research-skill browse
```

### Scheduled Daily Digest

Set up cron job for daily research:

```bash
# Run daily at 9am
0 9 * * * cd /path/to/kurt-demo && research-skill daily >> .logs/research.log 2>&1
```

---

## Tips

1. **Be specific with queries** - "Latest Claude Code features" is better than "AI tools"
2. **Use appropriate recency** - Breaking news needs `--recency hour`, trends need `--recency week`
3. **Save valuable research** - Always use `--save` flag for important queries
4. **Review citations** - Research files include full citation list in YAML frontmatter
5. **Integrate with content** - Use research files as sources in content-writing-skill
6. **Monitor regularly** - Daily research helps identify trends early
7. **Clean up old research** - Archive or delete outdated research files periodically

---

## See Also

- CLI Reference: `kurt research --help`
- Configuration: `.kurt/README.md`
- Content Integration: `content-writing-skill`
- Project Planning: `project-management-skill`
- Perplexity Docs: https://docs.perplexity.ai/
