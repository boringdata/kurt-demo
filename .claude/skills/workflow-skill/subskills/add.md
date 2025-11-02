# Add Workflow Subskill

**Purpose:** Interactive wizard to create new recurring workflow
**Parent Skill:** workflow-skill
**Operation:** Management
**Output:** Workflow definition in `.kurt/workflows/workflow-registry.yaml`

---

## Context Received from Parent Skill

- `$REGISTRY_PATH` - `.kurt/workflows/workflow-registry.yaml`
- `$TEMPLATE_PATH` - `.kurt/workflows/templates/_workflow-template.yaml`
- `$ARGUMENTS` - Optional `--from-description "description"`

---

## Workflow

### Step 1: Get Workflow Description

```
═══════════════════════════════════════════════════════
Create New Workflow
═══════════════════════════════════════════════════════

What type of work do you do repeatedly?

Examples:
  • Product launches (research → content → launch)
  • Weekly/monthly newsletters
  • Tutorial series publication
  • Quarterly docs refreshes
  • Event promotion campaigns
  • Content refresh cycles

Describe your workflow in your own words:
> _
```

**Capture:** `WORKFLOW_DESCRIPTION`

**If `--from-description` provided:**
- Use that description
- Skip this step

---

### Step 2: Extract Phases

**Analyze description to detect potential phases:**

```
I detected these potential phases from your description:

{{DETECTED_PHASES}}

Does this match your workflow? (y/n or describe differently): _
```

**Example detections:**
- "publish tutorials weekly" → topic-selection, outlining, drafting, review, publish
- "product launches" → research, positioning, content-creation, review, launch
- "docs refresh quarterly" → audit, prioritization, updates, review, publication

**If yes:** Use detected phases

**If no:**
```
Please describe the major steps/phases:
> _
```

Parse user input to extract phases.

**Store:** `PHASES` (list of phase names)

---

### Step 3: Configure Each Phase

For each phase in `PHASES`:

```
───────────────────────────────────────────────────────
Phase {{N}}: {{PHASE_NAME}}
───────────────────────────────────────────────────────

How long does this phase typically take?
Examples: "1 day", "2-3 days", "1 week", "2 weeks"
> _
```

**Capture:** `PHASE_DURATION`

```
What are the main tasks in this phase?
[Enter one per line, or comma-separated. Press Enter twice when done]
> _
```

**Capture:** `PHASE_TASKS` (list)

```
What outputs does this phase create?
Examples: "research/brief.md", "drafts/outline.md", "reviews/feedback.md"
[Enter paths, one per line. Press Enter twice when done]
> _
```

**Capture:** `PHASE_OUTPUTS` (list)

```
Does this phase depend on other phases completing first? (y/n): _
```

**If yes:**
```
Which phases must complete first?
Available phases: {{PREVIOUS_PHASES}}
[Comma-separated]
> _
```

**Capture:** `PHASE_DEPENDENCIES` (list)

```
Does this phase require specific rules? (style guides, structure templates, personas)
Examples: "style/technical", "structure/tutorial", "personas/developer"
(y/n): _
```

**If yes:**
```
Which rules are required?
[Enter rule paths, comma-separated]
> _
```

**Capture:** `REQUIRED_RULES` (list)

```
Does this phase require review/approval? (y/n): _
```

**If yes:**
```
Who reviews?
Examples: "engineering-team", "legal", "marketing-vp"
[Comma-separated]
> _
```

**Capture:** `REVIEWERS` (list)

```
Is approval blocking? (must approve before continuing)
(y/n): _
```

**Capture:** `APPROVAL_REQUIRED` (boolean)

**Repeat for all phases.**

---

### Step 4: Define Workflow Metadata

```
───────────────────────────────────────────────────────
Workflow Metadata
───────────────────────────────────────────────────────

Give this workflow a name (slug format):
Examples: "weekly-tutorial", "product-launch", "docs-refresh"
> _
```

**Capture:** `WORKFLOW_ID`

**Validate:** Check if workflow ID already exists in registry

```
Display name:
Example: "Weekly Technical Tutorial"
> _
```

**Capture:** `WORKFLOW_NAME`

```
How often do you run this workflow?
Options: weekly, monthly, quarterly, on-demand
> _
```

**Capture:** `FREQUENCY`

---

### Step 5: Define Success Criteria

```
───────────────────────────────────────────────────────
Success Criteria
───────────────────────────────────────────────────────

What must be true for this workflow to be considered successful?

Examples:
  • "All drafts created"
  • "Technical review passed"
  • "Published to blog"
  • "Analytics tracking set up"

Enter success criteria (one per line, Enter twice when done):
> _
```

**Capture:** `SUCCESS_CRITERIA` (list)

