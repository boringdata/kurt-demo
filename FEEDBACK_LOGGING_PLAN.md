# Feedback Logging Plan: kurt-core CLI Integration

**Date:** February 2, 2025
**Status:** Design

---

## Overview

This document specifies what feedback events should be logged to PostHog from kurt-core CLI level, building on the existing telemetry infrastructure from the telemetry branch.

**Key Principle:** Separate local user-facing feedback (detailed, project-specific) from remote developer analytics (anonymized, aggregated insights).

---

## Architecture

### Two-Tier Feedback System

**Tier 1: Local Feedback Tracking (feedback-skill in Claude Code)**
- Detailed user ratings and free-text feedback
- Project-specific context (project names, workflow IDs, rule paths)
- Full improvement action history with outcomes
- Storage: SQLite in kurt-core database
- Purpose: User-facing feedback loops and improvement execution

**Tier 2: Remote Feedback Logging (kurt-core CLI → PostHog)**
- Anonymized feedback events for developer insights
- Aggregate metrics (avg ratings, common issues, improvement success rates)
- Usage patterns across feedback loops
- Storage: PostHog
- Purpose: Product development insights and tool performance monitoring

---

## Feedback Events to Log (PostHog)

### Event 1: `feedback_submitted`

**When:** User submits feedback via any of the 3 feedback loops

**Properties:**
```python
{
    "feedback_type": str,  # "content_quality" | "project_plan" | "workflow_retrospective"
    "rating": int,         # 1-5 scale
    "has_comment": bool,   # true if user provided text feedback (not the text itself)
    "issue_identified": bool,  # true if user identified specific issue
    "issue_category": str,     # "tone" | "structure" | "info" | "tasks" | "timeline" | "phase_usefulness" | null

    # Context (anonymized)
    "skill_name": str,         # "content-writing-skill" | "project-management-skill" | etc
    "operation": str,          # "outline" | "draft" | "create-project" | etc
    "workflow_used": bool,     # true if project used workflow
    "has_analytics": bool,     # true if analytics configured

    # Timing
    "execution_count": int,    # nth execution of this operation
    "prompted": bool,          # true if automatic prompt (every 5th), false if explicit request
}
```

**Privacy:**
- NO project names, file paths, workflow IDs, or user text
- Only feedback type, rating, and issue category
- Anonymized context about what was being worked on

---

### Event 2: `improvement_suggested`

**When:** System suggests an improvement based on feedback

**Properties:**
```python
{
    "feedback_type": str,      # Same as Event 1
    "issue_category": str,     # Issue that triggered suggestion
    "improvement_type": str,   # "update_rule" | "update_workflow" | "update_config" | "extract_new_rule"

    # Improvement context (anonymized)
    "rule_type": str,          # "style" | "structure" | "persona" | "publisher" | null
    "rule_age_days": int,      # Days since rule last updated (if applicable)
    "content_count": int,      # Number of content pieces since last rule update

    # Suggestion outcome
    "user_response": str,      # "accepted" | "rejected" | "dismissed"
}
```

**Privacy:**
- NO rule names, file paths, or content
- Only improvement type and high-level context

---

### Event 3: `improvement_executed`

**When:** User accepts a suggestion and improvement is executed

**Properties:**
```python
{
    "improvement_type": str,   # Same as Event 2
    "rule_type": str,          # Same as Event 2

    # Execution details
    "command": str,            # High-level command (e.g., "writing-rules-skill style --update")
    "success": bool,           # true if command succeeded
    "duration_ms": int,        # Time to execute

    # Before/after (anonymized)
    "content_analyzed": int,   # Number of content pieces analyzed
    "rules_updated": int,      # Number of rule files modified
}
```

**Privacy:**
- NO file paths or content
- Only command type and success metrics

---

### Event 4: `improvement_validated`

**When:** User works with improved component after improvement (next usage)

**Properties:**
```python
{
    "improvement_type": str,   # Same as previous events
    "rule_type": str,          # Same as previous events

    # Validation
    "days_since_improvement": int,  # Days between improvement and next usage
    "subsequent_rating": int,       # Rating on next feedback (1-5) - if provided
    "issue_resolved": bool,         # true if same issue not reported again
}
```

**Privacy:**
- NO identifying information
- Only timing and effectiveness metrics

---

### Event 5: `workflow_phase_rated`

**When:** User rates individual phases during retrospective

