# Feedback Skill Integration Guide

This document describes how other skills should integrate with the feedback system.

---

## Overview

The feedback skill provides three feedback loops that can be integrated into other skills:

1. **Loop 1: Content Quality** - Rate content artifacts (outlines, drafts)
2. **Loop 2: Project Plan Quality** - Review project plans
3. **Loop 3: Workflow Retrospective** - Review completed workflows

---

## Integration Pattern

### Basic Pattern

```bash
# After completing operation
if should_prompt_for_feedback; then
    echo ""
    echo "Would you like to rate this ${OPERATION}? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        feedback-skill ${OPERATION_TYPE} \
            --asset-path "${ASSET_PATH}" \
            $(additional_args)
    fi
fi
```

### Prompt Frequency

By default, prompt every 5th execution:

```bash
should_prompt_for_feedback() {
    local operation=$1

    # Get execution count from database
    local count=$(sqlite3 .kurt/kurt.sqlite "
        SELECT COUNT(*) + 1 FROM feedback_events
        WHERE operation = '${operation}'
        AND skill_name = '${SKILL_NAME}'
    ")

    # Prompt every 5th execution
    if [ $((count % 5)) -eq 0 ]; then
        return 0
    else
        return 1
    fi
}
```

---

## Loop 1: Content Quality Integration

### For content-writing-skill

#### Integration Points

**In `content-writing-skill/subskills/draft.md`:**

After draft generation completes:

```bash
# Draft generation complete
echo "✓ Draft created: ${DRAFT_PATH}"
echo ""

# Check if we should prompt for feedback
EXECUTION_COUNT=$(get_execution_count "draft")

if [ $((EXECUTION_COUNT % 5)) -eq 0 ]; then
    echo "Would you like to rate this draft? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        # Invoke feedback skill
        feedback-skill rate \
            --asset-path "${DRAFT_PATH}" \
            --asset-type "draft" \
            --project-id "${PROJECT_ID}" \
            --skill-name "content-writing-skill" \
            --operation "draft" \
            --execution-count "${EXECUTION_COUNT}" \
            --prompted true
    fi
fi
```

**In `content-writing-skill/subskills/outline.md`:**

After outline generation completes:

```bash
# Outline generation complete
echo "✓ Outline created: ${OUTLINE_PATH}"
echo ""

# Check if we should prompt for feedback
EXECUTION_COUNT=$(get_execution_count "outline")

if [ $((EXECUTION_COUNT % 5)) -eq 0 ]; then
    echo "Would you like to rate this outline? (Y/n): "
    read -r RESPONSE

    if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
        # Invoke feedback skill
        feedback-skill rate \
            --asset-path "${OUTLINE_PATH}" \
            --asset-type "outline" \
            --project-id "${PROJECT_ID}" \
            --skill-name "content-writing-skill" \
            --operation "outline" \
            --execution-count "${EXECUTION_COUNT}" \
            --prompted true
    fi
fi
```

#### Helper Function

```bash
get_execution_count() {
    local operation=$1

    # Query database for execution count
    local count=$(sqlite3 .kurt/kurt.sqlite "
        SELECT COUNT(*) FROM feedback_events
        WHERE operation = '${operation}'
        AND skill_name = 'content-writing-skill'
    " 2>/dev/null || echo "0")

    # Return count + 1 (for current execution)
    echo $((count + 1))
}
```

---

## Loop 2: Project Plan Review Integration

### For project-management-skill

#### Integration Point

**In `project-management-skill/subskills/create-project.md`:**

After project structure and project.md are created:

```bash
# Project structure complete
echo "✓ Project created: projects/${PROJECT_ID}"
echo ""
echo "Project structure:"
echo "  • project.md"
echo "  • Project phases and folders"
echo ""

# Prompt for plan review
echo "Would you like to review the project plan? (Y/n): "
read -r RESPONSE

if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
    # Invoke feedback skill for plan review
    feedback-skill review-plan \
        --project-path "projects/${PROJECT_ID}" \
        --project-id "${PROJECT_ID}" \
        $([ -n "${WORKFLOW_ID}" ] && echo "--workflow-id ${WORKFLOW_ID}")
fi
```

#### When to Prompt

- **Always** prompt after project creation (not periodic)
- Only prompt if project was created successfully
- Only prompt if project used a workflow (workflow-based planning)

#### Optional: Skip for Simple Projects

```bash
# Only prompt for workflow-based projects
if [ -n "${WORKFLOW_ID}" ]; then
    echo "Would you like to review the project plan? (Y/n): "
    # ... rest of prompt
fi
```

---

## Loop 3: Workflow Retrospective Integration

### For project-management-skill

#### Integration Point

**When marking project as complete:**