---

### Step 6: Test Workflow Logic

```
Testing workflow definition...
```

**Validation checks:**

1. **Phase Dependencies**
```bash
# Check for circular dependencies
# Build dependency graph and detect cycles
```

```
✓ No circular dependencies detected
```

2. **Required Rules**
```bash
# Check if all required rules exist
for rule in $REQUIRED_RULES; do
  if [ ! -f "rules/$rule" ]; then
    echo "⚠️  Rule not found: $rule"
  fi
done
```

```
✓ All required rules exist
```
OR
```
⚠️  Some required rules not found:
  - personas/backend-developer

  Create with: writing-rules-skill persona --audience-type technical
```

3. **Timeline Calculation**
```bash
# Calculate total duration from phase durations and dependencies
# Consider parallel vs sequential phases
```

```
✓ Timeline estimate: 3-5 days (based on critical path)
```

4. **Output Paths**
```bash
# Validate output paths are valid
```

```
✓ All output paths valid
```

**Display validation summary:**

```
═══════════════════════════════════════════════════════
Validation Summary
═══════════════════════════════════════════════════════

Workflow: {{WORKFLOW_NAME}}
Phases: {{PHASE_COUNT}}
Dependencies: {{DEPENDENCY_COUNT}}
Required rules: {{REQUIRED_RULES_COUNT}}
Review gates: {{REVIEW_GATES_COUNT}}
Estimated duration: {{TOTAL_DURATION}}

Validation:
  ✓ Dependencies valid
  {{RULE_VALIDATION_STATUS}}
  ✓ Timeline calculated
  ✓ Paths valid

{{WARNINGS}}
```

---

### Step 7: Review and Confirm

```
───────────────────────────────────────────────────────
Workflow Summary
───────────────────────────────────────────────────────

Name: {{WORKFLOW_NAME}}
ID: {{WORKFLOW_ID}}
Frequency: {{FREQUENCY}}
Phases: {{PHASE_COUNT}}
Duration: {{TOTAL_DURATION}}

Phases:
{{#each PHASES}}
  {{N}}. {{NAME}} ({{DURATION}})
     {{#if DEPENDENCIES}}Depends on: {{DEPENDENCIES}}{{/if}}
     {{#if REQUIRED_RULES}}Rules: {{REQUIRED_RULES}}{{/if}}
     {{#if REVIEWERS}}Review: {{REVIEWERS}}{{/if}}
{{/each}}

Success criteria:
{{#each SUCCESS_CRITERIA}}
  • {{CRITERION}}
{{/each}}

───────────────────────────────────────────────────────

Save this workflow? (y/n/edit): _
```

**If yes:** Continue to Step 8
**If no:** Cancel
**If edit:** Return to specific phase for editing

---

### Step 8: Generate Workflow Definition

**Load template:**
```bash
TEMPLATE=$(cat .kurt/workflows/templates/_workflow-template.yaml)
```

**Replace placeholders:**
```bash
# Replace all {{PLACEHOLDERS}} with captured data
# - {{WORKFLOW_ID}}
# - {{WORKFLOW_NAME}}
# - {{WORKFLOW_DESCRIPTION}}
# - {{FREQUENCY}}
# - {{CREATED_DATE}}
# - {{PHASES}} (full phase definitions)
# - {{SUCCESS_CRITERIA}}
# etc.
```

**Generate phase definitions:**
```yaml
phases:
  - id: {{PHASE_ID}}
    name: "{{PHASE_NAME}}"
    duration: "{{DURATION}}"
    depends_on: [{{DEPENDENCIES}}]
    tasks:
      {{#each TASKS}}
      - {{TASK}}
      {{/each}}
    outputs:
      {{#each OUTPUTS}}
      - {{OUTPUT}}
      {{/each}}
    required_rules:
      {{#each RULES}}
      - {{RULE}}
      {{/each}}
    {{#if REVIEW_WORKFLOW}}
    review_workflow:
      reviewers: [{{REVIEWERS}}]
      approval_required: {{APPROVAL_REQUIRED}}
    {{/if}}
```

---

### Step 9: Add to Registry

**Load existing registry:**
```bash
REGISTRY=".kurt/workflows/workflow-registry.yaml"
```

**Add workflow to registry:**
```yaml
workflows:
  {{WORKFLOW_ID}}:
    name: "{{WORKFLOW_NAME}}"
    version: "1.0"
    description: "{{WORKFLOW_DESCRIPTION}}"
    frequency: "{{FREQUENCY}}"
    avg_duration: "{{TOTAL_DURATION}}"
    created: "{{CREATED_DATE}}"
    last_used: null
    times_executed: 0
    success_rate: 0.0
    phases: {{PHASE_DEFINITIONS}}
    generates:
      - task-breakdown.md
      - timeline.md
      - workflow-tracking.md
    success_criteria: {{SUCCESS_CRITERIA}}
    optimization_notes: []
```

