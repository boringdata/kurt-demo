# Retrospective Subskill

**Purpose:** Collect user feedback on workflow effectiveness after project completion
**Parent Skill:** feedback-skill
**Feedback Loop:** Loop 3 - Workflow Retrospective → Workflow Refinement
**Operation:** Interactive workflow review and phase-by-phase rating

---

## Context Received from Parent Skill

- `$PROJECT_PATH` - Path to completed project directory
- `$PROJECT_ID` - Project identifier (directory name)
- `$WORKFLOW_ID` - Workflow ID that was used for this project
- `$COMPLETION_DATE` - Date project was marked complete (optional)

---

## Workflow

### Step 1: Validate Project Completion

```bash
# Check if project is marked complete
PROJECT_STATUS=$(sqlite3 .kurt/kurt.sqlite "
    SELECT status FROM projects
    WHERE id = '${PROJECT_ID}'
" 2>/dev/null || echo "unknown")

if [ "$PROJECT_STATUS" != "completed" ]; then
    echo "⚠️  Project '${PROJECT_ID}' is not marked as complete."
    echo ""
    echo "Retrospectives are most useful after project completion."
    echo "Would you like to continue anyway? (y/N): "
    read -r RESPONSE

    if [ "$RESPONSE" != "y" ] && [ "$RESPONSE" != "Y" ]; then
        echo "Retrospective cancelled."
        exit 0
    fi
fi
```

---

### Step 2: Load Workflow Definition

```bash
# Load workflow from registry
WORKFLOW_FILE=".kurt/workflows/${WORKFLOW_ID}.yaml"

if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "⚠️  Workflow definition not found: ${WORKFLOW_ID}"
    echo ""
    echo "Cannot perform retrospective without workflow definition."
    exit 1
fi

# Extract workflow metadata
WORKFLOW_NAME=$(yq eval ".name" "$WORKFLOW_FILE")
PHASE_COUNT=$(yq eval ".phases | length" "$WORKFLOW_FILE")
TOTAL_DURATION=$(yq eval ".metadata.estimated_duration" "$WORKFLOW_FILE")
```

---

### Step 3: Present Retrospective Context

```
═══════════════════════════════════════════════════════
Workflow Retrospective
═══════════════════════════════════════════════════════

Project: {{PROJECT_ID}}
Workflow: {{WORKFLOW_NAME}} ({{WORKFLOW_ID}})

Phases: {{PHASE_COUNT}}
Estimated duration: {{TOTAL_DURATION}}

Now that you've completed this project, let's review how well
the workflow worked for you. Your feedback will help improve
future projects using this workflow.
```

---

### Step 4: Collect Overall Rating

```
First, how was the overall workflow experience?

Rating (1-5):
  1 - Poor (major issues, workflow didn't help)
  2 - Below expectations (significant problems)
  3 - Acceptable (worked but had issues)
  4 - Good (minor issues)
  5 - Excellent (workflow worked great)

Your rating: _
```

**Capture:** `OVERALL_RATING` (1-5)

```
[Optional] Any overall comments about the workflow? (Enter to skip):
> _
```

**Capture:** `OVERALL_COMMENT` (optional)

---

### Step 5: Phase-by-Phase Review

```
Now let's review each phase individually.

───────────────────────────────────────────────────────
```

**For each phase in workflow:**

```bash
# Load phase definition
PHASE_ID=$(yq eval ".phases[${PHASE_INDEX}].id" "$WORKFLOW_FILE")
PHASE_NAME=$(yq eval ".phases[${PHASE_INDEX}].name" "$WORKFLOW_FILE")
PHASE_DURATION=$(yq eval ".phases[${PHASE_INDEX}].duration" "$WORKFLOW_FILE")
PHASE_TASKS=$(yq eval ".phases[${PHASE_INDEX}].tasks[]" "$WORKFLOW_FILE" | wc -l)

# Display phase info
cat <<EOF

Phase ${PHASE_POSITION}: ${PHASE_NAME}
Estimated duration: ${PHASE_DURATION}
Tasks: ${PHASE_TASKS}

How useful was this phase?

Rating (1-5):
  1 - Not useful (waste of time)
  2 - Somewhat useful (could skip)
  3 - Moderately useful (kept it)
  4 - Very useful (helped a lot)
  5 - Essential (couldn't do without)

Your rating: _
EOF
```

