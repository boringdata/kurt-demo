# Dashboard Subskill

**Purpose:** Show feedback summary and improvement effectiveness
**Parent Skill:** feedback-skill
**Operation:** View feedback metrics, trends, and improvement results

---

## Context Received from Parent Skill

- `$TYPE_FILTER` - Optional filter (content_quality | project_plan | workflow_retrospective)
- `$WORKFLOW_FILTER` - Optional workflow ID filter
- `$DAYS` - Optional time window (default: 30 days)

---

## Workflow

### Step 1: Parse Arguments

```bash
# Default values
TYPE_FILTER=""
WORKFLOW_FILTER=""
DAYS=30

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --type)
            TYPE_FILTER="$2"
            shift 2
            ;;
        --workflow)
            WORKFLOW_FILTER="$2"
            shift 2
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
```

---

### Step 2: Display Header

```
═══════════════════════════════════════════════════════
Feedback Dashboard
═══════════════════════════════════════════════════════

Time period: Last ${DAYS} days
{{#if TYPE_FILTER}}Filter: ${TYPE_FILTER}{{/if}}
{{#if WORKFLOW_FILTER}}Workflow: ${WORKFLOW_FILTER}{{/if}}

Generated: $(date +"%Y-%m-%d %H:%M")
```

---

### Step 3: Feedback Summary

```bash
# Query feedback counts by type
FEEDBACK_STATS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    feedback_type,
    COUNT(*) as count,
    AVG(rating) as avg_rating,
    SUM(CASE WHEN issue_identified = 1 THEN 1 ELSE 0 END) as issues_identified,
    SUM(CASE WHEN prompted = 1 THEN 1 ELSE 0 END) as prompted_count,
    SUM(CASE WHEN prompted = 0 THEN 1 ELSE 0 END) as explicit_count
FROM feedback_events
WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
$([ -n "$TYPE_FILTER" ] && echo "AND feedback_type = '${TYPE_FILTER}'")
GROUP BY feedback_type
ORDER BY feedback_type;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Feedback Summary
───────────────────────────────────────────────────────

{{#each FEEDBACK_TYPES}}
{{TYPE_NAME}}:
  Submissions: {{COUNT}}
  Average rating: {{AVG_RATING}}/5.0 {{RATING_ICON}}
  Issues identified: {{ISSUES_IDENTIFIED}} ({{ISSUE_RATE}}%)
  Prompted: {{PROMPTED_COUNT}} | Explicit: {{EXPLICIT_COUNT}}
{{/each}}

{{#if NO_FEEDBACK}}
No feedback collected in the last ${DAYS} days.

Get started:
  • Create content: content-writing-skill draft
  • Create project: /create-project
  • Complete project: Mark project as complete for retrospective
{{/if}}
```

**Rating icons:**
- 4.5-5.0: "⭐⭐⭐"
- 4.0-4.4: "⭐⭐"
- 3.5-3.9: "⭐"
- 3.0-3.4: "~"
- < 3.0: "⚠️"

---

### Step 4: Recent Feedback

```bash
# Query recent feedback
RECENT_FEEDBACK=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    substr(created_at, 1, 10) as date,
    feedback_type,
    rating,
    issue_category,
    COALESCE(project_id, 'N/A') as project,
    COALESCE(workflow_id, 'N/A') as workflow
FROM feedback_events
WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
$([ -n "$TYPE_FILTER" ] && echo "AND feedback_type = '${TYPE_FILTER}'")
$([ -n "$WORKFLOW_FILTER" ] && echo "AND workflow_id = '${WORKFLOW_FILTER}'")
ORDER BY created_at DESC
LIMIT 10;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Recent Feedback
───────────────────────────────────────────────────────

{{#each FEEDBACK}}
{{DATE}} | {{TYPE}} | Rating: {{RATING}}/5
  {{#if ISSUE}}Issue: {{ISSUE_CATEGORY}}{{/if}}
  {{#if PROJECT}}Project: {{PROJECT}}{{/if}}
  {{#if WORKFLOW}}Workflow: {{WORKFLOW}}{{/if}}
{{/each}}

{{#if MORE_THAN_10}}
... and {{ADDITIONAL_COUNT}} more

View all: sqlite3 .kurt/kurt.sqlite "SELECT * FROM feedback_events"
{{/if}}
```

---

### Step 5: Improvement Summary

