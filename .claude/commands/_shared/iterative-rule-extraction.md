# Iterative Rule Extraction

This shared module provides an iterative, collaborative workflow for extracting writing rules with the user.

## Why Iterative?

Rule extraction requires user validation:
- Users need to see which documents will be analyzed before committing
- Different rule types need different source documents
- Preview helps users assess if there's enough content for quality extraction
- Review helps users evaluate extracted rules and decide if more are needed

## Pattern: Analyze → Propose → Approve → Extract → Review

```
┌─────────────────────────────────────────────────────┐
│ Analyze available indexed content                   │
│ - Group by type, domain, date range                │
│ - Assess extraction readiness                       │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Propose extraction with PREVIEW                     │
│ - Show 3-5 sample document titles/URLs             │
│ - Show coverage stats                              │
│ - Explain what patterns could be learned           │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ User Decision                                       │
│ - Approve: Extract from these documents            │
│ - Refine: Use different documents                  │
│ - Skip: Not now                                    │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Execute approved extraction                         │
│ - Run writing-rules-skill                          │
│ - Show progress                                    │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Review & Iterate                                    │
│ - Show extracted rule file + key characteristics   │
│ - Offer: Extract more / Refine / Continue          │
└─────────────────────────────────────────────────────┘
                       ↓
              Loop back or continue
```

---

## Prerequisites Check

**Before any extraction**, verify content is ready:

```bash
# Check indexed content count
indexed_count=$(kurt document list --status INDEXED | wc -l | tr -d ' ')

if [ "$indexed_count" -lt 10 ]; then
  echo "⚠️  Need at least 10 indexed pages to extract rules"
  echo "Currently have: $indexed_count indexed pages"
  echo ""
  echo "Please fetch and index more content first."
  exit 1
fi

echo "✓ Found $indexed_count indexed pages"
echo "Ready for rule extraction"
```

**If insufficient content:**
```
⚠️ Not enough content for quality rule extraction

Currently: 3 indexed pages
Recommended: 10+ pages for foundation rules, 20+ for content-specific rules

Would you like to:
a) Add more sources first
b) Extract anyway (may be incomplete)
c) Skip rule extraction for now

Choose (a/b/c):
```

---

## Step 1: Analyze Available Content

Before proposing any extraction, analyze what content is available.

### 1.1: Inventory Indexed Content

```bash
# List all indexed documents
kurt document list --status INDEXED --output json > indexed-content.json

# Analyze by domain
echo "Content by domain:"
cat indexed-content.json | jq -r '.[].url' | sed 's|https\?://||' | cut -d'/' -f1 | sort | uniq -c | sort -rn

# Analyze by date (if available)
echo ""
echo "Content date range:"
cat indexed-content.json | jq -r '.[].published_date // "unknown"' | grep -v "unknown" | sort | head -1
echo "to"
cat indexed-content.json | jq -r '.[].published_date // "unknown"' | grep -v "unknown" | sort | tail -1

# Show content types/topics
echo ""
echo "Common topics:"
cat indexed-content.json | jq -r '.[].topics[]? // empty' | sort | uniq -c | sort -rn | head -10
```

### 1.2: Group Content for Rule Types

Based on analysis, identify what rule types are possible:

```
**Available content for extraction:**

Foundation Rules (good for all projects):
✓ Publisher Profile - 50 pages from marketing site, about pages
✓ Primary Voice - 45 pages from blog, docs, marketing

Content-Specific Rules (based on your content):
✓ Technical Documentation Style - 30 pages from /docs/*
✓ Tutorial Structure - 15 pages from /docs/guides/*
✓ Blog Article Style - 20 pages from /blog/*
✓ Developer Persona - 25 pages targeting technical audience

Content volume is sufficient for quality extraction.
```

---

## Step 2: Propose Extraction with Preview

For each rule type, propose extraction **with sample documents preview**.

### 2.1: Propose Foundation Rules First

Foundation rules benefit all projects, so recommend these first:

#### Publisher Profile