**Properties:**
```python
{
    "phase_type": str,         # Generic phase type (not phase name)
                               # "selection" | "planning" | "creation" | "review" | "publication"
    "phase_position": int,     # 1, 2, 3, etc (position in workflow)
    "total_phases": int,       # Total phases in workflow

    # Rating
    "usefulness_rating": int,  # 1-5 scale
    "duration_accurate": bool, # true if duration estimate was accurate
    "tasks_complete": bool,    # true if all tasks were relevant

    # Outcome
    "suggested_change": bool,  # true if user suggested change to phase
    "change_type": str,        # "add_tasks" | "remove_tasks" | "adjust_duration" | "reorder" | null
}
```

**Privacy:**
- NO workflow names or specific task descriptions
- Only phase characteristics and ratings

---

### Event 6: `feedback_loop_completed`

**When:** Full feedback loop completes (feedback → suggestion → execution → validation)

**Properties:**
```python
{
    "feedback_type": str,      # Same as Event 1
    "loop_duration_days": int, # Days from initial feedback to validation

    # Loop metrics
    "suggestions_made": int,   # Number of suggestions offered
    "improvements_accepted": int,  # Number accepted
    "improvements_successful": int,  # Number that executed successfully
    "issue_resolved": bool,    # true if original issue resolved

    # Context
    "subsequent_rating_change": int,  # Change in rating (-4 to +4)
}
```

**Privacy:**
- NO specific details
- Only high-level loop effectiveness metrics

---

## Implementation in kurt-core

### New File: `src/kurt/telemetry/feedback_tracker.py`

