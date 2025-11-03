# Improve Subskill

**Purpose:** Execute improvements based on user feedback
**Parent Skill:** feedback-skill
**Operations:** Analyze feedback, suggest improvements, execute changes, track results
**Invoked by:** rate.md, review-plan.md, retrospective.md

---

## Context Received from Parent Subskill

### From rate.md (Content Quality):
- `$FEEDBACK_ID` - Feedback event UUID
- `$ISSUE_CATEGORY` - Issue type (wrong_tone_style, missing_structure, missing_info)
- `$SKILL_NAME` - Skill that created content
- `$OPERATION` - Operation (outline, draft)
- `$ASSET_PATH` - Path to rated content

### From review-plan.md (Project Plan):
- `$FEEDBACK_ID` - Feedback event UUID
- `$ISSUE_CATEGORY` - Issue type (missing_tasks, wrong_timeline, missing_dependencies, unclear_goals)
- `$WORKFLOW_ID` - Workflow that was used
- `$PROJECT_PATH` - Path to project

### From retrospective.md (Workflow):
- `$RETROSPECTIVE_ID` - Retrospective UUID
- `$WORKFLOW_ID` - Workflow that was reviewed
- `$PHASE_ISSUES` - Array of phase-specific issues (optional, extracted from database)

---

## Workflow

### Step 1: Load Feedback Context

```bash
# Determine feedback type based on parameters
if [ -n "${FEEDBACK_ID}" ]; then
    # Load feedback event from database
    FEEDBACK_DATA=$(sqlite3 .kurt/kurt.sqlite "
        SELECT feedback_type, issue_category, skill_name, operation, asset_path, project_id, workflow_id
        FROM feedback_events
        WHERE id = '${FEEDBACK_ID}'
    ")

    IFS='|' read -r FEEDBACK_TYPE ISSUE_CATEGORY SKILL_NAME OPERATION ASSET_PATH PROJECT_ID WORKFLOW_ID <<< "$FEEDBACK_DATA"

elif [ -n "${RETROSPECTIVE_ID}" ]; then
    # Load retrospective from database
    FEEDBACK_TYPE="workflow_retrospective"

    RETROSPECTIVE_DATA=$(sqlite3 .kurt/kurt.sqlite "
        SELECT project_id, workflow_id
        FROM workflow_retrospectives
        WHERE id = '${RETROSPECTIVE_ID}'
    ")

    IFS='|' read -r PROJECT_ID WORKFLOW_ID <<< "$RETROSPECTIVE_DATA"

else
    echo "⚠️  No feedback context provided."
    exit 1
fi
```

---

### Step 2: Load Improvement Mappings

```bash
# Load feedback configuration
CONFIG_FILE=".kurt/feedback/feedback-config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  Feedback configuration not found: ${CONFIG_FILE}"
    echo ""
    echo "Cannot suggest improvements without configuration."
    exit 1
fi

# Load issue mapping for this issue category
MAPPING=$(yq eval ".issue_mappings.${ISSUE_CATEGORY}" "$CONFIG_FILE")

if [ "$MAPPING" = "null" ]; then
    echo "No automatic improvement available for issue: ${ISSUE_CATEGORY}"
    exit 0
fi

# Extract mapping details
CHECK_TYPE=$(yq eval ".issue_mappings.${ISSUE_CATEGORY}.check" "$CONFIG_FILE")
SUGGEST_MESSAGE=$(yq eval ".issue_mappings.${ISSUE_CATEGORY}.suggest" "$CONFIG_FILE")
COMMAND_TEMPLATE=$(yq eval ".issue_mappings.${ISSUE_CATEGORY}.command" "$CONFIG_FILE")
```

---

### Step 3: Run Pre-Improvement Check

```
───────────────────────────────────────────────────────
Analyzing improvement opportunity...
───────────────────────────────────────────────────────
```

**Execute check based on check_type:**

