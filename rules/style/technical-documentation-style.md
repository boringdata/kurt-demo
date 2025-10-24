# dbt Technical Documentation Style Guide

**Created:** 2025-10-24
**Applies To:** Tutorials, guides, installation docs, technical reference documentation
**Sources:** dbt Fusion quickstart, installation docs, VS Code extension docs

---

## Voice & Tone

### Overall Characteristics

**Professional but Accessible:**
- Speaks to technical practitioners without being overly academic
- Assumes competence but provides necessary context
- Direct and clear, avoiding unnecessary verbosity

**Instructional:**
- Focused on helping users accomplish specific tasks
- Step-by-step when appropriate
- Action-oriented language

**Confident but Not Boastful:**
- Presents capabilities clearly ("significantly improved speed," "blazing speed")
- Backs up claims with specifics ("30x faster," "in seconds")
- Avoids hyperbole in favor of concrete benefits

**Supportive:**
- Acknowledges challenges users may face
- Provides troubleshooting guidance
- Anticipates common questions

---

## Writing Conventions

### Audience Assumptions

**Technical Level:**
- Readers understand basic data warehousing concepts
- Familiar with command-line interfaces
- Know SQL and data modeling fundamentals
- May be new to specific dbt concepts

**Context Awareness:**
- Users often migrating from other tools
- May have production systems they can't disrupt
- Operating under time constraints
- Looking for practical guidance, not theory

### Voice Characteristics

**Use Active Voice:**
- ✅ "The extension integrates with Fusion to provide..."
- ✅ "Verify your installation by running..."
- ❌ "Installation can be verified by running..." (passive)

**Be Direct:**
- ✅ "To complete this guide, you'll need..."
- ✅ "Run the following command:"
- ❌ "It would be advisable to perhaps consider running..."

**Use "You" for Instructions:**
- ✅ "You'll need administrative privileges"
- ✅ "Make sure you have..."
- ✅ "Follow these steps to complete setup"

**Use Present Tense:**
- ✅ "The extension activates automatically"
- ✅ "Fusion handles parallelism differently"
- ❌ "The extension will activate" (future tense adds uncertainty)

---

## Document Structure

### Standard Sections

**1. Title + Introduction:**
- Clear, descriptive title
- Brief (1-2 sentence) overview explaining purpose
- Link to what the doc enables users to do

**2. Prerequisites (when applicable):**
- Bulleted list of requirements
- Technical prerequisites (system access, tools)
- Knowledge prerequisites (understanding of concepts)
- Data platform compatibility

**3. Main Content:**
- Installation steps, configuration guidance, feature explanations
- Organized with clear headings (H2, H3)
- Sequential when order matters

**4. Verification/Next Steps:**
- How to confirm success
- What to do after completing the guide
- Links to related documentation

**5. Troubleshooting (when applicable):**
- Common issues and resolutions
- Where to get help

**6. Additional Resources:**
- Links to related docs
- Community resources
- Advanced topics

---

## Formatting Standards

### Headings

**Use Sentence Case:**
- ✅ "Installation steps"
- ✅ "Setting up your first project"
- ❌ "Installation Steps"
- ❌ "Setting Up Your First Project"

