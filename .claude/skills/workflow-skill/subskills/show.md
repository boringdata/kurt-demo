# Show Workflow Subskill

**Purpose:** Display detailed information about a specific workflow
**Parent Skill:** workflow-skill
**Operation:** Read
**Output:** Comprehensive workflow details

---

## Overview

This subskill displays complete information about a workflow including phases, tasks, rules, success criteria, and usage statistics.

---

## Step 1: Parse Arguments

```bash
WORKFLOW_ID="$1"

if [ -z "$WORKFLOW_ID" ]; then
  echo "Error: Workflow name required"
  echo ""
  echo "Usage: workflow-skill show <workflow-name>"
  echo ""
  echo "Available workflows:"
  yq '.workflows | keys | .[]' .kurt/workflows/workflow-registry.yaml
  exit 1
fi
```

---

## Step 2: Load Workflow Definition

```bash
REGISTRY=".kurt/workflows/workflow-registry.yaml"

# Check if workflow exists
WORKFLOW_EXISTS=$(yq ".workflows | has(\"$WORKFLOW_ID\")" "$REGISTRY")

if [ "$WORKFLOW_EXISTS" != "true" ]; then
  echo "❌ Workflow not found: $WORKFLOW_ID"
  echo ""
  echo "Available workflows:"
  yq '.workflows | keys | .[]' "$REGISTRY"
  echo ""
  echo "Create new workflow with:"
  echo "  workflow-skill add"
  exit 1
fi

# Load workflow data
WORKFLOW_DATA=$(yq ".workflows.$WORKFLOW_ID" "$REGISTRY")
```

---

## Step 3: Extract Workflow Details

```bash
# Basic info
NAME=$(echo "$WORKFLOW_DATA" | yq '.name')
VERSION=$(echo "$WORKFLOW_DATA" | yq '.version')
DESCRIPTION=$(echo "$WORKFLOW_DATA" | yq '.description')
FREQUENCY=$(echo "$WORKFLOW_DATA" | yq '.frequency')
AVG_DURATION=$(echo "$WORKFLOW_DATA" | yq '.avg_duration')
CREATED=$(echo "$WORKFLOW_DATA" | yq '.created')
LAST_USED=$(echo "$WORKFLOW_DATA" | yq '.last_used // "Never"')

# Statistics
TIMES_EXECUTED=$(echo "$WORKFLOW_DATA" | yq '.times_executed // 0')
SUCCESS_RATE=$(echo "$WORKFLOW_DATA" | yq '.success_rate // 0')

# Calculate success percentage
if [ "$TIMES_EXECUTED" -gt 0 ]; then
  SUCCESS_PCT=$(echo "scale=0; $SUCCESS_RATE * 100" | bc)
  SUCCESSES=$(echo "scale=0; $TIMES_EXECUTED * $SUCCESS_RATE" | bc)
  SUCCESSES=$(printf "%.0f" "$SUCCESSES")
else
  SUCCESS_PCT=0
  SUCCESSES=0
fi

# Phases
PHASE_COUNT=$(echo "$WORKFLOW_DATA" | yq '.phases | length')
```

---

## Step 4: Display Workflow Overview

```
═══════════════════════════════════════════════════════
Workflow: {{WORKFLOW_ID}}
═══════════════════════════════════════════════════════

Name: {{NAME}}
Version: {{VERSION}}
Description: {{DESCRIPTION}}

Frequency: {{FREQUENCY}}
Avg Duration: {{AVG_DURATION}}
Created: {{CREATED}}
{{#if LAST_USED != "Never"}}Last used: {{LAST_USED}}{{/if}}

{{#if TIMES_EXECUTED > 0}}
Usage Stats:
  Times executed: {{TIMES_EXECUTED}}
  Success rate: {{SUCCESS_PCT}}% ({{SUCCESSES}}/{{TIMES_EXECUTED}})
{{#if AVG_ACTUAL_DURATION}}  Avg actual duration: {{AVG_ACTUAL_DURATION}}{{/if}}
{{/if}}
```

