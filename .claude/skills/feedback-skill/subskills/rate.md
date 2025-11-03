# Rate Content Subskill

**Purpose:** Collect user feedback on content quality (outlines, drafts)
**Parent Skill:** feedback-skill
**Feedback Loop:** Loop 1 - Content Quality → Rules/Prompts
**Operation:** Interactive rating and issue identification

---

## Context Received from Parent Skill

- `$ASSET_PATH` - Path to content being rated
- `$ASSET_TYPE` - "outline" or "draft"
- `$PROJECT_ID` - Optional project identifier
- `$SKILL_NAME` - Skill that created the content
- `$OPERATION` - Operation that created the content (e.g., "outline", "draft")
- `$EXECUTION_COUNT` - Nth execution of this operation
- `$PROMPTED` - Whether this was automatic prompt (true/false)

---

## Workflow

### Step 1: Present Content Context

```
═══════════════════════════════════════════════════════
Content Feedback
═══════════════════════════════════════════════════════

You just created: {{ASSET_TYPE}}
Location: {{ASSET_PATH}}

How would you rate this {{ASSET_TYPE}}?
```

### Step 2: Collect Rating

```
Rating (1-5):
  1 - Poor (major issues)
  2 - Below expectations
  3 - Acceptable (some issues)
  4 - Good (minor issues)
  5 - Excellent (no issues)

Your rating: _
```

**Capture:** `RATING` (1-5)

### Step 3: Handle Rating-Based Flow

**If rating >= 4 (Good/Excellent):**
```
Great! Glad the {{ASSET_TYPE}} worked well for you.

[Optional] Any additional comments? (Enter to skip): _
```

**Capture:** `COMMENT` (optional)

**Store feedback and exit** (no issue identification needed)

---

**If rating <= 3 (Acceptable or below):**

Continue to Step 4 (Issue Identification)

---

### Step 4: Issue Identification

```
What was the main issue?

  a) Wrong tone or style (too formal/casual, wrong voice)
  b) Missing or incorrect structure (poor organization)
  c) Missing or incorrect information (content gaps)
  d) Other (please describe)

Choose (a/b/c/d): _
```

**Capture:** `ISSUE_CHOICE`

**Map to issue categories:**
- `a` → `wrong_tone_style`
- `b` → `missing_structure`
- `c` → `missing_info`
- `d` → `other` (prompt for description)

**If user chose "d" (Other):**
```
Please describe the issue:
> _
```

**Capture:** `ISSUE_DESCRIPTION`

---

### Step 5: Store Feedback in Database

```bash
# Generate UUID for feedback event
FEEDBACK_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Store in database
sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO feedback_events (
    id,
    created_at,
    feedback_type,
    project_id,
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
    'content_quality',
    '${PROJECT_ID}',
    '${SKILL_NAME}',
    '${OPERATION}',
    '${ASSET_PATH}',
    ${RATING},
    '${COMMENT}',
    $([ "${RATING}" -le 3 ] && echo "1" || echo "0"),
    '${ISSUE_CATEGORY}',
    ${EXECUTION_COUNT},
    $([ "${PROMPTED}" = "true" ] && echo "1" || echo "0")
);
EOF
```

---

### Step 6: Check for Improvement Opportunity

**If issue was identified (rating <= 3):**

```
Checking if I can help improve this...
```

**Query for relevant improvements:**

```bash
# Check if there's a recent improvement for this issue
RECENT_IMPROVEMENT=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM improvements i
    JOIN feedback_events f ON i.feedback_event_id = f.id
    WHERE f.issue_category = '${ISSUE_CATEGORY}'
    AND f.skill_name = '${SKILL_NAME}'
    AND i.status IN ('executed', 'accepted')
    AND datetime(i.created_at) > datetime('now', '-7 days')
")

if [ "$RECENT_IMPROVEMENT" -gt 0 ]; then
    # Recent improvement exists, don't suggest again
    echo "I recently made an improvement for this issue. Give it a few more tries to see if it helps."
    exit 0
fi
```

**If no recent improvement, invoke improve subskill:**

```
feedback-skill improve \
    --feedback-id "${FEEDBACK_ID}" \
    --issue-category "${ISSUE_CATEGORY}" \
    --skill-name "${SKILL_NAME}" \
    --operation "${OPERATION}" \
    --asset-path "${ASSET_PATH}"
```

This will analyze the issue and suggest specific improvements.

---

### Step 7: Thank User and Exit

