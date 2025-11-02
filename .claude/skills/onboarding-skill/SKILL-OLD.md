# Onboarding Skill

**Purpose:** One-time team setup that creates Kurt profile and foundation rules
**Entry:** `/start` command
**Output:** `.kurt/profile.md` + foundation rules + indexed content

---

## Overview

This skill guides new teams through initial Kurt setup in an adaptive, user-friendly way. It:

1. **Captures team context** - Company, goals, content types, personas
2. **Maps content sources** - Website, CMS, research sources
3. **Extracts foundation rules** - Publisher profile, style guides, personas
4. **Creates team profile** - Centralized `.kurt/profile.md` with all setup info
5. **Suggests next steps** - Based on what was completed and what's missing

**Key principle:** Users can skip questions they're unsure about - the system adapts.

---

## Workflow

### Step 1: Welcome & Introduction

```
═══════════════════════════════════════════════════════
Welcome to Kurt!
═══════════════════════════════════════════════════════

I'll help you set up Kurt for your team. This takes 5-10 minutes.

You can skip questions you're unsure about - we'll help you discover
the answers as you work.

Press Enter to start...
```

---

### Step 2: Company & Team Context

```
───────────────────────────────────────────────────────
COMPANY & TEAM
───────────────────────────────────────────────────────

What company/organization do you work for?
> _

What team are you on? (Marketing, DevRel, Product, etc.)
[Skip if not applicable]
> _

What industry/vertical?
[Skip if not sure]
> _
```

**Capture:**
- `COMPANY_NAME`
- `TEAM_NAME`
- `TEAM_ROLE`
- `INDUSTRY` (optional)

---

### Step 3: Communication Goals

```
───────────────────────────────────────────────────────
COMMUNICATION GOALS
───────────────────────────────────────────────────────

What are you trying to achieve with content? (Select all that apply)
  1. Drive product adoption
  2. Build thought leadership
  3. Enable customers (docs, tutorials)
  4. Generate leads
  5. Developer education
  6. Community building
  7. Other (specify)

Select (comma-separated) or press Enter to skip: _
```

**Capture:**
- `GOALS` (list)

**If "Other" selected:**
```
Please describe your content goals:
> _
```

---

### Step 4: Content Types

```
───────────────────────────────────────────────────────
CONTENT TYPES
───────────────────────────────────────────────────────

What types of content do you create regularly?
  1. Blog posts
  2. Technical tutorials
  3. API documentation
  4. Case studies
  5. Email campaigns
  6. Social content
  7. Landing pages
  8. Whitepapers
  9. Video scripts
  10. Other (specify)

Select (comma-separated) or press Enter to skip: _
```

**Capture:**
- `CONTENT_TYPES` (list)

---

### Step 5: Target Personas

```
───────────────────────────────────────────────────────
TARGET PERSONAS
───────────────────────────────────────────────────────

Who do you write for?

Do you have defined personas/audience profiles? (y/n/not sure): _
```

**If yes:**
```
Great! What are your target personas? (e.g., "Backend Developer", "CTO", "Data Analyst")
[Comma-separated]
> _
```

**Capture:**
- `KNOWN_PERSONAS` (list)

**If no or not sure:**
```
No problem! Kurt can help extract personas from your existing content.

For now, can you describe your typical readers in a few words?
[Press Enter to skip]
> _
```

**Capture:**
- `PERSONA_DESCRIPTION` (text)
- Flag: `PERSONAS_TO_DISCOVER = true`

---

### Step 6: Content Sources

```
───────────────────────────────────────────────────────
CONTENT SOURCES
───────────────────────────────────────────────────────

Where should Kurt look for your existing content?

Company website/blog:
[Press Enter to skip]
> _

Documentation site:
[Press Enter to skip]
> _

Do you have a CMS? (Sanity/Contentful/WordPress/None): _
```

**If CMS = Sanity/Contentful/WordPress:**
```
Would you like to configure CMS access now? (y/n): _
```

**If yes:** Invoke `cms-interaction onboard`
**If no:**
```
[Skipped - you can run cms-interaction onboard later]
```

**Capture:**
- `COMPANY_WEBSITE`
- `DOCS_URL`
- `BLOG_URL`
- `CMS_PLATFORM`
- `CMS_CONFIGURED` (boolean)

```
Other sources (competitor sites, industry publications)?
[Comma-separated URLs, or press Enter to skip]
> _
```

**Capture:**
- `RESEARCH_SOURCES` (list)

---

### Step 7: Recurring Workflows

