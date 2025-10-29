---
description: Resume work on an existing Kurt project
---

# Resume Kurt Project

Help the user resume work on an existing Kurt project by following these steps:

## Step 1: Check for Arguments

The user may have invoked this command with a project name: `/resume-project <project-name>`

**Check if a project name was provided:**
- If YES: Skip to Step 3 with that project name
- If NO: Continue to Step 2

## Step 2: List Available Projects (if no argument provided)

If no project name was provided, list all available projects:

1. Check if `projects/` directory exists
2. List all subdirectories in `projects/`
3. For each project, read `projects/<name>/project.md` and extract:
   - Project title (first H1)
   - Goal (## Goal section)
   - Intent category (## Intent Category section)

Display the projects in a numbered list and ask:

> Which project would you like to resume?
>
> 1. `project-name-1` - Goal: [brief goal description]
> 2. `project-name-2` - Goal: [brief goal description]
> ...
>
> Enter the project number or name:

**Wait for the user's response before proceeding.**

## Step 3: Load Project Context

Once you have the project name:

1. **Read the project.md file** to understand:
   - Project goal and intent
   - Content sources (if any have been mapped)
   - Topic clusters (if computed)
   - Previous next steps

2. **Check project status:**
   - Are there content sources listed? Have they been fetched?
   - Have clusters been computed?
   - What was the last recorded next step?

3. **Display project summary:**

```
# Resuming: <Project Name>

## Current Status
- **Goal:** <goal from project.md>
- **Intent:** <intent category>
- **Content Sources:** <count> sources mapped (<count> fetched / <count> not fetched)
- **Clusters:** <Yes/No, count if available>
- **Last Updated:** <file modification time if available>
```

## Step 4: Check Organizational Foundation & Project Content

**Before diving into project-specific work**, verify organizational foundation exists.

### 4.1: Check Organizational Foundation

**Execute the shared foundation check:**

Follow the workflow in `.claude/commands/_shared/check-organizational-foundation.md`

**This checks:**
1. **Content Map** - Organizational content in `/sources/`
2. **Core Rules** - Publisher profile + Primary voice + Personas

**If foundation exists:**
- Show quick summary
- Continue to Step 4.2

**If foundation missing:**
- Offer to set up before project work
- "Your organizational foundation isn't complete. Would you like to set it up now? This helps ensure consistency across all projects."
- If user declines: "You can set this up later. For now, I'll focus on project-specific content."

**Why this matters:**
- Core rules ensure consistency across all content
- Content map shows what exists organizationally
- Prevents duplicating effort across projects
- Foundation rules benefit all future projects

### 4.2: Check Project-Specific Content

Parse the project.md file and check for gaps:

1. **Check Sources section:**
   - Count items under "From Organizational Knowledge Base"
   - Count items under "Project-Specific Sources"
   - If both are empty or say "add references here", flag as missing

2. **Check Targets section:**
   - Count items under "Existing Content to Update"
   - Count items under "New Content to Create"
   - If both are empty or say "add references here", flag as missing

3. **Check Rules sections (NEW):**
   - Check "Style Guidelines" section - any extracted styles listed?
   - Check "Structure Templates" section - any templates listed?
   - Check "Target Personas" section - any personas listed?
   - Check "Publisher Profile" section - is there a profile reference?
   - Flag if sections say "To be extracted" or are empty

4. **Display warnings:**

**If no sources found:**
```
⚠️ No ground truth sources found.

Do you have source material to add?

Available source types:

**1. Web Content** - URLs or entire websites
   Example: "docs.example.com/features"

**2. CMS Content** - Sanity (if configured)
   Example: "existing tutorials about authentication"

**3. Local Content** - Files, transcripts, notes
   Example: "conversation transcript from research"

**4. Research** - Competitive analysis (if available)
   Example: "research Auth0 and Okta patterns"

Describe the sources you need, or skip for now:
```

**If no targets found:**
```
⚠️ No target content identified.

What do you want to create or update?
- Existing docs to update
- New content to create

Would you like to identify targets now?
```

**If no rules extracted (NEW):**
```
⚠️ No writing rules extracted yet.

Rules help ensure consistency when creating/updating content:
- Primary voice and content styles
- Document structure templates
- Audience personas
- Company messaging/positioning

Would you like to extract rules now?
```

**If user wants to add content:**

Use **project-management gather-sources** subskill:

`project-management gather-sources`

This orchestrates iterative source gathering:
- Routes to appropriate domain skills (research, ingest, cms)
- Two-checkpoint validation (proposal → execute → review)
- Conversational exploration for research queries
- Batch operations (no looping)

**If user wants to extract rules (NEW):**

Use **project-management extract-rules** subskill:

`project-management extract-rules`

This orchestrates iterative rule extraction:
- Routes to writing-rules-skill with preview mode
- Shows sample documents before extraction
- Iterates until user satisfied

## Step 5.7: Extract Rules (If Missing and Content Ready)

**If user wants to extract rules**, use **project-management extract-rules** subskill:

`project-management extract-rules`

**Prerequisites:**
- ✅ Content must be FETCHED + INDEXED (verify with Step 5)
- ✅ At least 10 indexed pages for foundation rules

**The subskill will:**
1. Analyze available content
2. Propose rules with sample document preview (via writing-rules-skill)
3. Prioritize based on:
   - Foundation rules (if missing globally)
   - Content-specific rules (based on project intent/targets)
4. Get approval before each extraction
5. Execute via writing-rules-skill --auto-discover
6. Review extracted rules
7. Iterate until satisfied

**Integrate with project:**
- Update project.md with extracted rules
- Validate rule coverage for target content

## Step 5: Analyze Content Status & Fetch/Index Gaps

Check the actual Kurt database status for this project and verify fetch + index completion:

### 5.1: Parse Sources and Targets from project.md

Extract all URLs/paths from:
- "From Organizational Knowledge Base" section
- "Existing Content to Update" section

### 5.2: Check Fetch Status for All Content

For each URL in sources + targets:

```bash
# Check fetch status
kurt content list --url <url>

# Look for:
# - status: FETCHED (good)
# - status: NOT_FETCHED (needs fetch)
# - status: ERROR (needs investigation)
```

**Display fetch status summary:**
```
Fetch Status:

Sources (8 total):
✓ 6 FETCHED
✗ 2 NOT_FETCHED
  - https://docs.company.com/page1
  - https://docs.company.com/page2

Targets (23 total):
✓ 15 FETCHED
✗ 8 NOT_FETCHED
  - https://docs.company.com/target1
  - https://docs.company.com/target2
  ...
```

### 5.3: Fetch Missing Content

If any NOT_FETCHED content found:

```bash
# Batch fetch by URL prefix if possible
kurt content fetch --url-prefix https://docs.company.com/

# Or fetch individual URLs
kurt content fetch https://docs.company.com/page1
kurt content fetch https://docs.company.com/page2
```

**Show progress:**
```
Fetching missing content...
✓ Fetched 2 sources
✓ Fetched 8 targets
All content now fetched.
```

### 5.4: Check Index Status for All Content

**Critical:** Check if fetched content has been indexed (metadata extracted):

```bash
# Check if content has metadata
kurt content get-metadata <url>

# Look for extracted fields:
# - title, author, published_date (frontmatter or extracted)
# - topics, entities (LLM-extracted)
# - indexed_at timestamp

# If these are missing or null, content needs indexing
```

**Display index status summary:**
```
Index Status:

Sources (8 total):
✓ 3 INDEXED (metadata extracted)
✗ 5 FETCHED but NOT INDEXED
  - Missing topics/entities
  - Need to run: kurt content index --url-prefix <prefix>

Targets (23 total):
✓ 5 INDEXED
✗ 18 FETCHED but NOT INDEXED
```

### 5.5: Index All Fetched Content

If any fetched but not indexed content found:

```bash
# Batch index by URL prefix (recommended)
kurt content index --url-prefix https://docs.company.com/

# Or index specific URLs
kurt content index --url <url1> --url <url2>
```

**Show progress:**
```
Indexing content (extracting metadata + topics)...
This may take 10-30 seconds depending on volume...

✓ Indexed 5 sources
✓ Indexed 18 targets
All content now indexed and ready for analysis.
```

### 5.6: Check Clusters (if relevant)

```bash
kurt content cluster
```

### Final Content Status Summary

After fetch + index complete:

```
✅ Content Processing Complete

Sources: 8 total
  ✓ All fetched
  ✓ All indexed
  ✓ Ready for rule extraction

Targets: 23 total
  ✓ All fetched
  ✓ All indexed
  ✓ Ready for content work

Next: Check rule coverage...
```

## Step 6: Recommend Next Steps

Based on the project intent and current status, recommend specific next actions:

**Priority order for recommendations:**
1. Fix critical gaps (no sources, no targets)
2. Extract missing rules (if targets exist but rules don't)
3. Validate rule coverage for specific target work
4. Proceed with content work

**If intent is (a) - Update positioning/messaging:**
- Check: Publisher profile + primary voice extracted?
- Check: Landing page structure + marketing persona extracted?
- Suggest fetching product/marketing pages if not done
- Recommend extracting claims and entities
- Offer to analyze gaps in current messaging

**If intent is (b) - Write marketing assets:**
- Check: Publisher profile + primary voice extracted?
- Check: Relevant structure template for asset type?
- Suggest reviewing similar past content in clusters
- Recommend extracting positioning elements
- Offer to build a content brief

**If intent is (c) - Update technical docs:**
- Check: Technical doc style + tutorial structure + developer persona?
- Suggest identifying stale content (old published_date)
- Recommend mapping doc structure via clusters
- Offer to find gaps in coverage

**If intent is (d) - General setup:**
- Ask what specific task they want to work on
- Check rule coverage for that task type
- Offer to explore content or run analysis

**Common next steps by status (priority order):**

1. **No content mapped:**
   - Run `kurt content add <url>` to discover and fetch content

2. **Content mapped but not fetched:**
   - Run `kurt content fetch --url-prefix <url>` to download
   - **Required before** indexing or extraction

3. **Content fetched but not indexed:**
   - Run `kurt content index --url-prefix <url>` to extract metadata
   - **Required before** rule extraction or content work
   - Check: `kurt content get-metadata <url>` should show topics/metadata

4. **Content fetched + indexed, but no clusters:**
   - Run `kurt content cluster` to analyze topics (optional)

5. **Content ready, but no rules extracted:**
   - Extract foundation rules (publisher + primary voice)
   - Extract content-specific rules based on intent

6. **Rules incomplete for targets:**
   - Extract content-specific rules for target types
   - Validate coverage for each target

7. **Ready for work with rules:**
   - Validate rule coverage for specific target
   - Start content work

## Step 7: Validate Rules Before Content Work

**Before starting any content creation/update work**, validate rule coverage:

1. **User indicates they want to work on specific target:**
   - "Let's update the quickstart tutorial"
   - "I want to create a new blog post"
   - "Time to work on the landing page"

2. **Inspect target content:**
   - Determine content type, purpose, audience
   - Use project-management-skill rule matching logic

3. **Check rule coverage:**
   ```
   Target: quickstart tutorial

   Required rules:
   ✓ Style: Technical documentation style found
   ✗ Structure: Tutorial structure NOT FOUND
   ✓ Persona: Developer persona found
   ✓ Publisher: Company profile found

   Missing: Tutorial structure template
   ```

4. **If rules missing:**
   - **Recommend extraction:** "Extract from existing tutorials?"
   - **Offer alternatives:** "Use general documentation structure?"
   - **Let user decide:** "Proceed without structure template?"

5. **If all rules present:**
   - Proceed with content work
   - Reference appropriate rules during creation/update

## Step 8: Update Project Notes

After the user begins working, offer to update the project.md with:
- Today's date in Progress section
- Tasks completed in this session
- Rules extracted (if any)
- New action items for Next Steps

## Important Notes

- Always read the project.md file first to understand context
- Check both the project.md records AND the actual Kurt database status
- **NEW: Check rule coverage before starting content work**
- Validate that appropriate rules exist for target content types
- Extract missing rules proactively when gaps identified
- Provide specific, actionable next steps based on intent category
- Offer to update project documentation as work progresses
- If the project directory doesn't exist, inform the user and suggest `/create-project`
