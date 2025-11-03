# Suggest Improvements Subskill

**Purpose:** Analyze feedback patterns and suggest improvements
**Parent Skill:** feedback-skill
**Operation:** Identify common issues and improvement opportunities from accumulated feedback

---

## Context Received from Parent Skill

- `$DAYS` - Optional time window (default: 30 days)
- `$MIN_FREQUENCY` - Minimum issue occurrences to suggest (default: 3)
- `$TYPE_FILTER` - Optional filter (content_quality | project_plan | workflow_retrospective)

---

## Workflow

### Step 1: Parse Arguments

```bash
# Default values
DAYS=30
MIN_FREQUENCY=3
TYPE_FILTER=""
SHOW_ALL=false

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --days)
            DAYS="$2"
            shift 2
            ;;
        --min-frequency)
            MIN_FREQUENCY="$2"
            shift 2
            ;;
        --type)
            TYPE_FILTER="$2"
            shift 2
            ;;
        --all)
            SHOW_ALL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
```

---

### Step 2: Query Feedback Patterns

```bash
# Query common issues
COMMON_ISSUES=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    f.issue_category,
    f.feedback_type,
    COUNT(*) as occurrence_count,
    AVG(f.rating) as avg_rating,
    COUNT(DISTINCT CASE WHEN f.skill_name IS NOT NULL THEN f.skill_name
                        WHEN f.workflow_id IS NOT NULL THEN f.workflow_id
                        ELSE f.project_id END) as affected_items,
    SUM(CASE WHEN EXISTS (
        SELECT 1 FROM improvements i
        WHERE i.feedback_event_id = f.id
        AND i.status IN ('executed', 'accepted')
    ) THEN 1 ELSE 0 END) as improvement_attempts,
    SUM(CASE WHEN EXISTS (
        SELECT 1 FROM improvements i
        WHERE i.feedback_event_id = f.id
        AND i.issue_resolved = 1
    ) THEN 1 ELSE 0 END) as resolutions
FROM feedback_events f
WHERE datetime(f.created_at) > datetime('now', '-${DAYS} days')
AND f.issue_identified = 1
$([ -n "$TYPE_FILTER" ] && echo "AND f.feedback_type = '${TYPE_FILTER}'")
GROUP BY f.issue_category, f.feedback_type
HAVING occurrence_count >= ${MIN_FREQUENCY}
ORDER BY occurrence_count DESC, avg_rating ASC;
EOF
)
```

---

### Step 3: Display Header

```
═══════════════════════════════════════════════════════
Improvement Suggestions
═══════════════════════════════════════════════════════

Analysis period: Last ${DAYS} days
Minimum frequency: ${MIN_FREQUENCY} occurrences
$([ -n "$TYPE_FILTER" ] && echo "Filter: ${TYPE_FILTER}")

Based on your feedback patterns, here are recommended improvements:
```

---

### Step 4: Check if Suggestions Available

```bash
SUGGESTION_COUNT=$(echo "$COMMON_ISSUES" | wc -l | tr -d ' ')

if [ "$SUGGESTION_COUNT" -eq 0 ]; then
    echo ""
    echo "✓ No improvement suggestions at this time."
    echo ""
    echo "This could mean:"
    echo "  • No recurring issues in recent feedback"
    echo "  • Not enough feedback collected (need ≥ ${MIN_FREQUENCY} for same issue)"
    echo "  • All issues have been addressed"
    echo ""
    echo "Keep providing feedback when prompted to help identify patterns."
    echo ""
    echo "Recent feedback summary:"
    echo ""

    # Show quick stats
    sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    feedback_type,
    COUNT(*) as count,
    AVG(rating) as avg_rating
FROM feedback_events
WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
GROUP BY feedback_type;
EOF

    exit 0
fi
```

---

### Step 5: Display Suggestions by Priority

**Priority calculation:**
- High: occurrence_count >= 5 AND resolution_rate < 50%
- Medium: occurrence_count >= 3 AND resolution_rate < 75%
- Low: All others