```python
"""Feedback-specific telemetry tracking.

Extends base telemetry infrastructure with feedback events.
"""

from typing import Optional, Literal
from .tracker import track_event
from .config import is_telemetry_enabled

FeedbackType = Literal["content_quality", "project_plan", "workflow_retrospective"]
IssueCategory = Literal["tone", "structure", "info", "tasks", "timeline", "phase_usefulness"]
ImprovementType = Literal["update_rule", "update_workflow", "update_config", "extract_new_rule"]


def track_feedback_submitted(
    feedback_type: FeedbackType,
    rating: int,
    has_comment: bool = False,
    issue_identified: bool = False,
    issue_category: Optional[IssueCategory] = None,
    skill_name: Optional[str] = None,
    operation: Optional[str] = None,
    workflow_used: bool = False,
    has_analytics: bool = False,
    execution_count: int = 1,
    prompted: bool = False,
) -> None:
    """Track user feedback submission.

    Args:
        feedback_type: Type of feedback loop
        rating: User rating (1-5)
        has_comment: Whether user provided text feedback
        issue_identified: Whether user identified specific issue
        issue_category: Category of identified issue
        skill_name: Name of skill being rated
        operation: Operation being rated
        workflow_used: Whether project used workflow
        has_analytics: Whether analytics configured
        execution_count: Nth execution of operation
        prompted: Whether automatic prompt or explicit request
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "feedback_type": feedback_type,
        "rating": rating,
        "has_comment": has_comment,
        "issue_identified": issue_identified,
        "issue_category": issue_category,
        "skill_name": skill_name,
        "operation": operation,
        "workflow_used": workflow_used,
        "has_analytics": has_analytics,
        "execution_count": execution_count,
        "prompted": prompted,
    }

    # Remove None values
    properties = {k: v for k, v in properties.items() if v is not None}

    track_event("feedback_submitted", properties)


def track_improvement_suggested(
    feedback_type: FeedbackType,
    issue_category: IssueCategory,
    improvement_type: ImprovementType,
    user_response: Literal["accepted", "rejected", "dismissed"],
    rule_type: Optional[str] = None,
    rule_age_days: Optional[int] = None,
    content_count: Optional[int] = None,
) -> None:
    """Track improvement suggestion.

    Args:
        feedback_type: Type of feedback loop
        issue_category: Issue that triggered suggestion
        improvement_type: Type of improvement suggested
        user_response: How user responded to suggestion
        rule_type: Type of rule (if applicable)
        rule_age_days: Days since rule last updated
        content_count: Number of content pieces since last update
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "feedback_type": feedback_type,
        "issue_category": issue_category,
        "improvement_type": improvement_type,
        "user_response": user_response,
        "rule_type": rule_type,
        "rule_age_days": rule_age_days,
        "content_count": content_count,
    }

    properties = {k: v for k, v in properties.items() if v is not None}

    track_event("improvement_suggested", properties)


def track_improvement_executed(
    improvement_type: ImprovementType,
    command: str,
    success: bool,
    duration_ms: int,
    rule_type: Optional[str] = None,
    content_analyzed: Optional[int] = None,
    rules_updated: Optional[int] = None,
) -> None:
    """Track improvement execution.

    Args:
        improvement_type: Type of improvement
        command: High-level command executed
        success: Whether command succeeded
        duration_ms: Execution duration
        rule_type: Type of rule (if applicable)
        content_analyzed: Number of content pieces analyzed
        rules_updated: Number of rule files modified
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "improvement_type": improvement_type,
        "command": command,
        "success": success,
        "duration_ms": duration_ms,
        "rule_type": rule_type,
        "content_analyzed": content_analyzed,
        "rules_updated": rules_updated,
    }

    properties = {k: v for k, v in properties.items() if v is not None}

    track_event("improvement_executed", properties)


def track_improvement_validated(
    improvement_type: ImprovementType,
    days_since_improvement: int,
    issue_resolved: bool,
    rule_type: Optional[str] = None,
    subsequent_rating: Optional[int] = None,
) -> None:
    """Track improvement validation (next usage).

    Args:
        improvement_type: Type of improvement
        days_since_improvement: Days between improvement and validation
        issue_resolved: Whether same issue not reported again
        rule_type: Type of rule (if applicable)
        subsequent_rating: Rating on next feedback
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "improvement_type": improvement_type,
        "days_since_improvement": days_since_improvement,
        "issue_resolved": issue_resolved,
        "rule_type": rule_type,
        "subsequent_rating": subsequent_rating,
    }

    properties = {k: v for k, v in properties.items() if v is not None}

    track_event("improvement_validated", properties)


def track_workflow_phase_rated(
    phase_type: str,
    phase_position: int,
    total_phases: int,
    usefulness_rating: int,
    duration_accurate: bool,
    tasks_complete: bool,
    suggested_change: bool = False,
    change_type: Optional[str] = None,
) -> None:
    """Track workflow phase rating in retrospective.

    Args:
        phase_type: Generic phase type
        phase_position: Position in workflow (1-indexed)
        total_phases: Total phases in workflow
        usefulness_rating: Rating (1-5)
        duration_accurate: Whether duration estimate was accurate
        tasks_complete: Whether all tasks were relevant
        suggested_change: Whether user suggested change
        change_type: Type of suggested change
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "phase_type": phase_type,
        "phase_position": phase_position,
        "total_phases": total_phases,
        "usefulness_rating": usefulness_rating,
        "duration_accurate": duration_accurate,
        "tasks_complete": tasks_complete,
        "suggested_change": suggested_change,
        "change_type": change_type,
    }

    properties = {k: v for k, v in properties.items() if v is not None}

    track_event("workflow_phase_rated", properties)


def track_feedback_loop_completed(
    feedback_type: FeedbackType,
    loop_duration_days: int,
    suggestions_made: int,
    improvements_accepted: int,
    improvements_successful: int,
    issue_resolved: bool,
    subsequent_rating_change: int,
) -> None:
    """Track complete feedback loop from feedback to validation.

    Args:
        feedback_type: Type of feedback loop
        loop_duration_days: Days from feedback to validation
        suggestions_made: Number of suggestions offered
        improvements_accepted: Number accepted
        improvements_successful: Number that executed successfully
        issue_resolved: Whether original issue resolved
        subsequent_rating_change: Change in rating (-4 to +4)
    """
    if not is_telemetry_enabled():
        return

    properties = {
        "feedback_type": feedback_type,
        "loop_duration_days": loop_duration_days,
        "suggestions_made": suggestions_made,
        "improvements_accepted": improvements_accepted,
        "improvements_successful": improvements_successful,
        "issue_resolved": issue_resolved,
        "subsequent_rating_change": subsequent_rating_change,
    }

    track_event("feedback_loop_completed", properties)
```

---

## Database Schema (kurt-core SQLite)

### New Tables for Local Feedback Tracking

