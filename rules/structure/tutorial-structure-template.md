# dbt Tutorial Structure Template

**Created:** 2025-10-24
**Applies To:** Quickstart guides, getting started tutorials, installation guides
**Sources:** Fusion quickstart, installation docs, VS Code extension setup guide

---

## Overview

dbt tutorials follow a consistent structure that:
- Sets clear expectations upfront (prerequisites)
- Provides step-by-step instructions
- Includes verification steps
- Addresses common problems (troubleshooting)
- Points to next steps and related resources

This template provides the standard structure for dbt technical tutorials.

---

## Standard Tutorial Structure

### 1. Title + Introduction

**Format:**
```markdown
# [Action-Oriented Title]

## Introduction

[1-3 paragraphs explaining what this tutorial covers, what users will accomplish, and why it matters]
```

**Guidelines:**
- **Title**: Use clear, action-oriented language
  - ✅ "Quickstart for the dbt Fusion Engine"
  - ✅ "Install the dbt VS Code extension"
  - ❌ "About Installation" (not action-oriented)

- **Introduction**: Briefly cover:
  - What the technology/feature is
  - What the tutorial will teach
  - What users will be able to do after completing it

**Example:**
```markdown
# Quickstart for the dbt Fusion Engine

## Introduction

The dbt Fusion Engine represents "a powerful new approach to classic dbt ideas" built entirely in Rust. It enables developers to compile and execute dbt projects with significantly improved speed—often completing tasks in seconds.

This guide walks you through installing Fusion and setting up your first project using the command line and VS Code extension.
```

---

### 2. Availability / Context (Optional)

**When to Include:**
- Preview/Beta features
- Platform-specific availability
- Version requirements

**Format:**
```markdown
### Availability

[Feature] is currently accessible through:
- [Environment 1] (Status)
- [Environment 2] (Status)
- [Environment 3] (Status)
```

**Example:**
```markdown
### Availability

Fusion is currently accessible through three environments:
- Local command line interface (Preview)
- VS Code and Cursor with dbt extension (Preview)
- dbt platform environments (Private preview)
```

---

### 3. Prerequisites

**Format:**
```markdown
## Prerequisites

To complete this guide, you'll need:

- [Requirement 1 with details]
- [Requirement 2 with details]
- [Requirement 3 with details]
```

**Categories to Include:**

**Knowledge/Skills:**
- Understanding of relevant concepts
- Familiarity with tools (command line, git, etc.)

**System Requirements:**
- Operating system compatibility
- Admin/install privileges
- Specific software installed

**Data Platform:**
- Supported adapters
- Authentication methods
- Account requirements

**Example (Simple List):**
```markdown
## Prerequisites

To complete this guide, you'll need:

- Understanding of dbt projects, git workflows, and data warehouse requirements
- A supported adapter (BigQuery, Databricks, Redshift, or Snowflake) with compatible authentication
- macOS, Linux, or Windows machine with admin/install privileges
- Visual Studio Code or Cursor installed
```

**Example (Table Format for Complex Prerequisites):**
```markdown
## Prerequisites

To use the extension, you must meet the following prerequisites:

| Prerequisite | Details |
|---|---|
| **dbt Fusion Engine** | Version 2.0.0-beta.66 or higher installed |
| **Registration** | After installation, use for 14 days then register |
| **Project files** | `profiles.yml` configuration file required |
| **Editor** | VS Code or Cursor code editor |
| **Operating systems** | macOS (X86-64, ARM), Linux (X86-64, ARM), Windows (X86-64) |
```

**Guidelines:**
- Be specific (not "a data warehouse" but "BigQuery, Databricks, Redshift, or Snowflake")
- Group related items with bold category labels
- Note platform differences when relevant
- Link to setup guides for complex prerequisites

---

### 4. Installation Steps / Main Content

**Format:**
```markdown
## [Installation Steps / Setup Instructions / Main Task]

[Brief introduction to this section]

### [Step 1 Name]

[Instructions for step 1]

### [Step 2 Name]

[Instructions for step 2]
```

**Guidelines:**

**Use Platform-Specific Subsections When Needed:**
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