```
───────────────────────────────────────────────────────
RECURRING WORKFLOWS
───────────────────────────────────────────────────────

Do you have recurring content projects? (monthly newsletter,
quarterly feature launches, weekly tutorials, etc.)

Examples:
  • Product launches (research → content → launch)
  • Weekly/monthly newsletters
  • Tutorial series
  • Quarterly docs refreshes

Describe a recurring workflow, or press Enter to skip:
> _
```

**Capture:**
- `WORKFLOW_DESCRIPTION` (text or null)

**If provided:**
```
Great! We can help you codify this workflow after initial setup.
```

**Flag:** `HAS_WORKFLOW_TO_CREATE = true`

---

### Step 8: Setup Summary

```
═══════════════════════════════════════════════════════
Setup Summary
═══════════════════════════════════════════════════════

Company: {{COMPANY_NAME}} ({{TEAM_NAME}} team)
Goals: {{GOALS_LIST}}
Content: {{CONTENT_TYPES_LIST}}
Personas: {{PERSONAS_SUMMARY}}
Sources: {{SOURCES_LIST}}
Workflows: {{WORKFLOW_SUMMARY}}

───────────────────────────────────────────────────────
Next Steps
───────────────────────────────────────────────────────

I'll now help you:
  1. Map your content sources (discover what exists)
  2. Extract your company profile and writing style
  3. Set up your first workflow (optional)

This will take 10-15 minutes. Continue? (y/n): _
```

**If no:**
```
No problem! Your setup has been saved. You can continue anytime with:
  /start --continue

Your profile: .kurt/profile.md
```

→ Create profile.md with what we have, mark as incomplete
→ Exit

**If yes:** Continue to Step 9

---

### Step 9: Map Content Sources

```
───────────────────────────────────────────────────────
Step 1/3: Mapping Content Sources
───────────────────────────────────────────────────────
```

**For each source provided:**

```
Discovering content from: {{SOURCE_URL}}
```

Invoke: `kurt map url {{SOURCE_URL}} --cluster-urls`

```
✓ Found {{PAGE_COUNT}} pages across {{CLUSTER_COUNT}} topic clusters
```

**After all sources mapped:**

```
Content Discovery Summary:
  • {{COMPANY_URL}}: {{COMPANY_PAGES}} pages
  • {{OTHER_SOURCES}}: {{OTHER_PAGES}} pages

Total: {{TOTAL_PAGES}} pages across {{TOTAL_CLUSTERS}} topic clusters

Would you like to fetch this content now? (y/n): _
```

**If yes:**

```
Fetching and indexing content...
```

Invoke: `kurt fetch --include {{all_mapped_urls}}`

```
✓ {{FETCHED_COUNT}} documents fetched and indexed
✓ Content ready for analysis
```

**If no:**
```
Skipped. You can fetch content later with:
  kurt fetch --include <url>
```

**Update profile:**
- `COMPANY_CONTENT_STATUS = "Mapped, not fetched" | "Fetched and indexed"`
- `TOTAL_DOCS = {{count}}`

---

### Step 10: Extract Foundation Rules

```
───────────────────────────────────────────────────────
Step 2/3: Extract Foundation Rules
───────────────────────────────────────────────────────

Now extracting:
  • Company profile (who you are, what you offer)
  • Writing style (voice and tone)
  • Target personas (who you write for)

This may take a few minutes...
```

**Auto-run extraction (in sequence):**

1. **Publisher Profile:**
```
Extracting company profile...
```

Invoke: `writing-rules-skill publisher --auto-discover`

```
✓ Publisher profile created
  Location: rules/publisher/publisher-profile.md
```

2. **Style Guide:**
```
Extracting writing style...
```

Invoke: `writing-rules-skill style --type corporate --auto-discover`

```
✓ Style guide created: {{STYLE_NAME}}
  Location: rules/style/{{STYLE_FILE}}
```

3. **Personas:**
```
Extracting target personas...
```

Invoke: `writing-rules-skill persona --audience-type all --auto-discover`

```
✓ {{PERSONA_COUNT}} personas extracted:
{{PERSONA_LIST}}
```

**Update profile:**
- `PUBLISHER_STATUS = "Extracted"`
- `PUBLISHER_PATH = "rules/publisher/publisher-profile.md"`
- `STYLE_COUNT = {{count}}`
- `STYLE_LIST = {{files}}`
- `PERSONA_COUNT = {{count}}`
- `PERSONA_LIST = {{files}}`

**Handle errors gracefully:**

If extraction fails (e.g., insufficient content):
```
⚠️  Unable to extract {{RULE_TYPE}}
    Reason: {{ERROR_MESSAGE}}

    You can extract this later with:
      writing-rules-skill {{RULE_TYPE}} ...
```

