---
description: Clone a project template and customize it for your needs (project)
---

# Clone Project from Template

This command clones a template project and guides you through customizing it.

Use the Skill tool to invoke:

```
project-management clone-project [template-name]
```

**Available templates:**
- **weekly-tutorial** - Recurring tutorial publication
- **product-launch** - Multi-format product launch campaign
- **tutorial-refresh** - Analytics-driven tutorial updates
- **documentation-audit** - Comprehensive traffic audit
- **gap-analysis** - Identify missing content vs competitor
- **competitive-analysis** - Quality benchmark against competitor

The skill will guide you through:
1. Showing template preview
2. Getting new project name and goal
3. Customizing template sections (sources, targets, etc.)
4. Creating customized project structure

All orchestration logic lives in the skill. See `.claude/skills/project-management-skill/subskills/clone-project.md` for details.
