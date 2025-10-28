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

Display explanation to user:

```
⚠️  Core rules not found

To ensure consistency, I need to understand your organization's voice and positioning.

**Core rules I'll help you extract:**

1. **Publisher Profile** - Company positioning and messaging
   - What I'll look for: About pages, product pages, value propositions
   - Used for: Brand consistency across all content

2. **Primary Voice** - Brand tone and writing style
   - What I'll look for: Marketing pages, blog posts, documentation
   - Used for: Maintaining consistent voice and tone

3. **Personas** - Target audience profiles
   - What I'll look for: Customer-facing content, help docs, tutorials
   - Used for: Writing at appropriate technical depth for audience

I'll show you which pages I'll analyze before extracting each rule.

Ready to start? (Y/n)
```

**If user confirms, proceed with iterative extraction:**

### Extract Publisher Profile (if missing)

**Step 1: Query and Preview Documents**

Query indexed content for publisher profile extraction:

```bash
# Find key company pages
kurt document list --status INDEXED --output json > /tmp/indexed-content.json

# Look for homepage, about, product pages
homepage=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("^https?://[^/]+/?$")) | .url' | head -1)
about_pages=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/about|/company|/mission|/values")) | .url' | head -3)
product_pages=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/product|/solutions|/platform")) | .url' | head -3)

# Count total available
total_publisher_docs=$(echo "$homepage"; echo "$about_pages"; echo "$product_pages" | grep -v '^$' | wc -l | tr -d ' ')
```

**If no suitable documents found ($total_publisher_docs is 0 or very low):**

```
⚠️  Couldn't find suitable pages for publisher profile

I looked for:
  - Homepage (root domain pages)
  - About/company pages (/about, /company, /mission, /values)
  - Product pages (/product, /solutions, /platform)

Found: $total_publisher_docs pages (need at least 3 for quality extraction)

Options:
  1. Add more content - Map and fetch your company's main website
  2. Show me what's available - I'll list all indexed pages so you can choose
  3. Skip for now - Extract publisher profile later

What would you like to do? (1/2/3)
```

**If user chooses 1:** Guide them through content mapping (return to Check 1 workflow).
**If user chooses 2:** List all indexed URLs and let user specify which to use.
**If user chooses 3:** Skip to next rule type.

**If suitable documents found, continue:**

**Show preview to user:**

```
**Propose: Extract Publisher Profile**

Sample documents I'll analyze (showing 5 of $total_publisher_docs):
1. $homepage - "Homepage"
2. (first about page) - "(title from metadata)"
3. (second about page) - "(title from metadata)"
4. (first product page) - "(title from metadata)"
5. (second product page) - "(title from metadata)"

**Coverage:**
- $total_publisher_docs pages available
- Domains: (list unique domains)
- Content types: Homepage, about/company pages, product pages

**What I'll extract:**
- Company mission and value proposition
- Key messaging themes
- Brand personality and positioning
- Target market and differentiators

**Output:** rules/publisher/publisher-profile.md

Extract publisher profile from these documents?

Options:
  Y - Yes, extract from these documents
  D - Use different documents (you'll specify which)
  S - Skip for now

Choose (Y/D/S):
```

**Wait for user response.**

**If Y (approve):**

Use the Skill tool: `writing-rules publisher --auto-discover`

Then verify creation:
```bash
# Check if rule was created
if [ -f "rules/publisher/publisher-profile.md" ]; then
  echo "✓ Publisher profile extracted: rules/publisher/publisher-profile.md"
else
  echo "⚠️  Publisher profile extraction failed"
fi
```

**If D (different documents):**

Ask user:
```
Which documents should I use instead?

You can specify:
  - URL patterns (e.g., "only pages from example.com/about/*")
  - Specific URLs (e.g., "https://example.com/company")
  - Content types (e.g., "only product pages")

Describe the documents you want me to use:
```

Wait for response, then re-query with user's criteria and show new preview.

**If S (skip):**

```
Skipping publisher profile for now.
You can extract it later with: writing-rules-skill publisher --auto-discover
```

Proceed to next rule type.

---

### Extract Primary Voice (if missing)

**Step 1: Query and Preview Documents**

Query indexed content for primary voice extraction:

```bash
# Find representative content for voice
kurt document list --status INDEXED --output json > /tmp/indexed-content.json

# Look for blog, docs, marketing content
blog_pages=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/blog|/news|/articles")) | .url' | head -5)
doc_pages=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/docs|/documentation|/guides")) | .url' | head -5)
marketing_pages=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/features|/product|/solutions")) | .url' | head -3)

# Count total available
total_voice_docs=$(echo "$blog_pages"; echo "$doc_pages"; echo "$marketing_pages" | grep -v '^$' | wc -l | tr -d ' ')
```

**If no suitable documents found ($total_voice_docs is 0 or very low):**

