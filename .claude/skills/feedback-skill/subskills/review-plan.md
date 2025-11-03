# Review Plan Subskill

**Purpose:** Collect user feedback on project planning (project.md, task-breakdown.md, timeline.md)
**Parent Skill:** feedback-skill
**Feedback Loop:** Loop 2 - Project Plan Quality → Workflow Definition
**Operation:** Interactive plan review and issue identification

---

## Context Received from Parent Skill

- `$PROJECT_PATH` - Path to project directory
- `$PROJECT_ID` - Project identifier (directory name)
- `$WORKFLOW_ID` - Workflow ID if project used workflow (optional)
- `$PLAN_FILES` - List of plan files created (project.md, task-breakdown.md, timeline.md)

---

## Workflow

### Step 1: Present Plan Context

```
═══════════════════════════════════════════════════════
Project Plan Review
═══════════════════════════════════════════════════════

Project: {{PROJECT_ID}}
{{#if WORKFLOW_ID}}Workflow: {{WORKFLOW_ID}}{{/if}}

Plan files created:
{{#each PLAN_FILES}}
  • {{FILE}}
{{/each}}

I've created the project plan. Let's review it to make sure everything
is in place before you start working.
```

### Step 2: Display Plan Summary

```bash
# Extract key information from project.md
PROJECT_GOAL=$(grep -A 5 "## Goal" "${PROJECT_PATH}/project.md" | tail -n +2 | head -n 3)
SOURCE_COUNT=$(grep -c "^\- \[" "${PROJECT_PATH}/project.md" || echo "0")
TARGET_COUNT=$(grep -c "^\- \[ \]" "${PROJECT_PATH}/project.md" || echo "0")

# Display summary
cat <<EOF

───────────────────────────────────────────────────────
Plan Summary
───────────────────────────────────────────────────────

Goal:
${PROJECT_GOAL}

Sources: ${SOURCE_COUNT} item(s)
Targets: ${TARGET_COUNT} item(s)

{{#if WORKFLOW_ID}}
Workflow phases: {{PHASE_COUNT}}
Estimated duration: {{DURATION}}
{{/if}}

───────────────────────────────────────────────────────
EOF
```

### Step 3: Collect Overall Rating

```
How complete does this plan look?

Rating (1-5):
  1 - Missing major elements
  2 - Significant gaps
  3 - Acceptable but needs work
  4 - Good (minor gaps)
  5 - Excellent (ready to start)

Your rating: _
```

**Capture:** `RATING` (1-5)

### Step 4: Handle Rating-Based Flow

**If rating >= 4 (Good/Excellent):**
```
Great! The plan looks solid.

[Optional] Any suggestions to improve the plan? (Enter to skip): _
```

**Capture:** `COMMENT` (optional)

**Store feedback and exit** (no issue identification needed)

---

**If rating <= 3 (Needs work):**

Continue to Step 5 (Issue Identification)

---

### Step 5: Issue Identification

```
What seems to be missing or unclear?

  a) Missing or incomplete tasks
  b) Timeline seems off (too short/long)
  c) Missing dependencies or ordering issues
  d) Unclear goals or success criteria
  e) Other (please describe)

Choose (a/b/c/d/e): _
```

**Capture:** `ISSUE_CHOICE`

**Map to issue categories:**
- `a` → `missing_tasks`
- `b` → `wrong_timeline`
- `c` → `missing_dependencies`
- `d` → `unclear_goals`
- `e` → `other` (prompt for description)

**If user chose "e" (Other):**
```
Please describe what's missing:
> _
```

**Capture:** `ISSUE_DESCRIPTION`

---

### Step 6: Store Feedback in Database

```bash
# Generate UUID for feedback event
FEEDBACK_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Sanitize comment for SQL
COMMENT_SANITIZED=$(echo "$COMMENT" | sed "s/'/''/g")

# Store in database
sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO feedback_events (
    id,
    created_at,
    feedback_type,
    project_id,
    workflow_id,
    skill_name,
    operation,
    asset_path,
    rating,
    comment,
    issue_identified,
    issue_category,
    execution_count,
    prompted
) VALUES (
    '${FEEDBACK_ID}',
    '${TIMESTAMP}',
    'project_plan',
    '${PROJECT_ID}',
    $([ -n "${WORKFLOW_ID}" ] && echo "'${WORKFLOW_ID}'" || echo "NULL"),
    'project-management-skill',
    'create-project',
    '${PROJECT_PATH}/project.md',
    ${RATING},
    '${COMMENT_SANITIZED}',
    $([ "${RATING}" -le 3 ] && echo "1" || echo "0"),
    '${ISSUE_CATEGORY}',
    1,
    0
);
EOF
```

