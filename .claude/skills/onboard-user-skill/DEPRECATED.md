# ⚠️ DEPRECATED: User Onboarding Skill

This skill is **deprecated** - replaced by project commands.

## Replacement

Use **`/create-project`** and **`/resume-project`** commands instead.

### What This Skill Did

- Guided new users through 7-step setup workflow
- Mapped content sources
- Computed clusters
- Extracted rules
- Created projects

### New Approach

**Project commands** handle all onboarding:

#### For New Users

Use **`/create-project`** - Interactive project creation:

```bash
/create-project
```

**Workflow**:
1. Asks about project intent (positioning, marketing, docs updates)
2. Helps collect sources (maps sitemaps, queries content)
3. Identifies targets (existing or new content)
4. Verifies content is fetched and indexed
5. Optionally extracts rules (style, structure, personas)
6. Creates organized project structure

#### For Returning Users

Use **`/resume-project`** - Resume existing projects:

```bash
/resume-project
# Or with project name
/resume-project my-project-name
```

**Workflow**:
1. Lists available projects
2. Checks content map status
3. Verifies sources and targets are fetched
4. Checks rule coverage
5. Recommends next steps based on project state

## Exploratory Discovery (Without Project)

If you just want to explore content without creating a project:

### 1. Map a Domain

```bash
python .claude/scripts/map_sitemap.py docs.example.com --recursive
```

### 2. Query Content Map

```bash
# See what content types exist
cat sources/docs.example.com/_content-map.json | jq '{
  total: (.sitemap | length),
  by_type: (.sitemap | group_by(.content_type) |
    map({type: .[0].content_type, count: length}))
}'

# List specific content types
cat sources/docs.example.com/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "guide") |
  .key' | head -10
```

### 3. Fetch Content

Use WebFetch tool on URLs you want to explore (hooks auto-save + index)

### 4. Create Project When Ready

Once you know what you want to work on:
```bash
/create-project
```

## Benefits of New Approach

1. **More Focused** - Project commands are goal-oriented
2. **Better Integration** - Commands work with file-based content maps
3. **Cleaner Workflow** - No database, no CLI orchestration
4. **Same Features** - All onboarding functionality preserved

## Comparison

| Feature | Onboard Skill | /create-project |
|---------|---------------|-----------------|
| Understand intent | ✓ | ✓ |
| Map sources | Kurt CLI | File-based |
| Compute clusters | Separate step | Automatic on fetch |
| Extract rules | ✓ | ✓ |
| Create project | Manual | Automatic |
| Resume work | - | /resume-project |

## Migration

Instead of:
```bash
invoke onboard-user-skill
```

Use:
```bash
/create-project
```

**All onboarding is now handled by project commands.**
