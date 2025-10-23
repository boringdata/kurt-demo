---
description: Generate task breakdown from project brief
argument-hint: [project-brief-path] [optional: --detailed] [optional: --assign]
---

# Task Generation from Project Brief

## Step 1: Process Arguments
Project brief to analyze: $ARGUMENTS

Parse arguments for:
- Project brief file path (required)
- `--detailed` flag (creates granular sub-tasks)
- `--assign` flag (prompts for task assignments and timeline)

## Step 2: Brief Analysis & Validation
Read the specified project brief file:

**Validate brief structure:**
- Confirm project objectives and timeline are defined
- Verify asset inventory exists with detailed specifications
- Check that production guidelines are clear
- **Verify rule assignments** for each asset:
  - Persona files exist in `rules/personas/`
  - Style files exist in `rules/style/`
  - Structure templates exist in `rules/structure/`
  - Publisher profile exists at `rules/publisher/publisher-profile.md`

**Extract rule assignments from brief:**
- Note which style guide(s) will be used (e.g., technically-writing-style.md)
- Note which persona(s) are targeted (e.g., ai-curious-professional.md)
- Note which structure template(s) apply (e.g., glossary-faq-enhanced.md)

**If brief incomplete or missing rules:**
❓ "The project brief appears incomplete. Missing elements:
- [List missing sections]
- [List missing or unspecified rule files]

Would you like to:
- Update the brief first with `/create-project-brief --update`
- Auto-select appropriate rules based on project type
- Proceed with task generation using available information
- Generate tasks for specific assets only"

## Step 3: Asset-to-Task Breakdown
For each asset in the project brief, generate comprehensive task breakdown:

**Standard Task Categories:**
1. **Research & Planning Tasks**
   - Content research and fact-checking
   - Competitive analysis (if needed)
   - Subject matter expert interviews
   - Asset-specific planning

2. **Content Creation Tasks**
   - Outline development
   - First draft creation
   - Content optimization (SEO, readability)
   - Visual/media requirements

3. **Review & Refinement Tasks**
   - Internal content review
   - Stakeholder feedback integration
   - Legal/compliance review (if needed)
   - Final edit and polish

4. **Production & Publishing Tasks**
   - CMS/platform setup
   - Publishing and formatting
   - Internal linking and cross-promotion
   - Distribution execution

5. **Measurement & Optimization Tasks**
   - Performance tracking setup
   - Initial performance review
   - Optimization recommendations

## Step 4: Dependency Mapping
Analyze task relationships:

**Identify dependencies:**
- **Sequential dependencies** (Task A must complete before Task B)
- **Parallel opportunities** (Tasks that can run simultaneously)
- **Resource conflicts** (Tasks requiring same person/resource)
- **Cross-asset dependencies** (Asset 1 informs Asset 2)

**Critical Path Analysis:**
- Identify longest sequence of dependent tasks
- Flag potential bottlenecks
- Suggest timeline optimization opportunities

## Step 5: Task Assignment & Timeline (Optional)
**If `--assign` flag used:**

❓ **Resource Planning Questions:**
- Who is the primary content creator for this project?
- Are there specific reviewers or approvers required?
- What's the target completion date for the full project?
- Are there any fixed deadlines or external constraints?
- Do any tasks require external resources (design, dev, legal)?

**Auto-suggest task assignments based on:**
- Task type and skill requirements
- Workload balancing across timeline
- Standard review/approval workflows

## Step 6: Task Document Creation
Read the task breakdown template from `.claude/system-prompts/task-breakdown-template.md` and create comprehensive task plan.

**Create task tracking structure:**
```
/projects/[project-name]/
├── project-brief.md              # Strategic document (unchanged)
├── task-breakdown.md             # Operational tasks (new)
├── research-findings.md          # Research insights
└── assets/                       # Content files
    └── [individual assets...]
```

**Task format for each item:**
```markdown
### Task: [Descriptive Task Name]
- **Task ID:** [unique-identifier]
- **Asset:** [Which asset this supports]
- **Type:** [Research / Creation / Review / Publishing / Measurement]
- **Group:** [Optional: batch-group-name for related tasks]
- **Priority:** [Critical / High / Medium / Low]
- **Estimated Hours:** [Time estimate]
- **Assignee:** [Person responsible]
- **Due Date:** [Target completion]
- **Status:** [Not Started / In Progress / Review / Complete]
- **Dependencies:** [Other tasks that must complete first]
- **Description:** [Specific work to be done]
- **Acceptance Criteria:** [How to know task is complete]
- **Resources Needed:** [Tools, access, information required]
- **Rule Files:** [List applicable rules from the project brief]
  - Style: @rules/style/[file].md
  - Persona: @rules/personas/[file].md
  - Structure: @rules/structure/[file].md
```

**Task Group Definition (for batch operations):**
```markdown
## Task Groups
### Group: phase-1-outlines
**Description:** All outline creation tasks for Phase 1 glossary terms
**Tasks:** llm-create-01, inf-create-01, rag-create-01, tok-create-01...
**Execution Strategy:** Can be executed in parallel by same person

### Group: phase-2-content
**Description:** All content creation for new glossary terms
**Tasks:** agent-create-01, prompt-create-01, context-create-01...
**Execution Strategy:** Sequential by priority, batch processable
```

## Step 7: Timeline Optimization
**If `--detailed` flag used:**

Analyze the generated task list for optimization opportunities:

**Timeline Analysis:**
- Total estimated hours vs available time
- Resource utilization and potential conflicts
- Critical path bottlenecks
- Parallel execution opportunities

**Optimization Recommendations:**
- Tasks that could be combined for efficiency
- Dependencies that could be relaxed
- Resources that could accelerate delivery
- Risk mitigation for critical path items

## Step 8: Task Review & Finalization
Present the task breakdown for review:

❓ **Task Review:**
"I've generated [X] tasks across [Y] categories for this project:
- **Critical path:** [X] days with [key bottleneck tasks]
- **Total estimated hours:** [X] hours across [Y] people
- **Key dependencies:** [Major blocking relationships]

Would you like to:
- **Proceed with task breakdown as-is**
- **Adjust task assignments or timeline**
- **Modify task granularity (more/fewer tasks)**
- **Export to external project management tool**
- **Begin task execution**"

## Usage Examples

```bash
# Basic task generation
/generate-tasks @projects/product-launch/project-brief.md

# Detailed task breakdown with timeline optimization
/generate-tasks @projects/content-series/project-brief.md --detailed

# Include assignment planning
/generate-tasks @projects/seo-hub/project-brief.md --assign --detailed

# Quick task generation for single asset
/generate-tasks @projects/blog-series/project-brief.md asset:introduction-post
```

## Success Indicators
**A complete task breakdown should include:**
- ✅ Comprehensive tasks for each asset in the brief
- ✅ Clear dependencies and critical path identified
- ✅ Realistic time estimates and resource allocation
- ✅ Specific acceptance criteria for each task
- ✅ Actionable next steps for project execution
- ✅ Risk identification and mitigation strategies
