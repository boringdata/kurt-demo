# Create Project Subskill

**Purpose:** Create a new Kurt project with goals, sources, targets, and rules
**Parent Skill:** project-management
**Pattern:** Guided multi-step workflow with progressive disclosure

---

## Overview

This subskill guides users through creating a new Kurt project:

1. **Check for team profile** - Load context from `/start` if available
2. **Load workflow (optional)** - Use workflow template if `--workflow` flag provided
3. Understand project intent (what are you trying to accomplish?)
4. Get project name and goal
5. Check organizational foundation (content map + core rules)
6. Collect project-specific sources (optional)
7. Identify target content (optional)
8. Extract project-specific rules (optional)
9. Create project structure and project.md

**Key principles:**
- Uses profile context when available (simpler flow)
- Progressive disclosure (only required info upfront)
- All steps except name/goal are optional
- User can skip and return later
- Organizational foundation before project-specific work
- Can use workflow templates for recurring patterns

---

## Step 0: Check for Team Profile and Workflow

### Check for Profile

```bash
# Check if profile exists
if [ -f ".kurt/profile.md" ]; then
  PROFILE_EXISTS=true
  # Load context from profile
else
  PROFILE_EXISTS=false
fi
```

**If profile exists:**
```
Loading your team profile...
✓ Company: {{COMPANY_NAME}}
✓ Team: {{TEAM_NAME}}
✓ Foundation rules: {{RULES_STATUS}}
```

Load context:
- `COMPANY_NAME`, `TEAM_NAME`, `INDUSTRY`
- `COMMUNICATION_GOALS`
- `CONTENT_TYPES`
- `KNOWN_PERSONAS`
- `PUBLISHER_STATUS`, `STYLE_STATUS`, `PERSONA_STATUS`

**If profile doesn't exist:**
```
⚠️  No team profile found

It looks like this is your first time using Kurt.

Recommendation: Run /start first to set up your team profile and foundation rules.
This takes 10-15 minutes and makes project creation much easier.

Options:
  a) Run /start now (recommended)
  b) Continue without profile (minimal setup)
  c) Cancel

Choose: _
```

**If (a):** Invoke `onboarding-skill` → Exit create-project, user restarts after onboarding
**If (b):** Continue with minimal setup (no profile context)
**If (c):** Exit

### Check for Workflow Flag

```bash
# Parse arguments for --workflow flag
WORKFLOW_NAME=$(parse_arg "--workflow")
```

**If `--workflow` provided:**

```bash
# Load workflow definition
if [ -f ".kurt/workflows/workflow-registry.yaml" ]; then
  WORKFLOW_DEF=$(yq ".workflows.${WORKFLOW_NAME}" .kurt/workflows/workflow-registry.yaml)

  if [ -n "$WORKFLOW_DEF" ]; then
    WORKFLOW_MODE=true
    echo "Using workflow: $(yq '.name' <<< "$WORKFLOW_DEF")"
  else
    echo "⚠️  Workflow '${WORKFLOW_NAME}' not found"
    echo "Available workflows:"
    yq '.workflows | keys' .kurt/workflows/workflow-registry.yaml
    exit 1
  fi
fi
```

**If workflow loaded:**
```
Using workflow: {{WORKFLOW_NAME}}
Description: {{WORKFLOW_DESCRIPTION}}
Phases: {{PHASE_COUNT}}
Estimated duration: {{AVG_DURATION}}

This project will follow the predefined workflow structure.
```

Store:
- `WORKFLOW_MODE = true`
- `WORKFLOW_DEF` (full workflow definition)
- `WORKFLOW_PHASES` (list of phases)

### Check Analytics Context (if profile exists)

