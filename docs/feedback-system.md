# Feedback System

**Status:** Simplified (February 2025)
**Purpose:** Lightweight content feedback → Pattern identification → Rule updates

---

## Overview

The feedback system helps identify recurring issues in content quality and recommends rule updates. It's designed to be simple, non-intrusive, and pattern-based.

### Core Flow

```
1. Create content (drafts, outlines)
2. Rate content quality (1-5) + identify issues
3. View trends in dashboard
4. When patterns emerge (≥3 occurrences), get recommendations
5. Manually update rules based on patterns
```

---

## Components

### 1. feedback-skill

**Location:** `.claude/skills/feedback-skill/`

**Operations:**
- `rate` - Collect content ratings
- `dashboard` - View feedback trends
- `patterns` - Identify recurring issues

**Data:** Stores in `.kurt/kurt.sqlite` (feedback_events table)

### 2. writing-rules-skill Updates

**Location:** `.claude/skills/content-writing/writing-rules-skill/`

**New operations:**
- `style --update` - Update style rules based on feedback
- `structure --update` - Update structure templates based on feedback
- `persona --update` - Update personas based on feedback

**Integration:** Recommended by patterns subskill

---

## Usage

### Rate Content

```bash
feedback-skill rate projects/my-tutorial/draft.md
```

**Collects:**
- Rating (1-5)
- Issue category (tone, structure, info, etc.) if rating ≤3
- Optional text comment

### View Trends

```bash
feedback-skill dashboard

# Or with custom time window
feedback-skill dashboard --days 7
```

**Shows:**
- Overall stats (count, avg rating)
- Issue breakdown by category
- Weekly rating trends
- Recent feedback

### Check for Patterns

```bash
feedback-skill patterns

# Or with custom settings
feedback-skill patterns --days 30 --min-frequency 3
```

**Shows:**
- Recurring issues (≥3 occurrences)
- Sample feedback comments
- Recommended update commands

### Update Rules

```bash
# Copy command from patterns output
writing-rules-skill style --type technical-docs --update
```

**Process:**
1. Loads existing rule
2. Queries recent feedback with matching issues
3. Loads problem content
4. Analyzes pattern and generates updates
5. Shows diff preview
6. Gets user approval
7. Writes updated rule with backup

---

## Database Schema

### feedback_events (Simplified)

```sql
CREATE TABLE feedback_events (
    id TEXT PRIMARY KEY,           -- UUID
    created_at TEXT NOT NULL,      -- ISO 8601
    rating INTEGER NOT NULL,       -- 1-5
    comment TEXT,                  -- Optional text
    issue_category TEXT,           -- tone|structure|info|etc
    asset_path TEXT,               -- Path to content
    project_id TEXT                -- Optional context
);
```

### Removed Tables

Previous complex version had 5 tables. Simplified version uses only 1:

- ❌ `improvements` - No automated execution tracking
- ❌ `workflow_retrospectives` - Workflows removed
- ❌ `workflow_phase_ratings` - Workflows removed
- ❌ `feedback_loops` - Too complex

---

## Issue Categories

| Category | Description | Maps To |
|----------|-------------|---------|
| `tone` | Wrong tone/style | style rules |
| `structure` | Poor organization | structure templates |
| `info` | Missing information | personas, sources |
| `comprehension` | Hard to understand | style + structure |
| `length` | Too long/short | personas |
| `examples` | Code example issues | structure |
| `other` | Manual review | - |

---

## Design Principles

1. **Lightweight:** No complex automation or tracking
2. **Pattern-based:** Only show issues that occur ≥3 times
3. **Manual control:** User decides when to update rules
4. **Non-blocking:** Never interrupts workflow
5. **Content-focused:** Only content quality (no projects/workflows)
6. **Privacy-conscious:** Minimal data storage

---

## What Changed

### Removed (from complex version)

- **Project plan feedback** (Loop 2)
- **Workflow retrospectives** (Loop 3)
- **Automated improvement execution**
- **Validation & effectiveness tracking**
- **Feedback loop completion metrics**
- **Multiple feedback types** (now just content)
- **~2,000 lines of automation code**

### Kept (simplified)

- **Content rating** with issue identification
- **Pattern analysis** across feedback
- **Dashboard** for trend visualization
- **Manual recommendations** for rule updates

---

## Integration

### Optional: content-writing-skill

Can prompt for feedback after content creation:

```bash
# After draft
echo "Rate this draft? (y/N): "
read -r RESPONSE
if [ "$RESPONSE" = "y" ]; then
    feedback-skill rate "$DRAFT_PATH"
fi
```

### Recommended by: onboarding-skill

Onboarding can mention feedback system as optional feature.

---

## Configuration

Minimal config in `.kurt/feedback/feedback-config.yaml`:

```yaml
feedback:
  enabled: true
  min_pattern_frequency: 3
  default_time_window_days: 30
```

---

## Files Changed

### Created
- `writing-rules-skill/subskills/update-style.md` (~350 lines)
- `writing-rules-skill/subskills/update-structure.md` (~350 lines)
- `writing-rules-skill/subskills/update-persona.md` (~350 lines)

### Simplified
- `feedback-skill/subskills/rate.md` (~500 → ~290 lines)
- `feedback-skill/subskills/patterns.md` (~600 → ~280 lines)
- `feedback-skill/subskills/dashboard.md` (~655 → ~394 lines)
- `feedback-skill/SKILL.md` (complete rewrite, ~280 lines)

### Deleted
- `feedback-skill/subskills/review-plan.md`
- `feedback-skill/subskills/retrospective.md`
- `feedback-skill/subskills/improve.md`

### Net Change
- **Removed:** ~2,000 lines (workflow automation)
- **Added:** ~1,050 lines (rule update subskills)
- **Result:** ~950 lines fewer, much simpler

---

## Kurt-Core Changes Needed

See `KURT_CORE_CHANGES.md` for database migration requirements.

---

*For implementation details, see skill files in `.claude/skills/feedback-skill/` and `.claude/skills/content-writing/writing-rules-skill/`*
