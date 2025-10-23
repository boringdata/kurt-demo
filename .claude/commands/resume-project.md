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

## Step 4: Check for Missing Content (Gap Detection)

Parse the project.md file and check for gaps:

1. **Check Sources section:**
   - Count items under "From Organizational Knowledge Base"
   - Count items under "Project-Specific Sources"
   - If both are empty or say "add references here", flag as missing

2. **Check Targets section:**
   - Count items under "Existing Content to Update"
   - Count items under "New Content to Create"
   - If both are empty or say "add references here", flag as missing

3. **Display warnings:**

**If no sources found:**
```
⚠️ No ground truth sources found.

Do you have source material to add?
- Product specs or documentation (for your project type)
- Reference materials
- Internal docs or notes

Would you like to add sources now?
```

**If no targets found:**
```
⚠️ No target content identified.

What do you want to create or update?
- Existing docs to update
- New content to create

Would you like to identify targets now?
```

**If user wants to add content:**
- Use project-management-skill to guide them through adding sources/targets

## Step 5: Analyze Content Status

Check the actual Kurt database status for this project:

1. **Check documents:**
   ```bash
   # If project has specific URL patterns, filter by those
   kurt document list --limit 5
   ```

2. **Check clusters:**
   ```bash
   kurt cluster list
   ```

## Step 6: Recommend Next Steps

Based on the project intent and current status, recommend specific next actions:

**If intent is (a) - Update positioning/messaging:**
- Suggest fetching product/marketing pages if not done
- Recommend extracting claims and entities
- Offer to analyze gaps in current messaging

**If intent is (b) - Write marketing assets:**
- Suggest reviewing similar past content in clusters
- Recommend extracting positioning elements
- Offer to build a content brief

**If intent is (c) - Update technical docs:**
- Suggest identifying stale content (old published_date)
- Recommend mapping doc structure via clusters
- Offer to find gaps in coverage

**If intent is (d) - General setup:**
- Ask what specific task they want to work on
- Offer to explore content or run analysis

**Common next steps by status:**
- **No content mapped:** Run `kurt ingest map <url>` to discover content
- **Content mapped but not fetched:** Run `kurt ingest fetch --url-prefix <url>` to ingest
- **Content fetched but no clusters:** Run `kurt cluster compute` to analyze topics
- **Ready for work:** Ask user what they want to accomplish today

## Step 7: Update Project Notes

After the user begins working, offer to update the project.md "Next Steps" section with:
- Today's date
- Tasks completed in this session
- New action items

## Important Notes

- Always read the project.md file first to understand context
- Check both the project.md records AND the actual Kurt database status
- Provide specific, actionable next steps based on intent category
- Offer to update project documentation as work progresses
- If the project directory doesn't exist, inform the user and suggest `/create-project`