```bash
if [ "$PROFILE_EXISTS" = "true" ]; then
  # Check if analytics is configured in profile
  ANALYTICS_CONFIGURED=$(grep -q "## Analytics Configuration" .kurt/profile.md && grep -q "Status: ✓ Analytics enabled" .kurt/profile.md && echo "true" || echo "false")

  if [ "$ANALYTICS_CONFIGURED" = "true" ]; then
    echo ""
    echo "✓ Analytics configured"

    # Extract analytics domains from profile
    ANALYTICS_DOMAINS=$(grep -A 20 "## Analytics Configuration" .kurt/profile.md | grep "^\*\*" | sed 's/\*\*\(.*\)\*\* (.*/\1/' | tr '\n' ', ' | sed 's/,$//')

    echo "  Domains: $ANALYTICS_DOMAINS"

    # If workflow requires analytics, check data freshness
    if [ "$WORKFLOW_MODE" = "true" ]; then
      WORKFLOW_ANALYTICS_REQUIRED=$(echo "$WORKFLOW_DEF" | yq '.analytics.required // false')

      if [ "$WORKFLOW_ANALYTICS_REQUIRED" = "true" ]; then
        echo ""
        echo "This workflow requires analytics data for prioritization."
        echo "Checking data freshness..."

        # Check if analytics data is stale (>7 days)
        # Parse last synced dates from profile
        # If stale, offer to sync now

        echo ""
        echo "Analytics data may be stale. Sync now? (Y/n):"
        read -p "> " SYNC_CHOICE

        if [ "$SYNC_CHOICE" != "n" ] && [ "$SYNC_CHOICE" != "N" ]; then
          echo ""
          echo "Syncing analytics data..."
          kurt analytics sync --all --if-stale

          if [ $? -eq 0 ]; then
            echo "✓ Analytics data updated"
          else
            echo "⚠️  Some analytics syncs failed"
            echo "Continuing with existing data..."
          fi
        fi
      fi
    fi
  else
    # Analytics not configured
    if [ "$WORKFLOW_MODE" = "true" ]; then
      WORKFLOW_ANALYTICS_REQUIRED=$(echo "$WORKFLOW_DEF" | yq '.analytics.required // false')

      if [ "$WORKFLOW_ANALYTICS_REQUIRED" = "true" ]; then
        echo ""
        echo "⚠️  This workflow requires analytics, but it's not configured."
        echo ""
        echo "Would you like to set up analytics now? (Y/n):"
        read -p "> " SETUP_CHOICE

        if [ "$SETUP_CHOICE" != "n" ] && [ "$SETUP_CHOICE" != "N" ]; then
          echo ""
          echo "Let's set up analytics..."
          echo "Run: /start --update"
          echo "Then return to create your project."
          exit 0
        else
          echo ""
          echo "⚠️  Continuing without analytics."
          echo "Note: Workflow prioritization features won't be available."
          echo ""
        fi
      fi
    fi
  fi
fi
```

---

## Step 1: Understand Project Intent

Ask the user what they want to accomplish:

```
What are you looking to accomplish with this project?

a) Update core product positioning + messaging (on website or internally)
b) Write new marketing assets (e.g., for a product launch)
c) Make sure technical docs + tutorials are up-to-date (and update or remove stale content)
d) Nothing specific, just setting up a general project
e) Something else (please describe)
```

**Wait for the user's response before proceeding.**

Store the user's response as `$PROJECT_INTENT` for use in later steps (recommending appropriate rules, sources, etc.).

---

## Step 2: Get Project Name and Goal

Ask the user for:

1. **Project name** (use kebab-case: e.g., `product-messaging-refresh`, `q4-launch-content`)
2. **Brief description** of what they want to accomplish

```
Great! Let's set up your project.

**Project name** (kebab-case):
Examples: product-messaging-refresh, q4-launch-content, docs-update-2024

**What do you want to accomplish?** (1-2 sentences):
```

**Wait for user response.**

**Project naming guidelines:**
- Use kebab-case: `product-messaging-refresh` not `Product Messaging Refresh`
- Be specific: `q4-launch-content` not `marketing`
- Keep it short: 2-4 words maximum

Store `$PROJECT_NAME` and `$PROJECT_GOAL` for use in project.md.

---

## Step 2.5: Check Organizational Foundation

**Before collecting project-specific sources**, verify that organizational context exists.

### If Profile Exists (PROFILE_EXISTS = true)

**Check foundation status from profile:**

```bash
PUBLISHER_STATUS=$(grep "Publisher Profile:" .kurt/profile.md)
STYLE_STATUS=$(grep "Style Guides:" .kurt/profile.md)
PERSONA_STATUS=$(grep "Personas:" .kurt/profile.md)
CONTENT_STATUS=$(grep "Total Documents:" .kurt/profile.md)
```

**If foundation complete (all rules extracted + content indexed):**
```
✓ Foundation ready
  Publisher: {{PUBLISHER_PATH}}
  Style guides: {{STYLE_COUNT}}
  Personas: {{PERSONA_COUNT}}
  Indexed content: {{TOTAL_DOCS}} documents

Skipping foundation check - continuing to project setup...
```

