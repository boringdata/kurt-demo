# Check Organizational Foundation

This shared module verifies that foundational organizational context exists before project work.

## Why This Matters

The organizational foundation helps you:
- **Understand existing content** - Know what's already published (for updates/gaps)
- **Learn content patterns** - Identify voice, structure, and messaging
- **Make informed decisions** - Choose relevant sources based on org context

## Prerequisites

This check should run:
- **In /create-project:** After getting project name, before collecting project sources (Step 2.5)
- **In /resume-project:** After loading project, before continuing work (Step 4)

---

## Check 1: Content Map (URLs/Sitemaps)

The content map provides a foundation of your organization's published content.

### Check if Content Map Exists

```bash
# Count organizational content in /sources/ (exclude projects/)
content_count=$(ls sources/ 2>/dev/null | grep -v "^projects$" | wc -l | tr -d ' ')

if [ "$content_count" -lt 3 ]; then
  echo "⚠️  No content map found"
else
  echo "✓ Content map exists ($content_count domains mapped)"
fi
```

### If Content Map Missing

Display prompt to user:

```
⚠️  No organizational content map found

To work effectively, I need to understand your organization's existing content.

**What are your organization's main websites?**

Examples:
- Public website: yourcompany.com
- Documentation: docs.yourcompany.com
- Blog: blog.yourcompany.com
- Marketing site: marketing.yourcompany.com

**Provide root domains or sitemap URLs** (one per line):
[Wait for user input]
```

**User provides domains, for example:**
```
docs.yourcompany.com
blog.yourcompany.com
```

### Map Each Domain

For each domain the user provides, run the full ingest workflow:

**Step 1: Map (Discover URLs)**

```bash
# Map the domain to discover URLs
kurt ingest map https://docs.yourcompany.com --discover-dates

# Show what was discovered
discovered_count=$(kurt document list --url-prefix https://docs.yourcompany.com --status NOT_FETCHED | wc -l | tr -d ' ')
echo "✓ Discovered $discovered_count URLs from docs.yourcompany.com"
```

**Step 2: Fetch (Download Content)**

```bash
# Fetch all discovered URLs
kurt ingest fetch --url-prefix https://docs.yourcompany.com

# Show progress
fetched_count=$(kurt document list --url-prefix https://docs.yourcompany.com --status FETCHED | wc -l | tr -d ' ')
echo "✓ Fetched $fetched_count pages to /sources/"
```

**Step 3: Index (Extract Metadata)**

```bash
# Index fetched content for analysis
kurt index --url-prefix https://docs.yourcompany.com

# Verify completion
indexed_count=$(kurt document list --url-prefix https://docs.yourcompany.com --status INDEXED | wc -l | tr -d ' ')
echo "✓ Indexed $indexed_count pages (metadata extracted)"
```

**Repeat for all domains**, then show summary:

```
✅ Content Map Complete

Mapped domains:
- docs.yourcompany.com (50 pages)
- blog.yourcompany.com (120 pages)

Total: 170 pages indexed in /sources/

Your organizational content is now queryable and ready for rule extraction.
```

### If Content Map Exists

Just show summary and continue:

```
✓ Content map exists

Mapped content:
- docs.yourcompany.com (50 pages)
- blog.yourcompany.com (120 pages)
→ Total: 170 pages in /sources/

Continuing...
```

---

## Check 2: Core Rules (Publisher + Primary Voice + Personas)

Core rules ensure consistency across all content.

### Check if Core Rules Exist

```bash
# Check for publisher profile
if [ -f "rules/publisher/publisher-profile.md" ]; then
  echo "✓ Publisher profile exists"
  publisher_exists=true
else
  echo "⚠️  Publisher profile missing"
  publisher_exists=false
fi

# Check for primary voice
primary_voice=$(ls rules/style/*primary* 2>/dev/null | head -1)
if [ -n "$primary_voice" ]; then
  echo "✓ Primary voice exists: $primary_voice"
  voice_exists=true
else
  echo "⚠️  Primary voice missing"
  voice_exists=false
fi

# Check for personas
persona_count=$(ls rules/personas/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$persona_count" -gt 0 ]; then
  echo "✓ Personas exist ($persona_count found)"
  personas_exist=true
else
  echo "⚠️  Personas missing"
  personas_exist=false
fi
```

### If Core Rules Missing

**Prerequisites check:**
Content must be mapped/fetched/indexed before extracting rules.

```bash
# Verify content exists for extraction
content_count=$(kurt document list --status INDEXED | wc -l | tr -d ' ')
if [ "$content_count" -lt 10 ]; then
  echo "⚠️  Need at least 10 indexed pages to extract rules"
  echo "Please complete content map first (Check 1)"
  exit 1
fi
```

