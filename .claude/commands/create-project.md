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
   - Run `kurt ingest map <url>` to discover content
   - Run `kurt ingest fetch --url-prefix <url>` to fetch
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
   - Or note URLs/paths to fetch later

3. **For new content:**
   - Ask for planned file names
   - Note in Targets as planned drafts

4. Update project.md Targets section

**If they choose (b) - Skip:**
- Note in project.md that targets will be added later
- Continue to Step 5

## Step 5: Create Project Structure

Once you have the name, goal, and optionally sources/targets:

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
(Reserved for future use)

## Structure Templates
(Reserved for future use)

## Progress
- [x] Project created (<today's date>)

## Next Steps
<Will be updated as work progresses>
```

## Step 6: Offer Next Steps

After creating the project, summarize what was set up:

> Project created at `projects/<project-name>/`
>
> Status:
> - Sources: <count> added (or "none yet")
> - Targets: <count> identified (or "none yet")

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
