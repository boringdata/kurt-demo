# Data Analyst Persona

**Created:** 2025-10-24
**Primary Audience For:** Getting started guides, beginner tutorials, visual tool documentation (dbt Canvas), dbt Cloud quickstarts
**Sources:** Product pages (/analyst, /dbt-copilot), docs introduction, community resources

---

## Persona Overview

### Who They Are

**Job Titles:**
- Data Analyst
- Business Intelligence Analyst
- Analytics Analyst
- Junior Analytics Engineer
- BI Developer

**Core Identity:**
Data analysts are professionals who "explore, transform, and model data" to deliver insights to business stakeholders. They work between engineering teams and business users, traditionally building dashboards and performing analysis. Many are learning to "work more like software engineers" and contribute to production data pipelines.

**Experience Level:**
- 1-5 years in data/analytics roles
- SQL proficient but may not be a daily advanced user
- Basic familiarity with business intelligence tools
- Learning version control and modern data practices
- May have business or statistics background

**Technical Proficiency:**
> "I'm fairly SQL proficient, but not a daily user" (typical self-assessment)

- Can write SELECT statements, joins, basic aggregations
- Less comfortable with complex CTEs, window functions, optimization
- May rely on visual query builders or SQL assistants
- Learning git and command-line tools

---

## Day-to-Day Responsibilities

### Core Activities

**Ad-Hoc Analysis:**
- Respond to last-minute data requests
- Answer business questions with queries
- Validate KPIs and metrics
- Investigate data anomalies

**Dashboard & Reporting:**
- Build and maintain business dashboards
- Create scheduled reports
- Visualize data for stakeholders
- Monitor key business metrics

**Data Exploration:**
- Find and verify data across multiple sources
- Understand data lineage and definitions
- Discover available datasets
- Assess data quality

**Collaboration:**
- Work with business stakeholders to understand needs
- Partner with data engineers on requirements
- Share insights across teams
- Educate business users on data

**Learning & Upskilling:**
- Adopting analytics engineering practices
- Learning transformation tools like dbt
- Understanding testing and documentation
- Building more maintainable data assets

---

## Current Challenges & Pain Points

### Workflow Frustrations

**Engineering Bottlenecks:**
- "Engineering bottlenecks or ungoverned point solutions slow their work"
- Wait for data engineers to build pipelines
- Can't make changes to transformations quickly
- Dependent on technical teams for data access

**Fragmented Tools:**
- Working across "tabs, silos, and endless wait times"
- Disconnected tools that don't talk to each other
- Context switching between SQL editors, BI tools, documentation
- Lost time searching for the right data

**Data Trust Issues:**
- "Unreliable data creates rework and erodes trust"
- Inconsistent definitions across reports
- Data quality problems discovered too late
- Multiple versions of "truth" across systems

**Lack of Governance:**
- "Lack of governance makes it hard to scale analytics"
- No clear ownership of data assets
- Inconsistent naming conventions
- Difficult to understand what's production-ready

### Skill Gaps

**Technical Limitations:**
- Not comfortable with command-line tools
- Learning git and version control
- Unfamiliar with CI/CD concepts
- May struggle with complex SQL

**Knowledge Discovery:**
- Don't know what data exists
- Can't find documentation
- Unclear who owns what data
- Difficulty understanding transformations

---

## Goals & Motivations

### Primary Goals

1. **Get Fast Answers Without Dependencies**
   - Self-service data access
   - Transform data without engineering handoffs
   - Respond quickly to business requests
   - Reduce waiting time

2. **Build Trusted, Reliable Data**
   - Know data is correct and current
   - Understand data lineage
   - Access documented, validated datasets
   - Avoid embarrassing errors

3. **Work More Efficiently**
   - Spend less time searching for data
   - Reduce context switching
   - Automate repetitive tasks
   - Focus on analysis, not data plumbing

4. **Grow Technical Skills**
   - Learn analytics engineering practices
   - Contribute to production pipelines
   - Apply software engineering best practices
   - Become more valuable to their organization

5. **Collaborate Without Compromising Quality**
   - Work with team on shared data
   - Follow governance standards
   - Build maintainable assets
   - Share knowledge effectively

---

## What They Need from dbt

### Key Capabilities

**Self-Service Transformation:**
- Build models without deep technical knowledge
- Visual model building (dbt Canvas)
- Natural language queries
- Template-based workflows

**Data Discovery:**
- Centralized catalog (dbt Catalog)
- Search across all datasets
- Understand lineage visually
- Find documentation easily

**Guided Workflows:**
- Built-in testing and validation
- Suggested best practices
- Pre-built templates
- Clear error messages

**Reduced Friction:**
- Don't need to master command line
- Web-based IDE (dbt Cloud)
- Visual interfaces alongside code
- AI assistance (dbt Copilot)

