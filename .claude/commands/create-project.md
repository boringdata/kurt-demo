---
description: Create a new Kurt project with goals and structure
---

# Create New Kurt Project

Help the user create a new Kurt project by following these steps:

## Step 1: Understand Project Intent

Ask the user what they want to accomplish:

> What are you looking to accomplish with this project?
>
> a) Update core product positioning + messaging (on website or internally)
> b) Write new marketing assets (e.g., for a product launch)
> c) Make sure technical docs + tutorials are up-to-date (and update or remove stale content)
> d) Nothing specific, just setting up a general project
> e) Something else (please describe)

**Wait for the user's response before proceeding.**

## Step 2: Get Project Name and Goal

Ask the user for:
1. **Project name** (use kebab-case: e.g., `product-messaging-refresh`, `q4-launch-content`)
2. **Brief description** of what they want to accomplish

**Project naming guidelines:**
- Use kebab-case: `product-messaging-refresh` not `Product Messaging Refresh`
- Be specific: `q4-launch-content` not `marketing`
- Keep it short: 2-4 words maximum

## Step 3: Collect Ground Truth Sources (Skippable)

Ask the user for source material they'll be working FROM:

> Do you have ground truth sources (material you'll work FROM)?
>
> Examples based on your project type:
> - **(a) Positioning**: Product docs, value props, competitive research
> - **(b) Marketing assets**: Product specs, feature docs, launch plans
> - **(c) Docs updates**: Technical specs, feature documentation
>
> Options:
> a) Add sources now (URLs or local files)
> b) Skip for now (add later)

**If they choose (a) - Add sources now:**

1. Ask: "What sources do you have?"
   - Web pages (URLs)
   - Local files (PDFs, markdown, etc.)
   - Both

2. **For web content:**

   **Step 2a: Map (discover URLs)**
   ```bash
   kurt ingest map <url>
   # Or with date discovery for blogs/docs
   kurt ingest map <url> --discover-dates
   ```

   **Step 2b: Fetch (download content)**
   ```bash
   # Check current fetch status
   kurt document list --url-prefix <url> --status NOT_FETCHED

   # Fetch content
   kurt ingest fetch --url-prefix <url>

   # Verify fetch completed
   kurt document list --url-prefix <url> --status FETCHED
   ```

   **Step 2c: Index (extract metadata + topics)**
   ```bash
   # Index fetched content for LLM analysis
   kurt index --url-prefix <url>

   # Verify indexing completed (check for topics/metadata)
   kurt document get <url>  # Should show extracted metadata
   ```

   **Important:**
   - **Fetch** creates the file in `/sources/`
   - **Index** extracts metadata (title, author, topics) via LLM analysis
   - Both are required for full content intelligence

   - Note the source paths in project.md

3. **For local files:**
   - Ask for file paths
   - Copy to `projects/<project-name>/sources/`
   - Note the files in project.md

4. Update project.md Sources section

**If they choose (b) - Skip:**
- Note in project.md that sources will be added later
- Continue to Step 4

## Step 4: Identify Target Content (Skippable)

Ask the user what content they'll be working ON:

> What content will you be updating or creating (working ON)?
>
> a) Identify targets now
> b) Skip for now (add later)

**If they choose (a) - Identify targets:**

1. Ask: "What content needs work?"
   - Existing content to update
   - New content to create
   - Both

2. **For existing content:**
   - Search in `/sources/` if already ingested
   - **Check fetch + index status:**
   ```bash
   # Check if content is fetched
   kurt document list --url <target-url>

   # If NOT_FETCHED, fetch it:
   kurt ingest fetch <target-url>

   # Check if content is indexed (has metadata)
   kurt document get <target-url>

   # If not indexed, index it:
   kurt index --url <target-url>
   ```
   - Or note URLs/paths to fetch/index later

3. **For new content:**
   - Ask for planned file names
   - Note in Targets as planned drafts

4. Update project.md Targets section

**If they choose (b) - Skip:**
- Note in project.md that targets will be added later
- Continue to Step 5

## Step 4.5: Verify Fetch + Index Status

**Before proceeding to rule extraction**, verify that all sources and targets are fully processed:

### Check Sources

For each source URL/path in project.md:

```bash
# 1. Check fetch status
kurt document list --url <source-url>

# 2. If NOT_FETCHED, fetch it
kurt ingest fetch <source-url>

# 3. Check index status (look for extracted metadata)
kurt document get <source-url>

# 4. If not indexed (no topics/metadata), index it
kurt index --url <source-url>
```

### Check Targets

For each target URL in project.md:

```bash
# Same process as sources
# 1. Check fetch status
kurt document list --url <target-url>

# 2. Fetch if needed
kurt ingest fetch <target-url>

# 3. Index if needed
kurt index --url <target-url>
```

### Display Status Summary

```
Content Processing Status:

Sources:
✓ 5 fetched (files in /sources/)
✓ 5 indexed (metadata extracted)
✗ 2 not fetched yet
✗ 3 fetched but not indexed

Targets:
✓ 10 fetched
✗ 10 fetched but not indexed (need to run: kurt index --url-prefix <prefix>)

Action needed:
- Fetch 2 remaining sources
- Index 3 sources + 10 targets
```

### Run Batch Operations

**Fetch remaining content:**
```bash
kurt ingest fetch --url-prefix <common-prefix>
```