```bash
# Query improvement stats
IMPROVEMENT_STATS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    improvement_type,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'suggested' THEN 1 ELSE 0 END) as suggested,
    SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected,
    SUM(CASE WHEN status = 'executed' THEN 1 ELSE 0 END) as executed,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
    SUM(CASE WHEN issue_resolved = 1 THEN 1 ELSE 0 END) as resolved,
    AVG(duration_ms) as avg_duration
FROM improvements i
JOIN feedback_events f ON i.feedback_event_id = f.id
WHERE datetime(i.created_at) > datetime('now', '-${DAYS} days')
$([ -n "$TYPE_FILTER" ] && echo "AND f.feedback_type = '${TYPE_FILTER}'")
GROUP BY improvement_type;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Improvement Activity
───────────────────────────────────────────────────────

{{#each IMPROVEMENT_TYPES}}
{{TYPE_NAME}}:
  Total suggested: {{TOTAL}}
  Accepted: {{ACCEPTED}} ({{ACCEPTANCE_RATE}}%)
  Executed: {{EXECUTED}} ({{SUCCESS_RATE}}% success)
  Issues resolved: {{RESOLVED}} ({{RESOLUTION_RATE}}%)
  {{#if AVG_DURATION}}Avg execution time: {{AVG_DURATION}}ms{{/if}}
{{/each}}

Overall:
  Acceptance rate: {{OVERALL_ACCEPTANCE}}%
  Execution success: {{OVERALL_SUCCESS}}%
  Issue resolution: {{OVERALL_RESOLUTION}}%

{{#if NO_IMPROVEMENTS}}
No improvements suggested yet.

Improvements are triggered when:
  • Content rated ≤ 3/5
  • Project plan rated ≤ 3/5
  • Workflow phase rated ≤ 3/5
{{/if}}
```

---

### Step 6: Recent Improvements

```bash
# Query recent improvements with details
RECENT_IMPROVEMENTS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    substr(i.created_at, 1, 10) as date,
    i.improvement_type,
    i.status,
    f.issue_category,
    i.target_path,
    i.issue_resolved,
    i.validation_rating
FROM improvements i
JOIN feedback_events f ON i.feedback_event_id = f.id
WHERE datetime(i.created_at) > datetime('now', '-${DAYS} days')
$([ -n "$TYPE_FILTER" ] && echo "AND f.feedback_type = '${TYPE_FILTER}'")
ORDER BY i.created_at DESC
LIMIT 10;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Recent Improvements
───────────────────────────────────────────────────────

{{#each IMPROVEMENTS}}
{{DATE}} | {{STATUS_ICON}} {{IMPROVEMENT_TYPE}}
  Issue: {{ISSUE_CATEGORY}}
  Target: {{TARGET_PATH}}
  Status: {{STATUS}}
  {{#if VALIDATED}}
  Validation: {{#if ISSUE_RESOLVED}}✓ Resolved{{else}}⚠ Not resolved{{/if}} ({{VALIDATION_RATING}}/5)
  {{/if}}
{{/each}}

Status icons:
  ✓ executed   ~ suggested   ✗ failed   - rejected
```

---

### Step 7: Feedback Loop Health

```bash
# Query feedback loop completion stats
LOOP_STATS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    COUNT(*) as total_loops,
    SUM(CASE WHEN validation_completed_at IS NOT NULL THEN 1 ELSE 0 END) as completed,
    AVG(CASE WHEN validation_completed_at IS NOT NULL THEN loop_duration_days ELSE NULL END) as avg_duration,
    SUM(CASE WHEN issue_resolved = 1 THEN 1 ELSE 0 END) as resolved,
    AVG(CASE WHEN validation_completed_at IS NOT NULL THEN rating_change ELSE NULL END) as avg_rating_change
FROM feedback_loops
WHERE datetime(created_at) > datetime('now', '-${DAYS} days');
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Feedback Loop Health
───────────────────────────────────────────────────────

Total loops started: {{TOTAL_LOOPS}}
Completed (validated): {{COMPLETED}} ({{COMPLETION_RATE}}%)
Average loop duration: {{AVG_DURATION}} days

Outcomes:
  Issues resolved: {{RESOLVED}} ({{RESOLUTION_RATE}}%)
  Average rating change: {{#if POSITIVE}}+{{/if}}{{AVG_RATING_CHANGE}}/5

{{#if LOW_COMPLETION_RATE}}
⚠️  Low completion rate ({{COMPLETION_RATE}}%)

Tips to improve:
  • Create more content to validate improvements
  • Start new projects to test workflow changes
  • Provide explicit feedback when prompted
{{/if}}

{{#if HIGH_RESOLUTION_RATE}}
✓ Great! {{RESOLUTION_RATE}}% of issues are being resolved.
{{/if}}
```

---

### Step 8: Issue Breakdown