---

### Step 7: Check for Improvement Opportunity

**If issue was identified (rating <= 3) AND project used workflow:**

```
Let me check if I can improve the workflow to address this...
```

**Determine if workflow can be improved:**

```bash
if [ -n "${WORKFLOW_ID}" ] && [ "${RATING}" -le 3 ]; then
    # Workflow-based project with issues
    # Invoke improve subskill
    feedback-skill improve \
        --feedback-id "${FEEDBACK_ID}" \
        --issue-category "${ISSUE_CATEGORY}" \
        --workflow-id "${WORKFLOW_ID}" \
        --project-path "${PROJECT_PATH}"
else
    # No workflow, or rating was acceptable
    echo ""
    echo "Noted. You can update the plan manually by editing:"
    echo "  • ${PROJECT_PATH}/project.md"
    [ -f "${PROJECT_PATH}/task-breakdown.md" ] && echo "  • ${PROJECT_PATH}/task-breakdown.md"
    [ -f "${PROJECT_PATH}/timeline.md" ] && echo "  • ${PROJECT_PATH}/timeline.md"
fi
```

---

### Step 8: Thank User and Exit

```
───────────────────────────────────────────────────────
✓ Plan review recorded
───────────────────────────────────────────────────────

Thank you for reviewing the plan!

{{#if IMPROVEMENT_SUGGESTED}}
I've suggested improvements to the workflow. If you accept them,
future projects will be better planned.
{{else}}
{{#if RATING >= 4}}
You're all set! Start working on your project:
  /resume-project {{PROJECT_ID}}
{{else}}
Feel free to update the plan files manually before starting work.
{{/if}}
{{/if}}
```

**Exit**

---

## Issue Category Mappings

### missing_tasks
- **Check:** Compare workflow phases to generated task list
- **Improvement:** Add missing phase tasks to workflow definition
- **Command:** Update workflow YAML to add tasks to relevant phase
- **Action:** `workflow-skill update --workflow-id {id} --add-tasks {phase}`

### wrong_timeline
- **Check:** Compare estimated duration to actual workflow phase durations
- **Improvement:** Adjust phase durations in workflow
- **Command:** Update workflow YAML to adjust phase durations
- **Action:** `workflow-skill update --workflow-id {id} --adjust-duration {phase}`

### missing_dependencies
- **Check:** Review phase dependencies in workflow
- **Improvement:** Add or reorder phase dependencies
- **Command:** Update workflow YAML dependencies
- **Action:** `workflow-skill update --workflow-id {id} --add-dependency {phase} {depends-on}`

### unclear_goals
- **Check:** Review success criteria in workflow
- **Improvement:** Improve success criteria clarity
- **Command:** Update workflow YAML success_criteria
- **Action:** Manual workflow update (requires user input)

### other
- **Action:** Log for manual review, no automatic improvement

---

## Database Schema Reference

```sql
-- Feedback event record
INSERT INTO feedback_events (
    id,                     -- UUID
    created_at,             -- ISO 8601 timestamp
    feedback_type,          -- 'project_plan'
    project_id,             -- Project directory name
    workflow_id,            -- Workflow ID (if used)
    skill_name,             -- 'project-management-skill'
    operation,              -- 'create-project'
    asset_path,             -- Path to project.md
    rating,                 -- 1-5
    comment,                -- User text feedback (optional)
    issue_identified,       -- 1 if rating <= 3, else 0
    issue_category,         -- 'missing_tasks', 'wrong_timeline', etc.
    execution_count,        -- Always 1 (per project)
    prompted                -- Always 0 (explicit in create-project flow)
);
```

---

## Integration Points

### Called from project-management-skill

**In `project-management-skill/subskills/create-project.md`:**

After project structure created and project.md written:

```bash
# After project setup complete
echo ""
echo "Project structure created!"
echo ""

# Prompt for plan review
echo "Would you like to review the project plan? (Y/n): "
read -r RESPONSE

if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
    feedback-skill review-plan \
        --project-path "projects/${PROJECT_NAME}" \
        --project-id "${PROJECT_NAME}" \
        $([ -n "${WORKFLOW_ID}" ] && echo "--workflow-id ${WORKFLOW_ID}")
fi
```

