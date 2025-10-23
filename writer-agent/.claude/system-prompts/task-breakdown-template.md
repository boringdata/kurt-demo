---
# Task Breakdown Template Metadata
template_type: task_breakdown
version: 1.0
created_date: 2025-09-25
last_updated: 2025-09-25
compatible_commands:
  - generate-tasks
generates_output_at: projects/[project-name]/
metadata_includes:
  - project_brief
  - creation_date
  - generation_command
  - template_version
---

# Task Breakdown Template

Use this template when creating task breakdowns in `/projects/[project-name]/task-breakdown.md`. Replace the bracketed placeholders with actual task details.

---
# Task Breakdown Metadata
content_type: task_breakdown
project_name: [project-name]
created_date: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
status: [active/complete]

# Project References
project_brief: /projects/[project-name]/project-brief.md
generation_command: generate-tasks
task_flags: [detailed/assign/etc]
generated_from_brief: [brief-file-path]

# Task Summary
total_tasks: [X]
total_estimated_hours: [X]
critical_path_duration: [X] days
task_categories:
  research_planning: [X] tasks
  content_creation: [X] tasks
  review_refinement: [X] tasks
  production_publishing: [X] tasks

# Resource Planning
primary_assignees:
  - [person-1]
  - [person-2]
external_dependencies:
  - [dependency-1]
  - [dependency-2]

# Timeline
project_start: [YYYY-MM-DD]
project_end: [YYYY-MM-DD]
critical_milestones:
  - [milestone-1]: [date]
  - [milestone-2]: [date]

# Progress Tracking
tasks_not_started: [X]
tasks_in_progress: [X]
tasks_in_review: [X]
tasks_blocked: [X]
tasks_complete: [X]
overall_progress: [X]%

# Risk Assessment
high_risk_tasks: [X]
external_dependency_risks: [X]
resource_conflicts: [X]
mitigation_strategies_defined: [true/false]
---

# [Project Name] - Task Breakdown

**Generated From:** [Path to project brief file]
**Generated:** [Date]
**Project Timeline:** [Start date - End date]
**Total Estimated Hours:** [X] hours
**Critical Path Duration:** [X] days

## Project Overview
**Brief Summary:** [One sentence project description]
**Primary Deliverables:** [X] content assets
**Key Stakeholders:** [Project owner, reviewers, approvers]

## Task Summary by Category

### Research & Planning: [X] tasks, [X] hours
### Content Creation: [X] tasks, [X] hours
### Review & Refinement: [X] tasks, [X] hours
### Production & Publishing: [X] tasks, [X] hours
### Measurement & Optimization: [X] tasks, [X] hours

---

## Task Details by Asset

### Asset: [Asset Name]
*[Brief description of asset and its purpose]*

#### Research & Planning Tasks

##### Task: [Specific Task Name]
- **Task ID:** [asset-abbreviation]-research-01
- **Asset:** [Asset name]
- **Type:** Research
- **Priority:** [Critical / High / Medium / Low]
- **Estimated Hours:** [X] hours
- **Assignee:** [Person responsible or TBD]
- **Due Date:** [Target completion date]
- **Status:** Not Started
- **Dependencies:** [Other task IDs that must complete first, or "None"]
- **Description:** [Specific work to be done - what research, what sources, what questions to answer]
- **Acceptance Criteria:**
  - [Criterion 1: How to verify task completion]
  - [Criterion 2: Quality standard or deliverable]
- **Resources Needed:** [Tools, access, information, or people required]
- **Risk Factors:** [Potential challenges or blockers]

#### Content Creation Tasks

##### Task: [Content Creation Task Name]
- **Task ID:** [asset-abbreviation]-create-01
- **Asset:** [Asset name]
- **Type:** Creation
- **Priority:** [Priority level]
- **Estimated Hours:** [X] hours
- **Assignee:** [Person responsible]
- **Due Date:** [Target completion]
- **Status:** Not Started
- **Dependencies:** [research-01, planning-tasks, etc.]
- **Description:** [Specific creation work - outline, draft, specific sections]
- **Acceptance Criteria:**
  - [Word count target or scope completion]
  - [Quality standards and rule compliance]
  - [Key messages and requirements included]
- **Resources Needed:** [Style guides, templates, research, tools]
- **Deliverables:** [Specific files or documents to produce]

#### Review & Refinement Tasks

##### Task: [Review Task Name]
- **Task ID:** [asset-abbreviation]-review-01
- **Asset:** [Asset name]
- **Type:** Review
- **Priority:** [Priority level]
- **Estimated Hours:** [X] hours
- **Assignee:** [Reviewer name]
- **Due Date:** [Review completion date]
- **Status:** Not Started
- **Dependencies:** [create-01 or other creation tasks]
- **Description:** [Type of review - content, legal, technical, brand compliance]
- **Acceptance Criteria:**
  - [Review completion checklist]
  - [Feedback provided and documented]
  - [Approval status determined]
