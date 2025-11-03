---
name: feedback
description: Collect user feedback and execute improvements to rules, workflows, and configurations
---

# Feedback Skill

## Overview

Enables continuous improvement through explicit user feedback on concrete outputs. The system:
- Collects ratings on content artifacts, project plans, and workflows
- Identifies specific issues that can be addressed
- Suggests and executes targeted improvements
- Tracks improvement effectiveness over time

**Philosophy:** Output-driven feedback with clear improvement paths

---

## Three Feedback Loops

### Loop 1: Content Quality → Rules/Prompts
- **Trigger:** After creating outlines or drafts (every 5th + explicit)
- **Rating:** User rates content quality (1-5)
- **Issues:** Tone, structure, information gaps
- **Improvements:** Update style rules, structure patterns, extract examples
- **Validation:** Next content creation with updated rules

### Loop 2: Project Plan Quality → Workflow Definition
- **Trigger:** After project creation with workflow
- **Rating:** User rates plan completeness (1-5)
- **Issues:** Missing tasks, wrong timeline, unclear dependencies
- **Improvements:** Add workflow tasks, adjust durations, update dependencies
- **Validation:** Next project using updated workflow

### Loop 3: Workflow Retrospective → Workflow Refinement
- **Trigger:** After project completion
- **Rating:** Overall + phase-by-phase ratings (1-5)
- **Issues:** Phase usefulness, duration accuracy, task relevance
- **Improvements:** Remove/reorder phases, adjust estimates, refine tasks
- **Validation:** Multiple projects showing trend improvement

---

## Operations

**rate** - Collect feedback on content quality (Loop 1)
- Entry: `feedback-skill rate --asset-path <path> --asset-type <type>`
- Subskill: `subskills/rate.md`
- Automatic: Called every 5th execution from content-writing-skill
- Manual: Can be invoked explicitly by user
- Output: Rating + issue identification → feedback_events table

**review-plan** - Collect feedback on project plan (Loop 2)
- Entry: `feedback-skill review-plan --project-path <path> --project-id <id>`
- Subskill: `subskills/review-plan.md`
- Automatic: Called after project creation in project-management-skill
- Output: Rating + issue identification → feedback_events table

**retrospective** - Collect feedback on workflow (Loop 3)
- Entry: `feedback-skill retrospective --project-id <id> --workflow-id <id>`
- Subskill: `subskills/retrospective.md`
- Automatic: Called after project marked complete
- Output: Overall + phase ratings → workflow_retrospectives + workflow_phase_ratings tables

**improve** - Execute improvements based on feedback
- Entry: `feedback-skill improve --feedback-id <id> --issue-category <category>`
- Subskill: `subskills/improve.md`
- Automatic: Called by rate/review-plan/retrospective when issues identified
- Output: Executed improvement → improvements table

**dashboard** - Show feedback summary and improvement effectiveness
- Entry: `feedback-skill dashboard [--type <type>]`
- Subskill: `subskills/dashboard.md`
- Shows: Recent feedback, improvement history, effectiveness metrics
- Filters: --type content_quality | project_plan | workflow_retrospective

**suggest** - Analyze feedback patterns and suggest improvements
- Entry: `feedback-skill suggest`
- Subskill: `subskills/suggest.md`
- Shows: Common issues, improvement opportunities based on feedback trends
- Output: Actionable suggestions based on accumulated feedback

---

## Routing Logic

Parse arguments → Route to subskill:

