---
description: Universal task executor that handles any task type
argument-hint: [task-breakdown-path] [task-selector-or-instruction] [optional: --interactive] [optional: --batch]
---

# Universal Task Executor

## Step 1: Process Arguments
Task to execute: $ARGUMENTS

Parse arguments for:
- Task breakdown file path (required)
- Task selector/instruction (required) - can be:
  - Specific task ID (e.g., `llm-create-01`)
  - Pattern match (e.g., `*-create-*` for all creation tasks)
  - Task type (e.g., `type:creation` for all creation tasks)
  - Task group (e.g., `group:phase-1-outlines`)
  - Natural language instruction (e.g., `"outline all glossary terms"`)
- `--interactive` flag (enables guided execution with prompts)
- `--batch` flag (processes multiple tasks in sequence)

## Step 2: Task Selection & Analysis

### Natural Language Processing
**If natural language instruction provided:**
1. Analyze the instruction to understand intent
2. Scan task breakdown for matching tasks
3. Present matching tasks for confirmation

Example: `"outline all glossary terms"`
→ Finds all tasks with type:creation and containing "outline" or "FAQ"
→ Groups them by phase or priority
→ Confirms selection before proceeding

### Pattern Matching
**If pattern or selector provided:**
- `*-create-*`: Match all task IDs containing "create"
- `type:creation`: Match all tasks with Type: Creation
- `group:phase-1`: Match all tasks in specified group
- `status:not-started priority:high`: Match by multiple criteria

**Present matched tasks:**
"Found [X] tasks matching your criteria:
- [Task 1]: [Brief description]
- [Task 2]: [Brief description]
...

Would you like to:
- Execute all tasks in sequence
- Select specific tasks to execute
- Review task details first"

### Single Task Selection
**If specific task ID provided:**
- Extract task details as before
- Check dependencies and prerequisites
- Proceed with single task execution

## Step 2.5: Batch Processing Strategy

**For batch operations:**
1. **Intelligent Ordering:** Sort tasks by:
   - Dependencies (execute prerequisites first)
   - Priority (critical → high → medium → low)
   - Asset grouping (keep related tasks together)

2. **Progress Tracking:**
   - Display overall progress (Task 3 of 15)
   - Estimate time remaining
   - Allow pausing/resuming batch operations

3. **Error Handling:**
   - If a task fails, offer options:
     - Skip and continue with remaining tasks
     - Retry with modifications
     - Pause batch for manual intervention
     - Roll back and stop

**Validate batch readiness:**
❓ **Batch Dependency Check:**
"Analyzing dependencies for [X] selected tasks...

**Ready to execute:** [Y] tasks
**Blocked by dependencies:** [Z] tasks

**Suggested execution order:**
Phase 1: [List of independent tasks]
Phase 2: [Tasks that depend on Phase 1]
Phase 3: [Final dependent tasks]

Proceed with this execution plan?"

## Step 3: Task Type Detection & Routing

**Route to appropriate execution strategy:**

### Research Tasks
- Gather information from specified sources
- Use MCP tools (Perplexity, web search) if external research needed
- Compile findings into structured research document
- Update task status and create deliverables

### Planning Tasks
- Route to `/outline-content` for content planning tasks
- Handle project setup and organizational tasks
- Create necessary file structures and documentation

### Content Creation Tasks
- Route to `/write-content` for draft creation
- Handle content formatting and optimization
- Apply specified rules (style, structure, persona)

### Review Tasks
- Read content and apply review criteria
- Generate feedback and improvement suggestions
- Update content based on review guidelines
- Mark review complete with approval status

### Publishing Tasks
- Format content for target platform
- Handle metadata and SEO optimization
- Execute publishing workflow
- Set up promotion and distribution

### Quality Assurance Tasks
- Run compliance checks against brand guidelines
- Verify content meets acceptance criteria
- Cross-reference with style and structure rules
- Generate QA report with pass/fail status

## Step 4: Task Execution by Type