```bash
# Mark project complete
mark_project_complete() {
    local project_id=$1

    # Update project status in database
    sqlite3 .kurt/kurt.sqlite <<EOF
UPDATE projects
SET status = 'completed',
    completed_at = '$(date -u +"%Y-%m-%dT%H:%M:%SZ")'
WHERE id = '${project_id}';
EOF

    echo "✓ Project '${project_id}' marked as complete!"
    echo ""

    # Check if project used a workflow
    local workflow_id=$(sqlite3 .kurt/kurt.sqlite "
        SELECT workflow_id FROM projects
        WHERE id = '${project_id}'
    " 2>/dev/null)

    if [ -n "${workflow_id}" ] && [ "${workflow_id}" != "NULL" ]; then
        # Prompt for retrospective
        echo "Would you like to provide feedback on the workflow? (Y/n): "
        read -r RESPONSE

        if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
            # Invoke feedback skill for retrospective
            feedback-skill retrospective \
                --project-id "${project_id}" \
                --workflow-id "${workflow_id}" \
                --completion-date "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        fi
    fi
}
```

#### When to Prompt

- **Always** prompt when project is marked complete
- Only prompt if project used a workflow
- Skip if project has no workflow_id

---

## Explicit Feedback (User-Initiated)

Users can always invoke feedback explicitly without waiting for prompts:

### Rate Content Anytime

```bash
# User explicitly rates a draft
feedback-skill rate \
    --asset-path "projects/my-project/draft.md" \
    --asset-type "draft"
```

### Review Plan Anytime

```bash
# User explicitly reviews a plan
feedback-skill review-plan \
    --project-id "my-project"
```

### Retrospective Anytime

```bash
# User explicitly provides retrospective
feedback-skill retrospective \
    --project-id "my-project"
```

---

## Configuration

### Prompt Frequency

Update in `.kurt/feedback/feedback-config.yaml`:

```yaml
feedback:
  enabled: true
  prompt_frequency: 5  # Every 5th execution

  integration:
    content_writing:
      operations: ["outline", "draft"]
      prompt_frequency: 5
      prompt_message: "Would you like to rate this {operation}?"

    project_management:
      operations: ["create-project"]
      prompt_timing: "after_completion"
      prompt_message: "Would you like to review the project plan?"

      retrospective_prompt: true
      retrospective_timing: "on_completion"
      retrospective_message: "Would you like to provide workflow feedback?"
```

### Disable Feedback Prompts

To disable automatic prompts:

```yaml
feedback:
  enabled: false
```

Or set prompt_frequency to 0:

```yaml
feedback:
  prompt_frequency: 0  # Never prompt automatically
```

---

## Database Queries

### Check if Feedback Enabled

```bash
is_feedback_enabled() {
    local enabled=$(yq eval ".feedback.enabled" .kurt/feedback/feedback-config.yaml 2>/dev/null)

    if [ "$enabled" = "true" ]; then
        return 0
    else
        return 1
    fi
}
```

### Get Prompt Frequency

```bash
get_prompt_frequency() {
    local operation=$1

    # Try operation-specific frequency first
    local freq=$(yq eval ".feedback.integration.content_writing.prompt_frequency" .kurt/feedback/feedback-config.yaml 2>/dev/null)

    # Fall back to global frequency
    if [ -z "$freq" ] || [ "$freq" = "null" ]; then
        freq=$(yq eval ".feedback.prompt_frequency" .kurt/feedback/feedback-config.yaml 2>/dev/null)
    fi

    # Default to 5 if not configured
    if [ -z "$freq" ] || [ "$freq" = "null" ]; then
        echo "5"
    else
        echo "$freq"
    fi
}
```

### Record Execution (for tracking prompts)

The feedback-skill automatically records executions when feedback is provided, but you can also track all executions:

```bash
record_execution() {
    local skill_name=$1
    local operation=$2

    # This is optional - only needed if you want to track
    # executions without feedback for more accurate counting
}
```

---

## Error Handling

### Feedback Skill Not Available

```bash
# Check if feedback skill exists
if [ ! -f ".claude/skills/feedback-skill/SKILL.md" ]; then
    # Feedback skill not available, skip prompt
    return
fi
```

### Database Not Available

```bash
# Check if database exists
if [ ! -f ".kurt/kurt.sqlite" ]; then
    # Database not available, skip prompt
    return
fi
```

### Graceful Degradation

Always allow the main operation to succeed even if feedback fails:

```bash
# Wrap feedback prompt in error handling
{
    if should_prompt_for_feedback "draft"; then
        feedback-skill rate --asset-path "$DRAFT_PATH" --asset-type "draft"
    fi
} || {
    # Feedback failed, but don't fail the whole operation
    echo "⚠️  Feedback collection failed (non-critical)"
}
```

---

## Testing Integration

### Manual Testing

1. **Test periodic prompts:**
   ```bash
   # Run operation 5 times
   for i in {1..5}; do
       content-writing-skill draft
   done

   # Should prompt on 5th execution
   ```

2. **Test explicit feedback:**
   ```bash
   # Create content
   content-writing-skill draft

   # Explicitly rate (should always work)
   feedback-skill rate --asset-path "path/to/draft.md" --asset-type "draft"
   ```

3. **Test plan review:**
   ```bash
   # Create project with workflow
   project-management-skill create-project --workflow "my-workflow"

   # Should prompt for plan review after creation
   ```

4. **Test retrospective:**
   ```bash
   # Mark project complete
   project-management-skill complete --project-id "my-project"

   # Should prompt for retrospective if workflow used
   ```