```
**Propose: Extract Publisher Profile**

This rule captures your company positioning and messaging for brand consistency.

**Sample documents I'll analyze (5 of 50):**
1. example.com/about - "About Our Company"
2. example.com/product - "Product Overview"
3. example.com/solutions - "Solutions for Teams"
4. example.com/values - "Our Values and Mission"
5. example.com/customers - "Customer Stories"

**Coverage:**
- 50 pages from marketing site
- Domains: example.com, www.example.com
- Content types: about, product, marketing

**What I'll extract:**
- Company mission and value proposition
- Key messaging themes
- Brand personality and positioning
- Target market and differentiators

**Output:** rules/publisher/publisher-profile.md

Extract publisher profile from these documents? (Y/n)
> Or: "Use different documents" / "Skip for now"
```

#### Primary Voice

```
**Propose: Extract Primary Voice**

This rule captures your brand tone and writing style for consistent voice.

**Sample documents I'll analyze (5 of 45):**
1. example.com/blog/intro-to-product - "Introduction to Our Product"
2. example.com/docs/quickstart - "Quickstart Guide"
3. example.com/blog/best-practices - "Best Practices for..."
4. example.com/marketing/launch - "Product Launch Announcement"
5. example.com/docs/concepts - "Core Concepts"

**Coverage:**
- 45 pages from blog and docs
- Domains: example.com
- Content types: blog posts, documentation, marketing
- Date range: 2023-06 to 2024-10

**What I'll extract:**
- Sentence structure patterns
- Tone characteristics (formal/casual, technical/accessible)
- Word choice preferences
- Common phrases and voice patterns
- How you explain complex concepts

**Output:** rules/style/primary-voice.md

Extract primary voice from these documents? (Y/n)
> Or: "Use different documents" / "Skip for now"
```

### 2.2: Propose Content-Specific Rules

After foundation rules, propose rules based on project intent and target content:

#### Technical Documentation Style

```
**Propose: Extract Technical Documentation Style**

This rule captures how you write technical documentation.

**Sample documents I'll analyze (5 of 30):**
1. docs.example.com/api/authentication - "Authentication API Reference"
2. docs.example.com/concepts/architecture - "Architecture Overview"
3. docs.example.com/guides/deployment - "Deployment Guide"
4. docs.example.com/reference/cli - "CLI Reference"
5. docs.example.com/troubleshooting - "Troubleshooting"

**Coverage:**
- 30 pages from /docs/*
- Content types: API reference, guides, concepts, troubleshooting
- Technical depth: High (developer-focused)

**What I'll extract:**
- Technical writing patterns (how you explain APIs, concepts, commands)
- Example usage patterns
- Warning and note styles
- Code snippet formatting
- Explanation depth for technical audience

**Output:** rules/style/technical-documentation.md

Relevant for your project? Extract this style? (Y/n)
> Or: "Use different documents" / "Skip for now"
```

#### Tutorial Structure

```
**Propose: Extract Tutorial Structure**

This rule captures how you structure tutorials and guides.

**Sample documents I'll analyze (5 of 15):**
1. docs.example.com/guides/quickstart - "Quickstart Tutorial"
2. docs.example.com/guides/build-first-app - "Build Your First App"
3. docs.example.com/guides/advanced-config - "Advanced Configuration"
4. docs.example.com/guides/integration - "Integration Guide"
5. docs.example.com/guides/migration - "Migration Guide"

**Coverage:**
- 15 pages from /docs/guides/*
- All step-by-step tutorials
- Varied difficulty levels

**What I'll extract:**
- Section structure patterns (prerequisites, steps, conclusion)
- How you introduce and explain steps
- Code example placement
- Troubleshooting integration
- Success criteria and next steps

**Output:** rules/structure/tutorial.md

Relevant for your project? Extract this structure? (Y/n)
> Or: "Use different documents" / "Skip for now"
```

#### Persona (Developer)

```
**Propose: Extract Developer Persona**

This rule captures how you target and communicate with developer audience.

**Sample documents I'll analyze (5 of 25):**
1. docs.example.com/quickstart - Technical quickstart
2. docs.example.com/api/reference - API documentation
3. blog.example.com/announcing-api-v2 - API announcement
4. docs.example.com/sdk/nodejs - SDK guide
5. docs.example.com/examples - Code examples

**Coverage:**
- 25 pages targeting technical audience
- Content types: API docs, SDKs, tutorials, technical blog posts
- Technical depth: Developer-focused

**What I'll extract:**
- Audience technical level (assumed knowledge)
- Communication preferences (direct, example-heavy, conceptual)
- Pain points addressed
- Preferred learning styles
- Example types that resonate

**Output:** rules/personas/developer.md

Relevant for your project? Extract this persona? (Y/n)
> Or: "Use different documents" / "Skip for now"
```