```bash
# Query most common issues
ISSUE_BREAKDOWN=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    issue_category,
    COUNT(*) as count,
    AVG(rating) as avg_rating,
    SUM(CASE WHEN EXISTS (
        SELECT 1 FROM improvements i
        WHERE i.feedback_event_id = f.id
        AND i.issue_resolved = 1
    ) THEN 1 ELSE 0 END) as resolved_count
FROM feedback_events f
WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
AND issue_identified = 1
$([ -n "$TYPE_FILTER" ] && echo "AND feedback_type = '${TYPE_FILTER}'")
GROUP BY issue_category
ORDER BY count DESC;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Issue Breakdown
───────────────────────────────────────────────────────

{{#each ISSUES}}
{{ISSUE_CATEGORY}} ({{COUNT}}×)
  Avg rating when reported: {{AVG_RATING}}/5
  Resolution rate: {{RESOLUTION_RATE}}%
  {{#if LOW_RESOLUTION}}⚠️  Difficult to resolve{{/if}}
{{/each}}

{{#if NO_ISSUES}}
✓ No issues identified in last ${DAYS} days!
{{/if}}
```

---

### Step 9: Rating Trends

```bash
# Query rating trends by feedback type
RATING_TRENDS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    feedback_type,
    strftime('%Y-%W', created_at) as week,
    AVG(rating) as avg_rating,
    COUNT(*) as count
FROM feedback_events
WHERE datetime(created_at) > datetime('now', '-${DAYS} days')
$([ -n "$TYPE_FILTER" ] && echo "AND feedback_type = '${TYPE_FILTER}'")
GROUP BY feedback_type, week
ORDER BY feedback_type, week;
EOF
)

# Calculate trend direction
TREND_DIRECTION=$(calculate_trend "$RATING_TRENDS")
```

**Display:**

```
───────────────────────────────────────────────────────
Rating Trends
───────────────────────────────────────────────────────

{{#each FEEDBACK_TYPES}}
{{TYPE_NAME}}:
  Current average: {{CURRENT_AVG}}/5
  Previous period: {{PREVIOUS_AVG}}/5
  Trend: {{TREND_ICON}} {{TREND_DIRECTION}} ({{TREND_CHANGE}})
{{/each}}

Trend icons:
  ↑ Improving  → Stable  ↓ Declining

{{#if OVERALL_IMPROVING}}
✓ Overall trend is improving! Keep it up.
{{else if OVERALL_DECLINING}}
⚠️  Ratings are declining. Review recent changes or check for new issues.
{{else}}
→ Ratings are stable.
{{/if}}
```

---

### Step 10: Workflow Performance (if applicable)

**If workflow filter or workflow retrospectives exist:**

```bash
# Query workflow-specific metrics
WORKFLOW_METRICS=$(sqlite3 .kurt/kurt.sqlite <<EOF
SELECT
    wr.workflow_id,
    COUNT(DISTINCT wr.id) as retrospective_count,
    AVG(wr.overall_rating) as avg_overall,
    AVG(wpr.usefulness_rating) as avg_phase_rating,
    SUM(CASE WHEN wpr.duration_accurate = 0 THEN 1 ELSE 0 END) as duration_issues,
    SUM(CASE WHEN wpr.tasks_complete = 0 THEN 1 ELSE 0 END) as task_issues
FROM workflow_retrospectives wr
LEFT JOIN workflow_phase_ratings wpr ON wr.id = wpr.retrospective_id
WHERE datetime(wr.created_at) > datetime('now', '-${DAYS} days')
$([ -n "$WORKFLOW_FILTER" ] && echo "AND wr.workflow_id = '${WORKFLOW_FILTER}'")
GROUP BY wr.workflow_id
ORDER BY retrospective_count DESC;
EOF
)
```

**Display:**

```
───────────────────────────────────────────────────────
Workflow Performance
───────────────────────────────────────────────────────

{{#each WORKFLOWS}}
{{WORKFLOW_ID}}:
  Retrospectives: {{RETROSPECTIVE_COUNT}}
  Avg overall rating: {{AVG_OVERALL}}/5 {{RATING_ICON}}
  Avg phase rating: {{AVG_PHASE_RATING}}/5
  Duration issues: {{DURATION_ISSUES}}
  Task issues: {{TASK_ISSUES}}
{{/each}}

{{#if NO_RETROSPECTIVES}}
No workflow retrospectives yet.

Complete a project to provide workflow feedback:
  1. Mark project complete
  2. Provide retrospective feedback
  3. Review workflow effectiveness
{{/if}}
```

---

### Step 11: Suggested Actions