```bash
# Process each issue and categorize
echo "$COMMON_ISSUES" | while IFS='|' read -r ISSUE_CATEGORY FEEDBACK_TYPE OCCURRENCE_COUNT AVG_RATING AFFECTED_ITEMS IMPROVEMENT_ATTEMPTS RESOLUTIONS; do

    # Calculate priority
    if [ "$RESOLUTIONS" -eq 0 ]; then
        RESOLUTION_RATE=0
    else
        RESOLUTION_RATE=$((RESOLUTIONS * 100 / OCCURRENCE_COUNT))
    fi

    if [ "$OCCURRENCE_COUNT" -ge 5 ] && [ "$RESOLUTION_RATE" -lt 50 ]; then
        PRIORITY="HIGH"
    elif [ "$OCCURRENCE_COUNT" -ge 3 ] && [ "$RESOLUTION_RATE" -lt 75 ]; then
        PRIORITY="MEDIUM"
    else
        PRIORITY="LOW"
    fi

    # Store for display
    echo "${PRIORITY}|${ISSUE_CATEGORY}|${FEEDBACK_TYPE}|${OCCURRENCE_COUNT}|${AVG_RATING}|${AFFECTED_ITEMS}|${RESOLUTION_RATE}"
done | sort -t'|' -k1,1r -k4,4nr > /tmp/suggestions_sorted.txt
```

**Display:**

```
───────────────────────────────────────────────────────
HIGH PRIORITY
───────────────────────────────────────────────────────

{{#each HIGH_PRIORITY_SUGGESTIONS}}
{{INDEX}}. {{ISSUE_NAME}} ({{FEEDBACK_TYPE_NAME}})

   Frequency: {{OCCURRENCE_COUNT}}× in last ${DAYS} days
   Avg rating when reported: {{AVG_RATING}}/5 {{RATING_ICON}}
   Items affected: {{AFFECTED_ITEMS}}
   Resolution rate: {{RESOLUTION_RATE}}% {{#if LOW_RESOLUTION}}⚠️{{/if}}

   {{ISSUE_DESCRIPTION}}

   Recommended action:
   {{RECOMMENDATION}}

   {{#if HAS_MAPPING}}
   Execute improvement:
     feedback-skill improve --issue-category {{ISSUE_CATEGORY}}
   {{else}}
   Manual review required:
     {{MANUAL_GUIDANCE}}
   {{/if}}

{{/each}}

{{#if NO_HIGH_PRIORITY}}
✓ No high-priority issues found.
{{/if}}
```

```
───────────────────────────────────────────────────────
MEDIUM PRIORITY
───────────────────────────────────────────────────────

{{#each MEDIUM_PRIORITY_SUGGESTIONS}}
{{INDEX}}. {{ISSUE_NAME}} ({{FEEDBACK_TYPE_NAME}})
   Frequency: {{OCCURRENCE_COUNT}}× | Avg rating: {{AVG_RATING}}/5
   Resolution rate: {{RESOLUTION_RATE}}%

   {{RECOMMENDATION}}

{{/each}}

{{#if NO_MEDIUM_PRIORITY}}
✓ No medium-priority issues found.
{{/if}}
```

**If --all flag, also show LOW priority:**

```
───────────────────────────────────────────────────────
LOW PRIORITY
───────────────────────────────────────────────────────

{{#each LOW_PRIORITY_SUGGESTIONS}}
{{INDEX}}. {{ISSUE_NAME}} - {{OCCURRENCE_COUNT}}× ({{RESOLUTION_RATE}}% resolved)
{{/each}}
```

---

### Step 6: Load Issue Details and Recommendations

```bash
# For each suggestion, load issue mapping and generate recommendation
get_recommendation() {
    local issue_category=$1
    local feedback_type=$2

    # Load from feedback-config.yaml
    local suggestion=$(yq eval ".issue_mappings.${issue_category}.suggest" .kurt/feedback/feedback-config.yaml)
    local command=$(yq eval ".issue_mappings.${issue_category}.command" .kurt/feedback/feedback-config.yaml)
    local description=$(yq eval ".issue_mappings.${issue_category}.description" .kurt/feedback/feedback-config.yaml)

    echo "${description}|${suggestion}|${command}"
}

# Get affected items for context
get_affected_items() {
    local issue_category=$1
    local feedback_type=$2

    sqlite3 .kurt/kurt.sqlite <<EOF
SELECT DISTINCT
    COALESCE(skill_name, workflow_id, project_id) as item
FROM feedback_events
WHERE issue_category = '${issue_category}'
AND feedback_type = '${feedback_type}'
AND datetime(created_at) > datetime('now', '-${DAYS} days')
LIMIT 5;
EOF
}
```

---

