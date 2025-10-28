# Kurt Configuration Guide

This document maps all configuration files in the Kurt system to their locations and purposes.

---

## Configuration Hierarchy

Kurt uses a two-level configuration hierarchy:

1. **Global Configs** (`.kurt/`) - User-level settings and credentials (gitignored)
2. **Project Configs** (`projects/<name>/`) - Project-specific settings (gitignored)
3. **System Configs** (`rules/`) - Rule type definitions (tracked in git)

---

## Global Configurations (`.kurt/`)

**Location:** `.kurt/` directory in your project root
**Git Status:** Gitignored (contains secrets)
**Purpose:** Store API credentials and global templates

### `cms-config.json`
**CMS integration credentials**

```json
{
  "sanity": {
    "project_id": "your-project-id",
    "dataset": "production",
    "token": "sk...read-token",
    "write_token": "sk...write-token",
    "base_url": "https://yoursite.com",
    "content_type_mappings": {
      "article": {
        "enabled": true,
        "content_field": "content_body_portable",
        "title_field": "title",
        "slug_field": "slug.current"
      }
    }
  }
}
```

**Used by:**
- `kurt cms` commands (search, fetch, import, publish)
- cms-interaction-skill

**Setup:**
1. Create file: `.kurt/cms-config.json`
2. Add credentials from your CMS (Sanity, Contentful, WordPress)
3. Run `kurt cms onboard` to auto-discover content types
4. File is automatically gitignored via `.kurt/*` pattern

**Learn more:** `.claude/skills/cms-interaction-skill/SKILL.md`

---

### `research-config.json`
**Research API credentials (Perplexity, etc.)**

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

**Used by:**
- `kurt research search` command
- `kurt research monitor` command
- research-skill

**Setup:**
1. Get API key: https://www.perplexity.ai/settings/api
2. Create file: `.kurt/research-config.json`
3. Add your API key and preferences
4. Test: `kurt research search "test query"`

**Learn more:** `.kurt/README.md` → "Perplexity Research API"

---

### `monitoring-config-template.yaml`
**Template for project monitoring configs**

```yaml
project_name: your-project-name
description: Brief description

sources:
  reddit:
    enabled: true
    subreddits: [dataengineering]
    keywords: []
    min_score: 10
    timeframe: day

  hackernews:
    enabled: true
    keywords: []
    min_score: 50
    timeframe: day

  feeds:
    enabled: true
    urls:
      - url: https://blog.example.com/rss.xml
        name: Example Blog
    since: "7 days"
```

**Used by:**
- Users creating new projects
- `research-skill setup-monitoring` (interactive)

**Setup:**
- Don't edit this file directly!
- Copy to `projects/<your-project>/monitoring-config.yaml`
- Or use: `research-skill setup-monitoring <project-name>` (recommended)

**Learn more:** `.kurt/README.md` → "Project-Based Monitoring"

---

## Project Configurations (`projects/<name>/`)

**Location:** `projects/<project-name>/` subdirectories
**Git Status:** Gitignored
**Purpose:** Project-specific monitoring and research settings

### `monitoring-config.yaml`
**Project monitoring configuration**

Located: `projects/<project-name>/monitoring-config.yaml`

**Purpose:**
- Define Reddit subreddits to monitor
- Set Hacker News search keywords
- Configure RSS feeds to track
- Set minimum score thresholds

**Setup:**

**Option 1: Interactive (Recommended)**
```bash
research-skill setup-monitoring your-project
```

**Option 2: Manual**
```bash
cp .kurt/monitoring-config-template.yaml projects/your-project/monitoring-config.yaml
# Edit the file
```

**Usage:**
```bash
kurt research monitor projects/your-project
```

**Output:**
- Saves signals to: `projects/<project>/research/signals/YYYY-MM-DD-signals.json`
- Shows top 10 signals in terminal

**Learn more:**
- `.kurt/README.md` → "Project-Based Monitoring"
- `projects/data-tools-watch/WORKFLOW.md` (example)