---

## Learning Journey with dbt

### Stage 1: Getting Started (Beginner)
**Needs:**
- Understand what dbt is and why it matters
- Get started without complex setup
- Follow along with simple examples
- See immediate value

**Preferred Learning Style:**
- Visual walkthroughs
- Point-and-click interfaces
- Guided tutorials with clear steps
- Video content

**Mindset:** "I want to understand the basics without feeling overwhelmed"

### Stage 2: Building First Models (Learning)
**Needs:**
- Create simple transformations
- Understand refs and sources
- Learn about testing
- Deploy changes safely

**Tools They Prefer:**
- dbt Cloud web IDE
- dbt Canvas for visual modeling
- dbt Copilot for SQL assistance
- Templates and examples

**Mindset:** "I want to build something useful for my team"

### Stage 3: Adopting Best Practices (Growing)
**Needs:**
- Write better documentation
- Implement data tests
- Collaborate via version control
- Organize projects logically

**Learning Path:**
- Formal training (dbt Learn)
- Certification (Analytics Engineer)
- Peer learning and code review
- Community resources

**Mindset:** "I want to do this the right way and grow my skills"

### Stage 4: Becoming Analytics Engineer (Advanced)
**Needs:**
- Master complex transformations
- Contribute to shared packages
- Mentor others on the team
- Design scalable data models

**Evolution:**
- May transition to analytics engineer title
- Takes on more technical responsibility
- Bridges to data engineering
- Leads data initiatives

**Mindset:** "I'm ready for more advanced challenges"

---

## What They Need from Documentation

### Tutorial Content

**Beginner-Friendly:**
- No assumptions about prior knowledge
- Explain concepts before diving in
- Step-by-step with screenshots
- Clear success criteria

**Multiple Learning Paths:**
- Web UI path (dbt Cloud)
- Visual tool path (Canvas)
- CLI path (for those ready)
- Video and written options

**Practical Examples:**
- Use realistic business scenarios
- Show complete workflows end-to-end
- Explain business context, not just syntax
- Demonstrate value to stakeholders

**Confidence Building:**
- Celebrate small wins
- Provide safety nets (how to undo)
- Explain what's happening behind the scenes
- Troubleshoot common beginner mistakes

### Content Structure

**What Works:**
- Short, focused lessons
- Progressive disclosure (basics first, complexity later)
- Glossary of terms
- FAQs for common questions
- Links to deeper content when ready

**What Doesn't Work:**
- Dense technical reference docs without context
- Assumptions about command-line comfort
- Jumping straight to advanced features
- No visual aids or examples

---

## How dbt Empowers This Persona

### From dbt's Product Messaging

**Before dbt:**
- Bottlenecked by engineering
- Working in disconnected tools
- Unreliable data, constant rework
- Can't scale their work

**With dbt:**
- "Fast answers, no handoffs"
- "All your work in one place"
- "Trusted, reliable data"
- "Collaborative workflows with built-in governance"

### Specific Features That Help

**dbt Canvas:**
- Visual, drag-and-drop model building
- No need to write SQL from scratch
- See relationships graphically
- Lower barrier to entry

**dbt Catalog:**
- Find data across the organization
- Understand what datasets exist
- See documentation and lineage
- Self-service discovery

**dbt Copilot:**
- Natural language to SQL
- Automatically generate documentation
- Create tests without deep knowledge
- Reduce manual work

**dbt Cloud IDE:**
- Web-based, no local setup
- Integrated environment
- Built-in collaboration
- Lower technical barriers

---

## Decision-Making Factors

### What Influences Their Adoption

**Ease of Use:**
- Can I get started quickly?
- Do I need to learn command line?
- Is there a visual interface?
- How steep is the learning curve?

**Support & Resources:**
- Are there good tutorials?
- Is there training available?
- Can I get help when stuck?
- Are there templates to start from?

**Team Adoption:**
- Is my team using this?
- Will I get support from colleagues?
- Is this becoming standard?
- Can I learn from others?

**Career Growth:**
- Will this make me more valuable?
- Can I get certified?
- Is this a marketable skill?
- Will this help me advance?

**Low Risk:**
- Can I try it without commitment?
- Will I break something?
- Is it reversible?
- Are there guardrails?

---

## Preferred Communication Style

### What Resonates

**Tone:** Encouraging, supportive, empowering (not condescending)

**Content Approach:**
- **Practical over theoretical:** Show me how this helps my work
- **Visual over text-heavy:** Screenshots, diagrams, videos
- **Guided over independent:** Walk me through it
- **Success-oriented:** Celebrate progress, not just perfection

**Language Patterns:**

✅ **Effective:**
- "Let's build your first model together"
- "You'll be able to answer this question yourself"
- "This helps you avoid waiting for engineering"
- "No command line required - use dbt Cloud"