### Step 7: Detailed Examples for Top Issues

**For top 2 high-priority issues, show examples:**

```bash
# Get sample feedback comments
SAMPLE_FEEDBACK=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    substr(created_at, 1, 10) as date,
    rating,
    comment,
    COALESCE(skill_name, workflow_id, 'N/A') as context
FROM feedback_events
WHERE issue_category = '${ISSUE_CATEGORY}'
AND feedback_type = '${FEEDBACK_TYPE}'
AND datetime(created_at) > datetime('now', '-${DAYS} days')
AND comment IS NOT NULL
AND comment != ''
ORDER BY created_at DESC
LIMIT 3;
EOF
)
```

**Display:**

```
   Recent feedback examples:
   {{#each SAMPLES}}
   • {{DATE}} (rating {{RATING}}/5) - {{CONTEXT}}
     "{{COMMENT_TRUNCATED}}"
   {{/each}}
```

---

### Step 8: Impact Analysis

```bash
# Calculate potential impact of addressing issues
TOTAL_FEEDBACK=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM feedback_events
    WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
")

ISSUES_PERCENTAGE=$((OCCURRENCE_COUNT * 100 / TOTAL_FEEDBACK))
```

**Display:**

```
───────────────────────────────────────────────────────
Impact Analysis
───────────────────────────────────────────────────────

Addressing the top 3 issues would improve:
  • {{PERCENTAGE}}% of all feedback submissions
  • {{AFFECTED_ITEMS}} items (skills/workflows/projects)
  • Estimated rating improvement: +{{ESTIMATED_IMPROVEMENT}}/5

Based on current resolution rates, focus on:
  1. {{TOP_UNRESOLVED_ISSUE}} ({{UNRESOLVED_COUNT}} unresolved)
  2. {{SECOND_UNRESOLVED_ISSUE}} ({{UNRESOLVED_COUNT}} unresolved)
```

---

### Step 9: Workflow-Specific Suggestions

**If workflow-related issues exist:**

```bash
# Identify workflows with consistent issues
PROBLEMATIC_WORKFLOWS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    workflow_id,
    COUNT(DISTINCT f.id) as issue_count,
    AVG(f.rating) as avg_rating,
    GROUP_CONCAT(DISTINCT f.issue_category) as issues
FROM feedback_events f
WHERE f.workflow_id IS NOT NULL
AND f.issue_identified = 1
AND datetime(f.created_at) > datetime('now', '-${DAYS} days')
GROUP BY workflow_id
HAVING issue_count >= 2
ORDER BY issue_count DESC;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Workflow-Specific Recommendations
───────────────────────────────────────────────────────

{{#each PROBLEMATIC_WORKFLOWS}}
{{WORKFLOW_ID}}:
  Issues: {{ISSUE_COUNT}} reported ({{ISSUES}})
  Avg rating: {{AVG_RATING}}/5

  Recommended:
  • Review workflow definition: .kurt/workflows/{{WORKFLOW_ID}}.yaml
  • Consider workflow retrospectives from completed projects
  • Run: feedback-skill dashboard --workflow {{WORKFLOW_ID}}

{{/each}}
```

---

### Step 10: Suggested Next Steps

```
───────────────────────────────────────────────────────
Recommended Next Steps
───────────────────────────────────────────────────────

{{#if HAS_HIGH_PRIORITY}}
1. Address high-priority issue: "{{TOP_ISSUE}}"
   {{COMMAND}}

2. Review recent feedback for context:
   feedback-skill dashboard --type {{FEEDBACK_TYPE}}

3. After improvement, validate with more content/projects

{{else if HAS_MEDIUM_PRIORITY}}
1. Review medium-priority issues when convenient
2. Continue collecting feedback to identify patterns
3. Monitor issue resolution rates

{{else}}
✓ No immediate action required

Continue providing feedback when prompted to maintain
improvement momentum and identify new patterns.
{{/if}}

{{#if LOW_RESOLUTION_RATE_EXISTS}}
⚠️  Note: Some issues have low resolution rates ({{RATE}}%)
   This may indicate:
   • Issue requires manual intervention
   • Current improvement mapping needs refinement
   • Issue is more complex than anticipated

   Consider manual investigation for these issues.
{{/if}}
```

---

### Step 11: Interactive Options