```bash
OPERATION=$1
shift

case "$OPERATION" in
    "rate")
        # Loop 1: Content Quality
        .claude/skills/feedback-skill/subskills/rate.md "$@"
        ;;

    "review-plan")
        # Loop 2: Project Plan
        .claude/skills/feedback-skill/subskills/review-plan.md "$@"
        ;;

    "retrospective")
        # Loop 3: Workflow
        .claude/skills/feedback-skill/subskills/retrospective.md "$@"
        ;;

    "improve")
        # Improvement execution
        .claude/skills/feedback-skill/subskills/improve.md "$@"
        ;;

    "dashboard")
        # View feedback summary
        .claude/skills/feedback-skill/subskills/dashboard.md "$@"
        ;;

    "suggest")
        # View suggestions from feedback patterns
        .claude/skills/feedback-skill/subskills/suggest.md "$@"
        ;;

    *)
        echo "Unknown operation: $OPERATION"
        echo ""
        echo "Available operations:"
        echo "  rate           - Rate content quality"
        echo "  review-plan    - Review project plan"
        echo "  retrospective  - Review completed workflow"
        echo "  improve        - Execute improvements"
        echo "  dashboard      - View feedback summary"
        echo "  suggest        - View improvement suggestions"
        exit 1
        ;;
esac
```

---

## Data Storage

### SQLite (`.kurt/kurt.sqlite`)

**feedback_events**
- All feedback submissions (ratings, comments, issues)
- Links to projects, workflows, skills, operations
- Tracks prompted vs explicit feedback

**improvements**
- Suggested and executed improvements
- Before/after snapshots
- Success/failure tracking
- Validation results

**workflow_retrospectives**
- Overall workflow ratings
- Project completion feedback

**workflow_phase_ratings**
- Phase-by-phase ratings
- Duration accuracy, task completeness
- Suggested changes

**feedback_loops**
- Complete loop tracking (feedback → improvement → validation)
- Rating changes
- Issue resolution
- Effectiveness metrics

### YAML Configuration (`.kurt/feedback/`)

**feedback-config.yaml**
- Issue category mappings
- Improvement commands
- Check logic
- Suggestion messages

---

## Configuration

### Issue Mappings

Maps issue categories to improvement actions:

```yaml
issue_mappings:
  wrong_tone_style:
    check: style_rule_age
    suggest: "Update style rule with patterns from recent content"
    command: "writing-rules-skill style --type {type} --update"

  missing_structure:
    check: structure_rule_exists
    suggest: "Extract or update structure pattern"
    command: "writing-rules-skill structure --type {type} --auto-discover"

  missing_tasks:
    check: workflow_phase_tasks
    suggest: "Add missing tasks to workflow phase"
    command: "workflow-skill update --workflow-id {workflow_id} --add-tasks {phase_id}"

  wrong_timeline:
    check: workflow_duration_accuracy
    suggest: "Adjust workflow phase duration estimates"
    command: "workflow-skill update --workflow-id {workflow_id} --adjust-duration {phase_id}"
```

---

## Integration Points

### From content-writing-skill

After draft or outline generation:

```bash
# Check if we should prompt for feedback (every 5th execution)
EXECUTION_COUNT=$(get_execution_count "$OPERATION")

if [ $((EXECUTION_COUNT % 5)) -eq 0 ]; then
    echo ""
    echo "Would you like to rate this $OPERATION? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ]; then
        feedback-skill rate \
            --asset-path "$ASSET_PATH" \
            --asset-type "$OPERATION" \
            --execution-count "$EXECUTION_COUNT" \
            --prompted true
    fi
fi
```

### From project-management-skill

After project creation:

```bash
# After project.md created
echo "Would you like to review the project plan? (Y/n): "
read -r RESPONSE

if [ "$RESPONSE" != "n" ]; then
    feedback-skill review-plan \
        --project-path "projects/$PROJECT_ID" \
        --project-id "$PROJECT_ID" \
        $([ -n "$WORKFLOW_ID" ] && echo "--workflow-id $WORKFLOW_ID")
fi
```

After project completion:

```bash
# When marking project complete
if [ -n "$WORKFLOW_ID" ]; then
    echo "Would you like to provide workflow feedback? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ]; then
        feedback-skill retrospective \
            --project-id "$PROJECT_ID" \
            --workflow-id "$WORKFLOW_ID" \
            --completion-date "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    fi
fi
```

---

## Improvement Flow