Display prompt to user:

```
⚠️  Core rules not found

To ensure consistency, I need to understand your organization's voice and positioning.

**I'll extract core rules from your content (takes 3-5 minutes):**

1. **Publisher Profile** - Company positioning and messaging
   - Extracted from: About pages, product pages, value props
   - Used for: Brand consistency across all content

2. **Primary Voice** - Brand tone and writing style
   - Extracted from: Marketing pages, blog posts, docs
   - Used for: Maintaining consistent voice and tone

3. **Personas** - Target audience profiles
   - Extracted from: Customer-facing content, help docs, tutorials
   - Used for: Writing at appropriate technical depth for audience

Ready to extract rules? (Y/n)
```

**If user confirms:**

### Extract Publisher Profile (if missing)

```bash
# Extract publisher profile (company positioning)
writing-rules-skill publisher --auto-discover

# Verify creation
if [ -f "rules/publisher/publisher-profile.md" ]; then
  echo "✓ Publisher profile extracted: rules/publisher/publisher-profile.md"
else
  echo "⚠️  Publisher profile extraction failed"
fi
```

### Extract Primary Voice (if missing)

```bash
# Extract primary voice/style
writing-rules-skill style --type primary --auto-discover

# Find the created file
primary_voice=$(ls rules/style/*primary* 2>/dev/null | head -1)
if [ -n "$primary_voice" ]; then
  echo "✓ Primary voice extracted: $primary_voice"
else
  echo "⚠️  Primary voice extraction failed"
fi
```

### Extract Personas (if missing)

```bash
# Extract personas (target audience profiles)
writing-rules-skill persona --auto-discover

# Count created personas
persona_count=$(ls rules/personas/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$persona_count" -gt 0 ]; then
  echo "✓ Personas extracted: $persona_count persona(s) in rules/personas/"
  ls rules/personas/*.md 2>/dev/null | while read persona; do
    echo "  - $(basename "$persona")"
  done
else
  echo "⚠️  Persona extraction failed"
fi
```

**Show completion:**

```
✅ Core Rules Complete

Extracted rules:
✓ Publisher profile: rules/publisher/publisher-profile.md
✓ Primary voice: rules/style/primary-voice.md
✓ Personas: [X persona(s)] in rules/personas/

These rules will ensure consistency in all content you create.
```

### If Core Rules Exist

Just show summary and continue:

```
✓ Core rules exist

Available rules:
✓ Publisher profile: rules/publisher/publisher-profile.md
✓ Primary voice: rules/style/primary-voice.md
✓ Personas: [X persona(s)] in rules/personas/

Continuing...
```

---

## Final Summary (After Both Checks Complete)

Display complete foundation summary:

```
✅ Organizational Foundation Complete

**Content Map:**
- docs.yourcompany.com (50 pages)
- blog.yourcompany.com (120 pages)
→ Total: 170 pages indexed in /sources/

**Core Rules:**
✓ Publisher profile: rules/publisher/publisher-profile.md
✓ Primary voice: rules/style/primary-voice.md
✓ Personas: [X persona(s)] in rules/personas/

**You're ready to:**
- Add project-specific sources (informed by org context)
- Create content (with consistent voice/positioning)
- Update existing content (knowing what exists)

[Continue to next step in parent command]
```

---

## Error Handling

**If content map fails:**
```
⚠️  Content mapping failed for: docs.yourcompany.com

Possible issues:
- Domain not accessible
- No sitemap found
- Network/firewall issues

Try:
1. Check domain is correct
2. Try with sitemap URL: docs.yourcompany.com/sitemap.xml
3. Verify network access

Skip this domain for now? (Y/n)
```

**If rule extraction fails:**
```
⚠️  Rule extraction failed

Possible issues:
- Not enough content to extract patterns
- Content not indexed yet
- API rate limits

Try:
1. Verify content is indexed: kurt document list --status INDEXED
2. Wait and retry
3. Continue without rules (can extract later)

Continue without rules? (Y/n)
```

---

## Usage Notes

**For /create-project:**
- Run this as Step 2.5 (after project name, before project sources)
- First-time users get full onboarding
- Veteran users see quick summary and continue

**For /resume-project:**
- Run this as part of Step 4 (checking project status)
- If foundation missing, offer to set up before project work
- Prevents working without necessary context

**Skip logic:**
- Content map exists if `/sources/` has 3+ domains
- Core rules exist if both publisher profile and primary voice present
- Only prompt for missing pieces (fast for repeat users)