Continue with other extractions.

---

### Step 11: Workflow Setup (Optional)

**If `HAS_WORKFLOW_TO_CREATE == true`:**

```
───────────────────────────────────────────────────────
Step 3/3: Define Your First Workflow (Optional)
───────────────────────────────────────────────────────

You mentioned: "{{WORKFLOW_DESCRIPTION}}"

Would you like to define this workflow now? (y/n/later): _
```

**If yes:**
```
Great! Let's create this workflow.
```

Invoke: `workflow-skill add --from-description "{{WORKFLOW_DESCRIPTION}}"`

**If no or later:**
```
No problem! You can create workflows anytime with:
  workflow-skill add
```

**Else (no workflow mentioned):**

```
───────────────────────────────────────────────────────
Step 3/3: Define Workflow (Optional)
───────────────────────────────────────────────────────

Would you like to define a recurring workflow now? (y/n/later): _
```

---

### Step 12: Create Profile File

```
Creating your Kurt profile...
```

**Generate `.kurt/profile.md`:**

1. Load template from `.kurt/templates/profile-template.md`
2. Replace all `{{PLACEHOLDERS}}` with captured data
3. Calculate next steps based on what's complete/missing
4. Write to `.kurt/profile.md`

```
✓ Profile created: .kurt/profile.md
```

---

### Step 13: Success & Next Steps

```
═══════════════════════════════════════════════════════
🎉 Setup Complete!
═══════════════════════════════════════════════════════

Your Kurt profile is ready:
  Location: .kurt/profile.md

Foundation rules extracted:
  {{EXTRACTED_RULES_SUMMARY}}

Content mapped:
  {{CONTENT_SUMMARY}}

───────────────────────────────────────────────────────
What's Next?
───────────────────────────────────────────────────────

{{NEXT_STEPS_PERSONALIZED}}

Example next steps:
  1. Define a recurring workflow:
     workflow-skill add

  2. Create your first project:
     /create-project

  3. Explore your content:
     kurt content list

───────────────────────────────────────────────────────

Need help? Type /help or see .kurt/profile.md for your setup
```

---

## Adaptive Next Steps Logic

Based on what was completed, suggest appropriate next steps:

**If workflows not defined:**
→ Suggest: `workflow-skill add`

**If content not mapped:**
→ Suggest: `kurt map url <website>`

**If content mapped but not fetched:**
→ Suggest: `kurt fetch --include <url>`

**If rules not extracted:**
→ Suggest specific extractions: `writing-rules-skill publisher`, etc.

**If CMS mentioned but not configured:**
→ Suggest: `cms-interaction onboard`

**If everything complete:**
→ Suggest: `/create-project` or `workflow-skill execute <workflow>`

---

## Profile Update Helper Functions

The skill should have helper functions to:

1. **Load profile template**
2. **Replace placeholders** with captured data
3. **Format lists** (goals, content types, personas, etc.)
4. **Calculate status** (what's done, what's missing)
5. **Generate next steps** (personalized based on gaps)
6. **Write profile file**

---

## Error Handling

**If .kurt/profile.md already exists:**
```
⚠️  Kurt profile already exists

Would you like to:
  a) View existing profile
  b) Update profile
  c) Start over (overwrites existing)

Choose: _
```

**If content mapping fails:**
```
⚠️  Unable to map content from: {{URL}}
    Error: {{ERROR_MESSAGE}}

    Skip this source? (y/n): _
```

**If rule extraction fails:**
```
⚠️  Unable to extract {{RULE_TYPE}}

    This is usually because:
    - Not enough content fetched (need 3-5 documents minimum)
    - Content not indexed yet

    Continue with setup? (y/n): _
```

---

## Integration Points

**Invokes:**
- `kurt map url` - Map content sources
- `kurt fetch` - Fetch and index content
- `writing-rules-skill publisher` - Extract company profile
- `writing-rules-skill style` - Extract style guide
- `writing-rules-skill persona` - Extract personas
- `cms-interaction onboard` - Configure CMS (optional)
- `workflow-skill add` - Create workflow (optional)

**Creates:**
- `.kurt/profile.md` - Team profile
- Foundation rules (via writing-rules-skill)
- Content mapping (via kurt CLI)

**Updates:**
- Profile status as steps complete
- Next steps based on completion

---

## Flags & Options

**`/start`** - Full interactive onboarding

**`/start --continue`** - Resume incomplete onboarding

**`/start --minimal`** - Skip optional steps (no content mapping, no rule extraction)

**`/start --update`** - Update existing profile

---

*This skill provides a comprehensive, adaptive onboarding experience that meets users where they are and guides them through initial setup.*
