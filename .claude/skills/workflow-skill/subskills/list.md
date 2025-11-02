# List Workflows Subskill

**Purpose:** Display all defined workflows with status and usage stats
**Parent Skill:** workflow-skill
**Operation:** Read
**Output:** Formatted list of workflows

---

## Overview

This subskill reads the workflow registry and displays all workflows with their key information and statistics.

---

## Step 1: Load Workflow Registry

```bash
REGISTRY=".kurt/workflows/workflow-registry.yaml"

# Check if registry exists
if [ ! -f "$REGISTRY" ]; then
  echo "⚠️  No workflows defined yet"
  echo ""
  echo "Create your first workflow with:"
  echo "  workflow-skill add"
  exit 0
fi

# Get total workflow count
TOTAL_WORKFLOWS=$(yq '.metadata.stats.total_workflows // 0' "$REGISTRY")

if [ "$TOTAL_WORKFLOWS" -eq 0 ]; then
  echo "═══════════════════════════════════════════════════════"
  echo "No Workflows Defined"
  echo "═══════════════════════════════════════════════════════"
  echo ""
  echo "Create your first workflow with:"
  echo "  workflow-skill add"
  echo ""
  echo "Example workflows:"
  echo "  • Weekly tutorial publication"
  echo "  • Product launch campaigns"
  echo "  • Quarterly docs refresh"
  exit 0
fi
```

---

## Step 2: Display Workflows

```
═══════════════════════════════════════════════════════
Defined Workflows
═══════════════════════════════════════════════════════

ACTIVE WORKFLOWS ({{TOTAL_WORKFLOWS}})
```

```bash
# Get all workflow IDs
WORKFLOW_IDS=$(yq '.workflows | keys | .[]' "$REGISTRY")

# For each workflow
while IFS= read -r workflow_id; do
  # Get workflow details
  NAME=$(yq ".workflows.${workflow_id}.name" "$REGISTRY")
  DESCRIPTION=$(yq ".workflows.${workflow_id}.description" "$REGISTRY")
  FREQUENCY=$(yq ".workflows.${workflow_id}.frequency" "$REGISTRY")
  PHASES=$(yq ".workflows.${workflow_id}.phases | length" "$REGISTRY")
  AVG_DURATION=$(yq ".workflows.${workflow_id}.avg_duration" "$REGISTRY")
  TIMES_EXECUTED=$(yq ".workflows.${workflow_id}.times_executed // 0" "$REGISTRY")
  SUCCESS_RATE=$(yq ".workflows.${workflow_id}.success_rate // 0" "$REGISTRY")
  LAST_USED=$(yq ".workflows.${workflow_id}.last_used // \"Never\"" "$REGISTRY")

  # Format success rate as percentage
  SUCCESS_PCT=$(echo "scale=0; $SUCCESS_RATE * 100" | bc)

  # Display workflow
  echo ""
  echo "  ✓ $workflow_id - $NAME"
  echo "    Frequency: $FREQUENCY"
  echo "    Phases: $PHASES"
  echo "    Avg duration: $AVG_DURATION"
  echo "    Executed: $TIMES_EXECUTED times"

  if [ "$TIMES_EXECUTED" -gt 0 ]; then
    echo "    Success rate: ${SUCCESS_PCT}%"
    echo "    Last used: $LAST_USED"
  fi

done <<< "$WORKFLOW_IDS"
```

```
───────────────────────────────────────────────────────

Total: {{TOTAL_WORKFLOWS}} workflow(s), {{TOTAL_EXECUTIONS}} execution(s)

Commands:
  workflow-skill show <name>       View workflow details
  workflow-skill execute <name>    Create project with workflow
  workflow-skill add               Create new workflow

───────────────────────────────────────────────────────
```

---

## Step 3: Optional Filtering

**If `--frequency` flag provided:**

```bash
FREQUENCY_FILTER="$1"

if [ -n "$FREQUENCY_FILTER" ]; then
  echo "Filtering by frequency: $FREQUENCY_FILTER"
  echo ""

  # Filter workflows
  FILTERED=$(yq ".workflows | to_entries | .[] | select(.value.frequency == \"$FREQUENCY_FILTER\") | .key" "$REGISTRY")

  if [ -z "$FILTERED" ]; then
    echo "No workflows with frequency: $FREQUENCY_FILTER"
    exit 0
  fi

  # Display filtered workflows
  # (same display logic as above, but only for filtered IDs)
fi
```

**Supported frequency filters:**
- `weekly`
- `monthly`
- `quarterly`
- `on-demand`

---

## Example Output

```
═══════════════════════════════════════════════════════
Defined Workflows
═══════════════════════════════════════════════════════

ACTIVE WORKFLOWS (2)

  ✓ weekly-tutorial - Weekly Technical Tutorial
    Frequency: weekly
    Phases: 5
    Avg duration: 3-5 days
    Executed: 12 times
    Success rate: 92%
    Last used: 2025-02-01

  ✓ product-launch - Product Launch Campaign
    Frequency: on-demand
    Phases: 5
    Avg duration: 3-4 weeks
    Executed: 3 times
    Success rate: 100%
    Last used: 2025-01-28

───────────────────────────────────────────────────────

Total: 2 workflows, 15 executions

Commands:
  workflow-skill show <name>       View workflow details
  workflow-skill execute <name>    Create project with workflow
  workflow-skill add               Create new workflow

───────────────────────────────────────────────────────
```

---

## Error Handling

**If yq not available:**
```
❌ Error: yq command not found

yq is required for reading workflow registry.

Install with:
  brew install yq          # macOS
  sudo apt install yq      # Ubuntu
  pip install yq           # Python
```

**If registry is malformed:**
```
❌ Error: Workflow registry is malformed

File: .kurt/workflows/workflow-registry.yaml

Please check YAML syntax:
  yq eval .kurt/workflows/workflow-registry.yaml
```

---

*This subskill provides a quick overview of all defined workflows.*