---

## Step 3: User Decision for Each Proposal

For each proposed extraction, wait for user response:

### Option A: Approve

```
User: "Y" or "Yes, extract this"

→ Proceed to Step 4 (Execute) for this rule
```

### Option B: Refine (Use Different Documents)

```
User: "Use different documents"

Ask: "Which documents should I use instead?"

Options:
1. Different URL pattern (e.g., /blog/* instead of /docs/*)
2. Different date range (e.g., only 2024 content)
3. Different domain (e.g., different subdomain)
4. Add more documents (fetch additional content first)

User specifies refinement
→ Return to Step 2.1/2.2 with adjusted document set
```

**Example refinement:**
```
User: "Only use docs from 2024, not older content"

Okay, I'll filter to 2024 content only.

**Updated sample documents (5 of 18):**
1. docs.example.com/guides/new-feature (2024-08)
2. docs.example.com/api/v2-reference (2024-06)
...

Extract from these updated documents? (Y/n)
```

### Option C: Skip

```
User: "n" or "Skip for now"

→ Move to next rule type proposal
→ If no more rule types, move to Step 5 (Review & Iterate)
```

---

## Step 4: Execute Approved Extraction

For each approved extraction, run the extraction:

### 4.1: Run Extraction Command

```bash
# Extract the approved rule
case "$rule_type" in
  publisher)
    echo "Extracting publisher profile..."
    writing-rules-skill publisher --auto-discover
    ;;

  style-primary)
    echo "Extracting primary voice..."
    writing-rules-skill style --type primary --auto-discover
    ;;

  style-technical)
    echo "Extracting technical documentation style..."
    writing-rules-skill style --type technical-docs --auto-discover
    ;;

  structure-tutorial)
    echo "Extracting tutorial structure..."
    writing-rules-skill structure --type tutorial --auto-discover
    ;;

  persona-developer)
    echo "Extracting developer persona..."
    writing-rules-skill persona --audience-type technical --auto-discover
    ;;
esac
```

### 4.2: Show Progress

```
Extracting: Publisher Profile

Analyzing 50 documents...
✓ Extracted mission and value proposition
✓ Identified key messaging themes
✓ Captured brand personality
✓ Documented positioning and differentiators

Extraction complete (took 45 seconds)
```

### 4.3: Verify Extraction

```bash
# Check if rule file was created
rule_file="rules/$rule_type/$rule_name.md"

if [ -f "$rule_file" ]; then
  echo "✓ Created: $rule_file"

  # Show file size
  file_size=$(wc -c < "$rule_file")
  echo "  Size: $file_size bytes"

  # Show key sections (preview)
  echo ""
  echo "Key sections extracted:"
  grep '^##' "$rule_file" | head -5
else
  echo "⚠️  Extraction failed - file not created"
fi
```

---

## Step 5: Review Extracted Rule

After extraction, show what was extracted and key characteristics:

```
**Extraction Complete: Publisher Profile**

✓ Created: rules/publisher/publisher-profile.md

**Key characteristics extracted:**

Mission:
> "Empowering developers to build secure, scalable applications with confidence"

Value Proposition:
> "Enterprise-grade authentication and authorization platform designed for developers"

Brand Personality:
- Professional yet approachable
- Developer-focused and technical
- Emphasizes security and reliability
- Values simplicity and great DX

Key Messaging Themes:
- Security without complexity
- Built for developers
- Enterprise-ready
- Flexible and scalable

Target Market:
- B2B SaaS companies
- Enterprise development teams
- Security-conscious organizations

**This rule will be applied to all content you create.**
```

---

## Step 6: Offer Continuation Options

After each extraction (or skip), offer next steps:

```
**What would you like to do next?**

a) **Extract more rules** - I'll propose the next recommended rule type
b) **Refine this rule** - Re-extract with different documents or adjustments
c) **Review all extracted rules** - Show summary of all rules extracted so far
d) **Continue to next step** - Move on (identify targets or start content work)

Choose (a/b/c/d):
```

### If (a) - Extract more rules:
- Propose next rule type from Step 2
- Follow same pattern: Preview → Approve → Extract → Review