→ Skip to Step 3

**If foundation incomplete:**
```
⚠️  Foundation partially complete

  ✓ Publisher: {{PUBLISHER_STATUS}}
  ✗ Style guides: {{STYLE_STATUS}}
  ✗ Personas: {{PERSONA_STATUS}}

Would you like to complete foundation setup now? (y/n): _
```

**If yes:** Invoke `check-foundation` subskill
**If no:** Note in project that foundation is incomplete, continue to Step 3

### If No Profile (PROFILE_EXISTS = false)

**Invoke check-foundation subskill:**

```
project-management check-foundation
```

This will:
1. **Check for Content Map** - Organizational content in `/sources/`
   - If missing: Guide user to provide root domains/sitemaps
   - For each domain: Map → Fetch → Index workflow

2. **Check for Core Rules** - Publisher profile + Primary voice + Personas
   - If missing: Extract from indexed content
   - Uses extract-rules subskill with --foundation-only

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

---

## Step 3: Collect Ground Truth Sources (Skippable)

**Now that organizational context is established**, gather project-specific sources.

Ask the user for source material they'll be working FROM:

```
Do you have ground truth sources (material you'll work FROM)?

Examples based on your project type:
- **(a) Positioning**: Product docs, value props, competitive research
- **(b) Marketing assets**: Product specs, feature docs, launch plans
- **(c) Docs updates**: Technical specs, feature documentation

Options:
a) Add sources now
b) Skip for now (add later)
```

**If they choose (a) - Add sources now:**

**Invoke gather-sources subskill:**

```
project-management gather-sources
```

This subskill orchestrates:
1. User describes sources needed
2. Routes to appropriate domain skill:
   - **research-skill** - Conversational refinement for research queries
   - **ingest-content-skill** - Map-then-fetch preview for web content
   - **cms-interaction-skill** - Search-then-fetch preview for CMS content
   - **Local handling** - For pasted content/files
3. Each domain skill provides preview before execution
4. Two-checkpoint validation (approve → execute → review)
5. Iterates until user is satisfied

See: `.claude/skills/project-management-skill/subskills/gather-sources.md`

**When iteration complete:**
- Sources are in `/sources/` (org KB) or `projects/$PROJECT_NAME/sources/` (project-specific)
- Continue to Step 4

**If they choose (b) - Skip:**
- Note in project.md that sources will be added later
- Continue to Step 4

---

## Step 4: Identify Target Content (Skippable)

Ask the user what content they'll be working ON:

```
What content will you be updating or creating (working ON)?

a) Identify targets now
b) Skip for now (add later)
```

**If they choose (a) - Identify targets:**

1. Ask: "What content needs work?"
   - Existing content to update
   - New content to create
   - Both

2. **For existing content:**
   - Search in `/sources/` if already ingested
   - **Check fetch status:**
   ```bash
   # Check if content exists and is fetched
   kurt content list --include "<target-url-pattern>"

   # If NOT_FETCHED, fetch it (downloads + indexes atomically):
   kurt fetch --include "<url-pattern>"
   # OR
   kurt fetch --urls "<url1>,<url2>"
   ```
   - Or note URLs/paths to fetch later

3. **For new content:**
   - Ask for planned file names
   - Note in Targets as planned drafts

4. Store list of target content items for project.md

**If they choose (b) - Skip:**
- Note in project.md that targets will be added later
- Continue to Step 5

---

## Step 4.5: Verify Fetch Status

**Before proceeding to rule extraction**, verify that all sources and targets are fetched.

### Check Sources & Targets

For URLs collected in Steps 3 & 4:

```bash
# Check fetch status
kurt content list --include "<url-pattern>"
kurt content list --with-status NOT_FETCHED  # Show what's not fetched yet
```

### Display Status Summary

```
Content Processing Status:

Sources:
✓ 5 fetched + indexed (ready for rule extraction)
✗ 2 not fetched yet

Targets:
✓ 10 fetched + indexed
✗ 5 not fetched yet

Action needed: Fetch 7 remaining documents
```

### Fetch Remaining Content

```bash
# Fetch by pattern (recommended for batch)
kurt fetch --include "<url-pattern>"

# OR fetch specific URLs
kurt fetch --urls "<url1>,<url2>,<url3>"

# OR fetch by cluster (if already clustered)
kurt fetch --in-cluster "ClusterName"
```

