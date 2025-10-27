---
name: cms-interaction
description: Complete CMS integration - onboard, search, fetch, import, and publish content (Sanity, Contentful, WordPress)
---

# CMS Interaction Skill

**Purpose:** End-to-end CMS integration for discovering, downloading, analyzing, and publishing content  
**Subskills:** onboard, search, fetch, import, publish  
**Supported CMSs:** Sanity (full support), Contentful (coming soon), WordPress (coming soon)

---

## Usage

**CMS functionality is now part of the core Kurt CLI.**

Use these commands directly:

```bash
# Interactive onboarding (first-time setup)
kurt cms onboard

# List available content types
kurt cms types

# Search CMS content
kurt cms search --query "tutorial" --content-type article

# Download CMS content as markdown
kurt cms fetch --id abc-123 --output-dir sources/cms/sanity/

# Import to Kurt database
kurt cms import --source-dir sources/cms/sanity/

# Publish draft to CMS
kurt cms publish --file draft.md --id abc-123
```

---

## Getting Started with Sanity

**If you have an existing Sanity account, here's how to get started:**

### Step 1: Get Sanity Credentials

From your Sanity project dashboard:

1. **Project ID**: Found in project settings or URL
2. **Dataset**: Usually `production`
3. **Read Token**: API → Tokens → Add New Token (Viewer role)
4. **Write Token** (optional): Add New Token (Editor role)

### Step 2: Create Initial Config

Create `.claude/scripts/cms-config.json`:

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

Add to `.gitignore`:
```bash
echo ".claude/scripts/cms-config.json" >> .gitignore
```

### Step 3: Run Onboarding

From Claude Code:
```
cms-interaction onboard
```

This discovers your content types and maps your custom field names.

### Step 4: Test Setup

```
cms-interaction search --limit 5
```

### Step 5: Complete Workflow

```bash
# Search
cms-interaction search --query "tutorial" --output json

# Fetch
cms-interaction fetch --document-id <id>

# Import
cms-interaction import --source-dir sources/cms/sanity/

# Create draft
content-writing-skill draft my-project updated-tutorial

# Publish to CMS
cms-interaction publish --file draft.md --document-id <id>
```

---

## Routing Logic

Routes to subskills based on first argument:

- `onboard` → subskills/onboard.md
- `search` → subskills/search.md
- `fetch` → subskills/fetch.md
- `import` → subskills/import.md
- `publish` → subskills/publish.md

---

## Workflow Examples

See full documentation in subskills for detailed examples.

---

*For complete documentation, see subskills/*.md files and README.md*
