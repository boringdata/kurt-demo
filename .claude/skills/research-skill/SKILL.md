---
name: research
description: Low-level research operations for AI-powered topic discovery and monitoring (general)
---

# Research Skill

## Overview

This skill provides **low-level research operations** using Perplexity AI and monitoring sources (Reddit, Hacker News, RSS). Use this skill when users need AI-powered research, topic discovery, or trend monitoring.

**Key principle:** This is a **utility skill** - it wraps `kurt research` CLI commands. It can be used directly by users OR called by higher-level skills (like content-writing or project-management).

---

## When to Use This Skill

✅ **Use research-skill when:**
- User asks for research on a specific topic: "Research AI coding tools trends"
- Need to discover what's trending: "What's popular on r/dataengineering today?"
- Monitoring competitor content: "Track dbt blog posts"
- Finding discussions: "See what people are saying about Snowflake on Hacker News"
- Review past research: "Show me recent research"

❌ **Don't use research-skill when:**
- User wants to search internal content → Use `cms-interaction-skill`
- Need web/CMS content ingestion → Use `kurt map` + `kurt fetch`
- Creating content from research → That's content-writing-skill's job (it can call this skill)

**Rule of thumb:** If it's AI research or monitoring external sources, use this skill. If it's searching/fetching internal content, use other skills.

**Note:** For orchestrating multiple research operations together, use workflows or project-management skills.

---

## Key Concept: Research ≠ Documents

**Research files:**
- Ephemeral (news, trends, discussions, time-sensitive topics)
- Saved as markdown in `sources/research/` or `projects/<name>/research/signals/`
- **NOT** imported to Kurt database
- Can be referenced as sources in content projects
- Browse with `kurt research list` (NOT `kurt content list`)

**Web/CMS content:**
- Stable documentation, articles, reference material
- Imported to Kurt DB for indexing and clustering
- Browse with `kurt content list`

---

## Operations

### 1. `search "<query>" [--recency hour|day|week|month] [--save]`

**Purpose:** Execute AI-powered research query using Perplexity

**Implementation:**
```bash
kurt research search "<query>" \
  ${recency:+--recency $recency} \
  ${save:+--save}
```

**Example usage:**
```
User: Research recent AI coding tools news

Claude (invokes research search "AI coding tools" --recency week --save):

Researching: AI coding tools
Recency: week

✓ Research complete (3.2s)

[AI-generated answer with inline citations]

**Key developments this week:**
- GitHub Copilot X announced with chat interface [1]
- Cursor raises $60M Series A for AI-first IDE [2]
...

Sources (15):
[1] https://github.blog/copilot-x
[2] https://techcrunch.com/cursor-funding
...

✓ Saved to: sources/research/2025-11-03-ai-coding-tools.md
```

**Options:**
- `--recency hour|day|week|month` - Time filter for results
- `--save` - Save results to sources/research/
- `--model sonar-reasoning|sonar|sonar-pro` - Override model
- `--output markdown|json` - Output format

**Recency guidance:**
- `hour` - Breaking news, real-time events
- `day` - Recent news (default for news queries)
- `week` - Trends, weekly roundups
- `month` - Monthly analysis, slower-moving topics
- Omit for general/timeless queries

---

### 2. `list [--limit N]`

**Purpose:** Browse past research results

**Implementation:**
```bash
kurt research list ${limit:+--limit $limit}
```

**Example usage:**
```
User: Show me recent research

Claude (invokes research list --limit 10):

Recent Research (23 results)

2025-11-03-ai-coding-tools.md
  Query: AI coding tools
  Date: 2025-11-03
  Sources: 15

2025-11-02-dbt-vs-dataform.md
  Query: dbt vs Dataform comparison
  Date: 2025-11-02
  Sources: 12

2025-11-01-snowflake-pricing.md
  Query: Snowflake cost optimization strategies
  Date: 2025-11-01
  Sources: 8

...
```

**Options:**
- `--limit N` - Show only N most recent results (default: 20)

---

### 3. `get <filename>`

**Purpose:** Display specific research result

**Implementation:**
```bash
kurt research get <filename>
```

**Example usage:**
```
User: Show me that dbt research

Claude (invokes research get 2025-11-02-dbt-vs-dataform):

Research Result
File: 2025-11-02-dbt-vs-dataform.md

Query: dbt vs Dataform comparison
Date: 2025-11-02
Source: perplexity
Sources: 12 citations

[Full research content displayed]
```

**Note:** Filename can be with or without .md extension

---

### 4. `reddit -s <subreddit> [--keywords "..."] [--min-score N]`

**Purpose:** Monitor Reddit for trending discussions

**Implementation:**
```bash
kurt research reddit -s <subreddit> \
  ${keywords:+--keywords "$keywords"} \
  ${min_score:+--min-score $min_score} \
  --timeframe ${timeframe:-day}
```

**Example usage:**
```
User: What's trending on r/dataengineering today?

Claude (invokes research reddit -s dataengineering --timeframe day --min-score 10):

Monitoring: r/dataengineering

✓ Found 15 posts

#  Title                                                Score  Comments  Relevance
1  "Dagster vs Prefect: Production experience?"         142    87        0.95
2  "How to handle slowly changing dimensions in dbt"     98    45        0.87
3  "Snowflake pricing is getting ridiculous"             76    62        0.82
...

User: Filter for dbt and Fivetran

Claude (invokes research reddit -s dataengineering --keywords "dbt,fivetran"):

Found 6 posts matching keywords...
```