```
───────────────────────────────────────────────────────
✓ Feedback recorded
───────────────────────────────────────────────────────

Thank you for the feedback! This helps improve future content.

{{#if IMPROVEMENT_SUGGESTED}}
Check the improvement suggestion above. If you accept it, I'll apply
the change immediately.
{{else}}
{{#if RATING >= 4}}
Great work! Keep creating.
{{else}}
If this issue persists, let me know and I can look for other improvements.
{{/if}}
{{/if}}
```

**Exit**

---

## Issue Category Mappings

### wrong_tone_style
- **Check:** When was the style rule last updated?
- **Improvement:** Update style rule with recent content examples
- **Command:** `writing-rules-skill style --type {type} --update`

### missing_structure
- **Check:** Does a structure rule exist for this content type?
- **Improvement:** Extract structure pattern from rated content or similar content
- **Command:** `writing-rules-skill structure --type {type} --auto-discover` OR `writing-rules-skill structure --type {type} --update`

### missing_info
- **Check:** Are there gaps in source content or project sources?
- **Improvement:** Suggest adding more sources to project or extracting personas
- **Action:** Prompt user to add sources or extract personas

### other
- **Action:** Log for manual review, no automatic improvement

---

## Database Schema Reference

```sql
-- Feedback event record
INSERT INTO feedback_events (
    id,                     -- UUID
    created_at,             -- ISO 8601 timestamp
    feedback_type,          -- 'content_quality'
    project_id,             -- Project identifier (optional)
    skill_name,             -- 'content-writing-skill'
    operation,              -- 'outline', 'draft'
    asset_path,             -- Path to rated content
    rating,                 -- 1-5
    comment,                -- User text feedback (optional)
    issue_identified,       -- 1 if rating <= 3, else 0
    issue_category,         -- 'wrong_tone_style', 'missing_structure', etc.
    execution_count,        -- Nth execution
    prompted                -- 1 if automatic, 0 if explicit
);
```

---

## Integration Points

### Called from content-writing-skill

**In `content-writing-skill/subskills/draft.md`:**

```bash
# After draft generation, check if we should prompt for feedback
EXECUTION_COUNT=$(get_execution_count "draft")

if [ $((EXECUTION_COUNT % 5)) -eq 0 ]; then
    # Every 5th execution
    echo ""
    echo "Would you like to rate this draft? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        feedback-skill rate \
            --asset-path "${DRAFT_PATH}" \
            --asset-type "draft" \
            --project-id "${PROJECT_NAME}" \
            --skill-name "content-writing-skill" \
            --operation "draft" \
            --execution-count ${EXECUTION_COUNT} \
            --prompted true
    fi
fi
```

**In `content-writing-skill/subskills/outline.md`:**

Similar integration for outline generation.

---

## Validation and Edge Cases

### If user provides invalid rating:
```
Invalid rating. Please enter a number from 1-5: _
```

### If database write fails:
```
⚠️  Failed to record feedback.

Error: ${ERROR}

Your feedback is valuable. Please try again or report this issue.
```

### If user cancels/exits during rating:
```
Feedback cancelled. No problem - feel free to rate anytime using:
  feedback-skill rate --asset-path <path>
```

### If no asset path provided:
```
Error: No asset path provided.

Usage:
  feedback-skill rate --asset-path <path> --asset-type <type>
```

---

## Helper Functions

### get_execution_count()
```bash
get_execution_count() {
    local operation=$1
    local count=$(sqlite3 .kurt/kurt.sqlite "
        SELECT COUNT(*) FROM feedback_events
        WHERE operation = '${operation}'
        AND skill_name = 'content-writing-skill'
    ")
    echo $((count + 1))
}
```

### sanitize_sql_string()
```bash
sanitize_sql_string() {
    # Escape single quotes for SQLite
    echo "$1" | sed "s/'/''/g"
}
```

---

## Success Metrics

**Track locally (from database):**
- Average rating by content type (outline vs draft)
- Most common issues
- Issue resolution rate (after improvements)
- Rating improvement after improvements

**Display to user:**
```bash
feedback-skill dashboard
```

Shows personal feedback history and improvement effectiveness.

---

## Example Usage

### Explicit rating (user-initiated):
```bash
feedback-skill rate \
    --asset-path "projects/my-project/drafts/tutorial.md" \
    --asset-type "draft" \
    --project-id "my-project"
```

### Automatic rating (every 5th execution):
Triggered automatically after draft/outline generation, user just answers prompts.

---

*This subskill provides a simple, actionable feedback collection mechanism that feeds into the improvement system.*