**Update metadata:**
```yaml
metadata:
  stats:
    total_workflows: {{count + 1}}
    active_workflows: {{count + 1}}
```

**Write to file:**
```bash
yq -i ".workflows.${WORKFLOW_ID} = $WORKFLOW_DEF" $REGISTRY
yq -i ".metadata.stats.total_workflows += 1" $REGISTRY
yq -i ".metadata.stats.active_workflows += 1" $REGISTRY
yq -i ".metadata.last_modified = \"$(date +%Y-%m-%d)\"" $REGISTRY
```

---

### Step 10: Success Message

```
═══════════════════════════════════════════════════════
✅ Workflow Created
═══════════════════════════════════════════════════════

Workflow: {{WORKFLOW_NAME}}
ID: {{WORKFLOW_ID}}
Location: .kurt/workflows/workflow-registry.yaml

Summary:
  • {{PHASE_COUNT}} phases defined
  • {{TOTAL_DURATION}} estimated duration
  • {{REVIEW_GATES_COUNT}} review gates
  • {{REQUIRED_RULES_COUNT}} required rules

───────────────────────────────────────────────────────
Next Steps
───────────────────────────────────────────────────────

1. View workflow details:
   workflow-skill show {{WORKFLOW_ID}}

2. Validate workflow:
   workflow-skill validate {{WORKFLOW_ID}}

3. Create project with this workflow:
   /create-project --workflow {{WORKFLOW_ID}}

───────────────────────────────────────────────────────

Would you like to create a project using this workflow now? (y/n): _
```

**If yes:**
```
Great! Let's create your first project with this workflow.
```

Invoke: `/create-project --workflow {{WORKFLOW_ID}}`

**If no:**
```
You can create projects with this workflow anytime using:
  /create-project --workflow {{WORKFLOW_ID}}
```

---

## Error Handling

**If workflow ID already exists:**
```
⚠️  Workflow '{{WORKFLOW_ID}}' already exists

Options:
  a) Choose different name
  b) View existing workflow
  c) Overwrite (creates version 2.0)

Choose: _
```

**If registry file doesn't exist:**
```
⚠️  Workflow registry not found

Creating new registry...
✓ Created .kurt/workflows/workflow-registry.yaml
```

**If template missing:**
```
⚠️  Workflow template not found

Expected: .kurt/workflows/templates/_workflow-template.yaml

Please check your Kurt installation.
```

**If required rules don't exist:**
```
⚠️  Some required rules not found:
  • {{RULE_PATH}}

Options:
  a) Continue anyway (can create rules later)
  b) Create rules now
  c) Cancel workflow creation

Choose: _
```

**If circular dependency detected:**
```
❌ Circular dependency detected

Phase '{{PHASE_A}}' depends on '{{PHASE_B}}'
Phase '{{PHASE_B}}' depends on '{{PHASE_A}}'

This creates an infinite loop. Please fix dependencies.
```

Return to phase configuration.

---

## Phase Detection Patterns

**Common patterns to detect:**

### Tutorial/Blog Post
- Keywords: "publish", "tutorial", "blog", "article", "weekly"
- Phases: topic-selection, outlining, drafting, review, publish

### Product Launch
- Keywords: "launch", "product", "feature", "campaign"
- Phases: research, positioning, content-creation, review, launch

### Documentation Update
- Keywords: "docs", "documentation", "update", "refresh"
- Phases: audit, prioritization, updates, review, publication

### Newsletter
- Keywords: "newsletter", "roundup", "weekly", "monthly"
- Phases: curation, drafting, review, scheduling

### Event Promotion
- Keywords: "event", "webinar", "conference"
- Phases: planning, content-creation, promotion, follow-up

---

## Helper Functions

### Parse Duration
```bash
parse_duration() {
  # Convert "2-3 days", "1 week", etc. to normalized format
  # Return: "2-3 days" (standardized)
}
```

### Detect Circular Dependencies
```bash
detect_circular_deps() {
  # Build dependency graph
  # Run cycle detection algorithm
  # Return: true if circular dependency exists
}
```

### Calculate Timeline
```bash
calculate_timeline() {
  # Consider dependencies
  # Identify critical path
  # Calculate min and max duration
  # Return: "X-Y days/weeks"
}
```

### Validate Rules
```bash
validate_rules() {
  # Check if all required rules exist
  # Return: list of missing rules
}
```

---

*This subskill provides an interactive, guided workflow creation experience that validates everything before saving.*
