---
name: writing-rules
description: Extract and manage writing rules (style, structure, persona, publisher, custom) (project)
---

# Writing Rules Skill

**Purpose:** Unified system for extracting writing rules AND managing the rule type registry
**Operations:** Extraction (style, structure, persona, publisher, custom) + Management (list, show, add, validate, generate, onboard)
**Output:** Rule files in `rules/` directories + rules-config.yaml registry

---

## Usage

### Extraction Operations

```bash
# Extract built-in rule types
writing-rules-skill style --type corporate --auto-discover
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill persona --audience-type technical --auto-discover
writing-rules-skill publisher --auto-discover

# Extract custom rule types (after adding them)
writing-rules-skill verticals --type healthcare --auto-discover
writing-rules-skill use-cases --type migration with documents: <paths>
```

### Management Operations

```bash
# List all rule types (built-in + custom)
writing-rules-skill list

# Show details about a rule type
writing-rules-skill show verticals

# Add new custom rule type (interactive with conflict detection)
writing-rules-skill add

# Validate registry configuration
writing-rules-skill validate

# Generate extraction subskill for custom type
writing-rules-skill generate-subskill verticals

# Onboarding wizard for new teams
writing-rules-skill onboard
```

---

## Preview Mode for Iterative Extraction

**When invoked from iterative rule extraction**, use preview mode before executing extractions:

### Pattern: Analyze → Preview → Approve → Extract

1. **Analyze available content:**
   - List all indexed documents
   - Group by domain, content type, date range
   - Identify which rule types are possible

2. **Preview documents before extraction:**
   ```
   **Propose: Extract Technical Documentation Style**

   Sample documents I'll analyze (5 of 30):
   1. docs.example.com/api/authentication - "Authentication API"
   2. docs.example.com/concepts/architecture - "Architecture Overview"
   3. docs.example.com/guides/deployment - "Deployment Guide"
   4. docs.example.com/reference/cli - "CLI Reference"
   5. docs.example.com/troubleshooting - "Troubleshooting"

   **Coverage:**
   - 30 pages from /docs/*
   - Content types: API reference, guides, concepts
   - Technical depth: High (developer-focused)

   **What I'll extract:**
   - Technical writing patterns
   - Example usage patterns
   - Warning and note styles
   - Code snippet formatting

   Extract from these documents? (Y/n)
   > Or: "Use different documents" / "Skip for now"
   ```

3. **Handle user response:**
   - **Approve**: Execute extraction with `--auto-discover`
   - **Refine**: User requests different documents → Adjust and re-preview
   - **Skip**: Move to next rule type

4. **After extraction, show what was created:**
   ```
   **Extraction Complete: Technical Documentation Style**

   ✓ Created: rules/style/technical-documentation.md

   **Key characteristics extracted:**
   - Tone: Professional, direct, precise
   - Structure: Short paragraphs, clear headings
   - Examples: Code-heavy with inline comments
   - Technical depth: High (assumes developer knowledge)

   This rule will be applied to technical content you create.
   ```

### Why Preview Mode?

- User sees which documents will be analyzed before API calls
- Prevents extracting from wrong/irrelevant content
- Allows content selection refinement
- Builds confidence in extraction quality
- Transparent about what's being used

### When to Use

- **Use preview mode**: When invoked from `/create-project` or `/resume-project` via iterative rule extraction module
- **Direct execution**: When user calls `writing-rules-skill <type> --auto-discover` directly (no preview, immediate execution)

---

## Routing Logic

This skill routes based on the first argument:

**Management Operations (hardcoded):**
- `list` → subskills/manage-list.md
- `show` → subskills/manage-show.md
- `add` → subskills/manage-add.md
- `validate` → subskills/manage-validate.md
- `generate-subskill` → subskills/manage-generate-subskill.md
- `onboard` → subskills/manage-onboard.md

**Extraction Operations (loaded dynamically from rules/rules-config.yaml):**
- Each enabled rule type → subskills/{extraction.subskill}
- Built-in types: `style`, `structure`, `persona`, `publisher`
- Custom types: Any additional types defined in registry
- Path construction: `subskills/` + `rule_types[{type}].extraction.subskill`
- Only enabled types are routable

**Dynamic routing benefits:**
- No code changes needed to add new rule types
- Registry is single source of truth
- Automatic validation and error handling
- Extensible system for team customization

---

## Step 1: Parse Arguments

Extract first argument and remaining arguments: $ARGUMENTS

**Argument categories:**

**Management operations** (no registry loading needed):
- `list`, `show`, `add`, `validate`, `generate-subskill`, `onboard`
- These operations manage the registry itself