```sql
-- Feedback events (detailed, local-only)
CREATE TABLE feedback_events (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    feedback_type TEXT NOT NULL,  -- content_quality, project_plan, workflow_retrospective

    -- Context (NOT sent to PostHog)
    project_id TEXT,
    workflow_id TEXT,
    skill_name TEXT,
    operation TEXT,
    asset_path TEXT,  -- Path to rated asset

    -- Rating
    rating INTEGER NOT NULL,  -- 1-5
    comment TEXT,  -- User's text feedback (local only)

    -- Issue identification
    issue_identified BOOLEAN DEFAULT FALSE,
    issue_category TEXT,  -- tone, structure, info, tasks, timeline, phase_usefulness

    -- Metadata
    execution_count INTEGER DEFAULT 1,
    prompted BOOLEAN DEFAULT FALSE,

    -- Telemetry
    telemetry_sent BOOLEAN DEFAULT FALSE,
    telemetry_event_id TEXT
);

CREATE INDEX idx_feedback_events_type ON feedback_events(feedback_type);
CREATE INDEX idx_feedback_events_project ON feedback_events(project_id);
CREATE INDEX idx_feedback_events_created ON feedback_events(created_at);


-- Improvements (detailed, local-only)
CREATE TABLE improvements (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    feedback_event_id TEXT NOT NULL,

    -- Improvement details
    improvement_type TEXT NOT NULL,  -- update_rule, update_workflow, update_config, extract_new_rule
    target_path TEXT,  -- Rule file, workflow file, etc (local only)
    command TEXT NOT NULL,  -- Full command executed (local only)

    -- Status
    status TEXT NOT NULL,  -- suggested, accepted, rejected, dismissed, executed, failed
    executed_at TEXT,
    duration_ms INTEGER,
    error TEXT,

    -- Before/after snapshots (local only)
    content_before TEXT,
    content_after TEXT,

    -- Validation
    validated_at TEXT,
    validation_rating INTEGER,  -- Rating on next usage
    issue_resolved BOOLEAN,

    -- Telemetry
    telemetry_sent BOOLEAN DEFAULT FALSE,
    telemetry_event_id TEXT,

    FOREIGN KEY (feedback_event_id) REFERENCES feedback_events(id)
);

CREATE INDEX idx_improvements_feedback ON improvements(feedback_event_id);
CREATE INDEX idx_improvements_status ON improvements(status);
CREATE INDEX idx_improvements_created ON improvements(created_at);


-- Workflow retrospectives (detailed, local-only)
CREATE TABLE workflow_retrospectives (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    project_id TEXT NOT NULL,
    workflow_id TEXT NOT NULL,  -- Local only

    -- Overall ratings
    overall_rating INTEGER NOT NULL,  -- 1-5
    overall_comment TEXT,  -- Local only

    -- Metadata
    total_duration_days INTEGER,
    completed_at TEXT,

    -- Telemetry
    telemetry_sent BOOLEAN DEFAULT FALSE,
    telemetry_event_id TEXT
);

CREATE INDEX idx_retrospectives_project ON workflow_retrospectives(project_id);
CREATE INDEX idx_retrospectives_workflow ON workflow_retrospectives(workflow_id);


-- Workflow phase ratings (detailed, local-only)
CREATE TABLE workflow_phase_ratings (
    id TEXT PRIMARY KEY,
    retrospective_id TEXT NOT NULL,
    phase_id TEXT NOT NULL,  -- Local only
    phase_name TEXT NOT NULL,  -- Local only
    phase_position INTEGER NOT NULL,

    -- Ratings
    usefulness_rating INTEGER NOT NULL,  -- 1-5
    duration_accurate BOOLEAN NOT NULL,
    tasks_complete BOOLEAN NOT NULL,
    comment TEXT,  -- Local only

    -- Suggestions
    suggested_change BOOLEAN DEFAULT FALSE,
    change_type TEXT,  -- add_tasks, remove_tasks, adjust_duration, reorder
    change_description TEXT,  -- Local only

    -- Telemetry
    telemetry_sent BOOLEAN DEFAULT FALSE,
    telemetry_event_id TEXT,

    FOREIGN KEY (retrospective_id) REFERENCES workflow_retrospectives(id)
);

CREATE INDEX idx_phase_ratings_retrospective ON workflow_phase_ratings(retrospective_id);


-- Feedback loop tracking (for completed loops)
CREATE TABLE feedback_loops (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    feedback_event_id TEXT NOT NULL,

    -- Loop timeline
    feedback_submitted_at TEXT NOT NULL,
    improvement_executed_at TEXT,
    validation_completed_at TEXT,
    loop_duration_days INTEGER,

    -- Loop metrics
    suggestions_made INTEGER DEFAULT 0,
    improvements_accepted INTEGER DEFAULT 0,
    improvements_successful INTEGER DEFAULT 0,
    issue_resolved BOOLEAN,

    -- Rating change
    initial_rating INTEGER NOT NULL,
    subsequent_rating INTEGER,
    rating_change INTEGER,

    -- Telemetry
    telemetry_sent BOOLEAN DEFAULT FALSE,
    telemetry_event_id TEXT,

    FOREIGN KEY (feedback_event_id) REFERENCES feedback_events(id)
);

CREATE INDEX idx_feedback_loops_event ON feedback_loops(feedback_event_id);
CREATE INDEX idx_feedback_loops_completed ON feedback_loops(validation_completed_at);
```