**Be Descriptive:**
- ✅ "Prerequisites" (tells you what's in the section)
- ✅ "Verify installation"
- ❌ "Background" (vague)

### Code Blocks

**Always Specify Language:**
````markdown
```bash
dbtf --version
```

```powershell
irm https://public.cdn.getdbt.com/fs/install/install.ps1 | iex
```
````

**Provide Context:**
- Explain what the command does before showing it
- Include expected output when helpful
- Note platform differences (macOS vs Linux vs Windows)

**Example Pattern:**
```markdown
Verify the installation by checking the version:

```bash
dbtf --version
```
````

### Lists

**Use Bullets for Unordered Items:**
- Requirements
- Features
- Options where order doesn't matter

**Use Numbers for Sequential Steps:**
1. First, install the prerequisites
2. Then, run the installation command
3. Finally, verify the installation

**Keep List Items Parallel:**
- ✅ "Administrative privileges" / "Command-line proficiency" / "Data warehouse account"
- ❌ "Administrative privileges" / "Proficient with command line" / "You need a data warehouse account"

### Links

**Use Descriptive Link Text:**
- ✅ "See the [Fusion upgrade guide](url) for migration steps"
- ✅ "For more information, see [about the dbt extension](url)"
- ❌ "Click [here](url) for more information"

**Reference Other Docs Naturally:**
- Integrate links into sentences
- Provide context about what user will find
- Don't overload with too many links in one paragraph

---

## Technical Terminology

### dbt-Specific Terms

**Use Official Product Names:**
- dbt Core (not "dbt-core" or "dbt core")
- dbt Cloud (not "dbt-cloud")
- dbt Fusion / dbt Fusion Engine (both acceptable)
- VS Code extension (not "VSCode extension" or "vscode extension")

**Commands:**
- Use code formatting: `dbtf` not dbtf
- Show full commands: `dbtf --version` not just "dbtf version"
- Use actual command when explaining: `dbtf init` initializes a project

**Concepts:**
- analytics engineering (lowercase unless starting sentence)
- Jinja (capitalized, it's a proper name)
- CTE (all caps, it's an acronym)
- macros (lowercase)
- models (lowercase)

### Industry Terms

**Be Consistent:**
- data warehouse (not "datawarehouse")
- command line / CLI (both acceptable, pick one per document)
- VS Code (not "vscode" or "VSCode")

**Define When Necessary:**
- First use: "State-Aware Orchestration that rebuilds models only when source data refreshes"
- Subsequent uses: "State-Aware Orchestration"

---

## Common Patterns

### Prerequisites Section

**Template:**
```markdown
## Prerequisites

To complete this guide, you'll need:

- **Category 1 Name**: Specific requirements
- **Category 2 Name**: Specific requirements
- **Category 3 Name**: Specific requirements
```

**Example:**
```markdown
## Prerequisites

To complete this guide, you'll need:

- Understanding of dbt projects, git workflows, and data warehouse requirements
- A supported adapter (BigQuery, Databricks, Redshift, or Snowflake) with compatible authentication
- macOS, Linux, or Windows machine with admin/install privileges
- Visual Studio Code or Cursor installed
```

### Installation Instructions

**Platform-Specific Pattern:**
```markdown
### For macOS & Linux:
```bash
[command]
```

### For Windows (PowerShell):
```powershell
[command]
```
```

**Verification Pattern:**
```markdown
### Verify Installation:
```bash
dbtf --version
```
```

### Feature Descriptions

**Pattern: Capability + Benefit**
- "**Data Preview**: View model results and CTE outputs directly in the editor"
- "**Lineage Visualization**: Explore model-level and column-level dependencies"
- "**SQL Intelligence**: Autocomplete, hover information, and real-time error detection"

Not just: "Data Preview, Lineage Visualization, SQL Intelligence"

### Troubleshooting

**Pattern: Issue + Resolution**
```markdown
## Troubleshooting

Common issues addressed:
- Extension activation problems requiring reinstallation
- Missing LSP features resolved through version updates or LSP reinstallation
- Workspace configuration errors requiring folder addition to workspace
```

---

## Specific Style Choices

### Numbers

**Spell Out vs. Numerals:**
- ✅ Use numerals for version numbers: `version 2.0.0-beta.66`
- ✅ Use numerals for metrics: "30x faster," "99% reduction"
- ✅ Use numerals for steps: "Step 1," "within 14 days"
- ✅ Spell out when starting sentence: "Three main ways to use Fusion"

### Abbreviations

**First Use:**
- Spell out with abbreviation in parentheses: "Command Line Interface (CLI)"
- Subsequent uses: CLI

**Common Abbreviations (no need to spell out):**
- SQL, API, CI/CD, IDE, JSON, YAML

### Emphasis

**Use Bold for:**
- Important callouts: "**Note:** Having a dbt platform user account isn't the same as..."
- UI elements: Click the **Install** button
- Key terms in lists: "**BigQuery** (Service Account/User Token, Native OAuth)"

**Use Italics for:**
- *Rarely used in dbt docs*
- Prefer bold or code formatting instead

**Use Code Formatting for:**
- Commands: `dbtf init`
- File names: `profiles.yml`, `dbt_cloud.yml`
- Directory paths: `~/.dbt/`
- Code snippets: `SELECT * FROM users`

---

## Callouts & Warnings

### Information Callouts

**Pattern:**
```markdown
**Note:** Additional context or important information the user should know.
```

**Example:**
"**Note:** Having a dbt platform user account isn't the same as having a dbt platform project—you don't need a dbt platform project to use the extension."

### Preview/Beta Indicators

**Pattern:**
```markdown
# Install the dbt VS Code extension [Preview]
```

In body text:
"The dbt extension is currently in **Preview**."

---

## Command Documentation

### Format

**Show Platform Variations Clearly:**

```markdown
### For macOS & Linux:
```bash
curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update
exec $SHELL
```

### For Windows (PowerShell):
```powershell
irm https://public.cdn.getdbt.com/fs/install/install.ps1 | iex
Start-Process powershell
```
```

**Explain Before Showing:**
"The guide walks through initializing the 'jaffle_shop' example project:"

Then show the commands.

---

## Examples & Demonstrations

### Use Concrete Examples

**Good:**
"This process loads sample data, creates models, runs tests, and validates the environment."

**Better:**
```markdown
```bash
dbtf init
cd jaffle_shop
dbtf build
```

This process loads sample data, creates models, runs tests, and validates the environment.
```

### Real Project Names

- Use "jaffle_shop" as the example project
- Use realistic file names: `profiles.yml`, `dbt_project.yml`
- Reference actual dbt concepts: models, macros, tests

---

## What to Avoid

### Don't Use:

❌ **Marketing superlatives in technical docs:**
- "Amazing features"
- "Revolutionary approach"
- "Best-in-class solution"

Keep marketing language in marketing materials.

❌ **Uncertain language:**
- "This might work..."
- "You could try..."
- "It should help..."

Be confident and direct.

❌ **Overly casual tone:**
- "Just run this command and you're good to go!"
- "Pretty cool, right?"
- Emoji or exclamation marks (except in community/blog content)

❌ **Condescending explanations:**
- "As you probably know..." (if they need to know, tell them; if not, skip it)
- "Obviously..." (if it's obvious, don't state it)
- "Simply..." or "Just..." (minimizes complexity unfairly)

❌ **Jargon without context:**
- Don't assume everyone knows every acronym
- Define specialized terms on first use
- Link to glossary or reference docs when appropriate

---

## Quality Checklist

Before publishing technical documentation, verify:

- [ ] Title clearly describes the content
- [ ] Introduction states the purpose and audience
- [ ] Prerequisites are listed explicitly
- [ ] Steps are in logical order
- [ ] Code blocks specify language
- [ ] Commands are tested and accurate
- [ ] Platform differences are noted (macOS/Linux/Windows)
- [ ] Links work and point to current documentation
- [ ] Terminology is consistent with dbt standards
- [ ] Verification steps are included
- [ ] Troubleshooting addresses common issues
- [ ] Next steps or related resources are provided

---

## Source Documents

**Examples Analyzed:**
- `/sources/docs.getdbt.com/guides/fusion-quickstart.md`
- `/sources/docs.getdbt.com/docs/fusion/install-fusion.md`
- `/sources/docs.getdbt.com/docs/install-dbt-extension.md`
- `/sources/docs.getdbt.com/docs/fusion/about-fusion.md`

These sources demonstrate dbt Labs' established technical writing style and conventions.