**Extraction operations** (require registry loading):
- Built-in: `style`, `structure`, `persona`, `publisher`
- Custom: Any rule type defined in rules-config.yaml

**Parsing logic:**
1. Extract first argument → `$OPERATION`
2. Extract remaining arguments → `$REMAINING_ARGS`
3. Determine operation category (management vs extraction)

**If no arguments:**
Show usage help with both management and extraction operations.

---

## Step 2: Determine Operation Type and Load Context

### Check Operation Type

**If `$OPERATION` IN [list, show, add, validate, generate-subskill, onboard]:**
- Operation type: **Management**
- Skip to Step 3 (Route to Management Subskill)
- Management operations will load registry as needed within their subskills

**Else (extraction operation):**
- Operation type: **Extraction**
- Continue with context loading below

### Load Rules Registry (for extraction operations)

```bash
# Load rules-config.yaml
registry_file="rules/rules-config.yaml"

if [ ! -f "$registry_file" ]; then
  error "Rules registry not found. Run 'writing-rules-skill validate' to check setup."
  exit 1
fi

# Parse YAML to extract all rule types
# This creates a dynamic list of available operations
all_rule_types=$(yq '.rule_types | keys | .[]' "$registry_file")

# Get enabled rule types only
enabled_rule_types=$(yq '.rule_types | to_entries | .[] | select(.value.enabled == true) | .key' "$registry_file")

# Check if $OPERATION is in enabled_rule_types
if ! echo "$enabled_rule_types" | grep -q "^${OPERATION}$"; then
  # Operation not found or disabled
  error "Unknown or disabled rule type: '$OPERATION'"
  echo ""
  echo "Available enabled rule types:"

  # Dynamically list enabled types with descriptions
  for type in $enabled_rule_types; do
    name=$(yq ".rule_types.${type}.name" "$registry_file")
    is_builtin=$(yq ".rule_types.${type}.built_in" "$registry_file")

    if [ "$is_builtin" = "true" ]; then
      echo "  • $type - $name (built-in)"
    else
      echo "  • $type - $name (custom)"
    fi
  done

  echo ""
  echo "To see all rule types: writing-rules-skill list"
  echo "To add new rule type: writing-rules-skill add"
  exit 1
fi

# Load rule type configuration
rule_type_config=$(yq ".rule_types.${OPERATION}" "$registry_file")

# Extract key fields
rule_type_name=$(echo "$rule_type_config" | yq '.name')
rule_type_directory=$(echo "$rule_type_config" | yq '.directory')
rule_type_subskill=$(echo "$rule_type_config" | yq '.extraction.subskill')
rule_type_is_builtin=$(echo "$rule_type_config" | yq '.built_in')

# Construct subskill path dynamically
subskill_path=".claude/skills/writing-rules-skill/subskills/${rule_type_subskill}"

# Validate subskill file exists
if [ ! -f "$subskill_path" ]; then
  error "Extraction subskill not found for '$OPERATION'"
  echo ""
  echo "The rule type '$OPERATION' is defined in the registry but no extraction subskill exists."
  echo "Expected: $subskill_path"
  echo ""

  if [ "$rule_type_is_builtin" = "false" ]; then
    echo "Generate one with: writing-rules-skill generate-subskill $OPERATION"
  else
    echo "This is a built-in type - the subskill should exist. Run: writing-rules-skill validate"
  fi

  exit 1
fi
```

**What this accomplishes:**
- Dynamically loads all rule types from registry (no hardcoding)
- Validates operation against registry in real-time
- Constructs subskill path from registry configuration
- Provides helpful error messages with actual available types
- Distinguishes between built-in and custom types in errors

### Load Project Context (for extraction operations)
- Check if we're in a project context
- Locate current project directory (if exists)
- Read project.md for context about sources and targets

### Check Source Content Status (for extraction operations)
- Are sources fetched? (files in `/sources/`)
- Are sources indexed? (metadata extracted via `kurt index`)

### Load Existing Rules (for extraction operations)
Check what's already been extracted for this rule type:
- Get directory from registry: `registry.rule_types[$OPERATION].directory`
- List existing rule files in `rules/{directory}/`
- Note which discovery modes have been extracted

---

## Step 3: Route to Subskill

### Management Operations

**For `list`:**
Invoke subskills/manage-list.md
- No arguments needed
- Loads registry and displays all rule types

**For `show`:**
Invoke subskills/manage-show.md with arguments:
- Rule type name (required)
- Loads registry and displays detailed information

