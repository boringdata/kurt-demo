# Testing Guide: End-to-End Onboarding + Workflow System

**Date:** February 2, 2025
**Status:** Ready for Testing

---

## What's Been Implemented

### ✅ Complete Components

1. **Onboarding System (`/start`)**
   - Main router: `.claude/skills/onboarding-skill/SKILL.md`
   - Subskills:
     - `questionnaire.md` - Interactive data collection
     - `map-content.md` - Maps and fetches sources via kurt CLI
     - `extract-foundation.md` - Extracts rules via writing-rules-skill
     - `create-profile.md` - Generates `.kurt/profile.md`
   - Command: `.claude/commands/start.md`

2. **Workflow System (`workflow-skill`)**
   - Main skill: `.claude/skills/workflow-skill/SKILL.md`
   - Subskills:
     - `add.md` - Interactive workflow creation wizard
     - `list.md` - Display all workflows
     - `show.md` - Display workflow details
   - Registry: `.kurt/workflows/workflow-registry.yaml`
   - Template: `.kurt/workflows/templates/_workflow-template.yaml`

3. **Updated Project Creation**
   - Updated: `.claude/skills/project-management-skill/subskills/create-project.md`
   - Now checks for profile first
   - Supports `--workflow <name>` flag
   - Uses profile context when available

4. **Infrastructure**
   - Profile template: `.kurt/templates/profile-template.md`
   - Workflow registry structure
   - Updated README with Quick Start

---

## Prerequisites

Before testing, ensure you have:

```bash
# 1. Kurt CLI installed
kurt --version

# 2. Kurt initialized in this project
kurt init
kurt migrate apply  # If migrations pending

# 3. yq installed (for YAML parsing)
yq --version

# 4. jq installed (for JSON parsing)
jq --version
```

---

## Test Plan: End-to-End Flow

### Test 1: First-Time Onboarding

**Goal:** Verify `/start` creates profile and extracts foundation rules

**Steps:**

1. **Run onboarding:**
   ```bash
   /start
   ```

2. **Expected flow:**
   ```
   Welcome to Kurt!
   [Questionnaire begins]
   ```

3. **Answer questionnaire:**
   - Company: "Acme Corp"
   - Team: "Developer Relations"
   - Industry: "Developer Tools"
   - Goals: Select 2, 5 (thought leadership, developer education)
   - Content types: Select 1, 2 (blog posts, technical tutorials)
   - Personas: y → "Backend Developer, Platform Engineer"
   - Company website: "https://docs.getdbt.com" (using dbt docs as example)
   - CMS: none
   - Workflow: "Weekly tutorial publication"

4. **Confirm content mapping:**
   ```
   Continue? (y/n): y
   ```

5. **Wait for:**
   - Content mapping (discovers URLs)
   - Content fetching (downloads + indexes)
   - **Analytics setup prompt** (NEW)
     - You'll be asked: "Would you like to set up analytics? (Y/n)"
     - **If yes:** Provide PostHog credentials (Project ID, API Key)
     - **If no:** Skip analytics (can add later via `/start --update`)
   - Rule extraction (publisher, style, personas)
   - Profile creation

6. **Verify outputs:**
   ```bash
   # Profile created
   ls -la .kurt/profile.md

   # View profile
   cat .kurt/profile.md

   # Check analytics section in profile
   grep -A 15 "## Analytics Configuration" .kurt/profile.md

   # Rules extracted
   ls rules/publisher/
   ls rules/style/
   ls rules/personas/

   # Content indexed
   kurt content list

   # If analytics was set up, verify
   kurt analytics list
   ```

**Success criteria:**
- ✅ `.kurt/profile.md` exists and contains correct info
- ✅ Profile contains "Analytics Configuration" section
  - If configured: Shows domains with traffic thresholds
  - If skipped: Shows "Not configured" with setup instructions
- ✅ Foundation rules extracted (publisher, style, 2 personas)
- ✅ Content fetched and indexed
- ✅ Next steps shown

---

### Test 2: Create Workflow

**Goal:** Verify `workflow-skill add` creates reusable workflow

**Steps:**

1. **Run workflow creation:**
   ```bash
   workflow-skill add
   ```

2. **Answer wizard:**
   - Workflow description: "Weekly tutorial publication"
   - Phases detected: y (accept: topic-selection, outlining, drafting, review, publish)