```bash
case "$CHECK_TYPE" in
    "style_rule_age")
        # Check when style rule was last updated
        RULE_TYPE=$(infer_rule_type_from_asset "$ASSET_PATH")
        RULE_FILE=$(find_rule_file "$RULE_TYPE" "style")

        if [ -f "$RULE_FILE" ]; then
            RULE_AGE_DAYS=$(get_file_age_days "$RULE_FILE")
            CONTENT_COUNT_SINCE=$(count_content_since_date "$RULE_FILE")

            if [ $RULE_AGE_DAYS -lt 7 ]; then
                echo "Style rule was recently updated (${RULE_AGE_DAYS} days ago)."
                echo "Give it a few more tries before updating again."
                exit 0
            fi

            if [ $CONTENT_COUNT_SINCE -lt 3 ]; then
                echo "Not enough content created (${CONTENT_COUNT_SINCE}) to update rule yet."
                echo "Need at least 3 examples."
                exit 0
            fi
        fi
        ;;

    "structure_rule_exists")
        # Check if structure rule exists
        RULE_TYPE=$(infer_rule_type_from_asset "$ASSET_PATH")
        RULE_FILE=$(find_rule_file "$RULE_TYPE" "structure")

        if [ ! -f "$RULE_FILE" ]; then
            # No rule exists - extraction is appropriate
            ACTION="extract"
        else
            # Rule exists - update is appropriate
            ACTION="update"
            RULE_AGE_DAYS=$(get_file_age_days "$RULE_FILE")

            if [ $RULE_AGE_DAYS -lt 7 ]; then
                echo "Structure rule was recently updated (${RULE_AGE_DAYS} days ago)."
                echo "Give it a few more tries before updating again."
                exit 0
            fi
        fi
        ;;

    "workflow_phase_tasks")
        # Check workflow phase tasks vs generated tasks
        # (for missing_tasks issue)
        # Compare workflow definition to actual project tasks
        ;;

    "workflow_duration_accuracy")
        # Check workflow duration estimates vs actual
        # (for wrong_timeline issue)
        ;;

    "recent_improvement_exists")
        # Generic check for any recent improvement on same issue
        RECENT_COUNT=$(sqlite3 .kurt/kurt.sqlite "
            SELECT COUNT(*) FROM improvements i
            JOIN feedback_events f ON i.feedback_event_id = f.id
            WHERE f.issue_category = '${ISSUE_CATEGORY}'
            AND f.skill_name = '${SKILL_NAME}'
            AND i.status IN ('executed', 'accepted')
            AND datetime(i.created_at) > datetime('now', '-7 days')
        ")

        if [ $RECENT_COUNT -gt 0 ]; then
            echo "A similar improvement was made recently."
            echo "Give it a few more tries before making another change."
            exit 0
        fi
        ;;
esac
```

---

### Step 4: Generate Improvement Command

```bash
# Substitute variables in command template
IMPROVEMENT_COMMAND=$(echo "$COMMAND_TEMPLATE" |
    sed "s/{type}/${RULE_TYPE}/g" |
    sed "s/{workflow_id}/${WORKFLOW_ID}/g" |
    sed "s/{phase_id}/${PHASE_ID}/g")

# Determine improvement type from command
case "$IMPROVEMENT_COMMAND" in
    *"writing-rules-skill style"*)
        IMPROVEMENT_TYPE="update_rule"
        TARGET_RULE="style"
        ;;
    *"writing-rules-skill structure"*)
        IMPROVEMENT_TYPE="update_rule"
        TARGET_RULE="structure"
        ;;
    *"workflow-skill update"*)
        IMPROVEMENT_TYPE="update_workflow"
        TARGET_RULE=""
        ;;
    *"analytics-config"*)
        IMPROVEMENT_TYPE="update_config"
        TARGET_RULE=""
        ;;
    *)
        IMPROVEMENT_TYPE="other"
        TARGET_RULE=""
        ;;
esac
```

---

### Step 5: Present Improvement Suggestion

```
───────────────────────────────────────────────────────
Improvement Suggestion
───────────────────────────────────────────────────────

Issue: {{ISSUE_CATEGORY}}
{{SUGGEST_MESSAGE}}

Proposed action:
  {{IMPROVEMENT_COMMAND}}

{{#if RULE_FILE}}
Current rule: {{RULE_FILE}}
Last updated: {{RULE_AGE_DAYS}} days ago
Content since: {{CONTENT_COUNT_SINCE}} pieces
{{/if}}
```