### If (b) - Refine this rule:
- Ask what to refine:
  - Different documents?
  - Different focus areas?
  - Combine with other rule?
- Return to Step 2 with refinements

### If (c) - Review all extracted rules:
```
**Extracted Rules Summary**

Foundation Rules:
✓ Publisher Profile: rules/publisher/publisher-profile.md
  - Mission, value prop, brand personality, positioning

✓ Primary Voice: rules/style/primary-voice.md
  - Tone: Professional but approachable
  - Structure: Short paragraphs, active voice
  - Style: Clear explanations with examples

Content-Specific Rules:
✓ Technical Docs Style: rules/style/technical-documentation.md
  - High technical depth
  - Example-heavy
  - Reference-oriented

✓ Tutorial Structure: rules/structure/tutorial.md
  - Prerequisites → Steps → Validation → Next Steps
  - Step-by-step with code snippets
  - Troubleshooting sections

✓ Developer Persona: rules/personas/developer.md
  - Audience: Backend/full-stack developers
  - Skill level: Intermediate to advanced
  - Learning style: Example-first, then concepts

**All rules will be applied when creating/updating content.**

What would you like to do next? (a: extract more / d: continue)
```

### If (d) - Continue:
- Update project.md with extracted rules
- Remind user rules can be extracted later
- Continue to next phase (identify targets or content work)

---

## Handling Insufficient Content

If user tries to extract but there isn't enough content:

```
⚠️ Warning: Limited content for this rule type

Proposed: Technical Documentation Style
Available: 5 pages from /docs/*
Recommended: 15+ pages for quality extraction

**Sample documents (all 5):**
1. docs.example.com/quickstart
2. docs.example.com/api-reference
3. docs.example.com/concepts
4. docs.example.com/deployment
5. docs.example.com/troubleshooting

**Risk:** Extraction may be incomplete or not capture full patterns.

What would you like to do?
a) **Add more documentation** - Fetch more docs before extracting
b) **Extract anyway** - Proceed with limited content (may need refinement later)
c) **Skip this rule** - Extract other rules first

Choose (a/b/c):
```

---

## Integration with Commands

### In `/create-project` Step 5:

```markdown
## Step 5: Extract Rules (Optional but Recommended)

Ask if user wants to extract rules:
> Would you like to extract writing rules from your content?
> a) Extract rules now (recommended if sources available)
> b) Skip for now (can extract later)

**If (a) - Extract rules now:**

Follow the complete iterative workflow in:
`.claude/commands/_shared/iterative-rule-extraction.md`

This will guide through:
1. Analyze available indexed content
2. Propose extraction with sample document preview
3. User approves/refines/skips each rule type
4. Execute approved extractions
5. Review extracted rules
6. Continue when user is satisfied

**If (b) - Skip:**
- Note in project.md that rules can be extracted later
- Continue to Step 6
```

### In `/resume-project` (for extracting rules):

When user wants to extract rules for existing project, use same module.

---

## Error Handling

### Extraction Failed

```
⚠️ Rule extraction failed

Rule type: Technical Documentation Style
Error: Insufficient analysis content

Possible issues:
- Documents not properly indexed
- Content too short or missing key sections
- API rate limit or timeout

Try:
1. Re-index content: kurt index --url-prefix <url>
2. Add more source documents
3. Try different document set
4. Skip for now and try later

What would you like to do?
```

### No Content Available

```
⚠️ No indexed content available for extraction

To extract rules, you need:
- At least 10 indexed pages for foundation rules
- At least 15-20 pages for content-specific rules

Current status: 0 indexed pages

Please:
1. Add sources (Step 3: Collect Sources)
2. Ensure sources are fetched and indexed
3. Return to rule extraction

Skip rule extraction for now? (Y/n)
```

---

## Key Design Principles

1. **Preview before execution**: Always show sample documents before extracting
2. **Progressive disclosure**: Start with foundation rules, then content-specific
3. **Explicit approval**: Wait for user confirmation before extraction
4. **Coverage transparency**: Show how many documents and what types
5. **Quality assessment**: Warn if insufficient content for quality extraction
6. **Reversibility**: Can refine and re-extract with different documents
7. **Iterative**: Continue proposing rules until user is satisfied

---

*This module is referenced by `/create-project` Step 5 and `/resume-project` for extracting rules in existing projects.*