**Capture:** `PHASE_RATING` (1-5)

```
Was the duration estimate accurate? (y/n): _
```

**Capture:** `DURATION_ACCURATE` (y/n)

```
Were all the tasks relevant? (y/n): _
```

**Capture:** `TASKS_COMPLETE` (y/n)

**If rating <= 3 OR duration_accurate = n OR tasks_complete = n:**

```
What would you change about this phase?

  a) Add more tasks
  b) Remove unnecessary tasks
  c) Adjust duration estimate
  d) Reorder (move earlier/later in workflow)
  e) Other (please describe)
  f) Skip (no specific change)

Choose (a/b/c/d/e/f): _
```

**Capture:** `CHANGE_TYPE`

**If user chose a-e:**
```
Please describe the change:
> _
```

**Capture:** `CHANGE_DESCRIPTION`

**Store phase rating:**

```bash
PHASE_RATING_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO workflow_phase_ratings (
    id,
    retrospective_id,
    phase_id,
    phase_name,
    phase_position,
    usefulness_rating,
    duration_accurate,
    tasks_complete,
    comment,
    suggested_change,
    change_type,
    change_description
) VALUES (
    '${PHASE_RATING_ID}',
    '${RETROSPECTIVE_ID}',
    '${PHASE_ID}',
    '${PHASE_NAME}',
    ${PHASE_POSITION},
    ${PHASE_RATING},
    $([ "${DURATION_ACCURATE}" = "y" ] && echo "1" || echo "0"),
    $([ "${TASKS_COMPLETE}" = "y" ] && echo "1" || echo "0"),
    '${PHASE_COMMENT}',
    $([ -n "${CHANGE_TYPE}" ] && [ "${CHANGE_TYPE}" != "f" ] && echo "1" || echo "0"),
    '${CHANGE_TYPE}',
    '${CHANGE_DESCRIPTION}'
);
EOF
```

**Repeat for all phases**

---

### Step 6: Store Retrospective in Database

```bash
# Generate UUID for retrospective
RETROSPECTIVE_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Calculate project duration
if [ -n "${COMPLETION_DATE}" ]; then
    PROJECT_START=$(sqlite3 .kurt/kurt.sqlite "
        SELECT created_at FROM projects
        WHERE id = '${PROJECT_ID}'
    ")

    # Calculate duration in days
    START_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$PROJECT_START" +%s 2>/dev/null || echo "0")
    END_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$COMPLETION_DATE" +%s 2>/dev/null || echo "0")
    DURATION_DAYS=$(( (END_EPOCH - START_EPOCH) / 86400 ))
else
    DURATION_DAYS=0
fi

# Sanitize comment for SQL
OVERALL_COMMENT_SANITIZED=$(echo "$OVERALL_COMMENT" | sed "s/'/''/g")

# Store in database
sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO workflow_retrospectives (
    id,
    created_at,
    project_id,
    workflow_id,
    overall_rating,
    overall_comment,
    total_duration_days,
    completed_at
) VALUES (
    '${RETROSPECTIVE_ID}',
    '${TIMESTAMP}',
    '${PROJECT_ID}',
    '${WORKFLOW_ID}',
    ${OVERALL_RATING},
    '${OVERALL_COMMENT_SANITIZED}',
    ${DURATION_DAYS},
    '${COMPLETION_DATE}'
);
EOF
```

---

### Step 7: Analyze Feedback and Suggest Improvements

```
───────────────────────────────────────────────────────
Analyzing feedback...
───────────────────────────────────────────────────────
```

**Check for improvement opportunities:**

```bash
# Count phases with low ratings
LOW_RATED_PHASES=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM workflow_phase_ratings
    WHERE retrospective_id = '${RETROSPECTIVE_ID}'
    AND usefulness_rating <= 3
")

# Count phases with suggested changes
PHASES_WITH_CHANGES=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM workflow_phase_ratings
    WHERE retrospective_id = '${RETROSPECTIVE_ID}'
    AND suggested_change = 1
")

# Count duration/task issues
DURATION_ISSUES=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM workflow_phase_ratings
    WHERE retrospective_id = '${RETROSPECTIVE_ID}'
    AND duration_accurate = 0
")

TASK_ISSUES=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM workflow_phase_ratings
    WHERE retrospective_id = '${RETROSPECTIVE_ID}'
    AND tasks_complete = 0
")
```

