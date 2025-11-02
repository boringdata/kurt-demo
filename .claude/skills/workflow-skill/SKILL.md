---
name: workflow
description: Create and manage recurring project workflow patterns
---

# Workflow Skill

**Purpose:** Define and manage recurring project workflows
**Registry:** `.kurt/workflows/workflow-registry.yaml`
**Pattern:** Self-generating configs (like writing-rules-skill)

---

## Overview

This skill helps teams codify their recurring project patterns into reusable workflows. Just as writing-rules-skill lets users define custom rule types, workflow-skill lets users define custom project workflows.

**Operations:**
- **add** - Interactive wizard to create new workflow
- **list** - Show all defined workflows
- **show <name>** - Display workflow details
- **validate <name>** - Check workflow definition
- **execute <name>** - Create project from workflow (alias for `/create-project --workflow <name>`)
- **stats <name>** - Performance metrics
- **optimize <name>** - Update workflow based on learnings

---

## Usage

```bash
# Create new workflow
workflow-skill add

# Create workflow from description
workflow-skill add --from-description "Weekly tutorial publication process"

# List all workflows
workflow-skill list

# Show workflow details
workflow-skill show weekly-tutorial

# Validate workflow
workflow-skill validate weekly-tutorial

# Execute workflow (create project)
workflow-skill execute weekly-tutorial

# View performance stats
workflow-skill stats weekly-tutorial

# Optimize based on past runs
workflow-skill optimize weekly-tutorial
```

---

## Operations

### add - Create New Workflow

Interactive wizard to define a recurring workflow pattern.

**Entry:** `workflow-skill add [--from-description "description"]`

**Workflow:**

1. **Describe workflow** - What recurring work pattern?
2. **Extract phases** - Break down into major steps
3. **Define each phase:**
   - Tasks to complete
   - Expected outputs
   - Duration estimates
   - Dependencies on other phases
   - Required rules
   - Review gates
4. **Test workflow logic** - Validate dependencies, check rules exist
5. **Save to registry** - Store in `.kurt/workflows/workflow-registry.yaml`

**Output:** Workflow definition in registry, ready to use

**Example interaction:**

```
═══════════════════════════════════════════════════════
Create New Workflow
═══════════════════════════════════════════════════════

What type of work do you do repeatedly?

Examples:
  • Product launches
  • Weekly content roundups
  • Documentation updates
  • Event promotions

Describe your workflow:
> We publish technical tutorials weekly

───────────────────────────────────────────────────────

I detected these potential phases:
  1. Topic selection
  2. Outlining
  3. Drafting
  4. Review
  5. Publication

Does this match your workflow? (y/n or describe differently): y

───────────────────────────────────────────────────────
Phase 1: Topic selection
───────────────────────────────────────────────────────

How long does this phase typically take?
> 1 day

What are the main tasks?
> - Review topic requests
  - Select high-value topic
  - Research existing content

What outputs does this phase create?
> - Topic brief
  - Research notes

───────────────────────────────────────────────────────
[Continues for each phase...]
───────────────────────────────────────────────────────

Testing workflow logic...
✓ Phase dependencies valid
✓ Required rules exist
✓ Output paths valid
✓ Timeline estimate: 3-5 days

Save workflow as: _
> weekly-tutorial

✅ Workflow created: weekly-tutorial
   Location: .kurt/workflows/workflow-registry.yaml

To use: /create-project --workflow weekly-tutorial
```

See: `.claude/skills/workflow-skill/subskills/add.md`

---

### list - Show All Workflows

Display all defined workflows with status and usage stats.

**Entry:** `workflow-skill list`

**Output:**

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

Total: 2 workflows, 15 executions
```

See: `.claude/skills/workflow-skill/subskills/list.md`

---

### show - Display Workflow Details

Show comprehensive information about a specific workflow.

**Entry:** `workflow-skill show <workflow-name>`

**Output:**

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

1. topic-selection (1 day)
   Tasks:
     - Review topic requests
     - Select high-value topic
     - Research existing content
   Outputs:
     - research/topic-brief.md

2. outlining (0.5 days)
   Depends on: topic-selection
   Required rules:
     - structure/tutorial
     - personas/backend-developer
   Tasks:
     - content-writing-skill outline <project> <asset>
   Outputs:
     - drafts/<asset>-outline.md

[... more phases ...]

───────────────────────────────────────────────────────
Auto-Generated Artifacts
───────────────────────────────────────────────────────

  • task-breakdown.md
  • timeline.md
  • workflow-tracking.md

───────────────────────────────────────────────────────
Success Criteria
───────────────────────────────────────────────────────

  ✓ Draft created
  ✓ Technical review passed
  ✓ Published to blog

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
```