**Include Verification Steps:**
```markdown
### Verify Installation:
```bash
dbtf --version
```
```

**Explain Commands:**
- Don't just show code—explain what it does
- Mention expected outcomes
- Note if something takes time to complete

**Example:**
```markdown
## Installation Steps

### For macOS & Linux:
Run the following installation script:

```bash
curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update
exec $SHELL
```

### Verify Installation:
Check that Fusion installed correctly:

```bash
dbtf --version
```

You should see version 2.0.0 or higher.
```

---

### 5. Feature Overview / Usage Guidance (Optional)

**When to Include:**
- After installation, show key features
- When there's immediate value to demonstrate
- To guide next steps after setup

**Format:**
```markdown
## [Feature Name] Features

The [tool/extension/feature] provides:

- **[Feature 1]**: [Brief description of what it does]
- **[Feature 2]**: [Brief description of what it does]
- **[Feature 3]**: [Brief description of what it does]
```

**Example:**
```markdown
## VS Code Extension Features

The dbt extension integrates with Fusion to provide:

- **Data Preview**: View model results and CTE outputs directly in the editor
- **Lineage Visualization**: Explore model-level and column-level dependencies
- **SQL Intelligence**: Autocomplete, hover information, and real-time error detection
- **Command Execution**: Run dbt commands with blazing speed through the IDE
```

---

### 6. Getting Started / First Project (Optional)

**When to Include:**
- Quickstart guides
- When there's a "hello world" equivalent
- To show immediate value

**Format:**
```markdown
## [Setting Up Your First Project / Getting Started]

[Brief introduction]

[Step-by-step walkthrough of first task]
```

**Example:**
```markdown
## Setting Up Your First Project

The guide walks through initializing the "jaffle_shop" example project:

```bash
dbtf init
cd jaffle_shop
dbtf build
```

This process loads sample data, creates models, runs tests, and validates the environment.
```

---

### 7. Troubleshooting

**Format:**
```markdown
## Troubleshooting

[Optional intro paragraph]

Common issues addressed:
- [Issue 1] requiring [resolution]
- [Issue 2] resolved through [solution]
- [Issue 3] requiring [fix]
```

**Alternative Format (Detailed):**
```markdown
## Troubleshooting

If you run into any issues, check the common problems below.

### [Issue 1 Name]

**Symptoms:** [What the user sees]
**Solution:** [How to fix it]

### [Issue 2 Name]

**Symptoms:** [What the user sees]
**Solution:** [How to fix it]
```

**Guidelines:**
- List most common issues first
- Be specific about symptoms users will see
- Provide clear resolution steps
- Link to support resources if needed

**Example:**
```markdown
## Troubleshooting

Common issues addressed:
- Extension activation problems requiring reinstallation
- Missing LSP features resolved through version updates or LSP reinstallation
- Workspace configuration errors requiring folder addition to workspace
- Unsupported dbt version errors requiring path verification
```

---

### 8. Additional Resources / Next Steps

**Format:**
```markdown
## [Additional Resources / Next Steps / Related Documentation]

[Optional brief intro]

- [Link 1 with context]
- [Link 2 with context]
- [Link 3 with context]
```

**Guidelines:**
- Group related links together
- Provide context for each link (what will users find there?)
- Order by relevance to current tutorial
- Include both next steps and reference docs

**Example:**
```markdown
## Additional Resources

The documentation references comprehensive guides for:

- [Upgrading to Fusion](link) - Migrate existing dbt Core projects
- [Supported Features](link) - Complete feature compatibility matrix
- [Licensing Information](link) - Understanding Fusion license terms
- [About dbt Extension](link) - Deep dive into VS Code extension capabilities
```

---

## Complete Template