**If improvement opportunities found:**

```bash
if [ $PHASES_WITH_CHANGES -gt 0 ] || [ $LOW_RATED_PHASES -gt 0 ]; then
    echo ""
    echo "I found ${PHASES_WITH_CHANGES} phase(s) with suggested improvements."
    echo ""
    echo "Would you like me to suggest workflow updates? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        # Invoke improve subskill
        feedback-skill improve \
            --retrospective-id "${RETROSPECTIVE_ID}" \
            --workflow-id "${WORKFLOW_ID}"
    fi
fi
```

---

### Step 8: Thank User and Summary

```
───────────────────────────────────────────────────────
✓ Retrospective complete
───────────────────────────────────────────────────────

Thank you for the detailed feedback!

Summary:
  Overall rating: {{OVERALL_RATING}}/5
  Phases reviewed: {{PHASE_COUNT}}
  Low-rated phases: {{LOW_RATED_PHASES}}
  Suggested changes: {{PHASES_WITH_CHANGES}}

{{#if IMPROVEMENT_SUGGESTED}}
I've suggested improvements to the workflow. If you accept them,
future projects using this workflow will be better structured.
{{else}}
{{#if OVERALL_RATING >= 4}}
Glad the workflow worked well! Your feedback helps validate the design.
{{else}}
Your feedback is noted. The workflow may need refinement based on
common issues across multiple projects.
{{/if}}
{{/if}}

You can view workflow feedback anytime:
  feedback-skill dashboard --type workflow_retrospective --workflow ${WORKFLOW_ID}
```

**Exit**

---

## Database Schema Reference

```sql
-- Retrospective record
INSERT INTO workflow_retrospectives (
    id,                     -- UUID
    created_at,             -- ISO 8601 timestamp
    project_id,             -- Project identifier
    workflow_id,            -- Workflow identifier
    overall_rating,         -- 1-5
    overall_comment,        -- User text feedback (optional)
    total_duration_days,    -- Actual project duration
    completed_at            -- Project completion date
);

-- Phase rating records (one per phase)
INSERT INTO workflow_phase_ratings (
    id,                     -- UUID
    retrospective_id,       -- Links to workflow_retrospectives
    phase_id,               -- Phase identifier from workflow
    phase_name,             -- Phase name for reference
    phase_position,         -- 1, 2, 3, etc
    usefulness_rating,      -- 1-5
    duration_accurate,      -- 1 if accurate, 0 if not
    tasks_complete,         -- 1 if all relevant, 0 if not
    comment,                -- Phase-specific feedback (optional)
    suggested_change,       -- 1 if change suggested, 0 if not
    change_type,            -- 'add_tasks', 'remove_tasks', etc
    change_description      -- User's description of change
);
```

---

## Integration Points

### Called from project-management-skill

**When project marked complete:**

```bash
# In project completion flow
if [ -n "${WORKFLOW_ID}" ]; then
    echo ""
    echo "Project complete! 🎉"
    echo ""
    echo "Would you like to provide feedback on the workflow? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        feedback-skill retrospective \
            --project-path "projects/${PROJECT_ID}" \
            --project-id "${PROJECT_ID}" \
            --workflow-id "${WORKFLOW_ID}" \
            --completion-date "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    fi
fi
```

---

## Analysis Helpers

### calculate_workflow_health()
```bash
calculate_workflow_health() {
    local workflow_id=$1

    # Get average ratings across all retrospectives
    sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    COUNT(DISTINCT wr.id) as retrospective_count,
    AVG(wr.overall_rating) as avg_overall,
    AVG(wpr.usefulness_rating) as avg_phase_rating,
    SUM(CASE WHEN wpr.duration_accurate = 0 THEN 1 ELSE 0 END) as duration_issues,
    SUM(CASE WHEN wpr.tasks_complete = 0 THEN 1 ELSE 0 END) as task_issues,
    SUM(CASE WHEN wpr.suggested_change = 1 THEN 1 ELSE 0 END) as suggested_changes
FROM workflow_retrospectives wr
LEFT JOIN workflow_phase_ratings wpr ON wr.id = wpr.retrospective_id
WHERE wr.workflow_id = '${workflow_id}';
EOF
}
```