---

## Integration Flow

### Flow 1: Feedback Submission

```
1. User rates content/plan/workflow in feedback-skill (Claude Code)
2. feedback-skill stores detailed feedback in SQLite
3. feedback-skill calls kurt CLI command to log telemetry
4. kurt CLI extracts anonymized properties
5. kurt CLI calls track_feedback_submitted() → PostHog
```

**Command:**
```bash
kurt feedback log-submission \
  --type "content_quality" \
  --rating 3 \
  --issue-category "tone" \
  --skill "content-writing-skill" \
  --operation "draft" \
  --event-id "abc123"
```

### Flow 2: Improvement Execution

```
1. feedback-skill suggests improvement
2. User accepts
3. feedback-skill executes improvement command
4. feedback-skill stores improvement in SQLite
5. feedback-skill calls kurt CLI to log execution
6. kurt CLI calls track_improvement_executed() → PostHog
```

**Command:**
```bash
kurt feedback log-improvement \
  --type "update_rule" \
  --rule-type "style" \
  --success true \
  --duration-ms 5230 \
  --event-id "def456"
```

### Flow 3: Improvement Validation

```
1. User works with improved component (e.g., generates new content with updated rule)
2. feedback-skill detects previous improvement
3. feedback-skill prompts for validation feedback
4. feedback-skill stores validation in SQLite
5. feedback-skill calls kurt CLI to log validation
6. kurt CLI calls track_improvement_validated() → PostHog
7. If loop complete, also calls track_feedback_loop_completed()
```

**Command:**
```bash
kurt feedback log-validation \
  --improvement-id "def456" \
  --days-since 3 \
  --issue-resolved true \
  --rating 4 \
  --event-id "ghi789"
```

---

## CLI Commands (kurt-core)

### New Command Group: `kurt feedback`

```bash
# Log feedback submission
kurt feedback log-submission \
  --type <content_quality|project_plan|workflow_retrospective> \
  --rating <1-5> \
  [--issue-category <category>] \
  [--skill <skill-name>] \
  [--operation <operation>] \
  [--workflow-used] \
  [--has-analytics] \
  [--execution-count <n>] \
  [--prompted] \
  --event-id <uuid>

# Log improvement suggestion
kurt feedback log-suggestion \
  --feedback-type <type> \
  --issue-category <category> \
  --improvement-type <type> \
  --user-response <accepted|rejected|dismissed> \
  [--rule-type <type>] \
  [--rule-age-days <n>] \
  [--content-count <n>] \
  --event-id <uuid>

# Log improvement execution
kurt feedback log-improvement \
  --type <improvement-type> \
  --rule-type <type> \
  --success <true|false> \
  --duration-ms <n> \
  [--content-analyzed <n>] \
  [--rules-updated <n>] \
  --event-id <uuid>

# Log improvement validation
kurt feedback log-validation \
  --improvement-id <uuid> \
  --days-since <n> \
  --issue-resolved <true|false> \
  [--rating <1-5>] \
  --event-id <uuid>

# Log workflow phase rating
kurt feedback log-phase-rating \
  --phase-type <type> \
  --phase-position <n> \
  --total-phases <n> \
  --rating <1-5> \
  --duration-accurate <true|false> \
  --tasks-complete <true|false> \
  [--suggested-change <true|false>] \
  [--change-type <type>] \
  --event-id <uuid>

# Query local feedback (for debugging)
kurt feedback list [--type <type>] [--since <date>]
kurt feedback stats
```

---

## Privacy Safeguards