1. **User provides feedback** (via rate/review-plan/retrospective)
2. **Issue identified** (if rating <= 3)
3. **Check if improvement needed** (rule age, recent improvements, etc.)
4. **Load improvement mapping** (from feedback-config.yaml)
5. **Generate improvement command** (substitute variables)
6. **Show preview** (what will change)
7. **Get user approval** (explicit confirmation)
8. **Execute improvement** (run command)
9. **Store before/after** (for validation)
10. **Track validation** (on next usage)
11. **Complete feedback loop** (measure effectiveness)

---

## Success Metrics

### Per-Loop Metrics

**Content Quality:**
- Average rating by content type
- Most common issues
- Rule update frequency
- Rating improvement after updates

**Project Plans:**
- Average rating by workflow
- Most common issues
- Workflow update frequency
- Plan quality trends

**Workflow Retrospectives:**
- Average overall rating by workflow
- Average phase ratings
- Duration estimate accuracy
- Task completeness rate

### Overall Metrics

- Feedback submission rate (prompted vs explicit)
- Improvement acceptance rate
- Improvement success rate
- Issue resolution rate
- Rating trends over time
- Feedback loop completion rate

---

## Example Usage

### Rate a draft explicitly:
```bash
feedback-skill rate \
    --asset-path "projects/my-tutorial/draft.md" \
    --asset-type "draft"
```

### Review a project plan:
```bash
feedback-skill review-plan \
    --project-path "projects/my-tutorial" \
    --project-id "my-tutorial" \
    --workflow-id "weekly-tutorial"
```

### Retrospective after completion:
```bash
feedback-skill retrospective \
    --project-id "my-tutorial" \
    --workflow-id "weekly-tutorial"
```

### View feedback dashboard:
```bash
feedback-skill dashboard
feedback-skill dashboard --type content_quality
feedback-skill dashboard --type workflow_retrospective
```

### View improvement suggestions:
```bash
feedback-skill suggest
```

---

## Design Principles

1. **Output-driven:** Only collect feedback on concrete, rateable artifacts
2. **Actionable:** Every issue maps to specific improvement command
3. **Occasional:** Prompt every 5th execution + explicit requests (not intrusive)
4. **Immediate:** Execute improvements on user approval (not just suggestions)
5. **Validating:** Track effectiveness through next usage and rating changes
6. **Transparent:** Show what will change before applying improvements
7. **Incremental:** Small, targeted improvements rather than large refactors

---

## Getting Started

1. **Create feedback configuration:**
   ```bash
   # Copy template
   cp .kurt/feedback/feedback-config-template.yaml .kurt/feedback/feedback-config.yaml
   ```

2. **Use the system naturally:**
   - Create content (drafts, outlines)
   - Create projects
   - Complete projects

3. **Provide feedback when prompted:**
   - Every 5th execution
   - After project creation
   - After project completion

4. **Review and accept improvements:**
   - System will suggest specific improvements
   - Preview what will change
   - Accept or reject

5. **Track effectiveness:**
   ```bash
   feedback-skill dashboard
   ```

---

## Advanced Usage

### Force feedback on any content:
```bash
feedback-skill rate --asset-path <path> --asset-type <type>
```

### Re-review a project plan:
```bash
feedback-skill review-plan --project-id <id>
```

### View retrospective without creating new one:
```bash
feedback-skill retrospective --view --project-id <id>
```

### Manually trigger improvement:
```bash
# After providing feedback, improvement will be suggested
# Or directly execute if you know the issue:
feedback-skill improve --feedback-id <id> --issue-category <category>
```

### Query feedback data:
```bash
# View all feedback
sqlite3 .kurt/kurt.sqlite "SELECT * FROM feedback_events ORDER BY created_at DESC LIMIT 10"

# View improvements
sqlite3 .kurt/kurt.sqlite "SELECT * FROM improvements WHERE status = 'executed' ORDER BY created_at DESC"

# View completed feedback loops
sqlite3 .kurt/kurt.sqlite "SELECT * FROM feedback_loops WHERE validation_completed_at IS NOT NULL"
```

---

*This skill enables data-driven continuous improvement through explicit user feedback on concrete outputs.*