```markdown
# [Action-Oriented Title]

## Introduction

[1-3 paragraphs: What is this? What will users learn? Why does it matter?]

### Availability (Optional)

[Where/how is this feature available? What's the status?]

## Prerequisites

To complete this guide, you'll need:

- [Knowledge/skill requirement]
- [System requirement]
- [Platform/account requirement]
- [Software requirement]

## [Installation / Setup / Main Task]

[Brief introduction to this section]

### For [Platform 1]:
```bash
[commands]
```

### For [Platform 2]:
```powershell
[commands]
```

### Verify [Installation/Setup]:
```bash
[verification command]
```

## [Feature Overview / Usage] (Optional)

The [tool] provides:

- **[Feature 1]**: [Description]
- **[Feature 2]**: [Description]
- **[Feature 3]**: [Description]

## [Getting Started / First Task] (Optional)

[Walk through a simple first task]

```bash
[example commands]
```

[Explanation of what happens]

## Troubleshooting

Common issues addressed:
- [Issue 1] requiring [solution]
- [Issue 2] resolved through [fix]
- [Issue 3] requiring [action]

## Additional Resources

[Optional intro]

- [Link with context]
- [Link with context]
- [Link with context]
```

---

## Tutorial Types & Variations

### Quickstart Tutorial

**Focus:** Get users up and running quickly
**Includes:** All sections, with emphasis on "Getting Started / First Project"
**Length:** Medium (800-1200 words)

**Example:** Fusion Quickstart

---

### Installation Guide

**Focus:** Detailed setup instructions
**Includes:** Heavy emphasis on Prerequisites, Installation Steps, Verification
**May Skip:** Feature overview (covered elsewhere), First project
**Length:** Short-Medium (500-800 words)

**Example:** Install Fusion CLI

---

### Feature Setup Guide

**Focus:** Configure a specific feature
**Includes:** Prerequisites, Setup steps, Feature overview, Usage examples
**Emphasis on:** Configuration and usage patterns
**Length:** Medium-Long (1000-1500 words)

**Example:** Install VS Code Extension (includes registration, upgrade tool)

---

### Platform-Specific Quickstart

**Focus:** Get started with dbt on a specific data platform
**Includes:** Platform setup, dbt installation, first project, platform-specific considerations
**Emphasis on:** Integration points and platform differences
**Length:** Medium-Long (1200-1800 words)

**Example:** BigQuery Quickstart, Snowflake Quickstart

---

## Content Principles

### Progressive Disclosure

Start simple, add complexity gradually:
1. Basic installation
2. Verification
3. First simple task
4. Feature exploration
5. Advanced configuration (link to separate doc)

### Accessibility

- Provide options for different platforms (macOS/Linux/Windows)
- Note different authentication methods
- Acknowledge multiple valid paths
- Link to alternative approaches

### Validation

Always include verification steps:
- After installation: version check
- After configuration: connection test
- After first task: expected output

### Safety

Guide users toward success:
- Clear prerequisites prevent wasted time
- Troubleshooting catches common errors
- Verification confirms each step

---

## Writing Tips

### Do:
- Use descriptive section headings
- Provide code examples with explanations
- Include verification steps after major actions
- Address platform differences explicitly
- Link to related documentation
- Anticipate common questions

### Don't:
- Assume knowledge not listed in prerequisites
- Skip verification steps
- Leave users hanging (always have "next steps")
- Hide platform differences in footnotes
- Over-explain obvious UI interactions
- Write steps out of order

---

## Quality Checklist

- [ ] Title clearly states what user will accomplish
- [ ] Introduction explains purpose and value
- [ ] Prerequisites are complete and specific
- [ ] Steps are in logical order
- [ ] Platform differences are addressed
- [ ] Commands are tested and accurate
- [ ] Verification steps are included
- [ ] Common issues have troubleshooting guidance
- [ ] Next steps / related resources are provided
- [ ] Links are tested and current

---

## Source Examples

**Analyzed Tutorials:**
- **Fusion Quickstart**: `/sources/docs.getdbt.com/guides/fusion-quickstart.md`
  - Comprehensive quickstart with all elements
  - Example of "getting started" section

- **Install Fusion**: `/sources/docs.getdbt.com/docs/fusion/install-fusion.md`
  - Installation-focused guide
  - Table format for complex prerequisites

- **Install VS Code Extension**: `/sources/docs.getdbt.com/docs/install-dbt-extension.md`
  - Feature setup guide with multiple workflows
  - Registration and upgrade processes
  - Detailed troubleshooting

These examples demonstrate dbt Labs' established tutorial structure and organization patterns.