---

## System Configurations (`rules/`)

**Location:** `rules/` directory
**Git Status:** Tracked in git (shared across team)
**Purpose:** Define available rule types for content creation

### `rules-config.yaml`
**Rules registry - defines all available rule types**

Located: `rules/rules-config.yaml`

**Purpose:**
- Registry of built-in and custom rule types
- Defines what each rule type extracts
- Configures extraction subskills
- Sets up conflict detection

**Built-in rule types:**
- `style` - Writing voice, tone, sentence structure
- `structure` - Document organization, section flow
- `persona` - Target audience characteristics
- `publisher` - Organizational identity and positioning

**Managed by:**
- `writing-rules-skill` commands

**Common operations:**
```bash
# List all rule types
writing-rules-skill list

# View rule type details
writing-rules-skill show style

# Add custom rule type (interactive)
writing-rules-skill add

# Validate registry
writing-rules-skill validate
```

**Learn more:**
- `KURT.md` → "Rules System"
- `.claude/skills/writing-rules-skill/SKILL.md`

---

## Configuration Locations Quick Reference

| Config Type | Location | Gitignored? | Used By |
|------------|----------|-------------|---------|
| **CMS credentials** | `.kurt/cms-config.json` | ✅ Yes | kurt cms, cms-interaction-skill |
| **Research API keys** | `.kurt/research-config.json` | ✅ Yes | kurt research, research-skill |
| **Monitoring template** | `.kurt/monitoring-config-template.yaml` | ✅ Yes | Reference only |
| **Project monitoring** | `projects/<name>/monitoring-config.yaml` | ✅ Yes | kurt research monitor |
| **Rules registry** | `rules/rules-config.yaml` | ❌ No (tracked) | writing-rules-skill |

---

## Security Best Practices

### 1. Never Commit Secrets
- `.kurt/*` is gitignored by default
- `projects/*` is gitignored by default
- Never add exceptions for config files containing credentials

### 2. Rotate API Keys Regularly
- Research API keys (Perplexity)
- CMS tokens (Sanity, Contentful)

### 3. Use Read-Only Tokens When Possible
- CMS: Use read token for search/fetch, separate write token for publish
- Research: Perplexity tokens are read-only by default

### 4. Share Templates, Not Configs
- Commit: Templates (`.kurt/monitoring-config-template.yaml`)
- Don't commit: Actual configs with credentials

---

## Troubleshooting

### "Config file not found"

**For CMS:**
```bash
# Check if file exists
ls -la .kurt/cms-config.json

# Create from scratch
mkdir -p .kurt
echo '{"sanity": {"project_id": "YOUR_ID", "dataset": "production", "token": "YOUR_TOKEN"}}' > .kurt/cms-config.json

# Or run onboarding
kurt cms onboard
```

**For Research:**
```bash
# Check if file exists
ls -la .kurt/research-config.json

# Create template
mkdir -p .kurt
echo '{"perplexity": {"api_key": "YOUR_KEY", "default_model": "sonar-reasoning"}}' > .kurt/research-config.json
```

### "Invalid credentials"

```bash
# Verify config format
cat .kurt/cms-config.json | jq .
cat .kurt/research-config.json | jq .

# Check for placeholder values
grep -E "YOUR_|PLACEHOLDER" .kurt/*.json
```

### "Wrong config location"

**Before October 2025:**
Some old docs referenced `.claude/scripts/cms-config.json`

**Now:**
All configs live in `.kurt/` directory

**Migration:**
```bash
# If you have old config location, move it:
mv .claude/scripts/cms-config.json .kurt/cms-config.json
```

---

## See Also

- **System Overview:** `KURT.md`
- **User Instructions:** `CLAUDE.md`
- **Kurt Setup:** `.kurt/README.md`
- **Skills Documentation:** `.claude/skills/*/SKILL.md`
- **Example Project:** `projects/data-tools-watch/`