**Important:**
- **Fetch automatically indexes** (atomic operation, no separate step needed)
- **Batch operations are faster** than individual URLs
- **Fetching + indexing is required** for rule extraction (needs content analysis)
- See README.md "Kurt CLI Workflows" for detailed examples

---

## Step 5: Extract Rules (Optional but Recommended)

If the user has added sources in Step 3 AND they are fetched + indexed, ask if they want to extract reusable rules:

```
Would you like to extract writing rules from your content? This helps ensure consistency when creating/updating content.

Options:
a) Extract rules now (recommended if sources available)
b) Skip for now (can extract later)
```

**If they choose (a) - Extract rules now:**

**Invoke extract-rules subskill:**

```
project-management extract-rules
```

This subskill orchestrates:
1. **Prerequisites check**: Verify content is indexed (10+ pages minimum)
2. **Analyze**: Inventory available content by domain, type, date range
3. **Propose with preview**:
   - Routes to **writing-rules-skill** with preview mode
   - Shows 3-5 sample document titles/URLs for each rule type
   - Shows coverage stats (page count, date range, content types)
   - Explains what patterns will be learned
4. **User decision**: Approve / Refine (use different docs) / Skip
5. **Execute**: writing-rules-skill runs extraction with --auto-discover
6. **Review**: Show extracted rule file + key characteristics
7. **Iterate**: Offer to extract more rules or continue

See: `.claude/skills/project-management-skill/subskills/extract-rules.md`

**Key features:**
- writing-rules-skill owns extraction operations
- Preview sample documents before extraction
- Start with foundation rules (publisher + primary voice)
- Propose content-specific rules based on project intent
- Iterative: continue until user is satisfied

**When iteration complete:**
- Store list of extracted rules for project.md
- Continue to Step 6

**If they choose (b) - Skip:**
- Note in project.md that rules can be extracted later
- Continue to Step 6

---

## Step 6: Create Project Structure

Once you have the name, goal, and optionally sources/targets/rules:

### If Workflow Mode (WORKFLOW_MODE = true)

Create workflow-based project structure:

```bash
# Base directories
mkdir -p projects/$PROJECT_NAME/sources
mkdir -p projects/$PROJECT_NAME/drafts

# Phase-based directories (from workflow definition)
for phase in $WORKFLOW_PHASES; do
  phase_id=$(yq ".phases[] | select(.id == \"$phase\") | .id" <<< "$WORKFLOW_DEF")
  mkdir -p projects/$PROJECT_NAME/$phase_id
done

# Example for "weekly-tutorial" workflow:
# projects/jan-15-kafka-tutorial/
# ├── topic-selection/
# ├── outlining/
# ├── drafting/
# ├── review/
# └── publish/
```

**Generate workflow artifacts:**

1. **task-breakdown.md** - From workflow phases and tasks
2. **timeline.md** - From phase durations and dependencies
3. **workflow-tracking.md** - Track phase progress

Store in `projects/$PROJECT_NAME/`

### If No Workflow (Standard Mode)

Create standard project structure:

```bash
mkdir -p projects/$PROJECT_NAME/sources
mkdir -p projects/$PROJECT_NAME/drafts
```

---

### Create project.md

Create `projects/$PROJECT_NAME/project.md` with appropriate template:

**If workflow mode:**
```markdown
# $PROJECT_NAME

## Goal
$PROJECT_GOAL

## Workflow
**Using:** $WORKFLOW_NAME (v$WORKFLOW_VERSION)
**Phases:** $PHASE_COUNT
**Estimated duration:** $AVG_DURATION

See `workflow-tracking.md` for phase progress.

## Intent Category
$PROJECT_INTENT

[... rest of standard template ...]
```

**If standard mode (no workflow), use this template:

```markdown
# $PROJECT_NAME

## Goal
$PROJECT_GOAL

## Intent Category
$PROJECT_INTENT (a/b/c/d/e from Step 1)

## Sources (Ground Truth)

### From Organizational Knowledge Base
[List web content references from /sources/]

### Project-Specific Sources
[List local files in projects/$PROJECT_NAME/sources/]

## Targets (Content to Update/Create)

### Existing Content to Update
[List content in /sources/ that needs updating]

### New Content to Create
[List planned new content to draft]

## Style Guidelines

*Extracted writing patterns applicable to this project's content:*
[List extracted style rules or "To be extracted"]

## Structure Templates

*Document format templates applicable to this project's content:*
[List extracted structure rules or "To be extracted"]

## Target Personas

*Audience profiles for this project's target content:*
[List extracted persona rules or "To be extracted"]

## Publisher Profile

*Organizational context for brand consistency:*
[Reference publisher profile or "To be extracted"]

## Progress
- [x] Project created ($TODAY_DATE)

## Next Steps
[Will be updated as work progresses]
```