3. **For each phase, provide:**

   **Phase 1: topic-selection**
   - Duration: "1 day"
   - Tasks: "Review topic requests, Select topic, Research existing content"
   - Outputs: "research/topic-brief.md"
   - Dependencies: none
   - Rules: none
   - Review: no

   **Phase 2: outlining**
   - Duration: "0.5 days"
   - Tasks: "content-writing-skill outline <project> <asset>"
   - Outputs: "drafts/<asset>-outline.md"
   - Dependencies: y → "topic-selection"
   - Rules: y → "structure/tutorial, personas/backend-developer"
   - Review: no

   **Phase 3: drafting**
   - Duration: "2-3 days"
   - Tasks: "content-writing-skill draft <project> <asset>, Test code examples"
   - Outputs: "drafts/<asset>-draft.md"
   - Dependencies: y → "outlining"
   - Rules: y → "style/technical, structure/tutorial"
   - Review: no

   **Phase 4: review**
   - Duration: "1-2 days"
   - Tasks: "Technical accuracy review, Code verification"
   - Outputs: "reviews/feedback.md"
   - Dependencies: y → "drafting"
   - Rules: none
   - Review: y → Reviewers: "engineering-team", Blocking: y

   **Phase 5: publish**
   - Duration: "0.5 days"
   - Tasks: "Publish to blog, Share on social"
   - Outputs: none
   - Dependencies: y → "review"
   - Rules: none
   - Review: no

4. **Workflow metadata:**
   - Name (slug): "weekly-tutorial"
   - Display name: "Weekly Technical Tutorial"
   - Frequency: "weekly"

5. **Success criteria:**
   - Enter: "Draft created, Technical review passed, Published"

6. **Analytics requirements (NEW):**
   - Does workflow require analytics? **y**
   - Prioritization strategy: **a** (Traffic-based)
   - Minimum traffic level: **d** (MEDIUM+)
   - Urgent threshold: **a** (CRITICAL - high traffic + declining)

7. **Review and confirm:**
   ```
   Save this workflow? (y/n): y
   ```

8. **Verify outputs:**
   ```bash
   # Workflow in registry
   cat .kurt/workflows/workflow-registry.yaml

   # List workflows
   workflow-skill list

   # Show workflow details
   workflow-skill show weekly-tutorial
   ```

**Success criteria:**
- ✅ Workflow saved to registry
- ✅ `workflow-skill list` shows workflow
- ✅ `workflow-skill show weekly-tutorial` displays full details
- ✅ Workflow includes analytics requirements:
  - `analytics.required: true`
  - `analytics.prioritization.strategy: "traffic-based"`
  - `analytics.prioritization.min_traffic_level: "MEDIUM"`
  - `analytics.prioritization.urgent_threshold: "CRITICAL"`
- ✅ Validation passes (no circular dependencies, rules checked)

---

### Test 3: Create Project with Workflow

**Goal:** Verify `/create-project --workflow` uses profile and workflow

**Steps:**

1. **Create project with workflow:**
   ```bash
   /create-project --workflow weekly-tutorial
   ```

2. **Expected:**
   ```
   Loading your team profile...
   ✓ Company: Acme Corp
   ✓ Team: Developer Relations
   ✓ Foundation rules: publisher, style, 2 personas

   Using workflow: Weekly Technical Tutorial
   Description: Weekly tutorial publication workflow
   Phases: 5
   Estimated duration: 3-5 days

   ✓ Analytics configured
     Domains: docs.company.com

   This workflow requires analytics data for prioritization.
   Checking data freshness...

   Analytics data may be stale. Sync now? (Y/n):
   ```

   **If analytics was configured in Test 1:**
   - You'll see analytics status from profile
   - If workflow requires analytics, you'll be prompted to sync if stale
   - If you choose "y", analytics will sync before project creation continues

   **If analytics was NOT configured:**
   - You'll see a warning that workflow requires analytics
   - Option to set up now (redirects to `/start --update`) or continue without

3. **Project setup (simplified since profile exists):**
   - Intent: Select or describe
   - Project name: "kafka-basics-tutorial"
   - Goal: "Tutorial on Kafka basics for backend engineers"
   - Sources: Skip (or add project-specific)
   - Targets: Skip (will create new content)
   - Rules: Skip extraction (using foundation rules from profile)

4. **Verify project structure:**
   ```bash
   ls -la projects/kafka-basics-tutorial/

   # Should have workflow-based folders
   projects/kafka-basics-tutorial/
   ├── project.md
   ├── workflow-tracking.md
   ├── task-breakdown.md
   ├── timeline.md
   ├── topic-selection/
   ├── outlining/
   ├── drafting/
   ├── review/
   └── publish/
   ```

5. **Check project.md:**
   ```bash
   cat projects/kafka-basics-tutorial/project.md
   ```

   Should include:
   - Workflow section (using weekly-tutorial v1.0)
   - Company context from profile
   - Foundation rules referenced

**Success criteria:**
- ✅ Profile loaded automatically (no repeated questions)
- ✅ Analytics status displayed from profile
- ✅ If workflow requires analytics:
  - Analytics freshness checked
  - Sync prompted if stale
  - Warning shown if not configured
- ✅ Workflow-based folder structure created
- ✅ `workflow-tracking.md` created with phase progress
- ✅ `task-breakdown.md` generated from workflow phases
- ✅ Foundation rules referenced in project.md

---

### Test 4: Create Project WITHOUT Workflow

**Goal:** Verify standard project creation still works

**Steps:**

1. **Create standard project:**
   ```bash
   /create-project
   ```