### Data Exclusions (NEVER logged to PostHog)

1. **Project identifiers**: Project names, IDs, descriptions
2. **File paths**: Rule paths, workflow paths, content paths
3. **User content**: Text feedback, comments, suggestions
4. **Workflow details**: Workflow names, phase names, task descriptions
5. **Rule content**: Before/after rule content, examples
6. **Personal information**: User names, emails, company names

### Data Transformations

1. **Phase names → Generic phase types**
   - "topic-selection" → "selection"
   - "drafting" → "creation"
   - "technical-review" → "review"

2. **Rule paths → Rule types**
   - "rules/style/technical-docs.md" → "style"
   - "rules/personas/backend-developer.md" → "persona"

3. **Command → High-level command**
   - "writing-rules-skill style --type technical-docs --update" → "writing-rules-skill style --update"

### Consent and Opt-Out

1. **Respects existing telemetry settings**
   - DO_NOT_TRACK environment variable
   - KURT_TELEMETRY_DISABLED environment variable
   - ~/.kurt/telemetry.json config
   - CI environment detection

2. **Separate feedback opt-out (optional)**
   - `kurt feedback disable` - Disable feedback logging only
   - `kurt telemetry disable` - Disable all telemetry (including feedback)

3. **Transparency**
   - Update TELEMETRY.md to document feedback events
   - Show examples of what IS and IS NOT logged
   - Provide data export: `kurt feedback export --format json`

---

## Testing Plan

### Unit Tests

1. **Test feedback_tracker.py functions**
   - Verify event properties
   - Test with telemetry disabled
   - Test with missing optional properties

2. **Test CLI commands**
   - Verify argument parsing
   - Test error handling
   - Test with various combinations

3. **Test database operations**
   - Insert feedback events
   - Query feedback
   - Calculate loop metrics

### Integration Tests

1. **End-to-end feedback loop**
   - Submit feedback → suggestion → execution → validation
   - Verify telemetry events sent to PostHog (test project)
   - Verify local database updated correctly

2. **Privacy compliance**
   - Verify NO PII in events
   - Verify NO file paths in events
   - Verify transformations applied correctly

3. **Opt-out behavior**
   - Verify telemetry respects opt-out
   - Verify local database still works

---

## Rollout Plan

### Phase 1: Database + Local Tracking (Week 1)
- Add database tables to kurt-core
- Implement local feedback storage (no telemetry yet)
- Test feedback-skill with local-only storage

### Phase 2: Telemetry Infrastructure (Week 2)
- Implement feedback_tracker.py
- Add CLI commands
- Test with PostHog test project

### Phase 3: Integration (Week 3)
- Update feedback-skill to call CLI commands
- End-to-end testing
- Privacy audit

### Phase 4: Documentation + Launch (Week 4)
- Update TELEMETRY.md
- Add feedback logging docs
- User communication about feedback system

---

## Success Metrics

### Developer Insights (from PostHog data)

1. **Feedback Volume**
   - Submissions per week
   - Breakdown by feedback type
   - Rating distribution

2. **Issue Identification**
   - Most common issue categories
   - Issue categories by feedback type
   - Correlation with ratings

3. **Improvement Effectiveness**
   - Suggestion acceptance rate
   - Improvement success rate
   - Issue resolution rate
   - Rating change after improvement

4. **Workflow Performance**
   - Phase ratings by phase type
   - Most problematic phases
   - Most useful phases
   - Duration accuracy

5. **Feedback Loop Health**
   - Average loop duration
   - Loop completion rate
   - Rating improvement over time

### User Value (from local database)

1. **Personal Improvement Tracking**
   - See their own feedback history
   - Track improvements made
   - Measure effectiveness

2. **Context Preservation**
   - Full text feedback preserved
   - Before/after snapshots
   - Project-specific insights

---

## Next Steps

1. **Review this plan** - Confirm approach and scope
2. **Create migration** - Add database tables to kurt-core
3. **Implement feedback_tracker.py** - Core telemetry functions
4. **Add CLI commands** - `kurt feedback` command group
5. **Update feedback-skill** - Integrate with CLI commands
6. **Test end-to-end** - Full feedback loops
7. **Privacy audit** - Verify no PII leakage
8. **Documentation** - Update TELEMETRY.md
9. **Launch** - Roll out to users

---

**This plan provides anonymized developer insights while preserving detailed local feedback for user benefit.**