**Variable replacements:**
- `$PROJECT_NAME` - from Step 2
- `$PROJECT_GOAL` - from Step 2
- `$PROJECT_INTENT` - from Step 1
- `$TODAY_DATE` - current date (YYYY-MM-DD format)
- Sources/Targets/Rules sections - populated from Steps 3-5

---

## Step 6.5: Review Project Plan (Optional)

After creating the project structure and project.md, offer to review the plan:

```
Would you like to review the project plan? (Y/n):
```

**If yes (or default):**

```bash
# Invoke feedback skill for plan review
feedback-skill review-plan \
  --project-path "projects/$PROJECT_NAME" \
  --project-id "$PROJECT_NAME"
```

This will:
1. Show the project.md contents
2. Ask for ratings on:
   - Goals clarity (1-5)
   - Sources completeness (1-5)
   - Rules coverage (1-5)
   - Overall project setup (1-5)
3. Collect open-ended feedback
4. Record feedback in database for workflow improvements

**If no:**
- Skip plan review
- Continue to next steps

**Notes:**
- Plan review is optional but recommended for complex projects
- Feedback helps improve project setup workflow over time
- User can always review later: `feedback-skill review-plan --project-path projects/$PROJECT_NAME`
- Plan review data feeds into workflow retrospectives

---

## Step 7: Offer Next Steps

After creating the project (and optionally reviewing the plan), summarize what was set up:

```
✅ Project created at `projects/$PROJECT_NAME/`

**Status:**
- Sources: [count] added (or "none yet")
- Targets: [count] identified (or "none yet")
- Rules: [list extracted rules or "none yet"]

**What would you like to do next?**

a) Add more sources or targets now
b) Start working on content
c) Save and resume later
```

**If they choose (a) - Add more sources/targets:**
- **For sources**: Invoke `project-management gather-sources`
- **For targets**: Guide through target identification (Step 4)
- Update project.md accordingly

**If they choose (b) - Start working on content:**
- Ask what they want to work on
- Check if appropriate rules exist for target content
- If rules exist: Recommend `content-writing-skill outline/draft`
- If rules missing: Recommend extracting rules first

**If they choose (c) - Save and resume later:**
- Confirm project saved
- Remind: "Resume with `/resume-project $PROJECT_NAME`"
- Remind: "Add sources anytime with `project-management gather-sources`"

---

## Important Notes

- Always create the `projects/` directory if it doesn't exist
- Use the exact template structure for project.md
- Update project.md as you gather more information
- Keep the user informed about each step
- All steps except Step 1-2 (intent and name) are optional/skippable
- Users can return later to complete skipped steps

---

## Integration with Other Subskills

### Invokes check-foundation (Step 2.5)
```
project-management check-foundation
```
Ensures organizational context before project-specific work.

### Invokes gather-sources (Step 3)
```
project-management gather-sources
```
Orchestrates iterative source collection across domain skills.

### Invokes extract-rules (Step 5)
```
project-management extract-rules
```
Orchestrates iterative rule extraction with preview mode.

---

## Error Handling

### Project directory already exists

```
⚠️  Project directory already exists: projects/$PROJECT_NAME/

Options:
a) Choose a different name
b) Resume existing project (use /resume-project $PROJECT_NAME)
c) Overwrite existing project (⚠️  will delete existing data)

Choose (a/b/c):
```

### Cannot create directory

```
⚠️  Failed to create project directory

Error: [error message]

Please check:
- Permissions in projects/ directory
- Disk space available
- Path is valid

Retry? (Y/n)
```

---

## Key Design Principles

1. **Progressive disclosure** - Only required info (name/goal) upfront
2. **Foundation first** - Org context before project-specific work
3. **Orchestration** - Delegates to specialized subskills (check-foundation, gather-sources, extract-rules)
4. **Optional steps** - Sources, targets, rules all skippable
5. **Batch operations** - Always use batched commands for multiple items
6. **User control** - Checkpoints before major operations
7. **Resumable** - User can save and return anytime

---

*This subskill orchestrates project creation by delegating to specialized subskills. It does not duplicate operational details from domain skills.*