### Automated Testing

```bash
# Test feedback integration
test_feedback_integration() {
    # Setup: Create test project
    PROJECT_ID="test-project-$(date +%s)"

    # Test 1: Create content and verify prompt
    output=$(content-writing-skill draft --project "$PROJECT_ID")
    if ! echo "$output" | grep -q "Would you like to rate"; then
        echo "✗ Feedback prompt not shown"
        return 1
    fi

    # Test 2: Provide feedback and verify storage
    echo "n" | feedback-skill rate --asset-path "test.md" --asset-type "draft"

    count=$(sqlite3 .kurt/kurt.sqlite "
        SELECT COUNT(*) FROM feedback_events
        WHERE project_id = '${PROJECT_ID}'
    ")

    if [ "$count" -eq 0 ]; then
        echo "✗ Feedback not stored"
        return 1
    fi

    echo "✓ Feedback integration tests passed"
}
```

---

## Migration Guide

### Adding Feedback to Existing Skill

1. **Identify integration points:**
   - Where does operation complete?
   - What artifacts are created?
   - What context is available (project_id, etc)?

2. **Add prompt after operation:**
   ```bash
   # Your operation
   create_draft() {
       # ... operation code ...

       # Operation complete - add feedback prompt here
       if should_prompt_for_feedback "draft"; then
           feedback-skill rate --asset-path "$OUTPUT_PATH" --asset-type "draft"
       fi
   }
   ```

3. **Test integration:**
   - Run operation 5 times to trigger prompt
   - Verify feedback stored in database
   - Check dashboard shows feedback

4. **Document in skill README:**
   - Mention feedback integration
   - Show explicit feedback commands
   - Link to feedback dashboard

---

## Best Practices

1. **Always ask before prompting**
   - Use "Would you like to...? (Y/n)" format
   - Default to Yes (Enter = yes)
   - Respect user's "no" response

2. **Keep prompts brief**
   - Don't interrupt user flow
   - Show prompt after operation completes
   - Make it easy to skip

3. **Provide context**
   - Tell user what they're rating
   - Show path to artifact
   - Include relevant metadata

4. **Handle errors gracefully**
   - Don't fail main operation if feedback fails
   - Log errors but continue
   - User can always provide feedback later

5. **Respect configuration**
   - Check if feedback enabled
   - Use configured prompt frequency
   - Allow users to disable

6. **Track execution counts accurately**
   - Query database for count
   - Include current execution
   - Handle database errors

---

## Example: Complete Integration

Here's a complete example showing all integration points:

```bash
# content-writing-skill/subskills/draft.md

# ... draft generation code ...

# Draft complete
DRAFT_PATH="projects/${PROJECT_ID}/drafts/${DRAFT_NAME}.md"
echo "✓ Draft created: ${DRAFT_PATH}"
echo ""

# Feedback integration
{
    # Check if feedback enabled
    if yq eval ".feedback.enabled" .kurt/feedback/feedback-config.yaml | grep -q "true"; then

        # Get execution count
        EXECUTION_COUNT=$(sqlite3 .kurt/kurt.sqlite "
            SELECT COUNT(*) + 1 FROM feedback_events
            WHERE operation = 'draft'
            AND skill_name = 'content-writing-skill'
        " 2>/dev/null || echo "1")

        # Get prompt frequency
        PROMPT_FREQ=$(yq eval ".feedback.prompt_frequency" .kurt/feedback/feedback-config.yaml 2>/dev/null || echo "5")

        # Check if we should prompt
        if [ $((EXECUTION_COUNT % PROMPT_FREQ)) -eq 0 ]; then
            echo "Would you like to rate this draft? (Y/n): "
            read -r RESPONSE

            if [ "$RESPONSE" != "n" ] && [ "$RESPONSE" != "N" ]; then
                feedback-skill rate \
                    --asset-path "${DRAFT_PATH}" \
                    --asset-type "draft" \
                    --project-id "${PROJECT_ID}" \
                    --skill-name "content-writing-skill" \
                    --operation "draft" \
                    --execution-count "${EXECUTION_COUNT}" \
                    --prompted true
            fi
        fi
    fi
} || {
    # Feedback failed, but don't stop the workflow
    echo "⚠️  Feedback collection unavailable (non-critical)" >&2
}
```

---

## Summary

**Key Points:**

1. Feedback prompts are **optional** and **non-blocking**
2. Prompt **every 5th execution** by default (configurable)
3. Always allow **explicit feedback** (user-initiated)
4. **Gracefully degrade** if feedback system unavailable
5. Store feedback in **SQLite database** for analysis
6. Use feedback to **drive continuous improvement**

**Integration Checklist:**

- [ ] Identify operation completion point
- [ ] Add should_prompt_for_feedback check
- [ ] Add feedback prompt (Y/n format)
- [ ] Pass required context (paths, IDs)
- [ ] Add error handling
- [ ] Test periodic prompts (every 5th)
- [ ] Test explicit feedback
- [ ] Document in skill README
- [ ] Verify database storage

---

*For questions or issues, see `.claude/skills/feedback-skill/SKILL.md` or run `feedback-skill --help`*
