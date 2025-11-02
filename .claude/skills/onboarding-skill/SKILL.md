---
name: onboarding
description: One-time team setup that creates Kurt profile and foundation rules
---

# Onboarding Skill

**Purpose:** One-time team setup and profile creation
**Entry:** `/start` command
**Output:** `.kurt/profile.md` + foundation rules + indexed content

---

## Overview

This skill orchestrates the onboarding process by routing through specialized subskills:

1. **questionnaire** - Capture team context, goals, sources
2. **map-content** - Map and fetch content from sources
3. **extract-foundation** - Extract publisher, style, personas
4. **create-profile** - Generate `.kurt/profile.md`

---

## Routing Logic

```bash
# Check if profile already exists
if [ -f ".kurt/profile.md" ]; then
  echo "⚠️  Kurt profile already exists"
  echo ""
  echo "Would you like to:"
  echo "  a) View existing profile"
  echo "  b) Update profile"
  echo "  c) Start over (overwrites existing)"
  echo ""
  read -p "Choose: " choice

  case "$choice" in
    a)
      cat .kurt/profile.md
      exit 0
      ;;
    b)
      OPERATION="update"
      ;;
    c)
      OPERATION="start-over"
      ;;
    *)
      echo "Cancelled"
      exit 0
      ;;
  esac
else
  OPERATION="new"
fi

# Parse flags
while [[ $# -gt 0 ]]; do
  case $1 in
    --continue)
      OPERATION="continue"
      shift
      ;;
    --minimal)
      OPERATION="minimal"
      shift
      ;;
    --update)
      OPERATION="update"
      shift
      ;;
    *)
      shift
      ;;
  esac
done
```

---

## Step 1: Welcome Message

```
═══════════════════════════════════════════════════════
Welcome to Kurt!
═══════════════════════════════════════════════════════

I'll help you set up Kurt for your team. This takes 5-10 minutes.

You can skip questions you're unsure about - we'll help you discover
the answers as you work.

Press Enter to start...
```

Wait for user to press Enter.

---

## Step 2: Run Questionnaire

Invoke: `onboarding-skill/subskills/questionnaire`

This captures:
- Company name, team, industry
- Communication goals
- Content types created
- Target personas
- Source content URLs
- CMS configuration (optional)
- Workflow description (optional)

**Output:** JSON file with all captured data at `.kurt/temp/onboarding-data.json`

---

## Step 3: Map Content (if sources provided)

Check if sources were provided:

```bash
SOURCES=$(jq -r '.sources | length' .kurt/temp/onboarding-data.json)

if [ "$SOURCES" -gt 0 ]; then
  echo ""
  echo "───────────────────────────────────────────────────────"
  echo "Step 1/3: Mapping Content Sources"
  echo "───────────────────────────────────────────────────────"
  echo ""

  # Invoke map-content subskill
  # This calls kurt CLI to map and fetch
fi
```

Invoke: `onboarding-skill/subskills/map-content`

**Input:** Sources from onboarding-data.json
**Output:** Updates onboarding-data.json with content stats

---

## Step 4: Extract Foundation Rules (if content fetched)

Check if content was fetched:

```bash
CONTENT_FETCHED=$(jq -r '.content_fetched' .kurt/temp/onboarding-data.json)

if [ "$CONTENT_FETCHED" = "true" ]; then
  echo ""
  echo "───────────────────────────────────────────────────────"
  echo "Step 2/3: Extract Foundation Rules"
  echo "───────────────────────────────────────────────────────"
  echo ""
fi
```

Invoke: `onboarding-skill/subskills/extract-foundation`

**Input:** Content status from onboarding-data.json
**Output:** Creates rules files, updates onboarding-data.json with rule paths

---

## Step 5: Create Profile

Always run (even if steps 3-4 skipped):

```
───────────────────────────────────────────────────────
Step 3/3: Creating Your Profile
───────────────────────────────────────────────────────

Generating your Kurt profile...
```

Invoke: `onboarding-skill/subskills/create-profile`

**Input:** All data from onboarding-data.json
**Output:** `.kurt/profile.md`

---

## Step 6: Cleanup

```bash
# Remove temporary data file
rm .kurt/temp/onboarding-data.json

# Create temp directory for future use
mkdir -p .kurt/temp
```

---

## Step 7: Success Message

```
═══════════════════════════════════════════════════════
🎉 Setup Complete!
═══════════════════════════════════════════════════════

Your Kurt profile is ready:
  Location: .kurt/profile.md

{{COMPLETION_SUMMARY}}

───────────────────────────────────────────────────────
What's Next?
───────────────────────────────────────────────────────

{{NEXT_STEPS}}

Need help? Type /help or see .kurt/profile.md for your setup
```

**Completion summary based on what was done:**
- If content mapped: "✓ Content mapped: X documents"
- If rules extracted: "✓ Rules extracted: publisher, style, personas"
- If workflow mentioned: "Suggestion: Run `workflow-skill add` to codify your workflow"

**Next steps based on gaps:**
- If no content: "1. Map content: kurt map url <website>"
- If no rules: "2. Extract rules: writing-rules-skill publisher --auto-discover"
- If workflow mentioned: "3. Define workflow: workflow-skill add"
- Always: "4. Create project: /create-project"

---

## Error Handling

**If subskill fails:**
```
⚠️  {{SUBSKILL_NAME}} failed

Error: {{ERROR_MESSAGE}}

Options:
  a) Retry
  b) Skip this step
  c) Cancel onboarding

Choose: _
```

**If .kurt/ directory doesn't exist:**
```
⚠️  Kurt not initialized

Run: kurt init
Then retry: /start
```

---

## Integration Points

**Invokes:**
- `onboarding-skill/subskills/questionnaire` - Capture user input
- `onboarding-skill/subskills/map-content` - Map and fetch sources
- `onboarding-skill/subskills/extract-foundation` - Extract rules
- `onboarding-skill/subskills/create-profile` - Generate profile

**Creates:**
- `.kurt/profile.md` - Team profile
- `.kurt/temp/onboarding-data.json` - Temporary data (deleted after)
- Foundation rules (via extract-foundation subskill)

---

*This router orchestrates the onboarding process through specialized subskills.*