---

## Step 5: Display Phases

```
───────────────────────────────────────────────────────
Phases ({{PHASE_COUNT}})
───────────────────────────────────────────────────────
```

```bash
# Get phases
PHASES=$(echo "$WORKFLOW_DATA" | yq '.phases[]')

# For each phase
PHASE_NUM=1
echo "$WORKFLOW_DATA" | yq -r '.phases[] | @json' | while read -r phase_json; do
  # Extract phase details
  PHASE_ID=$(echo "$phase_json" | jq -r '.id')
  PHASE_NAME=$(echo "$phase_json" | jq -r '.name')
  DURATION=$(echo "$phase_json" | jq -r '.duration // "Not specified"')
  PARALLEL=$(echo "$phase_json" | jq -r '.parallel // false')

  echo ""
  echo "$PHASE_NUM. $PHASE_NAME ($DURATION)"

  # Dependencies
  DEPS=$(echo "$phase_json" | jq -r '.depends_on[]?' 2>/dev/null)
  if [ -n "$DEPS" ]; then
    echo "   Depends on: $(echo "$DEPS" | tr '\n' ', ' | sed 's/,$//')"
  fi

  # Parallel flag
  if [ "$PARALLEL" = "true" ]; then
    echo "   Tasks can run in parallel: yes"
  fi

  # Tasks
  TASKS=$(echo "$phase_json" | jq -r '.tasks[]?' 2>/dev/null)
  if [ -n "$TASKS" ]; then
    echo "   Tasks:"
    while IFS= read -r task; do
      echo "     - $task"
    done <<< "$TASKS"
  fi

  # Outputs
  OUTPUTS=$(echo "$phase_json" | jq -r '.outputs[]?' 2>/dev/null)
  if [ -n "$OUTPUTS" ]; then
    echo "   Outputs:"
    while IFS= read -r output; do
      echo "     - $output"
    done <<< "$OUTPUTS"
  fi

  # Required rules
  RULES=$(echo "$phase_json" | jq -r '.required_rules[]?' 2>/dev/null)
  if [ -n "$RULES" ]; then
    echo "   Required rules:"
    while IFS= read -r rule; do
      # Check if rule exists
      if [ -f "rules/$rule" ]; then
        echo "     ✓ $rule"
      else
        echo "     ✗ $rule (not found)"
      fi
    done <<< "$RULES"
  fi

  # Review workflow
  REVIEWERS=$(echo "$phase_json" | jq -r '.review_workflow.reviewers[]?' 2>/dev/null)
  if [ -n "$REVIEWERS" ]; then
    APPROVAL_REQUIRED=$(echo "$phase_json" | jq -r '.review_workflow.approval_required // false')
    echo "   Review:"
    echo "     Reviewers: $(echo "$REVIEWERS" | tr '\n' ', ' | sed 's/,$//')"
    echo "     Approval required: $APPROVAL_REQUIRED"
  fi

  PHASE_NUM=$((PHASE_NUM + 1))
done
```

---

## Step 6: Display Auto-Generated Artifacts

```bash
GENERATES=$(echo "$WORKFLOW_DATA" | yq '.generates[]?')

if [ -n "$GENERATES" ]; then
  echo ""
  echo "───────────────────────────────────────────────────────"
  echo "Auto-Generated Artifacts"
  echo "───────────────────────────────────────────────────────"
  echo ""
  while IFS= read -r artifact; do
    echo "  • $artifact"
  done <<< "$GENERATES"
fi
```

---

## Step 7: Display Success Criteria

```bash
SUCCESS_CRITERIA=$(echo "$WORKFLOW_DATA" | yq -r '.success_criteria | to_entries | .[] | "- " + .value')

if [ -n "$SUCCESS_CRITERIA" ]; then
  echo ""
  echo "───────────────────────────────────────────────────────"
  echo "Success Criteria"
  echo "───────────────────────────────────────────────────────"
  echo ""
  while IFS= read -r criterion; do
    echo "  $criterion"
  done <<< "$SUCCESS_CRITERIA"
fi
```