### For Research Tasks:
1. **Source Analysis:** Review required research sources from task description
2. **Information Gathering:** Use appropriate tools (web search, MCP, existing files)
3. **Content Synthesis:** Organize findings according to research objectives
4. **Documentation:** Create research findings document in project working files
5. **Validation:** Ensure research meets acceptance criteria

### For Creation Tasks:
**Route to specialized commands:**
- Content outlining → `/outline-content [task-breakdown] [task-id]`
- Content writing → `/write-content [task-breakdown] [task-id]`
- Content editing → `/edit-content [existing-content] [task-requirements]`

### For Review Tasks:
1. **Content Analysis:** Read target content against review criteria
2. **Guidelines Application:** Apply brand, style, and quality standards
3. **Feedback Generation:** Create actionable improvement suggestions
4. **Approval Decision:** Determine if content meets standards
5. **Documentation:** Log review results and next steps

### For Publishing Tasks:
1. **Platform Preparation:** Format content for target CMS/platform
2. **Metadata Optimization:** Add SEO, tags, categories as needed
3. **Content Upload:** Execute publishing workflow
4. **Verification:** Confirm content is live and properly formatted
5. **Promotion Setup:** Initialize distribution and promotion activities

### For Management Tasks:
1. **Status Updates:** Review and update project progress
2. **Reporting:** Generate progress summaries
3. **Issue Resolution:** Address blockers and dependencies
4. **Communication:** Update stakeholders on project status

## Step 5: Task Completion & Status Update

**Document task completion:**
1. **Update task status** in task breakdown file
2. **Record completion details** (time, deliverables, issues encountered)
3. **Update dependent tasks** (mark as ready if dependencies satisfied)
4. **Create completion summary** with next recommended actions

**Completion format:**
```markdown
## Task Completion: [Task ID]
**Completed:** [Timestamp]
**Status:** Complete
**Deliverables:**
- [File 1: path and description]
- [File 2: path and description]
**Time Spent:** [Actual hours]
**Issues Encountered:** [Any problems and resolutions]
**Next Actions:** [Recommended follow-up tasks]
```

## Step 6: Progress Reporting & Next Steps

**Project progress update:**
"✅ Task [Task ID] completed successfully

**Deliverables created:**
- [List of files/outputs created]

**Project status:**
- Tasks complete: [X] of [Y]
- Next ready tasks: [List of unblocked tasks]
- Estimated time to completion: [X] days

**Recommended next actions:**
1. [Next logical task to execute]
2. [Any urgent dependencies to address]"

## Usage Examples

```bash
# Execute single task by ID
/execute-task @projects/launch/task-breakdown.md blog-create-01

# Execute all creation tasks in batch
/execute-task @projects/ai-glossary/task-breakdown.md "*-create-*" --batch

# Execute by task type
/execute-task @projects/ai-glossary/task-breakdown.md "type:creation" --batch

# Execute by task group (if defined in breakdown)
/execute-task @projects/campaign/task-breakdown.md "group:phase-1-outlines" --batch

# Natural language instruction
/execute-task @projects/ai-glossary/task-breakdown.md "outline all glossary terms" --batch --interactive

# Complex selector with multiple criteria
/execute-task @projects/seo-hub/task-breakdown.md "status:not-started priority:high type:research" --batch

# Execute all tasks for specific asset
/execute-task @projects/ai-glossary/task-breakdown.md "asset:llm-enhanced" --batch

# Interactive execution with guidance
/execute-task @projects/seo-hub/task-breakdown.md research-keywords-01 --interactive
```

## Task Type Support
**Currently supported task types:**
- ✅ Research and information gathering
- ✅ Content planning (routes to outline-content)
- ✅ Content creation (routes to write-content)
- ✅ Content editing (routes to edit-content)
- ✅ Review and quality assurance
- ✅ Publishing and distribution
- ✅ Project management and reporting

**For unsupported task types:**
"Task type '[type]' requires manual execution. The task details are:
[Display task information for manual completion]"