**Index all fetched content:**
```bash
# Index by URL prefix
kurt index --url-prefix <common-prefix>

# Or index specific URLs
kurt index --url <url1> --url <url2>
```

**Important:**
- **Fetch first, then index** (indexing requires fetched content)
- **Batch operations are faster** than individual URLs
- **Indexing is required** for rule extraction (needs content analysis)
- **Wait for indexing to complete** before extracting rules

## Step 5: Extract Rules (Optional but Recommended)

If the user has added sources in Step 3 AND they are fetched + indexed, ask if they want to extract reusable rules:

> Would you like to extract writing rules from your content? This helps ensure consistency when creating/updating content.
>
> Rules include:
> - **Corporate voice** - Brand voice from marketing pages
> - **Content type styles** - Writing patterns for docs, blog, etc.
> - **Structure templates** - Document formats (tutorials, API docs, etc.)
> - **Personas** - Audience targeting patterns
> - **Publisher profile** - Company messaging and positioning
>
> Options:
> a) Extract rules now (recommended if sources available)
> b) Skip for now (can extract later)

**If they choose (a) - Extract rules now:**

**Prerequisites check:**
```bash
# Verify sources are fetched + indexed
kurt document list --url-prefix <url> --status FETCHED
kurt document get <url>  # Should show metadata

# If not indexed, must run:
kurt index --url-prefix <url>
```

**⚠️ If sources not indexed:**
```
Cannot extract rules yet - content must be indexed first.

Running: kurt index --url-prefix <url>
Please wait... (this may take 10-30 seconds depending on content volume)

✓ Indexing complete. Ready to extract rules.
```

1. **Start with publisher profile** (if not already extracted):
   ```bash
   # Check if publisher profile exists
   ls /rules/publisher/publisher-profile.md

   # If not, extract from company pages (must be fetched + indexed)
   writing-rules-skill publisher --auto-discover
   ```

2. **Extract corporate voice** (if not already extracted):
   ```bash
   writing-rules-skill style --type corporate --auto-discover
   ```

3. **Ask about content-specific rules based on project intent:**

   - **If intent (b) - marketing assets or (a) - positioning:**
     - Ask: "Extract landing page structure?" → `writing-rules-skill structure --type landing-page --auto-discover`
     - Ask: "Extract marketing persona?" → `writing-rules-skill persona --audience-type business --auto-discover`

   - **If intent (c) - technical docs:**
     - Ask: "Extract technical doc style?" → `writing-rules-skill style --type technical-docs --auto-discover`
     - Ask: "Extract tutorial/guide structure?" → `writing-rules-skill structure --type tutorial --auto-discover`
     - Ask: "Extract developer persona?" → `writing-rules-skill persona --audience-type technical --auto-discover`

4. **Update project.md** with extracted rules references

**If they choose (b) - Skip:**
- Note in project.md that rules can be extracted later
- Continue to Step 6

**Important notes:**
- Publisher profile + corporate voice are most important (do first)
- Content-specific rules depend on what user will create
- Can always extract more rules later as needed

## Step 6: Create Project Structure

Once you have the name, goal, and optionally sources/targets/rules:

1. Create the project directory structure:
   ```bash
   mkdir -p projects/<project-name>/sources
   mkdir -p projects/<project-name>/targets/drafts
   ```

2. Create `projects/<project-name>/project.md` with this template:

```markdown
# <Project Name>

## Goal
<User's description of what they want to accomplish>

## Intent Category
<a/b/c/d/e from Step 1>

## Sources (Ground Truth)

### From Organizational Knowledge Base
<Web content fetched to /sources/ - add references here>

### Project-Specific Sources
<Local files in projects/<name>/sources/ - add references here>

## Targets (Content to Update/Create)

### Existing Content to Update
<Content in /sources/ that needs updating>

### New Content to Create
<Planned new content to draft>

## Style Guidelines

*Extracted writing patterns applicable to this project's content:*
<If extracted in Step 5, list them here. Otherwise leave note: "To be extracted">

## Structure Templates

*Document format templates applicable to this project's content:*
<If extracted in Step 5, list them here. Otherwise leave note: "To be extracted">

## Target Personas

*Audience profiles for this project's target content:*
<If extracted in Step 5, list them here. Otherwise leave note: "To be extracted">

## Publisher Profile

*Organizational context for brand consistency:*
<If extracted in Step 5, reference it. Otherwise leave note: "To be extracted">

## Progress
- [x] Project created (<today's date>)

## Next Steps
<Will be updated as work progresses>
```

## Step 7: Offer Next Steps

After creating the project, summarize what was set up:

> Project created at `projects/<project-name>/`
>
> Status:
> - Sources: <count> added (or "none yet")
> - Targets: <count> identified (or "none yet")
> - Rules: <list extracted rules or "none yet">

Then ask:

> Would you like to:
>
> a) Add more sources or targets now
> b) Start working on content
> c) Save and resume later

**If they choose (a):**
- Use project-management-skill to add sources/targets
- Update project.md accordingly

**If they choose (b):**
- Ask what they want to work on
- Proceed with content work

**If they choose (c):**
- Let them know they can resume with `/resume-project <project-name>`
- Remind them about project-management-skill for adding sources

## Important Notes

- Always create the `projects/` directory if it doesn't exist
- Use the exact template structure for project.md
- Update project.md as you gather more information
- Keep the user informed about each step
