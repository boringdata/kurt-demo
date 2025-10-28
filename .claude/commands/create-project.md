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

## Step 2.5: Check Organizational Foundation

**Before collecting project-specific sources**, verify that organizational context exists.

**Execute the shared foundation check:**

Follow the complete workflow in `.claude/commands/_shared/check-organizational-foundation.md`

**This will:**
1. **Check for Content Map** - Organizational content in `/sources/`
   - If missing: Guide user to provide root domains/sitemaps
   - For each domain: Map → Fetch → Index workflow

2. **Check for Core Rules** - Publisher profile + Primary voice + Personas
   - If missing: Extract from indexed content
   - Uses writing-rules-skill with --auto-discover

**If foundation exists:**
- Show quick summary
- Continue to Step 3

**If foundation missing:**
- Guide user through setup
- Takes 5-10 minutes for first-time setup
- Veteran users skip this automatically

**Why this matters:**
- Organizational context informs which project sources to use
- Having core rules before project work ensures consistency
- Content map shows what already exists (avoid duplication)

Once foundation check is complete, continue to Step 3.

## Step 3: Collect Ground Truth Sources (Skippable)

**Now that organizational context is established**, gather project-specific sources.

Ask the user for source material they'll be working FROM:

> Do you have ground truth sources (material you'll work FROM)?
>
> Examples based on your project type:
> - **(a) Positioning**: Product docs, value props, competitive research
> - **(b) Marketing assets**: Product specs, feature docs, launch plans
> - **(c) Docs updates**: Technical specs, feature documentation
>
> Options:
> a) Add sources now
> b) Skip for now (add later)

**If they choose (a) - Add sources now:**

Follow the **iterative source gathering workflow** in:

`.claude/commands/_shared/iterative-source-gathering.md`

**This workflow will:**
1. Ask user to describe sources needed
2. **CHECKPOINT 1**: Propose specific actions with preview
   - Show what will be fetched
   - Conversational exploration for research queries
   - User approves/refines/cancels each action
3. **EXECUTE**: Run approved actions with progress updates
4. **CHECKPOINT 2**: Review what was fetched
   - Show summary of fetched documents
   - Offer: Add more sources / Refine / Continue
5. **ITERATE**: Loop back until user is satisfied

**Key features:**
- Preview before fetching (see what will be discovered)
- Conversational refinement for research queries
- Review after fetching (evaluate if more sources needed)
- Two checkpoints ensure user validation before and after execution

**When iteration complete:**
- Update project.md with source list
- Continue to Step 4

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
> Options:
> a) Extract rules now (recommended if sources available)
> b) Skip for now (can extract later)

**If they choose (a) - Extract rules now:**

Follow the **iterative rule extraction workflow** in:

`.claude/commands/_shared/iterative-rule-extraction.md`

**This workflow will:**
1. **Prerequisites check**: Verify content is indexed (10+ pages minimum)
2. **Analyze**: Inventory available content by domain, type, date range
3. **Propose with preview**:
   - Show 3-5 sample document titles/URLs for each rule type
   - Show coverage stats (page count, date range, content types)
   - Explain what patterns could be learned
4. **User decision**: Approve / Refine (use different docs) / Skip
5. **Execute**: Run approved extractions with progress updates
6. **Review**: Show extracted rule file + key characteristics
7. **Iterate**: Offer to extract more rules or continue

**Key features:**
- Preview sample documents before extraction
- Start with foundation rules (publisher + primary voice)
- Propose content-specific rules based on project intent
- Explicit approval before each extraction
- Review extracted rules before continuing
- Iterative: continue until user is satisfied

**When iteration complete:**
- Update project.md with extracted rules
- Continue to Step 6

**If they choose (b) - Skip:**
- Note in project.md that rules can be extracted later
- Continue to Step 6

## Step 6: Create Project Structure

Once you have the name, goal, and optionally sources/targets/rules:

1. Create the project directory structure:
   ```bash
   mkdir -p projects/<project-name>/sources
   mkdir -p projects/<project-name>/drafts
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