### identify_problematic_phases()
```bash
identify_problematic_phases() {
    local workflow_id=$1

    # Find phases with consistently low ratings
    sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    wpr.phase_id,
    wpr.phase_name,
    AVG(wpr.usefulness_rating) as avg_rating,
    COUNT(*) as rating_count,
    SUM(CASE WHEN wpr.suggested_change = 1 THEN 1 ELSE 0 END) as change_suggestions
FROM workflow_phase_ratings wpr
JOIN workflow_retrospectives wr ON wpr.retrospective_id = wr.id
WHERE wr.workflow_id = '${workflow_id}'
GROUP BY wpr.phase_id, wpr.phase_name
HAVING avg_rating < 3.5
ORDER BY avg_rating ASC;
EOF
}
```

---

## Improvement Opportunity Detection

### Trigger improvement suggestions when:

1. **Low overall rating** (≤ 3)
   - Suggest comprehensive workflow review
   - Identify most problematic phases
   - Propose workflow restructure

2. **Specific phase issues**
   - Phase rating ≤ 3: Review phase necessity
   - Duration inaccurate: Adjust estimates
   - Tasks incomplete: Update task list
   - Suggested changes: Implement user suggestions

3. **Pattern detection** (multiple retrospectives)
   - Same phase consistently low-rated → Consider removing or redesigning
   - Same duration issues → Update default estimates
   - Common task suggestions → Add to workflow definition

---

## Validation and Edge Cases

### If workflow not found:
```
⚠️  Workflow '${WORKFLOW_ID}' not found.

Cannot perform retrospective without workflow definition.
```

### If project has no workflow:
```
⚠️  Project '${PROJECT_ID}' did not use a workflow.

Retrospectives are only available for workflow-based projects.
Would you like general project feedback instead? (y/N): _

[If yes, redirect to a simpler feedback form]
```

### If retrospective already exists:
```
A retrospective already exists for this project (${EXISTING_DATE}).

Would you like to:
  a) View existing retrospective
  b) Create a new one (useful if project was reopened)
  c) Cancel

Choose (a/b/c): _
```

### If user exits during phase review:
```
Retrospective partially saved (${COMPLETED_PHASES}/${TOTAL_PHASES} phases reviewed).

You can resume anytime using:
  feedback-skill retrospective --resume --project-id ${PROJECT_ID}
```

---

## Success Metrics

**Track locally (from database):**
- Average overall rating by workflow
- Average phase rating by workflow phase
- Common issues by workflow
- Improvement implementation rate
- Rating trends over time (are workflows getting better?)

**Display to user:**
```bash
# Overall workflow health
feedback-skill dashboard --type workflow --workflow-id ${WORKFLOW_ID}

# Specific retrospective
feedback-skill retrospective --view --project-id ${PROJECT_ID}
```

---

## Example Usage

### Automatic retrospective (after project completion):
```bash
feedback-skill retrospective \
    --project-path "projects/my-tutorial" \
    --project-id "my-tutorial" \
    --workflow-id "weekly-tutorial" \
    --completion-date "2025-02-02T15:30:00Z"
```

### Explicit retrospective (user-initiated):
```bash
feedback-skill retrospective \
    --project-id "my-tutorial"
```

### View existing retrospective:
```bash
feedback-skill retrospective \
    --view \
    --project-id "my-tutorial"
```

---

## Retrospective Report Format

When viewing an existing retrospective:

```
═══════════════════════════════════════════════════════
Retrospective: {{PROJECT_ID}}
═══════════════════════════════════════════════════════

Workflow: {{WORKFLOW_NAME}}
Date: {{CREATED_AT}}
Duration: {{TOTAL_DURATION_DAYS}} days

Overall Rating: {{OVERALL_RATING}}/5
Comment: {{OVERALL_COMMENT}}

───────────────────────────────────────────────────────
Phase Ratings
───────────────────────────────────────────────────────

{{#each PHASES}}
{{POSITION}}. {{PHASE_NAME}}
   Rating: {{USEFULNESS_RATING}}/5
   Duration accurate: {{DURATION_ACCURATE}}
   Tasks complete: {{TASKS_COMPLETE}}
   {{#if SUGGESTED_CHANGE}}
   Suggested change: {{CHANGE_TYPE}} - {{CHANGE_DESCRIPTION}}
   {{/if}}
{{/each}}

───────────────────────────────────────────────────────
```

---

*This subskill provides comprehensive workflow feedback that enables data-driven workflow refinement.*