2. **Expected:**
   ```
   Loading your team profile...
   [Profile context loaded]

   [Standard project creation flow]
   ```

3. **Setup:**
   - Intent: Select
   - Project name: "product-announcement-blog"
   - Goal: "Blog post announcing new product feature"
   - Sources/Targets: Add as normal

4. **Verify structure:**
   ```bash
   ls -la projects/product-announcement-blog/

   # Should have standard structure (no workflow)
   projects/product-announcement-blog/
   ├── project.md
   ├── sources/
   └── drafts/
   ```

**Success criteria:**
- ✅ Profile still used (context loaded)
- ✅ Standard structure (no workflow phases)
- ✅ No workflow-tracking.md
- ✅ Standard project.md format

---

### Test 5: Profile Updates

**Goal:** Verify profile can be updated

**Steps:**

1. **View current profile:**
   ```bash
   cat .kurt/profile.md
   ```

2. **Run onboarding again:**
   ```bash
   /start
   ```

3. **Expected:**
   ```
   ⚠️  Kurt profile already exists

   Would you like to:
     a) View existing profile
     b) Update profile
     c) Start over (overwrites existing)

   Choose:
   ```

4. **Test each option:**
   - `a` → Shows profile content
   - `b` → Updates profile with new answers
   - `c` → Completely recreates profile

**Success criteria:**
- ✅ Existing profile detected
- ✅ Options presented
- ✅ Update mode preserves some data
- ✅ Start over mode recreates from scratch

---

## Test Scenarios: Edge Cases

### Edge Case 1: No Content Sources

**Test:** Run `/start` and skip all content sources

**Expected:**
- Profile created without content stats
- Foundation rules skipped
- Next steps suggest adding content

### Edge Case 2: Insufficient Content

**Test:** Provide only 1-2 pages

**Expected:**
- Warning about minimum content requirement
- Option to continue anyway or add more
- Rules extraction may be less reliable

### Edge Case 3: Workflow with Missing Rules

**Test:** Create workflow requiring non-existent rules

**Expected:**
- Validation shows missing rules
- Warning displayed
- Option to create rules or continue anyway

### Edge Case 4: Profile Without Onboarding

**Test:** Try `/create-project` without running `/start`

**Expected:**
- Detects no profile
- Suggests running `/start` first
- Option to continue with minimal setup or cancel

---

## Troubleshooting

### Issue: `/start` command not found

**Solution:**
```bash
# Check command file exists
ls .claude/commands/start.md

# Verify command syntax
cat .claude/commands/start.md
```

### Issue: Onboarding fails at content mapping

**Possible causes:**
- Kurt CLI not installed: `kurt --version`
- Kurt not initialized: `kurt init`
- Network issues accessing URLs
- Invalid URL provided

**Debug:**
```bash
# Test kurt CLI directly
kurt map url https://docs.getdbt.com --cluster-urls

# Check kurt status
kurt content list
```

### Issue: Workflow validation fails

**Possible causes:**
- Circular dependencies in phases
- Required rules don't exist
- YAML syntax error

**Debug:**
```bash
# Validate YAML syntax
yq eval .kurt/workflows/workflow-registry.yaml

# Check for circular dependencies
# (review phase dependencies in workflow definition)
```

### Issue: Profile not loading in create-project

**Possible causes:**
- Profile file missing: `ls .kurt/profile.md`
- Malformed profile

**Debug:**
```bash
# Check if profile exists
test -f .kurt/profile.md && echo "Profile exists" || echo "Profile missing"

# View profile
cat .kurt/profile.md
```

---

## Success Metrics

After completing all tests, you should have:

1. **Profile System**
   - ✅ `.kurt/profile.md` with team context
   - ✅ Foundation rules extracted
   - ✅ Content indexed

2. **Workflow System**
   - ✅ At least one workflow defined
   - ✅ Workflow registry populated
   - ✅ Workflows can be listed and shown

3. **Project Creation**
   - ✅ Projects created with workflows
   - ✅ Projects created without workflows
   - ✅ Both use profile context

4. **Integration**
   - ✅ End-to-end flow works
   - ✅ No manual file editing needed
   - ✅ All commands functional

---

## Next Steps After Successful Testing

1. **Create Example Workflows**
   - Add 2-3 example workflows to repository
   - Document common workflow patterns

2. **Enhance Workflow Operations**
   - Implement `workflow-skill validate`
   - Implement `workflow-skill stats`
   - Implement `workflow-skill optimize`

3. **Content Writing Integration**
   - Update content-writing-skill to use workflow context
   - Track workflow phase progress

4. **User Documentation**
   - Create tutorial for first-time users
   - Add troubleshooting guide
   - Create video walkthrough

---

## Feedback

After testing, please note:
- What worked well
- What was confusing
- What broke
- What's missing
- Suggested improvements

This will help prioritize next development iterations.

---

**Ready to test!** Start with Test 1 (First-Time Onboarding) and work through sequentially.