**Generate before/after preview if possible:**

```bash
# For rule updates, show what will change
if [ "$IMPROVEMENT_TYPE" = "update_rule" ] && [ -f "$RULE_FILE" ]; then
    echo ""
    echo "Preview of changes:"
    echo ""
    echo "Before (current rule):"
    head -n 10 "$RULE_FILE" | sed 's/^/  /'
    echo "  ..."
    echo ""
    echo "After (updated rule):"
    echo "  [Rule will be updated with patterns from recent content]"
    echo "  • New examples from: ${ASSET_PATH}"
    echo "  • Analysis of ${CONTENT_COUNT_SINCE} recent pieces"
    echo ""
fi

# For workflow updates, show what phases will change
if [ "$IMPROVEMENT_TYPE" = "update_workflow" ]; then
    echo ""
    echo "Preview of changes:"
    echo ""

    case "$ISSUE_CATEGORY" in
        "missing_tasks")
            echo "Will add tasks to phase '${PHASE_ID}':"
            echo "  • Analyze ${PROJECT_PATH}/task-breakdown.md"
            echo "  • Extract missing tasks"
            echo "  • Update workflow definition"
            ;;
        "wrong_timeline")
            echo "Will adjust phase duration for '${PHASE_ID}':"
            echo "  • Current estimate: ${CURRENT_DURATION}"
            echo "  • Actual duration: ${ACTUAL_DURATION}"
            echo "  • Suggested adjustment: ${SUGGESTED_DURATION}"
            ;;
        "missing_dependencies")
            echo "Will update phase dependencies:"
            echo "  • Add dependency relationships"
            echo "  • Reorder phases if needed"
            ;;
    esac

    echo ""
fi
```

---

### Step 6: Get User Approval

```
Would you like me to apply this improvement? (Y/n): _
```

**Capture:** `USER_RESPONSE`

**Handle response:**

```bash
case "$USER_RESPONSE" in
    "n"|"N")
        # User rejected
        IMPROVEMENT_STATUS="rejected"
        echo ""
        echo "Improvement not applied."

        # Store rejection in database
        IMPROVEMENT_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

        sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO improvements (
    id, created_at, feedback_event_id, improvement_type,
    target_path, command, status
) VALUES (
    '${IMPROVEMENT_ID}', '${TIMESTAMP}', '${FEEDBACK_ID}',
    '${IMPROVEMENT_TYPE}', '${RULE_FILE}', '${IMPROVEMENT_COMMAND}',
    'rejected'
);
EOF

        exit 0
        ;;

    "")
        # Enter pressed (default: yes)
        ;;

    "y"|"Y")
        # Explicit yes
        ;;

    *)
        echo "Invalid response. Treating as 'no'."
        IMPROVEMENT_STATUS="rejected"
        exit 0
        ;;
esac
```

---

### Step 7: Create Improvement Record (Pre-Execution)

```bash
# Generate UUID for improvement
IMPROVEMENT_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Store before-content snapshot if applicable
if [ -f "$RULE_FILE" ]; then
    CONTENT_BEFORE=$(cat "$RULE_FILE" | base64)
else
    CONTENT_BEFORE=""
fi

# Create improvement record
sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO improvements (
    id,
    created_at,
    feedback_event_id,
    improvement_type,
    target_path,
    command,
    status,
    content_before
) VALUES (
    '${IMPROVEMENT_ID}',
    '${TIMESTAMP}',
    '${FEEDBACK_ID}',
    '${IMPROVEMENT_TYPE}',
    '${TARGET_PATH}',
    '${IMPROVEMENT_COMMAND}',
    'accepted',
    '${CONTENT_BEFORE}'
);
EOF
```

---

### Step 8: Execute Improvement

```
───────────────────────────────────────────────────────
Executing improvement...
───────────────────────────────────────────────────────
```