- **Resources Needed:** [Review guidelines, brand standards, legal requirements]
- **Review Process:** [How feedback will be collected and integrated]

#### Production & Publishing Tasks

##### Task: [Publishing Task Name]
- **Task ID:** [asset-abbreviation]-publish-01
- **Asset:** [Asset name]
- **Type:** Publishing
- **Priority:** [Priority level]
- **Estimated Hours:** [X] hours
- **Assignee:** [Publisher/webmaster]
- **Due Date:** [Go-live date]
- **Status:** Not Started
- **Dependencies:** [All review and approval tasks]
- **Description:** [Platform setup, formatting, publishing, promotion setup]
- **Acceptance Criteria:**
  - [Published and live at correct URL]
  - [Proper formatting and functionality verified]
  - [Promotion/distribution initiated]
- **Resources Needed:** [CMS access, publishing tools, promotion channels]
- **Go-Live Checklist:** [Pre-launch verification steps]

[Repeat task structure for each asset...]

---

## Cross-Asset Tasks

### Project Management Tasks

##### Task: Weekly Project Check-ins
- **Task ID:** proj-mgmt-01
- **Asset:** All assets
- **Type:** Management
- **Priority:** High
- **Estimated Hours:** 1 hour/week
- **Assignee:** [Project manager]
- **Due Date:** Weekly throughout project
- **Status:** Recurring
- **Dependencies:** None
- **Description:** Weekly review of task progress, timeline adjustments, issue resolution
- **Acceptance Criteria:**
  - Status updated for all active tasks
  - Blockers identified and mitigation planned
  - Timeline adjustments communicated to stakeholders

### Quality Assurance Tasks

##### Task: Brand Compliance Review
- **Task ID:** qa-brand-01
- **Asset:** All content assets
- **Type:** Review
- **Priority:** High
- **Estimated Hours:** [X] hours
- **Assignee:** [Brand manager]
- **Due Date:** [Before final publishing]
- **Status:** Not Started
- **Dependencies:** [All content creation tasks complete]
- **Description:** Comprehensive brand voice, messaging, and visual compliance check
- **Acceptance Criteria:**
  - All content aligns with brand guidelines
  - Messaging consistency across assets verified
  - Visual elements comply with brand standards

---

## Project Timeline & Dependencies

### Critical Path
[List the sequence of tasks that determines minimum project duration:]
1. [Task ID] → [Task ID] → [Task ID] → **[Final deliverable]**
2. Estimated critical path duration: **[X] days**

### Parallel Execution Opportunities
**Phase 1 (Days 1-X):** [Tasks that can run simultaneously]
- Task ID, Task ID, Task ID

**Phase 2 (Days X-Y):** [Next parallel phase]
- Task ID, Task ID, Task ID

### Resource Allocation by Week
**Week 1:**
- [Person 1]: [X] hours across [task types]
- [Person 2]: [X] hours across [task types]

**Week 2:**
- [Resource allocation for week 2]

[Continue for project duration...]

### Risk Assessment & Mitigation

#### High-Risk Tasks
**Task ID: [High-risk task]**
- **Risk:** [What could go wrong]
- **Impact:** [Effect on project if risk occurs]
- **Probability:** [High/Medium/Low]
- **Mitigation:** [How to prevent or respond to risk]
- **Contingency:** [Backup plan if risk occurs]

### Dependencies on External Resources
- **[External dependency 1]:** [What's needed, from whom, by when]
- **[External dependency 2]:** [Details and contact information]

---

## Task Status Tracking

### Task Status Legend
- **Not Started:** Task not yet begun
- **In Progress:** Actively being worked on
- **Review:** Submitted for review/approval
- **Blocked:** Cannot proceed due to dependency
- **Complete:** Finished and accepted

### Progress Summary
- **Not Started:** [X] tasks
- **In Progress:** [X] tasks
- **Review:** [X] tasks
- **Blocked:** [X] tasks
- **Complete:** [X] tasks

**Overall Project Progress:** [X]% complete

### Next Actions
1. **Immediate (Next 3 Days):**
   - [Task ID]: [Brief description]
   - [Task ID]: [Brief description]

2. **This Week:**
   - [Task ID]: [Brief description]
   - [Task ID]: [Brief description]

3. **Blockers to Resolve:**
   - [Task ID]: [What's blocking and action needed]

---

## Project Files
- **Project Brief:** `/projects/[project-name]/project-brief.md`
- **Research:** `/projects/[project-name]/research-findings.md`
- **Assets Directory:** `/projects/[project-name]/assets/`
- **Working Files:** `/projects/[project-name]/working-files/`

---
*Generated: [timestamp]*
*From brief: [brief-file-path]*
*Template: .claude/system-prompts/task-breakdown-template.md*