**For `add`:**
Invoke subskills/manage-add.md
- Interactive wizard (no arguments)
- Runs conflict detection
- Updates registry

**For `validate`:**
Invoke subskills/manage-validate.md
- No arguments needed
- Validates registry and file system
- Reports errors and warnings

**For `generate-subskill`:**
Invoke subskills/manage-generate-subskill.md with arguments:
- Rule type name (required)
- Generates extraction subskill from template

**For `onboard`:**
Invoke subskills/manage-onboard.md
- Interactive wizard (no arguments)
- Guides user through rule type configuration

### Extraction Operations

**Dynamic routing based on registry:**

```bash
# Subskill path was constructed dynamically in Step 2
# $subskill_path = ".claude/skills/writing-rules-skill/subskills/${rule_type_subskill}"

# Invoke the subskill with full context
invoke $subskill_path with:
  - RULE_TYPE: $OPERATION
  - RULE_TYPE_CONFIG: $rule_type_config (full config from registry)
  - REMAINING_ARGS: $REMAINING_ARGS
  - RULES_DIR: rules/${rule_type_directory}/
  - EXISTING_RULES: <files in rules directory>
  - PROJECT_CONTEXT: <project context if available>
  - SOURCES_STATUS: <fetch/index status>
```

**All extraction operations support:**
- Type-specific flags (discovery modes defined in registry)
- Auto-discovery flag (--auto-discover)
- Manual document selection (with documents: <paths>)
- Optional overwrite flag (--overwrite)
- Include/exclude patterns (--include, --exclude)

**Built-in types** (style, structure, persona, publisher):
- Have pre-built extraction subskills
- Support their documented discovery modes
- Maintained as part of core system

**Custom types** (any enabled type in registry):
- Generated from template via `generate-subskill`
- Support discovery modes defined during creation
- Fully extensible by teams

**Error handling is already done in Step 2:**
- Registry validation ensures rule type exists and is enabled
- Subskill existence check ensures file is present
- Helpful error messages guide users to solutions

---

## Step 4: Context Handoff

Pass the following to subskills:

### For Management Subskills

**Registry Context:**
```
REGISTRY_PATH: rules/rules-config.yaml
RULES_BASE_DIR: rules/
SUBSKILLS_DIR: .claude/skills/writing-rules-skill/subskills/
OPERATION: <management-operation>
ARGUMENTS: <remaining-args>
```

Management subskills will load registry as needed within their own logic.

### For Extraction Subskills

**Shared Context:**
```
PROJECT_NAME: <name> (if in project context)
PROJECT_PATH: /projects/<name>/ (if applicable)
PROJECT_BRIEF: /projects/<name>/project.md (if applicable)
REGISTRY_PATH: rules/rules-config.yaml
RULE_TYPE: <extraction-rule-type>
RULE_TYPE_CONFIG: <config-from-registry>
RULES_DIR: rules/<directory-for-this-type>/
EXISTING_RULES: <list of existing rule files for this type>
SOURCES_STATUS: fetched|not_fetched|indexed|not_indexed
ARGUMENTS: <remaining-args>
```

**Content Paths:**
```
SOURCES_PATH: /sources/ (organizational knowledge base)
PROJECT_SOURCES_PATH: /projects/<name>/sources/ (if applicable)
```

---

## Step 5: Prerequisites Validation

All rule extraction requires content to be **fetched + indexed**:

### Check Fetch Status
```bash
# Verify sources are downloaded to /sources/
kurt document list --url-prefix <url> --status FETCHED
```

### Check Index Status
```bash
# Verify metadata has been extracted
kurt document get <url>
# Should show: title, topics, entities, indexed_at
```

### If Not Ready
```
⚠️ Content must be fetched + indexed before extraction

Sources not fetched:
  - https://example.com/page1
  - https://example.com/page2

Run: kurt ingest fetch --url-prefix <url>

Sources fetched but not indexed:
  - /sources/example.com/page3.md
  - /sources/example.com/page4.md

Run: kurt index --url-prefix <url>

Once complete, retry extraction.
```

---

## Error Handling

**If operation is invalid:**
```
Error: Unknown or disabled rule type: 'invalid-type'

Available enabled rule types:
  • style - Style Guidelines (built-in)
  • structure - Structure Templates (built-in)
  • persona - Target Personas (built-in)
  • publisher - Publisher Profile (built-in)
  • verticals - Industry Verticals (custom)
  • channels - Channel Guidelines (custom)

To see all rule types: writing-rules-skill list
To add new rule type: writing-rules-skill add
```

**Note:** The list of available types is generated dynamically from the registry, so it always reflects the current system configuration including custom types.