```bash
# Record start time
START_TIME=$(date +%s%3N)

# Execute command and capture output
set +e
COMMAND_OUTPUT=$(eval "$IMPROVEMENT_COMMAND" 2>&1)
COMMAND_EXIT_CODE=$?
set -e

# Record end time
END_TIME=$(date +%s%3N)
DURATION_MS=$((END_TIME - START_TIME))

# Determine status
if [ $COMMAND_EXIT_CODE -eq 0 ]; then
    IMPROVEMENT_STATUS="executed"
    echo "✓ Improvement applied successfully"
else
    IMPROVEMENT_STATUS="failed"
    echo "✗ Improvement failed"
    echo ""
    echo "Error:"
    echo "$COMMAND_OUTPUT" | sed 's/^/  /'
fi
```

---

### Step 9: Store After-Content Snapshot

```bash
# Store after-content snapshot if applicable
if [ -f "$TARGET_PATH" ] && [ "$IMPROVEMENT_STATUS" = "executed" ]; then
    CONTENT_AFTER=$(cat "$TARGET_PATH" | base64)
else
    CONTENT_AFTER=""
fi

# Update improvement record
EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

sqlite3 .kurt/kurt.sqlite <<EOF
UPDATE improvements
SET
    status = '${IMPROVEMENT_STATUS}',
    executed_at = '${EXECUTED_AT}',
    duration_ms = ${DURATION_MS},
    content_after = '${CONTENT_AFTER}',
    error = '$(echo "$COMMAND_OUTPUT" | sed "s/'/''/g")'
WHERE id = '${IMPROVEMENT_ID}';
EOF
```

---

### Step 10: Show Results

**If successful:**

```
───────────────────────────────────────────────────────
✓ Improvement Complete
───────────────────────────────────────────────────────

{{#if RULE_FILE}}
Updated: {{RULE_FILE}}

The rule has been updated with patterns from recent content.
Try creating similar content to see if the issue is resolved.

{{else if WORKFLOW_ID}}
Updated: Workflow '{{WORKFLOW_ID}}'

The workflow has been updated with your suggested changes.
Future projects using this workflow will benefit from the improvement.

{{/if}}

Duration: {{DURATION_MS}}ms

Improvement ID: {{IMPROVEMENT_ID}}
(Use this to track effectiveness)
```

**If failed:**

```
───────────────────────────────────────────────────────
✗ Improvement Failed
───────────────────────────────────────────────────────

The improvement could not be applied.

Error:
{{COMMAND_OUTPUT}}

This has been logged for review. You can try:
  • Manually applying the change
  • Reporting this issue
  • Trying again later

Improvement ID: {{IMPROVEMENT_ID}}
```

---

### Step 11: Set Up Validation Tracking

**If improvement was successful, set up validation for next usage:**

```bash
# Create feedback loop record
if [ "$IMPROVEMENT_STATUS" = "executed" ]; then
    LOOP_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Get initial rating from feedback event
    INITIAL_RATING=$(sqlite3 .kurt/kurt.sqlite "
        SELECT rating FROM feedback_events WHERE id = '${FEEDBACK_ID}'
    ")

    sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO feedback_loops (
    id,
    created_at,
    feedback_event_id,
    feedback_submitted_at,
    improvement_executed_at,
    loop_duration_days,
    suggestions_made,
    improvements_accepted,
    improvements_successful,
    initial_rating
) VALUES (
    '${LOOP_ID}',
    '${TIMESTAMP}',
    '${FEEDBACK_ID}',
    '${FEEDBACK_TIMESTAMP}',
    '${EXECUTED_AT}',
    0,
    1,
    1,
    1,
    ${INITIAL_RATING}
);
EOF

    echo ""
    echo "───────────────────────────────────────────────────────"
    echo "Validation tracking enabled"
    echo "───────────────────────────────────────────────────────"
    echo ""
    echo "The next time you create similar content, I'll check if"
    echo "the issue was resolved and track the improvement's effectiveness."
fi
```

---

## Improvement Type Handlers

### update_rule (Style/Structure Rules)

```bash
execute_rule_update() {
    local rule_type=$1
    local content_type=$2
    local asset_path=$3

    # Call writing-rules-skill with update flag
    case "$rule_type" in
        "style")
            writing-rules-skill style \
                --type "$content_type" \
                --update \
                --examples "$asset_path"
            ;;
        "structure")
            writing-rules-skill structure \
                --type "$content_type" \
                --update \
                --analyze "$asset_path"
            ;;
    esac
}
```