```bash
# Analyze current state and suggest actions
SUGGESTED_ACTIONS=()

# Check for unvalidated improvements
UNVALIDATED_COUNT=$(sqlite3 .kurt/kurt.sqlite "
    SELECT COUNT(*) FROM feedback_loops
    WHERE validation_completed_at IS NULL
    AND datetime(improvement_executed_at) < datetime('now', '-7 days')
")

if [ "$UNVALIDATED_COUNT" -gt 0 ]; then
    SUGGESTED_ACTIONS+=("Validate $UNVALIDATED_COUNT improvements by creating more content")
fi

# Check for common unresolved issues
COMMON_ISSUES=$(sqlite3 .kurt/kurt.sqlite "
    SELECT issue_category FROM feedback_events
    WHERE datetime(created_at) > datetime('now', '-30 days')
    AND issue_identified = 1
    GROUP BY issue_category
    HAVING COUNT(*) >= 3
")

if [ -n "$COMMON_ISSUES" ]; then
    SUGGESTED_ACTIONS+=("Review common issues: $COMMON_ISSUES")
    SUGGESTED_ACTIONS+=("Run: feedback-skill suggest")
fi

# Check for low-rated workflows
LOW_RATED_WORKFLOWS=$(sqlite3 .kurt/kurt.sqlite "
    SELECT workflow_id FROM workflow_retrospectives
    WHERE datetime(created_at) > datetime('now', '-30 days')
    GROUP BY workflow_id
    HAVING AVG(overall_rating) < 3.5
")

if [ -n "$LOW_RATED_WORKFLOWS" ]; then
    SUGGESTED_ACTIONS+=("Review low-rated workflows: $LOW_RATED_WORKFLOWS")
fi
```

**Display:**

```
───────────────────────────────────────────────────────
Suggested Actions
───────────────────────────────────────────────────────

{{#each ACTIONS}}
{{INDEX}}. {{ACTION}}
{{/each}}

{{#if NO_ACTIONS}}
✓ No immediate actions needed.

Everything looks good! Continue using the system and provide
feedback when prompted to maintain improvement momentum.
{{/if}}
```

---

### Step 12: Footer and Options

```
───────────────────────────────────────────────────────

View options:
  • feedback-skill dashboard --type content_quality
  • feedback-skill dashboard --type project_plan
  • feedback-skill dashboard --type workflow_retrospective
  • feedback-skill dashboard --workflow <id>
  • feedback-skill dashboard --days 7

Other commands:
  • feedback-skill suggest       - View improvement suggestions
  • feedback-skill rate           - Rate content explicitly
  • feedback-skill retrospective  - Review completed workflow

Data location: .kurt/kurt.sqlite
```

---

## Helper Functions

### calculate_trend()
```bash
calculate_trend() {
    local trend_data=$1

    # Split into current and previous period
    local total_lines=$(echo "$trend_data" | wc -l)
    local midpoint=$((total_lines / 2))

    local previous_avg=$(echo "$trend_data" | head -n $midpoint | awk -F'|' '{sum+=$3; count++} END {print sum/count}')
    local current_avg=$(echo "$trend_data" | tail -n $midpoint | awk -F'|' '{sum+=$3; count++} END {print sum/count}')

    local diff=$(echo "$current_avg - $previous_avg" | bc -l)

    if (( $(echo "$diff > 0.3" | bc -l) )); then
        echo "improving|↑|$diff"
    elif (( $(echo "$diff < -0.3" | bc -l) )); then
        echo "declining|↓|$diff"
    else
        echo "stable|→|$diff"
    fi
}
```

### get_rating_icon()
```bash
get_rating_icon() {
    local rating=$1

    if (( $(echo "$rating >= 4.5" | bc -l) )); then
        echo "⭐⭐⭐"
    elif (( $(echo "$rating >= 4.0" | bc -l) )); then
        echo "⭐⭐"
    elif (( $(echo "$rating >= 3.5" | bc -l) )); then
        echo "⭐"
    elif (( $(echo "$rating >= 3.0" | bc -l) )); then
        echo "~"
    else
        echo "⚠️"
    fi
}
```

### get_status_icon()
```bash
get_status_icon() {
    local status=$1

    case "$status" in
        "executed") echo "✓" ;;
        "suggested") echo "~" ;;
        "accepted") echo "→" ;;
        "failed") echo "✗" ;;
        "rejected") echo "-" ;;
        *) echo "?" ;;
    esac
}
```

---

## Example Usage

### Overall dashboard:
```bash
feedback-skill dashboard
```

### Content quality only:
```bash
feedback-skill dashboard --type content_quality
```

### Specific workflow:
```bash
feedback-skill dashboard --workflow weekly-tutorial
```

### Last 7 days:
```bash
feedback-skill dashboard --days 7
```

### Combined filters:
```bash
feedback-skill dashboard --type workflow_retrospective --days 14
```

---

## Design Notes

- **Data-driven:** All metrics from explicit user feedback (no implicit signals)
- **Actionable:** Suggests specific next steps based on current state
- **Filterable:** Can focus on specific feedback types or workflows
- **Comprehensive:** Shows full picture from feedback → improvement → validation
- **Honest:** Shows both successes and failures, resolution rates

---

*This dashboard provides complete visibility into the feedback system's effectiveness and health.*