---

## Plan Analysis Helpers

### extract_plan_stats()
```bash
extract_plan_stats() {
    local project_path=$1
    local project_md="${project_path}/project.md"

    # Count sources and targets
    local sources=$(grep -A 100 "## Sources" "$project_md" | grep -c "^- \[" || echo "0")
    local targets=$(grep -A 100 "## Targets" "$project_md" | grep -c "^- \[ \]" || echo "0")

    # Count rules
    local rules=$(grep -A 100 "## Rules Configuration" "$project_md" | grep -c "^- " || echo "0")

    # Get workflow info if exists
    local workflow_id=""
    local phase_count=0
    local duration=""

    if grep -q "## Workflow" "$project_md"; then
        workflow_id=$(grep -A 5 "## Workflow" "$project_md" | grep "Using:" | sed 's/.*Using: \([^ ]*\).*/\1/')
        phase_count=$(grep -A 100 "## Workflow" "$project_md" | grep "^### Phase" | wc -l | tr -d ' ')
        duration=$(grep -A 5 "## Workflow" "$project_md" | grep "Duration:" | sed 's/.*Duration: //')
    fi

    echo "$sources|$targets|$rules|$workflow_id|$phase_count|$duration"
}
```

### check_workflow_coverage()
```bash
check_workflow_coverage() {
    local workflow_id=$1
    local project_path=$2

    # Check if all workflow phases have corresponding folders
    local workflow_phases=$(yq eval ".workflows.${workflow_id}.phases[].id" .kurt/workflows/workflow-registry.yaml)
    local missing_phases=""

    for phase in $workflow_phases; do
        if [ ! -d "${project_path}/${phase}" ]; then
            missing_phases="${missing_phases} ${phase}"
        fi
    done

    if [ -n "$missing_phases" ]; then
        echo "Missing phase folders:${missing_phases}"
        return 1
    fi

    return 0
}
```

---

## Validation and Edge Cases

### If project.md doesn't exist:
```
⚠️  Project file not found: ${PROJECT_PATH}/project.md

Cannot review plan. Please create the project first.
```

### If database write fails:
```
⚠️  Failed to record feedback.

Error: ${ERROR}

Your feedback is valuable but wasn't saved. The project is still
ready to use.
```

### If workflow not found (when workflow_id provided):
```
⚠️  Workflow '${WORKFLOW_ID}' not found in registry.

I can't suggest workflow improvements without the workflow definition.
You can still provide feedback, which will be logged.
```

### If user cancels during review:
```
Plan review cancelled.

You can review the plan anytime using:
  feedback-skill review-plan --project-path projects/<name>
```

---

## Success Metrics

**Track locally (from database):**
- Average rating by workflow (which workflows produce better plans?)
- Most common issues by workflow
- Issue resolution rate after workflow updates
- Rating improvement for projects using updated workflows

**Display to user:**
```bash
feedback-skill dashboard --type project_plan
```

Shows project plan feedback history and workflow improvement effectiveness.

---

## Example Usage

### Automatic review (in create-project flow):
```bash
# After project creation
feedback-skill review-plan \
    --project-path "projects/my-tutorial" \
    --project-id "my-tutorial" \
    --workflow-id "weekly-tutorial"
```

### Explicit review (user-initiated):
```bash
feedback-skill review-plan \
    --project-path "projects/my-tutorial" \
    --project-id "my-tutorial"
```

---

## Workflow Improvement Actions

When issues are identified, the improve subskill will:

1. **For missing_tasks:**
   - Compare workflow phase tasks to generated task-breakdown.md
   - Identify missing tasks
   - Suggest adding them to workflow definition

2. **For wrong_timeline:**
   - Compare estimated durations to user feedback
   - Suggest adjusted phase durations
   - Update workflow with more realistic estimates

3. **For missing_dependencies:**
   - Analyze phase ordering in generated timeline.md
   - Identify missing dependency relationships
   - Suggest updating workflow phase dependencies

4. **For unclear_goals:**
   - Review success_criteria in workflow
   - Prompt user for clarification
   - Suggest updated success criteria language

---

*This subskill provides actionable feedback on project planning that feeds directly into workflow refinement.*