**Management operations help:**
```
Usage: writing-rules-skill <operation> [arguments]

Extraction Operations:
  [Dynamically loaded from registry]

Management Operations:
  list                - Display all available rule types
  show <type>         - Show details about a rule type
  add                 - Create new custom rule type
  validate            - Check system health
  generate-subskill   - Generate extraction subskill
  onboard             - Setup wizard for new teams

Examples:
  writing-rules-skill style --type corporate --auto-discover
  writing-rules-skill list
  writing-rules-skill add
```

**If sources not ready:**
```
Error: Sources not ready for extraction

Requirements:
  ✓ Content must be fetched (files in /sources/)
  ✓ Content must be indexed (metadata extracted)

Current status: <fetch status> / <index status>

Next steps:
  1. Fetch content: kurt ingest fetch --url-prefix <url>
  2. Index content: kurt index --url-prefix <url>
  3. Retry extraction: writing-rules-skill <subskill> ...
```

**If project context missing (when needed):**
```
Warning: No project context found

Rule extraction will create global rules in rules/.
These will be available to all projects.

Continue? (Y/n)
```

---

## Success Indicators

✅ **Skill invoked successfully** when:
- Subskill identified and routed correctly
- Prerequisites validated (content fetched + indexed)
- Shared context loaded and validated
- Subskill execution completes
- Output includes rule files in `rules/` directories

✅ **Rule extraction complete** when:
- New rule file(s) created in appropriate `rules/` subdirectory
- Rule files include proper YAML frontmatter
- Source documents tracked in rule metadata
- Extraction date and method documented
- Rule characteristics clearly defined

---

## Integration with Other Skills

This skill is invoked by:
- **project-management-skill**: When validating rule coverage for content work
- **create-project command**: During project setup to extract foundation rules
- **resume-project command**: When gaps in rule coverage are detected

This skill creates rules used by:
- **content-writing-skill**: Applies rules during outline/draft/edit operations
- **project-management-skill**: Validates rule coverage before content work

---

## Next Steps After Invocation

After successful subskill execution, suggest next steps:

**After style extraction:**
```
✅ Style extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> style pattern(s) identified

📝 Style guide(s) created:
   - <filename>.md

Next steps:
  1. Review style guide characteristics
  2. Extract other rule types if needed (structure, persona, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After structure extraction:**
```
✅ Structure extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> structural pattern(s) identified

📝 Structure template(s) created:
   - <filename>.md

Next steps:
  1. Review structure template sections and flow
  2. Extract other rule types if needed (style, persona, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After persona extraction:**
```
✅ Persona extraction complete

📊 Analysis:
   - <count> documents analyzed
   - <count> distinct persona(s) identified

📝 Persona profile(s) created:
   - <filename>.md

Next steps:
  1. Review persona characteristics and needs
  2. Extract other rule types if needed (style, structure, publisher)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

**After publisher extraction:**
```
✅ Publisher profile extraction complete

📊 Sources analyzed:
   - <count> web pages
   - <count> local documents

📝 Profile action: <Created new|Updated existing> profile
   Location: rules/publisher/publisher-profile.md

Next steps:
  1. Review organizational identity and messaging
  2. Extract other rule types if needed (style, structure, persona)
  3. Use in content creation: content-writing-skill outline/draft <project> <asset>
```

---

## Workflow Examples

### Example 1: Extract Foundation Rules for New Project

Use the Skill tool to extract rules in this order:

**Step 1: Extract publisher profile (company context)**
`writing-rules publisher --auto-discover`

**Step 2: Extract corporate voice (brand style)**
`writing-rules style --type corporate --auto-discover`

**Step 3: Extract content-specific rules based on targets**
`writing-rules structure --type tutorial --auto-discover`
`writing-rules persona --audience-type technical --auto-discover`

Now ready for content creation with full rule coverage.

### Example 2: Extract Rules for Specific Content Type

Use the Skill tool to extract blog-specific rules:

**Need to create blog posts in new voice:**
`writing-rules style --type blog --auto-discover`
`writing-rules structure --type blog-post --auto-discover`
`writing-rules persona --audience-type business --auto-discover`

### Example 3: Update Existing Rules

Use the Skill tool to update rules:

**Company rebrand - update publisher profile:**
`writing-rules publisher --auto-discover --overwrite`

**New blog author - extract their voice:**
`writing-rules style --type author --author-name "Jane Smith" --auto-discover`

---

*This is the main entry point for the writing-rules-skill. It provides unified routing to style, structure, persona, and publisher extraction subskills with comprehensive validation and context loading capabilities.*