See: `.claude/skills/workflow-skill/subskills/show.md`

---

### validate - Check Workflow Definition

Validate workflow configuration for errors and inconsistencies.

**Entry:** `workflow-skill validate <workflow-name>`

**Validation checks:**

1. **Phase Dependencies**
   - No circular references
   - All referenced phases exist
   - Dependency order is logical

2. **Required Rules**
   - All referenced rules exist in rules/
   - Rule files are valid
   - No missing rule types

3. **Output Paths**
   - Directory paths are valid
   - No conflicting output locations

4. **Review Workflows**
   - Reviewers are defined
   - Approval thresholds are valid

5. **Timeline Logic**
   - Phase durations are reasonable
   - Parallel phases don't conflict
   - Total duration is calculated correctly

**Output:**

```
═══════════════════════════════════════════════════════
Validation Report: weekly-tutorial
═══════════════════════════════════════════════════════

WORKFLOW DEFINITION
  ✓ Valid YAML structure
  ✓ Required fields present
  ✓ Version: 1.2

PHASE DEPENDENCIES
  ✓ No circular references
  ✓ All dependencies valid
  ✓ 5 phases defined

REQUIRED RULES
  ✓ structure/tutorial exists
  ✓ style/technical exists
  ⚠  personas/backend-developer not found
      Create with: writing-rules-skill persona --audience-type technical

OUTPUT PATHS
  ✓ All paths valid

TIMELINE
  ✓ Total duration: 3-5 days
  ✓ Parallel phases: none
  ✓ Critical path: 5 days

Summary:
  ✓ 0 errors
  ⚠  1 warning

  Overall: Workflow is valid with minor warnings
```

See: `.claude/skills/workflow-skill/subskills/validate.md`

---

### execute - Create Project from Workflow

Create a new project using this workflow template.

**Entry:** `workflow-skill execute <workflow-name>`

**Alias for:** `/create-project --workflow <workflow-name>`

This delegates to the project-management-skill create-project subskill with the workflow flag.

---

### stats - Performance Metrics

Show usage and performance statistics for a workflow.

**Entry:** `workflow-skill stats <workflow-name>`

**Output:**

```
═══════════════════════════════════════════════════════
Performance Stats: weekly-tutorial
═══════════════════════════════════════════════════════

USAGE STATISTICS

Total executions: 12
Success rate: 92% (11 successes, 1 incomplete)
First used: 2025-01-15
Last used: 2025-02-01
Avg time between uses: 6.3 days

TIMING ANALYSIS

Phase                Estimated    Actual Avg   Variance
─────────────────────────────────────────────────────────
topic-selection      1 day        1.1 days     +10%
outlining            0.5 days     0.6 days     +20%
drafting             1-2 days     2.3 days     +15%
review               1-2 days     1.8 days     -10%
publish              0.5 days     0.4 days     -20%
─────────────────────────────────────────────────────────
TOTAL                3-5 days     4.2 days     Within range

BOTTLENECKS

  ⚠  Drafting phase consistently takes longer than estimated
     Recommendation: Update estimate to 2-3 days

  ✓ Review phase improving over time (was 2.5 days, now 1.8 days)

RECOMMENDATIONS

  1. Increase drafting phase estimate (current: 1-2 days → suggested: 2-3 days)
  2. Add buffer for code testing (observed: 3-4 hours)
  3. Consider parallel tasks in drafting phase (writing + screenshots)

Would you like to optimize this workflow based on these learnings? (y/n): _
```

See: `.claude/skills/workflow-skill/subskills/stats.md`

---

### optimize - Update Workflow

Update workflow definition based on past execution learnings.

**Entry:** `workflow-skill optimize <workflow-name>`

**What it does:**

1. Analyze past executions (timing, success rate, feedback)
2. Identify optimization opportunities
3. Suggest updates to workflow definition
4. Apply updates if approved