---

## Step 8: Display Optimization Notes

```bash
OPT_NOTES=$(echo "$WORKFLOW_DATA" | yq '.optimization_notes[]?')

if [ -n "$OPT_NOTES" ]; then
  echo ""
  echo "───────────────────────────────────────────────────────"
  echo "Optimization Notes"
  echo "───────────────────────────────────────────────────────"
  echo ""
  while IFS= read -r note; do
    echo "  • $note"
  done <<< "$OPT_NOTES"
fi
```

---

## Step 9: Usage Instructions

```
───────────────────────────────────────────────────────
Usage
───────────────────────────────────────────────────────

Create project with this workflow:
  /create-project --workflow {{WORKFLOW_ID}}

OR

  workflow-skill execute {{WORKFLOW_ID}}

───────────────────────────────────────────────────────
```

---

## Example Output

```
═══════════════════════════════════════════════════════
Workflow: weekly-tutorial
═══════════════════════════════════════════════════════

Name: Weekly Technical Tutorial
Version: 1.2
Description: Weekly tutorial publication workflow

Frequency: weekly
Avg Duration: 3-5 days
Created: 2025-01-15
Last used: 2025-02-01

Usage Stats:
  Times executed: 12
  Success rate: 92% (11/12)
  Avg actual duration: 4.2 days

───────────────────────────────────────────────────────
Phases (5)
───────────────────────────────────────────────────────

1. Topic Selection (1 day)
   Tasks:
     - Review topic requests
     - Select high-value topic
     - Research existing content
   Outputs:
     - research/topic-brief.md

2. Outlining (0.5 days)
   Depends on: topic-selection
   Required rules:
     ✓ structure/tutorial
     ✓ personas/backend-developer
   Tasks:
     - content-writing-skill outline <project> <asset>
   Outputs:
     - drafts/<asset>-outline.md

3. Drafting (2-3 days)
   Depends on: outlining
   Required rules:
     ✓ style/technical
     ✓ structure/tutorial
   Tasks:
     - content-writing-skill draft <project> <asset>
     - Test all code examples
     - Create screenshots
   Outputs:
     - drafts/<asset>-draft.md

4. Review (1-2 days)
   Depends on: drafting
   Review:
     Reviewers: engineering-team
     Approval required: true
   Tasks:
     - Technical accuracy review
     - Code verification
   Outputs:
     - reviews/technical-feedback.md

5. Publish (0.5 days)
   Depends on: review
   Tasks:
     - Publish to blog
     - Share on social
     - Track analytics

───────────────────────────────────────────────────────
Auto-Generated Artifacts
───────────────────────────────────────────────────────

  • task-breakdown.md
  • timeline.md
  • workflow-tracking.md

───────────────────────────────────────────────────────
Success Criteria
───────────────────────────────────────────────────────

  - Draft created
  - Technical review passed
  - Published to blog
  - All code examples tested

───────────────────────────────────────────────────────
Optimization Notes
───────────────────────────────────────────────────────

  • Code testing takes 3-4 hours (budget accordingly)
  • Engineering review faster with 48hr notice
  • Screenshots should be created during drafting phase

───────────────────────────────────────────────────────
Usage
───────────────────────────────────────────────────────

Create project with this workflow:
  /create-project --workflow weekly-tutorial

OR

  workflow-skill execute weekly-tutorial

───────────────────────────────────────────────────────
```

---

## Error Handling

**If workflow doesn't exist:**
```
❌ Workflow not found: {{WORKFLOW_ID}}

Available workflows:
  - weekly-tutorial
  - product-launch

Create new workflow with:
  workflow-skill add
```

**If registry is malformed:**
```
❌ Error: Cannot read workflow definition

The registry may be corrupted. Check:
  .kurt/workflows/workflow-registry.yaml

Validate YAML syntax:
  yq eval .kurt/workflows/workflow-registry.yaml
```

---

*This subskill provides comprehensive details about a specific workflow.*
