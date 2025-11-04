# Kurt-Core Changes - COMPLETED

**Related to:** Feedback system simplification
**Date:** 2025-02-03
**Status:** ✅ Implemented

---

## Database Schema Changes

### Option 1: Migration (Recommended)

Create migration to simplify feedback_events table and drop unused tables.

**File:** `kurt-core/src/kurt/migrations/00X_simplify_feedback.sql`

```sql
-- Drop unused tables
DROP TABLE IF EXISTS improvements;
DROP TABLE IF EXISTS workflow_retrospectives;
DROP TABLE IF EXISTS workflow_phase_ratings;
DROP TABLE IF EXISTS feedback_loops;

-- Simplify feedback_events table
-- Note: SQLite doesn't support DROP COLUMN, so we need to recreate

-- Create new simplified table
CREATE TABLE feedback_events_new (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    issue_category TEXT,
    asset_path TEXT,
    project_id TEXT
);

-- Copy data from old table (if exists)
INSERT INTO feedback_events_new (id, created_at, rating, comment, issue_category, asset_path, project_id)
SELECT
    id,
    created_at,
    rating,
    comment,
    issue_category,
    asset_path,
    project_id
FROM feedback_events
WHERE id IS NOT NULL;

-- Drop old table and rename new one
DROP TABLE feedback_events;
ALTER TABLE feedback_events_new RENAME TO feedback_events;

-- Create indices
CREATE INDEX idx_feedback_created ON feedback_events(created_at);
CREATE INDEX idx_feedback_category ON feedback_events(issue_category);
CREATE INDEX idx_feedback_rating ON feedback_events(rating);
```

**Removed columns from feedback_events:**
- `feedback_type` (always "content_quality" now)
- `skill_name` (not needed for patterns)
- `operation` (not needed for patterns)
- `workflow_id` (workflows removed)
- `execution_count` (automation removed)
- `prompted` (automation removed)
- `issue_identified` (implicit from issue_category presence)

---

### Option 2: Fresh Start

If no production data exists, simpler to just update the initial schema:

**File:** `kurt-core/src/kurt/migrations/001_add_feedback_tables.sql`

Replace with simplified version:

```sql
CREATE TABLE IF NOT EXISTS feedback_events (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    issue_category TEXT CHECK(issue_category IN (
        'tone', 'structure', 'info', 'comprehension',
        'length', 'examples', 'other', NULL
    )),
    asset_path TEXT,
    project_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback_events(created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_category ON feedback_events(issue_category);
CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback_events(rating);
```

---

## CLI Commands (Already Removed)

The following were already removed from `kurt-core/src/kurt/commands/feedback.py`:

✅ **Removed workflow-related options:**
- `log-phase-rating` command (entire command deleted)
- `--workflow-used` flag from `log-submission`
- `workflow_retrospective` from feedback type choices
- `update_workflow` from improvement type choices

✅ **Updated type definitions** in `kurt-core/src/kurt/telemetry/feedback_tracker.py`:
- `FeedbackType`: Removed `"workflow_retrospective"`
- `ImprovementType`: Removed `"update_workflow"`
- Removed `track_workflow_phase_rated()` function
- Removed `workflow_used` parameter from `track_feedback_submitted()`

---

## No New CLI Commands Needed

The simplified feedback system uses existing `kurt` CLI for:
- Database access (SQLite queries via `sqlite3` command)
- No new `kurt feedback` commands required

All feedback operations are handled in Claude Code via feedback-skill.

---

## Testing After Migration

### Test 1: Verify table exists
```bash
sqlite3 .kurt/kurt.sqlite "SELECT name FROM sqlite_master WHERE type='table' AND name='feedback_events';"
```

Expected: `feedback_events`

### Test 2: Verify schema
```bash
sqlite3 .kurt/kurt.sqlite "PRAGMA table_info(feedback_events);"
```

Expected columns:
- id (TEXT)
- created_at (TEXT)
- rating (INTEGER)
- comment (TEXT)
- issue_category (TEXT)
- asset_path (TEXT)
- project_id (TEXT)

### Test 3: Verify old tables removed
```bash
sqlite3 .kurt/kurt.sqlite "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('improvements', 'workflow_retrospectives', 'workflow_phase_ratings', 'feedback_loops');"
```

Expected: (empty result)

### Test 4: Insert test feedback
```bash
sqlite3 .kurt/kurt.sqlite <<EOF
INSERT INTO feedback_events (id, created_at, rating, issue_category, asset_path)
VALUES ('test-123', datetime('now'), 3, 'tone', '/test/path.md');
EOF
```

### Test 5: Query patterns
```bash
sqlite3 .kurt/kurt.sqlite <<EOF
SELECT issue_category, COUNT(*) as count
FROM feedback_events
GROUP BY issue_category;
EOF
```

---

## Implementation Steps

1. **Create migration file** (Option 1) OR update initial schema (Option 2)
2. **Run migration** (if using Option 1)
3. **Test database schema** (all 5 tests above)
4. **Update any existing queries** in kurt-core if needed
5. **Document migration** in kurt-core CHANGELOG

---

## Notes

- Existing feedback data (if any) will be preserved during migration
- Only relevant columns are copied to new simplified table
- All workflow-related data will be lost (intentional - workflows removed)
- No code changes needed in claude-code (feedback-skill already updated)

---

## Implementation Summary

### Files Changed in kurt-core:

1. **Created migration:** `src/kurt/db/migrations/versions/20251103_0004_simplify_feedback.py`
   - Drops 4 unused tables (improvements, workflow_retrospectives, workflow_phase_ratings, feedback_loops)
   - Recreates feedback_events with simplified schema (7 columns instead of 16)
   - Creates 3 indexes (created_at, issue_category, rating)
   - Handles both upgrade scenarios (existing tables + fresh install)

2. **Simplified CLI commands:** `src/kurt/commands/feedback.py`
   - Removed: log-suggestion, log-improvement, log-validation, log-loop-completed
   - Kept: log-submission (simplified to 3 parameters: rating, has_comment, issue_category)
   - Reduced from ~250 lines to ~50 lines

3. **Simplified telemetry tracker:** `src/kurt/telemetry/feedback_tracker.py`
   - Removed: FeedbackType, track_improvement_suggested, track_improvement_executed, track_improvement_validated, track_feedback_loop_completed
   - Simplified: track_feedback_submitted (now only 3 parameters)
   - Updated IssueCategory type to match new categories
   - Reduced from ~206 lines to ~38 lines

### Migration Applied in kurt-demo:

- Ran SQL migration on `.kurt/kurt.sqlite`
- Verified table schema updated correctly
- Confirmed unused tables dropped
- Confirmed indexes created

### Next Steps:

- Users can apply migration via: `kurt migrate apply` (once kurt-core is updated)
- Or manually via: `sqlite3 .kurt/kurt.sqlite < .kurt/migrations/002_simplify_feedback.sql`

---

*For context, see `docs/feedback-system.md` in kurt-demo*