```
What would you like to do?

{{#each HIGH_PRIORITY_SUGGESTIONS}}
{{INDEX}}. Execute improvement for "{{ISSUE_NAME}}"
{{/each}}
{{NEXT_INDEX}}. View detailed dashboard
{{NEXT_INDEX + 1}}. Exit

Choice: _
```

**Handle choice:**

```bash
read -r CHOICE

case "$CHOICE" in
    [1-9])
        # User selected an issue to address
        SELECTED_ISSUE=$(get_issue_by_index "$CHOICE")
        IFS='|' read -r ISSUE_CATEGORY FEEDBACK_TYPE <<< "$SELECTED_ISSUE"

        echo ""
        echo "Preparing improvement for ${ISSUE_CATEGORY}..."
        echo ""

        # Find most recent feedback event for this issue
        FEEDBACK_ID=$(sqlite3 .kurt/kurt.sqlite "
            SELECT id FROM feedback_events
            WHERE issue_category = '${ISSUE_CATEGORY}'
            AND feedback_type = '${FEEDBACK_TYPE}'
            ORDER BY created_at DESC
            LIMIT 1
        ")

        # Invoke improve subskill
        feedback-skill improve \
            --feedback-id "${FEEDBACK_ID}" \
            --issue-category "${ISSUE_CATEGORY}"
        ;;

    "d"|"D")
        # View dashboard
        feedback-skill dashboard
        ;;

    *)
        echo ""
        echo "Exiting. Run this command anytime to see suggestions:"
        echo "  feedback-skill suggest"
        ;;
esac
```

---

## Helper Functions

### get_issue_name()
```bash
get_issue_name() {
    local issue_category=$1

    case "$issue_category" in
        "wrong_tone_style") echo "Wrong Tone/Style" ;;
        "missing_structure") echo "Missing Structure" ;;
        "missing_info") echo "Missing Information" ;;
        "missing_tasks") echo "Missing Tasks" ;;
        "wrong_timeline") echo "Wrong Timeline" ;;
        "missing_dependencies") echo "Missing Dependencies" ;;
        "unclear_goals") echo "Unclear Goals" ;;
        "phase_not_useful") echo "Phase Not Useful" ;;
        "phase_duration_inaccurate") echo "Phase Duration Inaccurate" ;;
        "phase_tasks_incomplete") echo "Phase Tasks Incomplete" ;;
        "phase_ordering") echo "Phase Ordering" ;;
        "other") echo "Other Issue" ;;
        *) echo "$issue_category" ;;
    esac
}
```

### get_feedback_type_name()
```bash
get_feedback_type_name() {
    local feedback_type=$1

    case "$feedback_type" in
        "content_quality") echo "Content Quality" ;;
        "project_plan") echo "Project Plan" ;;
        "workflow_retrospective") echo "Workflow Retrospective" ;;
        *) echo "$feedback_type" ;;
    esac
}
```

### calculate_estimated_improvement()
```bash
calculate_estimated_improvement() {
    local occurrence_count=$1
    local current_avg_rating=$2

    # Simple heuristic: more occurrences = bigger potential impact
    if [ "$occurrence_count" -ge 10 ]; then
        echo "0.8-1.2"
    elif [ "$occurrence_count" -ge 5 ]; then
        echo "0.5-0.8"
    else
        echo "0.3-0.5"
    fi
}
```

---

## Example Usage

### Default suggestions:
```bash
feedback-skill suggest
```

### Show all priorities:
```bash
feedback-skill suggest --all
```

### Specific time window:
```bash
feedback-skill suggest --days 7
```

### Specific feedback type:
```bash
feedback-skill suggest --type content_quality
```

### Adjust frequency threshold:
```bash
feedback-skill suggest --min-frequency 5
```

---

## Design Notes

- **Pattern-based:** Identifies issues only when they occur multiple times
- **Actionable:** Every suggestion maps to specific improvement action
- **Prioritized:** Shows high-impact issues first
- **Contextual:** Includes examples and affected items
- **Honest:** Shows resolution rates to indicate difficulty
- **Interactive:** Can execute improvements directly from suggestions

---

## Integration with Other Subskills

- **dashboard.md:** Provides link to suggestions when common issues detected
- **improve.md:** Can be invoked directly from suggestions
- **rate.md/review-plan.md/retrospective.md:** Feed data that powers suggestions

---

*This subskill turns accumulated feedback into prioritized, actionable improvement recommendations.*