**Options:**
- `-s <subreddit>` - Subreddit name (required)
- `--keywords "word1,word2"` - Filter by keywords
- `--min-score N` - Minimum upvotes threshold
- `--timeframe hour|day|week|month` - Time window
- `--output table|json` - Output format

**Multi-subreddit:**
```bash
# Monitor multiple subreddits
research reddit -s "dataengineering+datascience"
```

---

### 5. `hackernews [--keywords "..."] [--min-score N]`

**Purpose:** Monitor Hacker News for trending tech discussions

**Implementation:**
```bash
kurt research hackernews \
  ${keywords:+--keywords "$keywords"} \
  ${min_score:+--min-score $min_score} \
  --timeframe ${timeframe:-day}
```

**Example usage:**
```
User: What's hot on Hacker News about AI?

Claude (invokes research hackernews --keywords "AI" --timeframe day):

Monitoring: Hacker News (day)
Keywords: AI

✓ Found 12 stories

#  Title                                            Points  Comments  Relevance
1  "Show HN: Open source AI coding assistant"       324     142       0.98
2  "AI won't replace developers, but..."            287     203       0.94
3  "Anthropic announces Claude 3.5"                 245     156       0.91
...
```

**Options:**
- `--keywords "word1,word2"` - Filter by keywords
- `--min-score N` - Minimum points (default: 10)
- `--timeframe hour|day|week|month` - Time window
- `--output table|json` - Output format

---

### 6. `feeds <feed-url> [--keywords "..."] [--since "7 days"]`

**Purpose:** Monitor RSS/Atom feeds for new content

**Implementation:**
```bash
kurt research feeds <feed-url> \
  ${since:+--since "$since"} \
  ${keywords:+--keywords "$keywords"}
```

**Example usage:**
```
User: Check dbt blog for new posts

Claude (invokes research feeds https://blog.getdbt.com/rss.xml --since "7 days"):

Monitoring feed: https://blog.getdbt.com/rss.xml
Since: 2025-10-27 00:00

✓ Found 3 entries

#  Title                                   Published    Domain
1  "Introducing dbt Cloud IDE v2"          2025-11-01   blog.getdbt.com
2  "dbt Semantic Layer updates"            2025-10-29   blog.getdbt.com
3  "How we use dbt at Scale"               2025-10-28   blog.getdbt.com

User: Only show posts about semantic layer

Claude (invokes research feeds https://blog.getdbt.com/rss.xml --keywords "semantic layer"):

Found 1 entry matching keywords...
```

**Options:**
- `<feed-url>` - RSS/Atom feed URL (required)
- `--since "N days|hours|weeks"` - Only entries since
- `--keywords "word1,word2"` - Filter by keywords
- `--limit N` - Max entries (default: 50)
- `--output table|json` - Output format

**Common feeds:**
- dbt blog: `https://blog.getdbt.com/rss.xml`
- Fivetran blog: `https://fivetran.com/blog/rss.xml`
- Airbyte blog: `https://airbyte.com/blog/rss.xml`

---

## Conversational Presentation

**Always provide:**
- Clear results summary with counts
- Relevant filtering hints based on results
- Suggestions for next steps
- Save confirmation when using --save

**Example good presentation:**
```
✓ Found 23 posts on r/dataengineering

HIGH RELEVANCE (>0.8): 6 posts
Most relevant to your keywords
1. "Dagster vs Prefect comparison" (142 points, 0.95 relevance)
   💡 Hot discussion - 87 comments

MEDIUM RELEVANCE (0.5-0.8): 10 posts
...

Suggestions:
- Add more specific keywords to refine results
- Check r/datascience too for broader coverage
- Save these for your project: research reddit -s dataengineering --keywords "..." --save
```

---

## Error Handling

### Perplexity not configured
```
⚠️ Perplexity not configured

Add your API key to .kurt/research-config.json:
{
  "perplexity": {
    "api_key": "your-key-here"
  }
}

Get API key from: https://www.perplexity.ai/settings/api
```

### No results found
```
No posts found matching criteria

Try:
- Broader time window: --timeframe week
- Lower score threshold: --min-score 5
- Different subreddit or remove keyword filters
```

### Feed fetch failed
```
⚠️ Failed to fetch feed: https://example.com/rss.xml

Possible causes:
- Feed URL changed or moved
- Temporary network issue
- Feed no longer exists

Check feed URL in browser first
```

---

## Key Principles

1. **Low-level utility** - Wraps `kurt research` commands with minimal orchestration
2. **Research is ephemeral** - Saved as markdown files, NOT in DB
3. **Used by humans and skills** - Can be called directly or by other skills
4. **Time-aware** - Use recency filters appropriately
5. **Composable** - Individual operations can be combined in workflows and projects

---

## See Also

- **content-writing-skill** - Uses research results as project sources
- **project-management-skill** - May call this for gathering research sources