### update_workflow (Workflow Definition)

```bash
execute_workflow_update() {
    local workflow_id=$1
    local issue_category=$2
    local retrospective_id=$3

    case "$issue_category" in
        "missing_tasks")
            # Extract missing tasks from project
            workflow-skill update \
                --workflow-id "$workflow_id" \
                --add-tasks-from-retrospective "$retrospective_id"
            ;;

        "wrong_timeline")
            # Adjust phase durations
            workflow-skill update \
                --workflow-id "$workflow_id" \
                --adjust-durations-from-retrospective "$retrospective_id"
            ;;

        "missing_dependencies")
            # Update phase dependencies
            workflow-skill update \
                --workflow-id "$workflow_id" \
                --update-dependencies-from-retrospective "$retrospective_id"
            ;;
    esac
}
```

### extract_new_rule (New Rule Creation)

```bash
execute_rule_extraction() {
    local rule_type=$1
    local content_type=$2
    local asset_path=$3

    # Call writing-rules-skill with auto-discover flag
    writing-rules-skill "$rule_type" \
        --type "$content_type" \
        --auto-discover \
        --from "$asset_path"
}
```

---

## Helper Functions

### infer_rule_type_from_asset()
```bash
infer_rule_type_from_asset() {
    local asset_path=$1

    # Try to infer from path
    # e.g., "projects/tutorials/draft.md" → "tutorial"
    # e.g., "projects/api-docs/outline.md" → "api-doc"

    local project_name=$(echo "$asset_path" | cut -d'/' -f2)

    # Query project for content type
    local content_type=$(sqlite3 .kurt/kurt.sqlite "
        SELECT content_type FROM projects
        WHERE id = '${project_name}'
    " 2>/dev/null || echo "")

    if [ -n "$content_type" ]; then
        echo "$content_type"
    else
        # Fallback: use project name
        echo "$project_name"
    fi
}
```

### find_rule_file()
```bash
find_rule_file() {
    local content_type=$1
    local rule_type=$2  # "style" or "structure"

    # Look for rule file in standard locations
    local rule_dir=".kurt/rules/${rule_type}"

    if [ -f "${rule_dir}/${content_type}.md" ]; then
        echo "${rule_dir}/${content_type}.md"
    elif [ -f "${rule_dir}/default.md" ]; then
        echo "${rule_dir}/default.md"
    else
        echo ""
    fi
}
```

### get_file_age_days()
```bash
get_file_age_days() {
    local file_path=$1

    if [ ! -f "$file_path" ]; then
        echo "999"
        return
    fi

    # Get file modification time
    local file_mtime=$(stat -f %m "$file_path" 2>/dev/null || stat -c %Y "$file_path" 2>/dev/null)
    local current_time=$(date +%s)

    # Calculate age in days
    local age_seconds=$((current_time - file_mtime))
    local age_days=$((age_seconds / 86400))

    echo "$age_days"
}
```

### count_content_since_date()
```bash
count_content_since_date() {
    local rule_file=$1

    # Get rule file modification time
    local rule_mtime=$(stat -f %m "$rule_file" 2>/dev/null || stat -c %Y "$rule_file" 2>/dev/null)
    local rule_date=$(date -r "$rule_mtime" +"%Y-%m-%dT%H:%M:%SZ")

    # Count feedback events since that date
    local count=$(sqlite3 .kurt/kurt.sqlite "
        SELECT COUNT(*) FROM feedback_events
        WHERE feedback_type = 'content_quality'
        AND datetime(created_at) > datetime('${rule_date}')
    ")

    echo "$count"
}
```

---

## Validation on Next Usage

### Triggered from rate.md or other feedback subskills:

```bash
# In rate.md, after collecting new feedback
# Check if there's an open feedback loop for this issue

OPEN_LOOP=$(sqlite3 .kurt/kurt.sqlite "
    SELECT fl.id, fl.feedback_event_id, i.improvement_type
    FROM feedback_loops fl
    JOIN improvements i ON i.feedback_event_id = fl.feedback_event_id
    JOIN feedback_events f ON f.id = fl.feedback_event_id
    WHERE fl.validation_completed_at IS NULL
    AND f.issue_category = '${ISSUE_CATEGORY}'
    AND f.skill_name = '${SKILL_NAME}'
    AND datetime(fl.improvement_executed_at) < datetime('now')
    LIMIT 1
")

if [ -n "$OPEN_LOOP" ]; then
    IFS='|' read -r LOOP_ID OLD_FEEDBACK_ID IMPROVEMENT_TYPE <<< "$OPEN_LOOP"

    # Get ratings
    OLD_RATING=$(sqlite3 .kurt/kurt.sqlite "SELECT rating FROM feedback_events WHERE id = '${OLD_FEEDBACK_ID}'")
    NEW_RATING=${RATING}  # From current feedback

    # Calculate if issue resolved
    ISSUE_RESOLVED=0
    if [ $NEW_RATING -gt $OLD_RATING ] && [ "${ISSUE_CATEGORY}" = "null" ]; then
        ISSUE_RESOLVED=1
    fi

    # Calculate days since improvement
    IMPROVEMENT_DATE=$(sqlite3 .kurt/kurt.sqlite "SELECT improvement_executed_at FROM feedback_loops WHERE id = '${LOOP_ID}'")
    DAYS_SINCE=$(calculate_days_between "$IMPROVEMENT_DATE" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")")

    # Update feedback loop
    sqlite3 .kurt/kurt.sqlite <<EOF
UPDATE feedback_loops
SET
    validation_completed_at = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
    subsequent_rating = ${NEW_RATING},
    rating_change = $((NEW_RATING - OLD_RATING)),
    issue_resolved = ${ISSUE_RESOLVED},
    loop_duration_days = ${DAYS_SINCE}
WHERE id = '${LOOP_ID}';
EOF

    # Update improvement validation
    sqlite3 .kurt/kurt.sqlite <<EOF
UPDATE improvements
SET
    validated_at = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
    validation_rating = ${NEW_RATING},
    issue_resolved = ${ISSUE_RESOLVED}
WHERE feedback_event_id = '${OLD_FEEDBACK_ID}';
EOF

    # Show validation result to user
    if [ $ISSUE_RESOLVED -eq 1 ]; then
        echo ""
        echo "✓ Previous improvement validated!"
        echo "  Rating improved from ${OLD_RATING} to ${NEW_RATING}"
        echo "  The '${ISSUE_CATEGORY}' issue appears to be resolved."
    else
        echo ""
        echo "⚠️  Previous improvement may not have worked"
        echo "  Rating: ${OLD_RATING} → ${NEW_RATING}"
        echo "  The '${ISSUE_CATEGORY}' issue may still exist."
    fi
fi
```

---

## Success Metrics

**Track locally (from database):**
- Improvement acceptance rate (accepted / suggested)
- Improvement success rate (executed / accepted)
- Issue resolution rate (issue_resolved = 1 in feedback_loops)
- Average rating change after improvement
- Most effective improvement types
- Average time to validation

**Display to user:**
```bash
feedback-skill dashboard --type improvements
```

Shows improvement history and effectiveness metrics.

---

## Error Handling

### Command execution failures:
- Store error in improvements table
- Mark status as 'failed'
- Show user the error
- Provide troubleshooting suggestions

### Database write failures:
- Log to stderr
- Continue execution if possible
- Warn user that tracking may be incomplete

### Missing dependencies (skills not available):
- Check if required skill exists before suggesting
- Provide alternative manual steps
- Log missing dependency

---

## Example Usage

### From rate.md (content quality issue):
```bash
feedback-skill improve \
    --feedback-id "abc-123" \
    --issue-category "wrong_tone_style" \
    --skill-name "content-writing-skill" \
    --asset-path "projects/tutorial/draft.md"
```

### From review-plan.md (project plan issue):
```bash
feedback-skill improve \
    --feedback-id "def-456" \
    --issue-category "missing_tasks" \
    --workflow-id "weekly-tutorial" \
    --project-path "projects/my-tutorial"
```

### From retrospective.md (workflow issue):
```bash
feedback-skill improve \
    --retrospective-id "ghi-789" \
    --workflow-id "weekly-tutorial"
```

---

*This subskill is the core of the improvement system, translating user feedback into actionable changes that improve the system over time.*
