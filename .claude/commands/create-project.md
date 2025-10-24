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

   **Step 2a: Map sitemap (discover URLs)**
   ```bash
   # Map entire domain sitemap
   python .claude/scripts/map_sitemap.py <domain> --recursive

   # Example:
   python .claude/scripts/map_sitemap.py docs.getdbt.com --recursive
   ```

   This discovers all URLs from the sitemap and stores them in `sources/{domain}/_content-map.json` with status: `DISCOVERED`

   **Step 2b: Review discovered content**
   ```bash
   # See what was discovered
   cat sources/<domain>/_content-map.json | jq '{
     total: (.sitemap | length),
     by_type: .content_types
   }'

   # List specific content types
   cat sources/<domain>/_content-map.json | jq '.sitemap |
     to_entries[] |
     select(.value.content_type == "docs") |
     .key' | head -10
   ```

   **Step 2c: Fetch content (automatic indexing)**

   Content is fetched on-demand using WebFetch. The hooks automatically:
   - Save to `/sources/{domain}/{path}.md` with frontmatter
   - Extract metadata (topics, entities, summary)
   - Update content map with status: `FETCHED`

   **Option 1: Fetch specific pages** (recommended)
   ```
   Use WebFetch tool for specific URLs you need:
   - Claude Code will suggest relevant pages based on content map
   - Hooks automatically save + index each page
   ```

   **Option 2: Batch fetch** (if you know exactly what you need)
   ```
   # Get URLs from content map
   urls=$(cat sources/<domain>/_content-map.json | jq -r '.sitemap |
     to_entries[] |
     select(.value.content_type == "docs") |
     .key' | head -20)

   # Fetch each (Claude can do this in a loop)
   for url in $urls; do
     # Use WebFetch tool for each URL
   done
   ```

   **Important:**
   - **Mapping** creates content map with all URLs (status: DISCOVERED)
   - **WebFetch** saves file + extracts metadata (status: FETCHED)
   - **Hooks run automatically** - no manual indexing needed
   - **Content map** tracks all URLs, statuses, and metadata

   - Note the source domain in project.md

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
   - Search in `/sources/` if already mapped/fetched
   - **Check fetch status in content map:**
   ```bash
   # Check if URL is in content map
   cat sources/<domain>/_content-map.json | jq '.sitemap["<target-url>"]'

   # If DISCOVERED but not FETCHED:
   # Use WebFetch tool to fetch it (hooks auto-index)

   # If not in content map at all:
   # 1. Map the domain sitemap first
   # 2. Or use WebFetch directly (hooks auto-save + index)
   ```
   - Or note URLs to fetch later

3. **For new content:**
   - Ask for planned file names
   - Note in Targets as planned drafts

4. Update project.md Targets section

**If they choose (b) - Skip:**
- Note in project.md that targets will be added later
- Continue to Step 5

## Step 4.5: Verify Content Map Status

**Before proceeding to rule extraction**, verify that sources and targets are available in content map:

### Check Content Map Exists

```bash
# Check if domain is mapped
ls sources/<domain>/_content-map.json

# If not, map the sitemap first:
python .claude/scripts/map_sitemap.py <domain> --recursive
```

### Check Sources and Targets Status

For each source/target domain in project.md:

```bash
# Get status summary
cat sources/<domain>/_content-map.json | jq '{
  total_urls: (.sitemap | length),
  discovered: [.sitemap | to_entries[] | select(.value.status == "DISCOVERED")] | length,
  fetched: [.sitemap | to_entries[] | select(.value.status == "FETCHED")] | length,
  content_types: (.sitemap | group_by(.content_type) | map({type: .[0].content_type, count: length}))
}'

# Check specific URLs
cat sources/<domain>/_content-map.json | jq '.sitemap["<specific-url>"]'
```

### Display Status Summary

```
Content Map Status:

docs.getdbt.com:
✓ 1,339 URLs mapped
✓ 45 fetched + indexed (files in /sources/, metadata extracted)
○ 1,294 discovered (available to fetch on-demand)

Content types available:
- 675 docs pages
- 228 blog posts
- 130 support pages
- 89 tutorials

Action available:
- Fetch specific pages on-demand with WebFetch (auto-indexed via hooks)
- Or batch fetch by content type
```

### Fetch Key Content (If Needed)

**On-demand (recommended):**
```
Use WebFetch tool for specific URLs:
- Hooks automatically save + index each page
- Content map updated from DISCOVERED → FETCHED
```

**Batch by content type:**
```bash
# Get URLs of specific type
cat sources/<domain>/_content-map.json | jq -r '.sitemap |
  to_entries[] |
  select(.value.content_type == "docs") |
  select(.value.status == "DISCOVERED") |
  .key' | head -20

# Then use WebFetch for each URL
# Hooks automatically handle save + indexing
```

**Important:**
- **Mapping** should be done first (creates content map)
- **WebFetch** fetches + indexes automatically (hooks)
- **No manual indexing needed** - hooks extract metadata
- **Content map** tracks all URLs and their status

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
# Verify domain is mapped and has fetched content
cat sources/<domain>/_content-map.json | jq '{
  fetched: [.sitemap | to_entries[] | select(.value.status == "FETCHED")] | length,
  with_topics: [.sitemap | to_entries[] | select(.value.topics)] | length
}'

# Should show fetched content with topics/metadata
```

**⚠️ If no content fetched yet:**
```
Cannot extract rules yet - need fetched content first.

Options:
1. Use WebFetch to fetch specific pages (recommended)
2. Batch fetch by content type from content map

After fetching, hooks automatically extract metadata.
Ready to extract rules once content is fetched.
```

1. **Start with publisher profile** (if not already extracted):
   ```bash
   # Check if publisher profile exists
   ls /rules/publisher/publisher-profile.md

   # If not, extract from company pages (must be fetched + indexed)
   invoke publisher-profile-extraction-skill --auto-discover
   ```

2. **Extract corporate voice** (if not already extracted):
   ```bash
   invoke style-extraction-skill --type corporate --auto-discover
   ```

3. **Ask about content-specific rules based on project intent:**

   - **If intent (b) - marketing assets or (a) - positioning:**
     - Ask: "Extract landing page structure?" → structure-extraction-skill
     - Ask: "Extract marketing persona?" → persona-extraction-skill

   - **If intent (c) - technical docs:**
     - Ask: "Extract technical doc style?" → style-extraction-skill --type technical-docs
     - Ask: "Extract tutorial/guide structure?" → structure-extraction-skill --type tutorial
     - Ask: "Extract developer persona?" → persona-extraction-skill --audience-type technical

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