**Example:**

```
═══════════════════════════════════════════════════════
Optimize Workflow: weekly-tutorial
═══════════════════════════════════════════════════════

Analyzing 12 past executions...

SUGGESTED OPTIMIZATIONS

1. Update Phase Duration: drafting
   Current: 1-2 days
   Suggested: 2-3 days
   Reason: Actual avg is 2.3 days (based on 12 executions)

2. Add Task: code-testing
   Phase: drafting
   Suggested task: "Test all code examples (budget 3-4 hours)"
   Reason: Common pattern across all executions

3. Add Optimization Note: engineering-review
   Phase: review
   Note: "Give engineering team 48hr notice for faster turnaround"
   Reason: Noted in 5/12 project retrospectives

4. Update Success Criterion: code-examples-tested
   Add: "All code examples tested and verified"
   Reason: Missing from 1 failed execution

Apply these optimizations? (y/n/review individually): _
```

See: `.claude/skills/workflow-skill/subskills/optimize.md`

---

## Routing Logic

```bash
# Parse first argument
OPERATION=$1

case "$OPERATION" in
  add)
    invoke: subskills/add.md
    ;;
  list)
    invoke: subskills/list.md
    ;;
  show)
    invoke: subskills/show.md
    ;;
  validate)
    invoke: subskills/validate.md
    ;;
  execute)
    # Alias for /create-project --workflow
    workflow_name=$2
    invoke: /create-project --workflow $workflow_name
    ;;
  stats)
    invoke: subskills/stats.md
    ;;
  optimize)
    invoke: subskills/optimize.md
    ;;
  *)
    echo "Unknown operation: $OPERATION"
    echo "Usage: workflow-skill <operation>"
    echo "Operations: add, list, show, validate, execute, stats, optimize"
    exit 1
    ;;
esac
```

---

## Data Storage

### Workflow Registry

**Location:** `.kurt/workflows/workflow-registry.yaml`

Stores all workflow definitions with:
- Phases and dependencies
- Tasks and outputs
- Required rules
- Review gates
- Success criteria
- Usage statistics
- Optimization notes

### Workflow Executions (Projects)

**Location:** `projects/<project-name>/workflow-tracking.md`

Tracks workflow execution for each project:
- Phase completion status
- Actual vs estimated durations
- Review approvals
- Learnings for optimization

### Templates

**Location:** `.kurt/workflows/templates/_workflow-template.yaml`

Template used when creating new workflows via `add` operation.

---

## Integration Points

**Called by:**
- `/create-project --workflow <name>` - Execute workflow
- `onboarding-skill` - Create first workflow during setup

**Calls:**
- `writing-rules-skill` - Validate required rules exist
- `project-management-skill` - Create project structure

**Uses:**
- Workflow registry for definitions
- Project tracking for execution history
- Templates for new workflow creation

---

## Key Principles

1. **Self-generating** - Users define their own workflows
2. **Adaptive** - Workflows improve based on usage data
3. **Reusable** - Define once, use many times
4. **Optional** - Projects can be created without workflows
5. **Learnings-driven** - Track execution, optimize over time
6. **Validation** - Ensure workflows are valid before use

---

## Example Workflows

### Weekly Tutorial

```yaml
weekly-tutorial:
  name: "Weekly Technical Tutorial"
  frequency: "weekly"
  phases:
    - topic-selection (1 day)
    - outlining (0.5 days)
    - drafting (2-3 days)
    - review (1-2 days)
    - publish (0.5 days)
```

### Product Launch

```yaml
product-launch:
  name: "Product Launch Campaign"
  frequency: "on-demand"
  phases:
    - research (3-5 days)
    - positioning (2-3 days)
    - content-creation (1-2 weeks, parallel)
    - review-approval (3-5 days)
    - launch (1 day)
```

### Quarterly Docs Refresh

```yaml
docs-refresh:
  name: "Quarterly Documentation Refresh"
  frequency: "quarterly"
  phases:
    - audit (2-3 days)
    - prioritization (1 day)
    - updates (1-2 weeks, parallel)
    - technical-review (3-5 days)
    - publication (1 day)
```

---

*This skill enables teams to codify their recurring project patterns into reusable workflows, similar to how writing-rules-skill enables custom rule types.*