```
⚠️  Couldn't find suitable pages for primary voice

I looked for:
  - Blog/news pages (/blog, /news, /articles)
  - Documentation (/docs, /documentation, /guides)
  - Marketing pages (/features, /product, /solutions)

Found: $total_voice_docs pages (need at least 5 for quality extraction)

Options:
  1. Add more content - Map and fetch your company's blog or docs
  2. Show me what's available - I'll list all indexed pages so you can choose
  3. Skip for now - Extract primary voice later

What would you like to do? (1/2/3)
```

**If user chooses 1:** Guide them through content mapping.
**If user chooses 2:** List all indexed URLs and let user specify which to use.
**If user chooses 3:** Skip to next rule type.

**If suitable documents found, continue:**

**Show preview to user:**

```
**Propose: Extract Primary Voice**

Sample documents I'll analyze (showing 5 of $total_voice_docs):
1. (first blog page) - "(title from metadata)"
2. (second blog page) - "(title from metadata)"
3. (first doc page) - "(title from metadata)"
4. (second doc page) - "(title from metadata)"
5. (first marketing page) - "(title from metadata)"

**Coverage:**
- $total_voice_docs pages available
- Content types: Blog posts, documentation, marketing pages
- Domains: (list unique domains)

**What I'll extract:**
- Tone characteristics (formal/casual, technical/accessible)
- Sentence structure patterns
- Word choice preferences
- Voice consistency patterns

**Output:** rules/style/primary-voice.md

Extract primary voice from these documents?

Options:
  Y - Yes, extract from these documents
  D - Use different documents (you'll specify which)
  S - Skip for now

Choose (Y/D/S):
```

**Wait for user response.**

**If Y (approve):**

Use the Skill tool: `writing-rules style --type primary --auto-discover`

Then verify creation:
```bash
# Check if rule was created
primary_voice=$(ls rules/style/*primary* 2>/dev/null | head -1)
if [ -n "$primary_voice" ]; then
  echo "✓ Primary voice extracted: $primary_voice"
else
  echo "⚠️  Primary voice extraction failed"
fi
```

**If D (different documents):**

Ask user for criteria, re-query, and show new preview.

**If S (skip):**

```
Skipping primary voice for now.
You can extract it later with: writing-rules-skill style --type primary --auto-discover
```

Proceed to next rule type.

---

### Extract Personas (if missing)

**Step 1: Query and Preview Documents**

Query indexed content for persona extraction:

```bash
# Find diverse content targeting different audiences
kurt document list --status INDEXED --output json > /tmp/indexed-content.json

# Look for technical, business, and customer-facing content
technical_content=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/docs|/api|/reference|/guides|/tutorial")) | .url' | head -5)
business_content=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/solutions|/pricing|/enterprise|/case-studies")) | .url' | head -3)
customer_content=$(cat /tmp/indexed-content.json | jq -r '.[] | select(.url | test("/help|/support|/getting-started|/faq")) | .url' | head -3)

# Count total available
total_persona_docs=$(echo "$technical_content"; echo "$business_content"; echo "$customer_content" | grep -v '^$' | wc -l | tr -d ' ')
```

**If no suitable documents found ($total_persona_docs is 0 or very low):**

```
⚠️  Couldn't find suitable pages for persona extraction

I looked for:
  - Technical content (/docs, /api, /reference, /guides, /tutorial)
  - Business content (/solutions, /pricing, /enterprise, /case-studies)
  - Customer content (/help, /support, /getting-started, /faq)

Found: $total_persona_docs pages (need at least 8-10 for quality persona extraction)

Options:
  1. Add more content - Map and fetch diverse content from your site
  2. Show me what's available - I'll list all indexed pages so you can choose
  3. Skip for now - Extract personas later

What would you like to do? (1/2/3)
```

**If user chooses 1:** Guide them through content mapping.
**If user chooses 2:** List all indexed URLs and let user specify which to use.
**If user chooses 3:** Skip to next rule type.

**If suitable documents found, continue:**

**Show preview to user:**

```
**Propose: Extract Personas**

Sample documents I'll analyze (showing 5 of $total_persona_docs):
1. (first technical doc) - "(title from metadata)"
2. (second technical doc) - "(title from metadata)"
3. (first business page) - "(title from metadata)"
4. (first customer page) - "(title from metadata)"
5. (second customer page) - "(title from metadata)"

**Coverage:**
- $total_persona_docs pages available
- Content types: Technical docs, business content, customer support
- Audience types: Technical implementers, business decision-makers, end users

**What I'll extract:**
- Target audience profiles
- Technical depth and skill levels
- Pain points and goals
- Communication preferences

**Output:** Multiple persona files in rules/personas/

Extract personas from these documents?

Options:
  Y - Yes, extract from these documents
  D - Use different documents (you'll specify which)
  S - Skip for now

Choose (Y/D/S):
```

**Wait for user response.**

**If Y (approve):**

Use the Skill tool: `writing-rules persona --audience-type all --auto-discover`

Then verify creation:
```bash
# Check if rules were created
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

**If D (different documents):**

Ask user for criteria, re-query, and show new preview.

**If S (skip):**

```
Skipping personas for now.
You can extract them later with: writing-rules-skill persona --audience-type all --auto-discover
```

---

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