❌ **Avoid:**
- "Obviously, you'll just..." (assumes knowledge)
- "Simply configure your profiles.yml" (not simple for beginners)
- "This is trivial once you understand..." (dismissive)
- Technical jargon without explanation

---

## Content Validation Questions

When creating content for data analysts, ask:

1. **Is it accessible?** Can someone without deep technical background follow it?
2. **Is it encouraging?** Does it build confidence, not intimidate?
3. **Is it practical?** Does it solve a real problem they face?
4. **Is it safe?** Are there guardrails and safety nets?
5. **Is it visual?** Are there screenshots, diagrams, or videos?
6. **Is it complete?** Have you explained prerequisite concepts?

---

## Use Cases & Scenarios

### Typical Projects

**KPI Dashboard:**
- Build models for key metrics
- Document metric definitions
- Test data quality
- Share with stakeholders

**Ad-Hoc Analysis:**
- Transform raw data for specific question
- Join multiple sources
- Validate results
- Save for future reuse

**Report Automation:**
- Replace manual data pulls
- Schedule transformations
- Ensure consistency
- Reduce repetitive work

**Data Exploration:**
- Discover available datasets
- Understand lineage
- Find documentation
- Assess quality

---

## Success Metrics for This Persona

### What "Success" Looks Like

**Efficiency Gains:**
- Reduced time waiting for data
- Fewer back-and-forth requests to engineering
- Faster turnaround on business questions
- More time for actual analysis

**Quality Improvements:**
- Fewer errors in reports
- Consistent metric definitions
- Better documented work
- Trusted data assets

**Skill Development:**
- Comfortable with SQL transformations
- Understanding of data modeling
- Able to contribute to production pipelines
- Growing analytics engineering skills

**Organizational Impact:**
- Stakeholders trust their work
- Self-sufficient for data needs
- Mentor others on the team
- Enable data-driven decisions

---

## Key Quotes & Insights

**On Technical Level:**
> "I'm fairly SQL proficient, but not a daily user" - indicating moderate technical comfort

**On Challenges:**
> "Engineering bottlenecks or ungoverned point solutions slow their work"
> "Working across tabs, silos, and endless wait times with disconnected tools"
> "Unreliable data creates rework and erodes trust"

**On Needs:**
> "Fast answers without engineering handoffs"
> "Find and verify data across multiple sources"
> "Self-service capabilities without compromising governance"

**On Goals:**
> "I want to work more like a software engineer and contribute to production pipelines"
> "Anyone on the data team comfortable with SQL can safely contribute"

---

## Relationship to Analytics Engineer Persona

### Key Differences

| Data Analyst | Analytics Engineer |
|---|---|
| SQL proficient, not daily advanced user | SQL expert, writes it daily |
| Learning git and version control | Comfortable with git workflows |
| Prefers visual/web interfaces | Comfortable with CLI and code editors |
| May use dbt Canvas, Copilot heavily | Uses VS Code extension, writes code directly |
| Following tutorials to learn | Reading reference docs to optimize |
| Building first models | Building reusable packages |
| Transitioning to production work | Owns production pipelines |

### Overlap

Many data analysts are **becoming** analytics engineers:
- Starting with visual tools, moving to code
- Learning best practices through dbt
- Growing technical skills over time
- Taking on more engineering responsibilities

The analyst persona represents the **entry point** into modern analytics engineering practices, while analytics engineers are the mature practitioners.

---

## Documentation Priorities for This Persona

### Essential Content:
1. **Getting Started Guide**
   - What is dbt?
   - Why should I use it?
   - How do I get access? (dbt Cloud signup)
   - First successful model

2. **Visual Tool Documentation**
   - dbt Canvas walkthrough
   - Catalog navigation
   - Using Copilot for SQL assistance

3. **Concept Explanations**
   - What are models, sources, tests?
   - Understanding lineage
   - How dbt fits in the data stack

4. **Best Practices for Beginners**
   - How to structure models
   - When to test data
   - Documentation tips
   - Collaboration basics

### Lower Priority:
- Advanced CLI features
- Complex macros and packages
- Performance optimization
- Infrastructure architecture

(They'll need these eventually as they grow, but not when starting)

---

## Source Material

**Product Pages:**
- https://www.getdbt.com/product/analyst (primary source for analyst persona)
- https://www.getdbt.com/product/dbt-copilot
- https://www.getdbt.com/product/dbt
- https://www.getdbt.com/analytics-engineering

**Documentation:**
- https://docs.getdbt.com/docs/introduction
- "Anyone on the data team comfortable with SQL can safely contribute to production-grade data pipelines"

**Community:**
- https://www.getdbt.com/community/join-the-community
- "From beginners to expert analytics engineers"
